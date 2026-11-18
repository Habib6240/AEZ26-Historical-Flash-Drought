"""Eq. (6) numerical audit (written 2026-11-13 for the Eq. 6/7 closure; NOT part of the original analysis code).
Rebuilds ERA5-Land 0-100 cm soil-water storage  SM = 70*theta1 + 210*theta2 + 720*theta3  (mm; layers 0-7, 7-28, 28-100 cm)
from the nine author-run Phase 7A layer chunks and compares it with the stored ERA5_SM_0_100_mean_mm of the Phase 7A pentad table.
Also checks the chunk files against the recorded SHA-256 values. Requires scripts/stage_flat_inputs.py to have been run."""
import pandas as pd, numpy as np, json, hashlib, os, pathlib, glob
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
D=str(ROOT/'data'/'derived')+'/'; V=ROOT/'data'/'eq6_eq7_verification'/'eq6'
OUT=ROOT/'results'/'eq6_eq7_rerun'; OUT.mkdir(parents=True,exist_ok=True)
files=sorted(glob.glob(str(V/'layer_chunks'/'*.csv')))
rec=pd.read_csv(V/'eq6_chunk_sha256.csv'); rec=dict(zip(rec['file'],rec['sha256']))
hash_ok={os.path.basename(f):hashlib.sha256(open(f,'rb').read()).hexdigest()==rec.get(os.path.basename(f)) for f in files}
C=pd.concat([pd.read_csv(f).assign(source_chunk_file=os.path.basename(f)) for f in files],ignore_index=True)
C['year']=C.year.astype(int); C['pentad_of_year']=C.pentad_of_year.astype(int)
C['rec_mm']=70*C.swvl1_mean_m3m3+210*C.swvl2_mean_m3m3+720*C.swvl3_mean_m3m3
S=pd.read_csv(D+'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv')[['year','pentad_of_year','ERA5_SM_0_100_mean_mm']]
S['year']=S.year.astype(int); S['pentad_of_year']=S.pentad_of_year.astype(int)
m=C.merge(S,on=['year','pentad_of_year'],how='outer',indicator=True)
m['diff']=m.rec_mm-m.ERA5_SM_0_100_mean_mm
m[['year','pentad_of_year','rec_mm','ERA5_SM_0_100_mean_mm','diff']].rename(columns={'ERA5_SM_0_100_mean_mm':'stored_mm'}).to_csv(OUT/'eq6_pentad_comparison.csv',index=False)
res=dict(n_chunks=len(files),chunk_sha256_match=hash_ok,n_pentads_reconstructed=int(C.shape[0]),n_stored=int(S.shape[0]),n_matched=int((m._merge=='both').sum()),
         max_abs_diff_mm=float(m['diff'].abs().max()),n_abs_diff_gt_1e9=int((m['diff'].abs()>1e-9).sum()))
json.dump(res,open(OUT/'eq6_reproduction_summary.json','w'),indent=1); print(json.dumps(res,indent=1))
