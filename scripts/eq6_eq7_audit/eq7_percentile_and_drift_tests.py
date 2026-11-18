# Paths resolved relative to the repository root. Requires the flat input view created by scripts/stage_flat_inputs.py (data/derived/).
import os, pathlib
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
D=str(ROOT/'data'/'derived')+'/'; V=str(ROOT/'data'/'eq6_eq7_verification')+'/'
OUT=str(ROOT/'results'/'eq6_eq7_rerun')+'/'; os.makedirs(OUT,exist_ok=True)
import pandas as pd, numpy as np
from scipy.stats import rankdata
m=pd.read_csv(OUT+'pentad_comparison_23.csv')
S=pd.read_csv(D+'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv').sort_values(['year','pentad_of_year']).reset_index(drop=True)
# percentile reproduction
def pct(df,col,y0,y1):
    out=pd.Series(np.nan,index=df.index)
    for p,g in df[df.year.between(y0,y1)].groupby('pentad_of_year'):
        r=rankdata(g[col].values,method='average'); out[g.index]=(r-0.5)/len(g)*100
    return out
for nm,(y0,y1) in {'ERA5_SM_pct_OVERLAP26':(2000,2025),'ERA5_SM_pct_LONG45':(1981,2025)}.items():
    p=pct(S,'ERA5_SM_0_100_mean_mm',y0,y1); ok=p.notna()
    print(nm,'max|diff|',np.abs(p[ok]-S.loc[ok,nm]).max())
# interannual SD of SM per pentad-of-year (to convert mm into SD units)
sd=S.groupby('pentad_of_year').ERA5_SM_0_100_mean_mm.std(ddof=1)
m['sm_sd_pentad']=m.pentad_of_year.map(sd); m['dSM_in_sd']=m.d_SM_0_100_mm/m.sm_sd_pentad
print(m[['year','pentad_of_year','d_SM_0_100_mm','sm_sd_pentad','dSM_in_sd']].round(3).to_string())
print('|dSM|/sd: mean %.3f max %.3f'%(m.dSM_in_sd.abs().mean(),m.dSM_in_sd.abs().max()))
# within-pentad year-to-year SD of d (P12,P13 four leap years)
W=m[m.pentad_of_year.isin([12,13])]; 
def pooled(col):
    v=0;df=0
    for p,g in W.groupby('pentad_of_year'): v+=g[col].var(ddof=1)*(len(g)-1); df+=len(g)-1
    return np.sqrt(v/df)
vars_=['d_t2m_C','d_td_C','d_RH_pct','d_VPD_mean_kPa','d_VPD_max_kPa','d_SM_0_100_mm']
P={v:pooled(v) for v in vars_}; print('pooled within-pentad SD of (B-A), df=6:',{k:round(v,4) for k,v in P.items()})
pd.Series(P).to_csv(OUT+'pooled_year_to_year_sd.csv',header=['sd'])
# drift test with pentad fixed effects (P12,P13 across 1988,2000,2016,2024)
import numpy.linalg as la
for v in vars_:
    y=W[v].values; yr=W.year.values; fe=(W.pentad_of_year.values==13).astype(float)
    Xm=np.c_[np.ones(len(y)),fe,(yr-2006)/10]; b,res,rk,_=la.lstsq(Xm,y,rcond=None)
    resid=y-Xm@b; s2=resid@resid/(len(y)-3); cov=s2*la.inv(Xm.T@Xm); se=np.sqrt(cov[2,2])
    from scipy.stats import t
    tc=t.ppf(.975,len(y)-3); print(v,'slope/decade %.4f  95%%CI [%.4f, %.4f]'%(b[2],b[2]-tc*se,b[2]+tc*se))
