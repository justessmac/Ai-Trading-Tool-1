import pandas as pd, numpy as np
from tradingbot.research.options_sim import approx_rates
g=pd.read_csv("data_cache/crypto_GBTC.csv",index_col=0,parse_dates=True).close
i=pd.read_csv("data_cache/crypto_IBIT.csv",index_col=0,parse_dates=True).close
r=pd.concat([g.pct_change()[g.index<"2024-01-12"], i.pct_change()[i.index>="2024-01-12"]]).dropna()
px=(1+r).cumprod(); cash=(approx_rates(px.index)/252).to_numpy(); rv=r.to_numpy(); p=px.to_numpy()
sma100=px.rolling(100).mean().to_numpy(); sma20=px.rolling(20).mean().to_numpy()
vol20=(r.rolling(20).std()*np.sqrt(252)).to_numpy()
COST=0.001
def sim(stop=None, vt=None, fast=False):
    n=len(p); w=np.zeros(n); state=0; peak=0; blocked=False
    for t in range(100,n-1):
        # decide at close t, hold on t+1
        if p[t]>sma100[t]*1.05 and not blocked: state=1
        if p[t]<sma100[t]*0.95: state=0; blocked=False
        if state==1:
            peak=max(peak,p[t]) if w[t]>0 else p[t]
            if stop and p[t]<peak*(1-stop): state=0; blocked=True
            if fast and p[t]<sma20[t]: state=0; blocked=True
        if blocked and p[t]>sma20[t] and p[t]>sma100[t]*1.05: blocked=False; state=1
        tgt=float(state)
        if tgt and vt: tgt=min(1.0, vt/max(vol20[t],1e-9))
        # only move if change > 10 points (limits churn), except full exits
        w[t+1]= tgt if (tgt==0 or abs(tgt-w[t])>0.10) else w[t]
    ret=w*rv+(1-w)*cash-np.abs(np.diff(w,prepend=0))*COST
    return pd.Series(ret,index=px.index), w
def st(ret,a,b):
    x=ret[(ret.index>=a)&(ret.index<b)]; eq=(1+x).cumprod(); y=(x.index[-1]-x.index[0]).days/365.25
    wk=(1+x).resample("W").prod()-1
    return eq.iloc[-1]**(1/y)-1,(eq/eq.cummax()-1).min(),wk.min()
P=[("2018-04-01","2022-01-01","IS"),("2022-01-01","2026-09-26","OOS")]
def show(name,ret):
    print(f"{name:30s}"+" | ".join(f"{l}: CAGR {c:+.0%} DD {d:.0%} worst wk {w:.0%}" for a,b,l in P for c,d,w in [st(ret,a,b)]))
show("Buy & hold", r)
show("Current: SMA100 5%", sim()[0])
for s in (0.15,0.20,0.25): show(f"+ trailing stop {s:.0%}", sim(stop=s)[0])
for v in (0.4,0.6,0.8): show(f"+ vol target {v:.0%}", sim(vt=v)[0])
show("+ fast exit below SMA20", sim(fast=True)[0])
print("\n--- whole portfolio (SPY 200d rule + BTC sleeve, monthly rebalance) 2018-04..2026-09 ---")
from tradingbot.research.data import load_daily
spy=load_daily("SPY",adjusted=False).close; rs=spy.pct_change()+0.015/252
sma=spy.rolling(200).mean(); s=pd.Series(np.nan,index=spy.index); s[spy>sma*1.02]=1; s[spy<sma*0.98]=0
s=s.ffill().fillna(0).shift(1).fillna(0)
spyt=pd.Series(np.where(s==1,rs,approx_rates(spy.index)/252)-s.diff().abs().fillna(0)*0.0002,index=spy.index)
def port(btc,wb):
    df=pd.concat([spyt,btc],axis=1,keys=["s","b"],sort=True).dropna(); df=df[df.index>="2018-04-01"]
    val=np.array([1-wb,wb]); m=None; eq=[]
    for d,row in df.iterrows():
        if m is not None and d.month!=m: val=val.sum()*np.array([1-wb,wb])
        m=d.month; val=val*(1+row.values); eq.append(val.sum())
    eq=pd.Series(eq,index=df.index); y=(eq.index[-1]-eq.index[0]).days/365.25
    wk=eq.resample("W").last().pct_change().min()
    oos=eq[eq.index>="2022-01-01"]; yo=(oos.index[-1]-oos.index[0]).days/365.25
    return f"CAGR {eq.iloc[-1]**(1/y)-1:+.1%} maxDD {(eq/eq.cummax()-1).min():.1%} worst wk {wk:.1%} | 2022+ CAGR {(oos.iloc[-1]/oos.iloc[0])**(1/yo)-1:+.1%} DD {(oos/oos.cummax()-1).min():.1%}"
base=sim()[0]
for wb in (0.3,): print(f"Current 70/30, no vol target:     {port(base,wb)}")
for v in (0.4,0.6):
    b=sim(vt=v)[0]
    for wb in (0.3,0.4,0.5): print(f"{int((1-wb)*100)}/{int(wb*100)}, vol target {v:.0%}:           {port(b,wb)}")
