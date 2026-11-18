"""Eq. (6) soil-water spatial-reduction offsets in the 35 compared pentads (written 2026-11-16; NOT part of the original analysis code).
B - A of the 0-100 cm storage (pathway B: explicit native grid; A: archived composite reduction) by month, period and soil-water state.
State = stored LONG45 percentile (average rank within pentad-of-year, 1981-2025); z-units = offset / interannual SD of the stored series for that pentad-of-year.
Input: data/eq6_eq7_verification/eq7_fullrecord/AEZ26_Eq7_ABC_35pentads_with_offline.csv and the stored extended ERA5-Land table.
Output: results/eq6_eq7_rerun/eq6_35pentad_soilwater_offsets.csv"""
import pathlib, pandas as pd, numpy as np
from scipy.stats import rankdata
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
C=pd.read_csv(ROOT/'data'/'eq6_eq7_verification'/'eq7_fullrecord'/'AEZ26_Eq7_ABC_35pentads_with_offline.csv')
S=pd.read_csv(ROOT/'data'/'pentad_indicators'/'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv')
S['year']=S.year.astype(int); S['pentad_of_year']=S.pentad_of_year.astype(int); sm='ERA5_SM_0_100_mean_mm'
sd45=S.groupby('pentad_of_year')[sm].std()
S['pct45']=S.groupby('pentad_of_year')[sm].transform(lambda s:rankdata(s,method='average')/len(s)*100)
C=C.merge(S[['year','pentad_of_year','pct45']],on=['year','pentad_of_year'],how='left')
C['dSM']=C.B_SM_0_100_mm-C.A_SM_0_100_mm; C['zoff']=C.dSM/C.pentad_of_year.map(sd45); C['month']=pd.to_datetime(C.pentad_start).dt.month
C['period']=np.where(C.year<2000,'1981-99','2000-25')
rows=[]
rows.append(['all','35',len(C),C.dSM.mean(),C.dSM.abs().mean(),C.dSM.abs().max(),C.zoff.abs().max()])
for m,g in C.groupby('month'): rows.append(['month',str(m),len(g),g.dSM.mean(),g.dSM.abs().mean(),g.dSM.abs().max(),g.zoff.abs().max()])
for p,g in C.groupby('period'): rows.append(['period',p,len(g),g.dSM.mean(),g.dSM.abs().mean(),g.dSM.abs().max(),g.zoff.abs().max()])
for lab,g in [('<=20th percentile',C[C.pct45<=20]),('20th-80th percentile',C[(C.pct45>20)&(C.pct45<80)]),('>=80th percentile',C[C.pct45>=80])]: rows.append(['state',lab,len(g),g.dSM.mean(),g.dSM.abs().mean(),g.dSM.abs().max(),g.zoff.abs().max()])
R=pd.DataFrame(rows,columns=['group','level','n','mean_B_minus_A_mm','mean_abs_mm','max_abs_mm','max_abs_in_interannual_SD'])
out=ROOT/'results'/'eq6_eq7_rerun'; out.mkdir(parents=True,exist_ok=True); R.to_csv(out/'eq6_35pentad_soilwater_offsets.csv',index=False); print(R.round(3).to_string(index=False))
