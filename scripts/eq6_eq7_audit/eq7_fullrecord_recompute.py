"""Eq. (7) per-pixel recomputation for all 3,285 pentads of 1981-2025 (written 2026-11-15; NOT part of the original analysis code).
Needs the per-pixel daily temperature/dew-point exports and the pixel-weights table made with gee/AEZ26_Eq7_FullRecord_SourceExport_v01.js; these are NOT redistributed in the releases (MISSING_INPUTS_AND_PERMISSIONS.md), so this script cannot be run from the releases alone.
Usage: python eq7_fullrecord_recompute.py --weights WEIGHTS.csv --pixel-dir DIR --out OUT.csv"""
import argparse,sys,pathlib
ap=argparse.ArgumentParser(description='Per-pixel Eq. 7 recomputation for 1981-2025 (needs the withheld per-pixel exports)')
ap.add_argument('--weights',required=True,help='AEZ26_Eq7FR_Pixel_Weights.csv (withheld)'); ap.add_argument('--pixel-dir',required=True,help='folder with the 45 AEZ26_Eq7FR_Pixel_T_Td_<year>.csv files (withheld), incl. 2000')
ap.add_argument('--out',default='AEZ26_Eq7_Recomputed_3285pentads.csv'); a=ap.parse_args()
WEIGHTS=a.weights; PIXDIR=a.pixel_dir; OUTFILE=a.out
import pandas as pd, numpy as np, datetime as dt, glob, re, hashlib
W=pd.read_csv(WEIGHTS); W=W[W.coverage_weight_sample>0].set_index('pixel_id')
files={}
for f in glob.glob(PIXDIR+'/*.csv'):
    if 'Pixel_T_Td' in f: files[int(re.search(r'_(\d{4})\.csv',f).group(1))]=f
assert sorted(files)==list(range(1981,2026))
d=pd.concat([pd.read_csv(files[y],parse_dates=['date']) for y in sorted(files)],ignore_index=True)
d['wn']=d.pixel_id.map(W.coverage_weight_native)
T=d.temperature_2m_K-273.15; Td=d.dewpoint_temperature_2m_K-273.15
es=0.6108*np.exp(17.27*T/(T+237.3)); ea=0.6108*np.exp(17.27*Td/(Td+237.3))
d['T']=T; d['Td']=Td; d['RH']=np.clip(100*ea/es,0,100); d['VPD']=np.maximum(es-ea,0)
print('rows',len(d),'RH>100 raw',int((100*ea/es>100).sum()),'neg raw VPD',int((es-ea<0).sum()))
# calendar
def window(y,p):
    leap=(y%4==0 and y%100!=0) or y%400==0
    s=dt.date(y,1,1)+dt.timedelta(days=(p-1)*5+(1 if leap and p>=13 else 0)); n=6 if leap and p==12 else 5
    return s,n
rows=[]
for y in range(1981,2026):
    for p in range(1,74):
        s,n=window(y,p); rows.append((y,p,pd.Timestamp(s),n))
cal=pd.DataFrame(rows,columns=['year','pentad_of_year','start','n_days'])
cal['end']=cal.start+pd.to_timedelta(cal.n_days-1,unit='D')
# assign each date to pentad
dm={}
for r in cal.itertuples():
    for k in range(r.n_days): dm[r.start+pd.Timedelta(days=k)]=(r.year,r.pentad_of_year)
dates=pd.Series(d.date.unique()); m=dates.map(dm); assert m.notna().all()
mp=dict(zip(dates,m)); pp=d.date.map(mp); d['py']=[a for a,b in pp]; d['pp']=[b for a,b in pp]
# per pixel/pentad
d['VPDmaxsrc']=d.VPD
g=d.groupby(['py','pp','pixel_id']).agg(T=('T','mean'),Td=('Td','mean'),RH=('RH','mean'),VPD=('VPD','mean'),VPDmax=('VPD','max'),Tmax=('T','max'),n=('T','size'),w=('coverage_weight','first'),wn=('wn','first')).reset_index()
def zone(col,wc):
    return (g[col]*g[wc]).groupby([g.py,g.pp]).sum()/g[wc].groupby([g.py,g.pp]).sum()
out=pd.DataFrame({'n_days_data':g.groupby(['py','pp']).n.first(),'npx':g.groupby(['py','pp']).size()})
for c in ['T','Td','RH','VPD','VPDmax','Tmax']:
    out['S_'+c]=zone(c,'w'); out['N_'+c]=zone(c,'wn')
out=out.reset_index().rename(columns={'py':'year','pp':'pentad_of_year'})
out=out.merge(cal,on=['year','pentad_of_year'])
print('pentads',len(out),'n_days mismatch',int((out.n_days_data!=out.n_days).sum()),'px per pentad',out.npx.unique())
out.to_csv(OUTFILE,index=False)
print(hashlib.sha256(open(OUTFILE,'rb').read()).hexdigest())
