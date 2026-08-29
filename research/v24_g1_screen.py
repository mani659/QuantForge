"""
V24 G1 Economic Plausibility Screen -- Precomputed Bar Lookups
CAND-071 / CAND-072 / CAND-073
"""
import pandas as pd, numpy as np, os, json
from datetime import timedelta

FRIC = 2.0
DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "m1")
ET = pd.Timedelta(hours=4)

def load(sym):
    df = pd.read_csv(f"{DIR}/{sym}_M1.csv", parse_dates=["timestamp"])
    df["timestamp"] += ET
    df.set_index("timestamp", inplace=True)
    df.sort_index(inplace=True)
    df["h"] = df.index.hour; df["m"] = df.index.minute; df["dow"] = df.index.dayofweek
    return df

def bar_at(g, h, m=0):
    b = g[(g["h"]==h)&(g["m"]==m)]
    if len(b)==0: b = g[g["h"]==h]
    return b.iloc[0] if len(b)>0 else None

def bar_range(g, sh, sm, eh, em):
    """Return (open_price, close_price) for bars between sh:sm and eh:em."""
    if sh == eh:
        b = g[(g["h"]==sh)&(g["m"]>=sm)&(g["m"]<em)]
    else:
        b = g[((g["h"]==sh)&(g["m"]>=sm))|((g["h"]>sh)&(g["h"]<eh))|((g["h"]==eh)&(g["m"]<em))]
    if len(b) < 2: return None, None
    return b.iloc[0]["open"], b.iloc[-1]["close"]

def analyze(name, tl, cl):
    if not tl:
        print("  NO EVENTS"); return {"N":0,"verdict":"ZERO-EVENT"}
    t = pd.DataFrame(tl); n=len(t)
    yrs = max((t["date"].max()-t["date"].min()).days/365.25,0.1)
    freq=n/yrs; r=t["ret"]
    mg,mdg=r.mean(),r.median(); mn,mdn=mg-FRIC,mdg-FRIC; wr=(r>0).mean()*100
    print(f"  N={n} Freq={freq:.1f}/yr MG={mg:.2f} MDG={mdg:.2f} MN={mn:.2f} MDN={mdn:.2f} WR={wr:.1f}%")
    if not cl:
        print("  CF: NONE")
        return {"N":n,"freq":freq,"mg":mg,"mdg":mdg,"mn":mn,"mdn":mdn,"wr":wr,
                "cf_mn":None,"cf_mdn":None,"cf_verdict":"NO-EVENT",
                "econ":"FAIL" if mn<=0 else("PASS" if mn>5 else"MARGINAL"),"verdict":"INSUFFICIENT"}
    c=pd.DataFrame(cl); cr=c["ret"]
    cmn,cmdn=cr.mean()-FRIC,cr.median()-FRIC; cwr=(cr>0).mean()*100
    if mn>cmn and mdn>cmdn: cfv="TREATMENT SUPERIOR"
    elif mn<cmn and mdn<cmdn: cfv="COUNTERFACTUAL SUPERIOR"
    else: cfv="SIMILAR"
    print(f"  CF: N={len(c)} MN={cmn:.2f} MDN={cmdn:.2f} WR={cwr:.1f}% Gate={cfv}")
    econ="FAIL" if mn<=0 else("PASS" if mn>5 else"MARGINAL")
    v="PROMOTE" if econ in("PASS","MARGINAL") and cfv=="TREATMENT SUPERIOR" else"INSUFFICIENT"
    print(f"  Econ={econ} Verdict={v}")
    return {"N":n,"freq":freq,"mg":mg,"mdg":mdg,"mn":mn,"mdn":mdn,"wr":wr,
            "cf_n":len(c),"cf_mn":cmn,"cf_mdn":cmdn,"cf_wr":cwr,"cf_verdict":cfv,"econ":econ,"verdict":v}

def run_071(xau, tech):
    print("\n--- CAND-071: Gold -> Tech ---")
    xg = {d: g for d, g in xau.groupby(xau.index.date)}
    tg = {d: g for d, g in tech.groupby(tech.index.date)}
    t, cf = [], []

    for d, g in tg.items():
        nd = d + timedelta(days=1)
        eve = xg.get(d); morn = xg.get(nd)
        if eve is None or morn is None: continue
        eve_h = eve[eve["h"]>=18]; morn_h = morn[morn["h"]<3]
        if len(eve_h)<2 or len(morn_h)<1: continue
        oret = (morn_h.iloc[-1]["close"]-eve_h.iloc[0]["open"])/eve_h.iloc[0]["open"]*10000
        if abs(oret)<50: continue
        dr = 1 if oret>0 else -1

        # Treatment: 09:30-10:00
        o,c = bar_range(g, 9, 30, 10, 0)
        if o is not None:
            t.append({"date":d, "ret":(c-o)/o*10000*dr})

        # Counterfactual: 12:00-12:30
        o,c = bar_range(g, 12, 0, 12, 30)
        if o is not None:
            cf.append({"date":d, "ret":(c-o)/o*10000*dr})

    return analyze("CAND-071", t, cf)

