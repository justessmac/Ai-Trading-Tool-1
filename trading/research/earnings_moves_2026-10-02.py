"""Historical earnings reactions (gap at the open and close-to-close) for next week's earnings candidates.
Data: Robinhood daily bars (saved tool output) + Robinhood earnings dates/timing."""
import json, sys
import pandas as pd

EARN = {  # report dates (timing) from get_earnings_results, past quarters only
 "APLD": [("2025-04-14","pm"),("2025-07-30","pm"),("2025-10-09","pm"),("2026-01-07","pm"),("2026-04-08","pm"),("2026-07-27","pm")],
 "LEVI": [("2025-04-07","pm"),("2025-07-10","pm"),("2025-10-09","pm"),("2026-01-28","pm"),("2026-04-07","pm"),("2026-07-08","pm")],
 "STZ":  [("2025-04-09","pm"),("2025-07-01","pm"),("2025-10-06","pm"),("2026-01-07","pm"),("2026-04-08","pm"),("2026-06-30","pm")],
 "PENG": [("2025-07-08","pm"),("2025-10-07","pm"),("2026-01-06","pm"),("2026-04-01","pm"),("2026-07-07","pm")],
 "DAL":  [("2025-04-09","am"),("2025-07-10","am"),("2025-10-09","am"),("2026-01-13","am"),("2026-04-08","am"),("2026-07-10","am")],
 "PEP":  [("2025-04-24","am"),("2025-07-17","am"),("2025-10-09","am"),("2026-02-03","am"),("2026-04-16","am"),("2026-07-09","am")],
}
raw = json.load(open(sys.argv[1]))
rows = []
for r in raw["data"]["results"]:
    df = pd.DataFrame(r["bars"])
    df["d"] = df.begins_at.str[:10]
    df = df.set_index("d")[["open_price","close_price"]].astype(float)
    idx = list(df.index)
    for d, t in EARN[r["symbol"]]:
        if d not in df.index: continue
        i = idx.index(d)
        before, after = (i, i+1) if t == "pm" else (i-1, i)
        if after >= len(idx): continue
        pc = df.close_price.iloc[before]
        rows.append({"sym": r["symbol"], "date": d, "gap_open": df.open_price.iloc[after]/pc-1,
                     "close_move": df.close_price.iloc[after]/pc-1})
out = pd.DataFrame(rows)
s = out.groupby("sym").agg(n=("gap_open","size"), avg_abs_gap=("gap_open", lambda x: x.abs().mean()),
                           avg_abs_close=("close_move", lambda x: x.abs().mean()),
                           max_abs_gap=("gap_open", lambda x: x.abs().max()), ups=("gap_open", lambda x: (x>0).sum()))
print(out.to_string(index=False, float_format=lambda v: f"{v:+.1%}"))
print(s.to_string(float_format=lambda v: f"{v:.1%}"))
