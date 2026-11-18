import pandas as pd, numpy as np
import pathlib
D=str(pathlib.Path(__file__).resolve().parents[2]/'data'/'derived')+'/'
E=pd.read_csv(D+'AEZ26_Phase2D_Event_Driver_Characterization.csv'); H=pd.read_csv(D+'AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv')
H['key']=H.year.astype(str)+'_P'+H.pentad_of_year.astype(int).map('{:02d}'.format)
Hk=H.set_index('key')
def win(e):
    y,p0=map(int,[e.onset_pentad[:4],e.onset_pentad[-2:]]); y2,p1=int(e.threshold_crossing_pentad[:4]),int(e.threshold_crossing_pentad[-2:])
    return y,p0,y2,p1
def stat(col,e,ddof=1,pent=None):
    y,p0,y2,p1=win(e)
    # event window (assumes same year or spans year end)
    def vals(yy):
        ks=[]
        for (a,b) in ([(p0,p1)] if y==y2 else [(p0,73),(1,p1)]):
            ks+=[(yy if a>=p0 and y==y2 or a==p0 else yy+1,q) for q in range(a,b+1)]
        return ks
    def mean_window(yy):
        ks=vals(yy); sub=H[[ (r.year,r.pentad_of_year) in set(ks) for r in H[['year','pentad_of_year']].itertuples()]] if False else None
    return None
# simpler: build list of (offset_year, pentad) for window
def wlist(e):
    y,p0,y2,p1=win(e); out=[]
    if y==y2: out=[(0,q) for q in range(p0,p1+1)]
    else: out=[(0,q) for q in range(p0,74)]+[(y2-y,q) for q in range(1,p1+1)]
    return y,out
def ref_series(col,e):
    y,wl=wlist(e); vals={}
    for yy in range(2000,2026):
        num=den=0;ok=True
        for off,q in wl:
            k=f'{yy+off}_P{q:02d}'
            if k not in Hk.index: ok=False;break
            n=Hk.loc[k,'n_days']; num+=Hk.loc[k,col]*n; den+=n
        if ok: vals[yy]=num/den
    return y,pd.Series(vals)
rows=[]
for e in E.itertuples():
    for col,zc in [('VPD_mean_kPa','VPD_standardized_anomaly_z'),('t2m_mean_C','temperature_standardized_anomaly_z'),('relative_humidity_mean_pct','RH_standardized_anomaly_z')]:
        y,s=ref_series(col,e)
        for ddof in (0,1):
            z=(s[y]-s.mean())/s.std(ddof=ddof)
            rows.append((e.event_id,col,ddof,z,getattr(e,zc),s.std(ddof=1)))
R=pd.DataFrame(rows,columns=['event','col','ddof','z_repro','z_stored','sd'])
for (c,dd),g in R.groupby(['col','ddof']): print(c,dd,'max|dz|',np.abs(g.z_repro-g.z_stored).max().round(4),'MAE',np.abs(g.z_repro-g.z_stored).mean().round(4))