def run_072(tech):
    print("\n--- CAND-072: Friday Compression -> Monday ---")
    fri = tech[tech.dow==4].copy(); fri["d"]=fri.index.date
    fr = fri.groupby("d").agg(rh=("high","max"),rl=("low","min"))
    fr["rng"]=fr["rh"]-fr["rl"]; fr=fr.reset_index()
    fr["p20"]=fr["rng"].rolling(4,min_periods=3).apply(lambda x:np.percentile(x,20),raw=True)
    fr["comp"]=fr["rng"]<=fr["p20"]
    fr["med"]=fr["rng"].rolling(4,min_periods=3).median()
    fr["exp"]=fr["rng"]>=fr["med"]
    fri_set = set(fr["d"])

    tg = {d: g for d, g in tech.groupby(tech.index.date)}
    mdays = sorted(d for d, g in tg.items() if g["dow"].iloc[0]==0)
    t, cf = [], []

    for md in mdays:
        fd = md - timedelta(days=3)
        if fd not in fri_set: continue
        frw = fr[fr["d"]==fd].iloc[0]
        g = tg[md]

        o,c = bar_range(g, 9, 30, 10, 0)
        if o is None: continue
        eb = (c-o)/o*10000*100
        if abs(eb)<30: continue
        dr = 1 if eb>0 else -1

        en = bar_at(g, 10, 0); ex = bar_at(g, 15, 45)
        if en is None or ex is None: continue
        tr = (ex["close"]-en["close"])/en["close"]*10000*dr

        ev = {"date":md, "ret":tr}
        if frw["comp"]: t.append(ev)
        elif frw["exp"]: cf.append(ev)

    return analyze("CAND-072", t, cf)

def run_073(tech):
    print("\n--- CAND-073: Lunch Reversal Continuation ---")
    tg = {d: g for d, g in tech.groupby(tech.index.date)}
    t, cf = [], []

    for d, g in tg.items():
        # Treatment: 12:00-12:30 + 12:30-12:45
        o,c = bar_range(g, 12, 0, 12, 30)
        if o is None: continue
        rb = (c-o)/o*10000*100
        if abs(rb)<40: continue
        dr = 1 if rb>0 else -1

        co,cc = bar_range(g, 12, 30, 12, 45)
        if co is None or (cc-co)/co*10000*100*dr<=0: continue

        en = bar_at(g, 12, 45); ex = bar_at(g, 13, 45)
        if en is None or ex is None: continue
        t.append({"date":d, "ret":(ex["close"]-en["close"])/en["close"]*10000*dr})

        # Counterfactual: 10:30-11:00 + 11:00-11:15
        o2,c2 = bar_range(g, 10, 30, 11, 0)
        if o2 is None: continue
        cb = (c2-o2)/o2*10000*100
        if abs(cb)<40: continue
        cdir = 1 if cb>0 else -1

        co2,cc2 = bar_range(g, 11, 0, 11, 15)
        if co2 is None or (cc2-co2)/co2*10000*100*cdir<=0: continue

        cen = bar_at(g, 11, 15); cex = bar_at(g, 12, 15)
        if cen is None or cex is None: continue
        cf.append({"date":d, "ret":(cex["close"]-cen["close"])/cen["close"]*10000*cdir})

    return analyze("CAND-073", t, cf)

if __name__=="__main__":
    print("V24 G1 ECONOMIC PLAUSIBILITY SCREEN\n")
    xau=load("XAUUSD"); tech=load("USATECHIDXUSD")
    print(f"XAUUSD: {len(xau)} | USATECHIDXUSD: {len(tech)}\n")
    r={}
    r["CAND-071"]=run_071(xau,tech)
    r["CAND-072"]=run_072(tech)
    r["CAND-073"]=run_073(tech)
    print("\n=== SUMMARY ===")
    for c,v in r.items(): print(f"  {c}: N={v['N']} Verdict={v['verdict']}")
    out=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"output","research_discovery","v24_g1_results.json")
    with open(out,"w") as f: json.dump(r,f,indent=2,default=str)
    print(f"\nSaved: {out}")
