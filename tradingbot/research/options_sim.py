"""Approximate backtest of short-premium SPY option strategies.

IMPORTANT LIMITATION: this does not use historical option quotes (those are
paid data, e.g. Cboe DataShop / ORATS). Option prices are modelled with
Black-Scholes using VIX as the at-the-money volatility level plus a simple
put-skew adjustment. That captures the volatility risk premium (VIX has
historically exceeded realised vol) and crash behaviour (VIX spikes), but
it will misprice deep-OTM wings and misses real bid/ask blowouts. Treat
results as a screen, then validate on real chain data before trading.

Structures (all defined-risk or cash-secured, i.e. Robinhood options L3):
  - "csp":          short put, cash-secured
  - "put_spread":   bull put credit spread
  - "iron_condor":  bull put spread + bear call spread
"""
from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy.special import ndtr

DIV_YIELD = 0.015

# Approximate annual-average 3-month T-bill yields (public Fed H.15 series,
# rounded; 2025-26 estimated). Used when no daily rate series is available.
APPROX_TBILL = {
    2000: 5.8, 2001: 3.4, 2002: 1.6, 2003: 1.0, 2004: 1.4, 2005: 3.2, 2006: 4.7, 2007: 4.4,
    2008: 1.4, 2009: 0.15, 2010: 0.14, 2011: 0.05, 2012: 0.09, 2013: 0.06, 2014: 0.03,
    2015: 0.05, 2016: 0.32, 2017: 0.93, 2018: 1.94, 2019: 2.06, 2020: 0.37, 2021: 0.05,
    2022: 2.02, 2023: 5.07, 2024: 4.97, 2025: 4.1, 2026: 3.7,
}


def approx_rates(index: pd.DatetimeIndex) -> pd.Series:
    return pd.Series([APPROX_TBILL.get(d.year, 2.0) / 100.0 for d in index], index=index)


def bs_price(S, K, T, r, q, sigma, kind):
    S, K, T, sigma = map(np.asarray, (S, K, T, sigma))
    T = np.maximum(T, 1e-6)
    sigma = np.maximum(sigma, 1e-4)
    sqrtT = np.sqrt(T)
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * sqrtT)
    d2 = d1 - sigma * sqrtT
    if kind == "put":
        return K * np.exp(-r * T) * ndtr(-d2) - S * np.exp(-q * T) * ndtr(-d1)
    return S * np.exp(-q * T) * ndtr(d1) - K * np.exp(-r * T) * ndtr(d2)


def implied_vol(S, K, T, vix, kind):
    """ATM vol ~ 0.9 * VIX; puts get richer (and calls cheaper) the further
    OTM they are, measured in ATM standard deviations."""
    atm = 0.9 * np.asarray(vix) / 100.0
    z = np.log(np.asarray(S) / np.asarray(K)) / (atm * np.sqrt(np.maximum(T, 1e-6)))
    if kind == "put":
        adj = 1 + 0.12 * np.clip(z, 0, 3)
    else:
        adj = 1 - 0.06 * np.clip(-z, 0, 2)
    return atm * adj


def strike_for_delta(S, T, r, vix, delta, kind):
    """Strike (rounded to $1) whose |delta| is closest to `delta`."""
    grid = np.arange(math.floor(S * 0.5), math.ceil(S * 1.5) + 1, 1.0)
    iv = implied_vol(S, grid, T, vix, kind)
    d1 = (np.log(S / grid) + (r - DIV_YIELD + 0.5 * iv**2) * T) / (iv * math.sqrt(T))
    dl = np.exp(-DIV_YIELD * T) * (ndtr(d1) - (1 if kind == "put" else 0))
    return float(grid[np.argmin(np.abs(np.abs(dl) - delta))])


@dataclass(frozen=True)
class OptConfig:
    structure: str
    short_delta: float
    long_delta: float | None
    dte: int
    take_profit: float | None  # fraction of credit captured to close early
    stop_mult: float | None  # close when loss >= stop_mult * credit
    exit_dte: int  # close when calendar DTE <= this (0 = hold to expiry)
    filt: str  # "none" | "trend" | "vix_lt30"

    def label(self) -> str:
        return (
            f"{self.structure}(sd={self.short_delta}, ld={self.long_delta}, dte={self.dte}, "
            f"tp={self.take_profit}, stop={self.stop_mult}, exit_dte={self.exit_dte}, filt={self.filt})"
        )


def _legs(cfg: OptConfig, S, T, r, vix):
    """Return list of (kind, strike, sign) with sign=-1 short, +1 long."""
    legs = []
    kp = strike_for_delta(S, T, r, vix, cfg.short_delta, "put")
    legs.append(("put", kp, -1))
    if cfg.structure in ("put_spread", "iron_condor"):
        kl = strike_for_delta(S, T, r, vix, cfg.long_delta, "put")
        legs.append(("put", min(kl, kp - 1), +1))
    if cfg.structure == "iron_condor":
        kc = strike_for_delta(S, T, r, vix, cfg.short_delta, "call")
        kcl = strike_for_delta(S, T, r, vix, cfg.long_delta, "call")
        legs.append(("call", kc, -1))
        legs.append(("call", max(kcl, kc + 1), +1))
    return legs


