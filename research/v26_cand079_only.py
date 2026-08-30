"""CAND-079 - fixed variable name, tighter transitions"""
import pandas as pd, numpy as np, time, warnings, os, json
warnings.filterwarnings('ignore')
DIR='data/m1'; UTC4=pd.Timedelta(hours=4); FRIC=2.0

t0=time.time()
xau=pd.read_csv(f'{DIR}/XAUUSD_M1.csv',parse_dates=['timestamp'])
xau['timestamp']+=UTC4; xau.set_index('timestamp',inplace=True); xau.sort_index(inplace=True); xau['date']=xau.index.date
tech=pd.read_csv(f'{DIR}/USATECHIDXUSD_M1.csv',parse_dates=['timestamp'])
tech['timestamp']+=UTC4; tech.set_index('timestamp',inplace=True); tech.sort_index(inplace=True); tech['date']=tech.index.date
print(f'Load: {time.time()-t0:.1f}s')

xr=xau['close'].pct_change().values
vol14=pd.Series(xr).rolling(14).std().values
vol_q25=pd.Series(vol14).rolling(200,min_periods=50).quantile(0.25).values
vol_q50=pd.Series(vol14).rolling(200,min_periods=50).quantile(0.50).values
print(f'Vol: {time.time()-t0:.1f}s')

xc=xau['close'].values; xo=xau['open'].values; xd=xau['date'].values; xidx=xau.index.values; xn=len(xau)
tc=tech['close'].values; tidx=tech.index.values; tn=len(tech)

# Tighter: vol crosses from below q25 to above q75 (not q50)
vol_q75=pd.Series(vol14).rolling(200,min_periods=50).quantile(0.75).values
print(f'Q75: {time.time()-t0:.1f}s')

# Transitions: current vol > q75 AND was < q25 within last 30 bars AND gap >= 30 bars
is_t=np.zeros(xn,dtype=bool); gm=np.zeros(xn)
for i in range(310,xn-30):
    if np.isnan(vol_q75[i]) or vol14[i]<=vol_q75[i]: continue
    # Check vol was below q25 within last 30 bars
    recent_v=vol14[i-30:i]
    recent_q=vol_q25[i-30:i]
    if np.any(np.isnan(recent_v)) or np.any(np.isnan(recent_q)): continue
    if np.min(recent_v) >= np.min(recent_q): continue  # Must have been below q25
    # At least 5 bars where vol < q25 in last 30
    below_count = np.sum(recent_v < recent_q)
    if below_count < 5: continue
    # Gold move during transition
    g=(xc[i]-xo[max(0,i-30)])/xo[max(0,i-30)]*10000
    if abs(g)<5: continue
    is_t[i]=True; gm[i]=g

# CF: vol > q75 for 30+ consecutive bars (already expanded, stable)
icf=np.zeros(xn,dtype=bool)
for i in range(310,xn-30):
    if np.isnan(vol_q75[i]) or vol14[i]<=vol_q75[i]: continue
    recent=vol14[i-30:i+1]
    rq=vol_q75[i-30:i+1]
    if np.any(np.isnan(recent)) or np.any(np.isnan(rq)): continue
    if np.all(recent > rq): icf[i]=True

ti_arr=np.where(is_t)[0]; ci_arr=np.where(icf)[0]
print(f'Trans: {len(ti_arr)} CF: {len(ci_arr)} ({time.time()-t0:.1f}s)')

tl=[]; cfl=[]
for t in ti_arr:
    gd=1 if gm[t]>0 else -1
    g_ts=pd.Timestamp(xidx[t])
    e_ts=g_ts+pd.Timedelta(minutes=30); x_ts=g_ts+pd.Timedelta(minutes=60)
    te=np.searchsorted(tidx, np.datetime64(e_ts.to_datetime64()))
    tx=np.searchsorted(tidx, np.datetime64(x_ts.to_datetime64()))
    if te>=tn or tx>=tn or te==tx: continue
    tr=(tc[tx]-tc[te])/tc[te]*10000*gd
    tl.append({'date':xd[t],'ret':tr})
    nb=ci_arr[(ci_arr>=t-50)&(ci_arr<=t+50)&(ci_arr!=t)]
    if len(nb)>0:
        j=nb[0]
        jts=pd.Timestamp(xidx[j]); jes=jts+pd.Timedelta(minutes=30); jxs=jts+pd.Timedelta(minutes=60)
        jte=np.searchsorted(tidx, np.datetime64(jes.to_datetime64()))
        jtx=np.searchsorted(tidx, np.datetime64(jxs.to_datetime64()))
        if jte<tn and jtx<tn and jte!=jtx:
            cr=(tc[jtx]-tc[jte])/tc[jte]*10000*gd
            cfl.append({'date':xd[j],'ret':cr})

tdf=pd.DataFrame(tl)
cdf=pd.DataFrame(cfl) if cfl else pd.DataFrame({'ret':pd.Series(dtype=float),'date':pd.Series(dtype=str)})
mn=tdf['ret'].mean()-FRIC; mdn=tdf['ret'].median()-FRIC
cmn=cdf['ret'].mean()-FRIC if len(cfl)>0 else 0; cmdn=cdf['ret'].median()-FRIC if len(cfl)>0 else 0
dm=mn-cmn; dd=mdn-cmdn
cfv='TREATMENT SUPERIOR' if dm>0 and dd>0 else('COUNTERFACTUAL SUPERIOR' if dm<0 and dd<0 else'MIXED')
wr=(tdf['ret']>0).mean()*100; cwr=(cdf['ret']>0).mean()*100 if len(cfl)>0 else 0
yrs=max((tdf['date'].max()-tdf['date'].min()).days/365.25,0.1)
print(f'N={len(tl)} Freq={len(tl)/yrs:.1f}/yr')
print(f'Gross: Mean={tdf["ret"].mean():.2f} Med={tdf["ret"].median():.2f}')
print(f'Net: Mean={mn:.2f} Med={mdn:.2f} WR={wr:.1f}%')
print(f'CF: N={len(cfl)} MN={cmn:.2f} MDN={cmdn:.2f} WR={cwr:.1f}%')
print(f'Delta: M={dm:.2f} D={dd:.2f} {cfv}')
print(f'Worst={tdf["ret"].min():.2f} Best={tdf["ret"].max():.2f}')
print(f'Total: {time.time()-t0:.1f}s')
out='output/research_discovery/v26_cand079_results.json'
r={'N':len(tl),'freq':round(len(tl)/yrs,1),'mg':round(tdf['ret'].mean(),2),
   'mdg':round(tdf['ret'].median(),2),'mn':round(mn,2),'mdn':round(mdn,2),
   'wr':round(wr,1),'cf_n':len(cfl),'cf_mn':round(cmn,2),'cf_mdn':round(cmdn,2),
   'cf_wr':round(cwr,1),'delta_mean':round(dm,2),'delta_median':round(dd,2),'cf_verdict':cfv}
with open(out,'w') as f: json.dump(r,f,indent=2,default=str)
print(f'Saved: {out}')
