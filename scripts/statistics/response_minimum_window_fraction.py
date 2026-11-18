"""POST HOC check 4 (Addendum B in documentation/PRESPEC_consensus_analysis.md): position of each response minimum within its search window (lag from onset / window length; window = onset to event end + post-event window of 64, 96, 365, 180 d)."""
import pathlib, numpy as np, pandas as pd
from scipy.stats import wilcoxon
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=ROOT/'data'/'derived'; OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
st=pd.read_csv(R/'AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv')
dur=(pd.to_datetime(st.event_end_date)-pd.to_datetime(st.onset_start_date)).dt.days+1
rows=[]
for name,col,post in [('MOD16 ET/PET','lag_onset_to_minimum_ETPET_days',64),('MOD13 NDVI','lag_onset_to_minimum_NDVI_days',96),('GRACE TWSA','lag_onset_to_minimum_TWSA_days',365),('JRC water fraction','lag_onset_to_minimum_water_fraction_days',180)]:
    lag=st[col]; win=dur+post; f=(lag/win).dropna(); w=win[f.index]
    rows.append(dict(product=name,n=len(f),median_lag_days=lag.dropna().median(),median_window_days=w.median(),median_fraction=f.median(),iqr=f"{f.quantile(.25):.2f}-{f.quantile(.75):.2f}",p_wilcoxon_vs_0p5=wilcoxon(f-0.5).pvalue))
A=pd.DataFrame(rows); A.to_csv(OUTD/'seasctl_timing_fraction.csv',index=False); print(A.to_string())