def _value(legs, S, T, r, vix):
    """Value of the position to BUY BACK (positive = liability), per share."""
    total = 0.0
    for kind, K, sign in legs:
        iv = implied_vol(S, K, T, vix, kind)
        total += -sign * bs_price(S, K, T, r, DIV_YIELD, iv, kind)
    return total


def _slip(legs, S, T, r, vix, slip_mult):
    """Round-trip-half cost for crossing the spread on every leg + fees."""
    cost = 0.0
    for kind, K, _ in legs:
        px = float(bs_price(S, K, T, r, DIV_YIELD, implied_vol(S, K, T, vix, kind), kind))
        cost += (0.01 + 0.02 * px) * slip_mult + 0.0004  # $0.04/contract fees
    return cost


def simulate(
    spy: pd.DataFrame, vix: pd.Series, rates: pd.Series, cfg: OptConfig, *, entry_every: int = 5, slip_mult: float = 1.0
) -> list[dict]:
    df = pd.DataFrame({"S": spy["close"], "vix": vix, "r": rates}).dropna()
    df["sma200"] = df["S"].rolling(200).mean()
    dates = df.index
    S_arr, V_arr, R_arr = df["S"].to_numpy(), df["vix"].to_numpy(), df["r"].to_numpy()
    trades = []
    for i in range(200, len(df), entry_every):
        S0, v0, r0 = S_arr[i], V_arr[i], R_arr[i]
        if cfg.filt == "trend" and S0 < df["sma200"].iat[i]:
            continue
        if cfg.filt == "vix_lt30" and v0 >= 30:
            continue
        expiry = dates[i] + pd.Timedelta(days=cfg.dte)
        T0 = cfg.dte / 365.0
        legs = _legs(cfg, S0, T0, r0, v0)
        credit = float(_value(legs, S0, T0, r0, v0)) - _slip(legs, S0, T0, r0, v0, slip_mult)
        if credit <= 0.01:
            continue
        if cfg.structure == "csp":
            risk = legs[0][1]
        else:
            put_w = legs[0][1] - legs[1][1]
            call_w = legs[3][1] - legs[2][1] if cfg.structure == "iron_condor" else 0
            risk = max(put_w, call_w) - credit
        if risk <= 0:
            continue

        # Revalue the position on every remaining day in one vectorised pass.
        end = int(np.searchsorted(dates.values, expiry.to_datetime64(), side="right"))
        if end <= i + 1 or end >= len(df):
            continue  # expiry beyond available data: trade not finished
        path = slice(i + 1, end)
        days_left = (expiry - dates[path]).days.to_numpy()
        S, v, r = S_arr[path], V_arr[path], R_arr[path]
        T = np.maximum(days_left, 0) / 365.0
        val = _value(legs, S, T, r, v)
        at_expiry = days_left <= 0
        at_expiry[-1] = True  # last trading day on/before expiry settles at intrinsic
        intrinsic = sum(
            -sign * np.maximum(0.0, (K - S) if kind == "put" else (S - K)) for kind, K, sign in legs
        )
        val = np.where(at_expiry, intrinsic, val)
        stop_now = at_expiry | (days_left <= cfg.exit_dte)
        if cfg.take_profit is not None:
            stop_now |= val <= (1 - cfg.take_profit) * credit
        if cfg.stop_mult is not None:
            stop_now |= val - credit >= cfg.stop_mult * credit
        hits = np.flatnonzero(stop_now)
        if not len(hits):
            continue
        h = int(hits[0])
        j = i + 1 + h
        exit_cost = 0.0 if (at_expiry[h] and val[h] <= 0) else _slip(legs, S[h], max(T[h], 1e-6), r[h], v[h], slip_mult)
        pnl = credit - float(val[h]) - exit_cost
        trades.append(
            {
                "symbol": "SPY",
                "entry_date": dates[i],
                "exit_date": dates[min(j, len(df) - 1)],
                "ret": pnl / risk,
                "credit": credit,
                "risk": risk,
            }
        )
    return trades


def grid() -> list[OptConfig]:
    cfgs = []
    for structure, sd, ld, dte, tp, stop, exit_dte, filt in itertools.product(
        ["csp", "put_spread", "iron_condor"],
        [0.10, 0.16, 0.20, 0.30],
        [0.05, 0.10],
        [30, 45],
        [0.5, None],
        [2.0, None],
        [21, 0],
        ["none", "trend", "vix_lt30"],
    ):
        if structure == "csp":
            if ld != 0.05:
                continue
            ld = None
        elif ld >= sd:
            continue
        if exit_dte >= dte:
            continue
        cfgs.append(OptConfig(structure, sd, ld, dte, tp, stop, exit_dte, filt))
    return cfgs
