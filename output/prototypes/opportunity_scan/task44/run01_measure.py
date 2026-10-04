import numpy as np, pandas as pd, json, warnings, time
warnings.filterwarnings("ignore")
BASE = "output/prototypes/fx_h4inv_adx_prep/_t37_h4_{sym}.npz"
SYMS = ["XAUUSDm","XAGUSDm","USTECm","EURUSDm","GBPUSDm","USDJPYm","EURGBPm","AUDNZDm","BTCUSDm","ETHUSDm","USOILm"]
WINDOWS = [4,8,13,26]
N_SIMS = 300
COST_TIERS = [10,5,0]
def load(path):
    d = np.load(path, allow_pickle=True)
    t = d["time"]; t = t.astype("int64")//10**9 if t.dtype.kind=="M" else t
    return pd.DataFrame({k:d[k] for k in d.files if k!="time"}, index=pd.to_datetime(t, unit="s", utc=True))
cd = []
for s in SYMS:
    df = load(BASE.format(sym=s)); df.index = df.index.tz_localize(None); df["sym"]=s
    cd.append(df[["close","sym"]])
piv = pd.concat(cd).pivot_table(index=pd.concat(cd).index, columns="sym", values="close").sort_index()
full = piv[piv.notna().all(axis=1)].copy()
rank = full.rank(axis=1, method="first", ascending=False)
n_full = len(full)
retw = {}
for w in WINDOWS:
    r = np.full((n_full-w, len(SYMS)), np.nan)
    for si in range(len(SYMS)):
        c = full[SYMS[si]].to_numpy()
        r[:, si] = c[w:]/c[:-w]-1
    retw[w] = r
tm = rank.le(3).to_numpy()
bm = rank.ge(9).to_numpy()
OUT = {}
t0 = time.time()
for wi, w in enumerate(WINDOWS):
    r = retw[w]; n2 = len(r)
    tm2 = tm[:n2]; bm2 = bm[:n2]
    top_means = np.array([r[i][tm2[i]].mean() for i in range(n2)])
    bot_means = np.array([r[i][bm2[i]].mean() for i in range(n2)])
    act = top_means - bot_means
    rng = np.random.default_rng(20261004+wi)
    idx = np.array([rng.permutation(len(SYMS)) for _ in range(N_SIMS)])
    top3 = idx[:, :3]; bot3 = idx[:, 3:6]
    null = np.empty(N_SIMS)
    for si in range(N_SIMS):
        top_mean = r[:, top3[si]].mean(axis=1)
        bot_mean = r[:, bot3[si]].mean(axis=1)
        null[si] = (top_mean - bot_mean).mean()
    ps = {}
    for tb in COST_TIERS:
        gross = float(act.sum())
        net = gross - 2.0*tb/10000.0*np.abs(act).sum()
        days = len(act)
        avg = float(act.mean()); vol = float(act.std())
        sharpe = avg/vol*np.sqrt(252) if vol>0 else float("nan")
        ann = ((1+gross)**(252/days)-1) if days>0 else float("nan")
        cum = float(np.prod(1+np.nan_to_num(act, nan=0.0)-1))
        cs = np.cumsum(act); rm = np.maximum.accumulate(cs); dd = (cs-rm)
        mdd = float(dd.min()) if len(dd) else float("nan")
        pf = float(act[act>0].sum()/abs(act[act<0].sum())) if (act<0).sum()>0 else float("inf")
        ps[tb] = dict(gross_ret=gross, net_ret=net, sharpe=sharpe, ann=ann, cum=cum, mdd=mdd, pf=pf,
                      turnover=float(2*np.abs(act).sum()/2.0), n_obs=days, exposure=float(np.abs(act).sum()))
    ts = pd.Series(act, index=full.index[w:])
    e = {}
    for yr in sorted(full.index.year.unique()):
        sub = ts[ts.index.year==yr]
        if len(sub)==0: continue
        g = float(sub.sum())
        net = g - 2.0*10/10000.0*np.abs(sub).sum()
        e[yr] = dict(gross=g, net=net, sharpe=float(sub.mean()/sub.std()*np.sqrt(252)) if sub.std()>0 else float("nan"), n=int(len(sub)))
    sym_contrib = np.zeros(len(SYMS))
    for i in range(n2):
        for k in range(len(SYMS)):
            if tm2[i,k]: sym_contrib[k]+=r[i,k]
            if bm2[i,k]: sym_contrib[k]-=r[i,k]
    OUT[wi] = dict(window=w, n_obs=int(len(act)), act_mean=float(act.mean()), act_std=float(act.std()),
                   act_p05=float(np.percentile(act,.05)), act_p95=float(np.percentile(act,.95)),
                   null_mean=float(null.mean()), null_std=float(null.std()),
                   null_p25=float(np.percentile(null,.05)), null_p75=float(np.percentile(null,.95)),
                   sym_contrib={s: float(v) for s,v in zip(SYMS, sym_contrib)},
                   ps=ps, era=e)
    print("W", w, "act_bps", round(act.mean()*1e6,4), "std_bps", round(act.std()*1e6,4), "null", round(null.mean()*1e6,4), "null_std", round(null.std()*1e6,4), "sec", round(time.time()-t0,2))
    print("   ps10:", {k: (round(v*1e6,4) if k=="gross_ret" else v) for k,v in ps[10].items() if k in ("gross_ret","net_ret","sharpe","ann","cum","mdd","pf","n_obs")})
    print("   eras:", {yr: (round(v["gross"],4), round(v["net"],4)) for yr,v in e.items()})
with open("output/prototypes/opportunity_scan/task44/run01_results.json","w") as f:
    json.dump(OUT, f, indent=2, default=str)
print("WROTE run01_results.json")
