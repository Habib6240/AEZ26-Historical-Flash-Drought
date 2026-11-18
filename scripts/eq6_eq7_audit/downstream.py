# Paths resolved relative to the repository root. Requires the flat input view created by scripts/stage_flat_inputs.py (data/derived/).
import os, pathlib
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
D=str(ROOT/'data'/'derived')+'/'; V=str(ROOT/'data'/'eq6_eq7_verification')+'/'
OUT=str(ROOT/'results'/'eq6_eq7_rerun')+'/'; os.makedirs(OUT,exist_ok=True)
import pandas as pd, numpy as np, json
from scipy.stats import kendalltau, theilslopes
exec(open(str(HERE/'z_repro.py')).read().split("rows=[]")[0])   # E,H,Hk,ref_series, win...
rng=np.random.default_rng(20261113)
# ---- A. driver flags: stored flags
flags={'VPD_mean_kPa':('VPD_standardized_anomaly_z',+1),'t2m_mean_C':('temperature_standardized_anomaly_z',+1),'relative_humidity_mean_pct':('RH_standardized_anomaly_z',-1)}
# margin to threshold
res=[]
for col,(zc,sg) in flags.items():
    z=E[zc].values; margin=np.abs(z-sg)  # distance to +1 / -1
    res.append(dict(var=col,n_flagged=int((sg*z>=1).sum()),min_margin=margin.min(),n_within_0p05=int((margin<0.05).sum()),n_within_0p10=int((margin<0.10).sum()),n_within_0p25=int((margin<0.25).sum())))
M=pd.DataFrame(res); print(M.round(3).to_string())
# ---- B. Monte Carlo: independent year-by-pentad noise (pessimistic: error NOT constant per pentad-of-year)
sd={'t2m_mean_C':0.0581,'VPD_mean_kPa':0.00797,'relative_humidity_mean_pct':0.2220}   # RMSE of 2000 pilot-vs-archived pentad differences
def mc(scale,nrep=500):
    flips={k:np.zeros(len(E)) for k in flags}; maxdz={k:0 for k in flags}
    base={}
    ev=[]
    for e in E.itertuples():
        ev.append(e)
    # pre-extract per-event window pentad keys to speed
    wl={e.event_id:wlist(e) for e in ev}
    arr={c:H.set_index('key')[c] for c in flags}
    for rep in range(nrep):
        noise={c:pd.Series(rng.normal(0,sd[c]*scale,len(H)),index=H.key) for c in flags}
        for e in ev:
            y,w=wl[e.event_id]
            for c,(zc,sg) in flags.items():
                vals={}
                for yy in range(2000,2026):
                    ks=[f'{yy+off}_P{q:02d}' for off,q in w]
                    if not all(k in arr[c].index for k in ks): continue
                    n=np.array([Hk.loc[k,'n_days'] for k in ks]); v=np.array([arr[c][k]+noise[c][k] for k in ks])
                    vals[yy]=(v*n).sum()/n.sum()
                s=pd.Series(vals); z=(s[y]-s.mean())/s.std(ddof=1)
                st=getattr(e,zc); 
                if (sg*z>=1)!=(sg*st>=1): flips[c][E.index[E.event_id==e.event_id][0]]+=1/nrep
                maxdz[c]=max(maxdz[c],abs(z-st))
    return flips,maxdz
out=[]
for scale in (1,3):
    fl,mz=mc(scale,150)
    for c in flags:
        out.append(dict(noise_scale=scale,var=c,expected_flips_per_run=float(fl[c].sum()),events_flipping_ge5pct_runs=int((fl[c]>=0.05).sum()),max_abs_dz=mz[c]))
O=pd.DataFrame(out); print(O.round(3).to_string())
M.to_csv(OUT+'flag_margins.csv',index=False); O.to_csv(OUT+'flag_montecarlo_superseded_earlier_SD_assumptions.csv',index=False)
# ---- C. trends and drift tipping
A=pd.read_csv(D+'AEZ26_Robustness_Annual_Hydroclimate_1981_2025.csv')
tr=pd.read_csv(D+'AEZ26_Robustness_Environment_and_Hashes.json'.replace('Environment_and_Hashes.json','Annual_FD_Counts_1981_2025.csv'))
def trend(y,v):
    s,i,lo,hi=theilslopes(v,y,0.95); t,p=kendalltau(y,v); return s*10,lo*10,hi*10,p
yrs=A.year.values
base={c:trend(yrs,A[c].values) for c in ['temperature_C','VPD_kPa','precipitation_mm','potential_evaporation_mm']}
print({k:tuple(round(x,4) for x in v) for k,v in base.items()})
cnt=pd.read_csv(D+'AEZ26_Robustness_Annual_FD_Counts_1981_2025.csv'); print(cnt.columns.tolist()[:4])
pc=[c for c in cnt.columns if 'count' in c.lower()][0]
pfd=trend(cnt.year.values,cnt[pc].values)[3]
def bh(ps):
    ps=np.array(ps); o=np.argsort(ps); m=len(ps); q=np.empty(m); run=1
    for r,i in enumerate(o[::-1]): 
        k=m-r; run=min(run,ps[i]*m/k); q[i]=run
    return q
rows=[]
for var in ['temperature_C','VPD_kPa']:
    for drift in np.round(np.arange(-0.10,0.1001,0.01 if var=='temperature_C' else 0.002),4):
        a=A.copy(); a[var]=a[var]+drift*(a.year-1981)/10   # linear drift in offset, units per decade
        ps=[pfd,trend(yrs,a.temperature_C.values)[3],trend(yrs,a.VPD_kPa.values)[3],base['precipitation_mm'][3],base['potential_evaporation_mm'][3]]
        s,lo,hi,p=trend(yrs,a[var].values); q=bh(ps)[1 if var=='temperature_C' else 2]
        rows.append(dict(var=var,drift_per_decade=drift,slope_per_decade=s,ci_lo=lo,ci_hi=hi,nominal_p=p,BH_q=q,CI_excludes_0=(lo>0 or hi<0),FDR_supported=q<=0.05))
T=pd.DataFrame(rows); T.to_csv(OUT+'trend_drift_sensitivity.csv',index=False)
for var in ['temperature_C','VPD_kPa']:
    g=T[T['var']==var]
    print(var,'baseline p',round(base[var][3],4),'; drift range with CI excluding 0:',g[g.CI_excludes_0].drift_per_decade.min() if g.CI_excludes_0.any() else None,g[g.CI_excludes_0].drift_per_decade.max() if g.CI_excludes_0.any() else None,'| any FDR_supported:',bool(g.FDR_supported.any()))
print('baseline BH q (as recomputed):',bh([pfd,base['temperature_C'][3],base['VPD_kPa'][3],base['precipitation_mm'][3],base['potential_evaporation_mm'][3]]).round(4))
