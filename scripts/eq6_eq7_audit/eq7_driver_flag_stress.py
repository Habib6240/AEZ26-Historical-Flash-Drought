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
sd={'t2m_mean_C':0.0205,'VPD_mean_kPa':0.0087,'relative_humidity_mean_pct':0.2609}   # RMSE of 2000 pilot-vs-archived pentad differences
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
for scale in (1,3,5):
    fl,mz=mc(scale,150)
    for c in flags:
        out.append(dict(noise_scale=scale,var=c,expected_flips_per_run=float(fl[c].sum()),events_flipping_ge5pct_runs=int((fl[c]>=0.05).sum()),max_abs_dz=mz[c]))
O=pd.DataFrame(out); print(O.round(3).to_string())
O.to_csv(OUT+'flag_montecarlo_measured_sd.csv',index=False)
