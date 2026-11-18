# Paths resolved relative to the repository root. Requires the flat input view created by scripts/stage_flat_inputs.py (data/derived/).
import os, pathlib
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
D=str(ROOT/'data'/'derived')+'/'; V=str(ROOT/'data'/'eq6_eq7_verification')+'/'
OUT=str(ROOT/'results'/'eq6_eq7_rerun')+'/'; os.makedirs(OUT,exist_ok=True)
import pandas as pd, numpy as np
X=pd.read_csv(V+'eq7/AEZ26_Eq7_Temporal_Robustness_23pentads_v02.csv')
S=pd.read_csv(D+'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv')
m=X.merge(S[['year','pentad_of_year','t2m_mean_C','relative_humidity_mean_pct','VPD_mean_kPa','VPD_dailymean_max_kPa','ERA5_SM_0_100_mean_mm']],on=['year','pentad_of_year'])
print(len(X),len(m))
# 1 A vs stored 7A
pairs=[('t2m_C','t2m_mean_C'),('RH_pct','relative_humidity_mean_pct'),('VPD_mean_kPa','VPD_mean_kPa'),('VPD_max_kPa','VPD_dailymean_max_kPa'),('SM_0_100_mm','ERA5_SM_0_100_mean_mm')]
rows=[]
for a,s in pairs:
    d=m['A_'+a]-m[s]; rows.append((a,d.abs().max(),d.abs().mean()))
print('A vs archived 7A (max, MAE):'); [print(' ',r[0],'%.3e %.3e'%(r[1],r[2])) for r in rows]
print('B==C max diff:',max((m['B_'+v]-m['C_'+v]).abs().max() for v in ['t2m_C','td_C','RH_pct','VPD_mean_kPa','VPD_max_kPa','SM_0_100_mm','n_sum','n_count']))
print('n_sum A',m.A_n_sum.unique(),'B',m.B_n_sum.unique(),'counts',m.A_n_count.unique(),m.B_n_count.unique())
print('era5 images==n_days',(m.era5_images==m.n_days).all())
vars_=['t2m_C','td_C','RH_pct','VPD_mean_kPa','VPD_max_kPa','SM_0_100_mm']
for v in vars_: m['d_'+v]=m['B_'+v]-m['A_'+v]
def st(x): return dict(bias=x.mean(),MAE=x.abs().mean(),RMSE=np.sqrt((x**2).mean()),max=x.abs().max(),sd=x.std(ddof=1),min=x.min(),maxv=x.max())
T=pd.DataFrame({v:st(m['d_'+v]) for v in vars_}).T; pd.set_option('display.width',200); print('B-A overall (n=23)\n',T.round(5))
T.to_csv(OUT+'BA_overall.csv')
S2=m.groupby('stratum')[['d_'+v for v in vars_]].agg(['mean',lambda x:x.abs().mean()]); 
print(m.groupby('stratum')[['d_t2m_C','d_td_C','d_VPD_mean_kPa','d_RH_pct','d_SM_0_100_mm']].agg(lambda x:x.abs().mean()).round(4))
print(m.groupby('stratum')[['d_t2m_C','d_td_C','d_VPD_mean_kPa','d_RH_pct','d_SM_0_100_mm']].mean().round(4))
m.to_csv(OUT+'pentad_comparison_23.csv',index=False)
# same-pentad repeats
print(m[m.pentad_of_year.isin([12,13])][['year','pentad_of_year','d_t2m_C','d_td_C','d_RH_pct','d_VPD_mean_kPa','d_VPD_max_kPa','d_SM_0_100_mm']].round(4).sort_values(['pentad_of_year','year']).to_string())
print(m[m.pentad_of_year.isin([52,53,54,55,56])][['year','pentad_of_year','d_t2m_C','d_td_C','d_RH_pct','d_VPD_mean_kPa','d_SM_0_100_mm']].round(4).sort_values(['pentad_of_year','year']).to_string())
