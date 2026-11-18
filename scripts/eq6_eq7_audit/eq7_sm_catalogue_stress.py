# Paths resolved relative to the repository root. Requires the flat input view created by scripts/stage_flat_inputs.py (data/derived/).
import os, pathlib
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
D=str(ROOT/'data'/'derived')+'/'; V=str(ROOT/'data'/'eq6_eq7_verification')+'/'
OUT=str(ROOT/'results'/'eq6_eq7_rerun')+'/'; os.makedirs(OUT,exist_ok=True)
import pandas as pd, numpy as np, json
from scipy.stats import rankdata
S=pd.read_csv(D+'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv').sort_values(['year','pentad_of_year']).reset_index(drop=True)
gc=pd.read_csv(D+'AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv')
lab2idx=lambda s:(int(s[:4])-1981)*73+int(s[-2:])-1
G=np.array([lab2idx(s) for s in gc.onset_pentad])      # index in 1981-based sequence
def detect(pct):
    n=len(pct);ev=[];i=0
    while i<n-1:
        if pct[i]<=40:i+=1;continue
        j=i+1;done=False
        while j<n:
            if pct[j]>40:i=j;done=True;break
            if pct[j]<=20:
                r=(pct[i]-pct[j])/(j-i);k=j+1
                while k<n and pct[k]<20:k+=1
                cens=k>=n;end=n-1 if cens else k-1;on=i+1;du=end-on+1
                if r>=5 and du>=3: ev.append(dict(onset=on,cross=j,end=end,dur=du,rate=r))
                i=n if cens else k;done=True;break
            j+=1
        if not done:i+=1
    return ev
def match(a,b,tol):
    c=sorted((abs(x-y),i,j) for i,x in enumerate(a) for j,y in enumerate(b) if abs(x-y)<=tol)
    ua,ub,n=set(),set(),0
    for d,i,j in c:
        if i not in ua and j not in ub: ua.add(i);ub.add(j);n+=1
    return n
yr=S.year.values; pp=S.pentad_of_year.values
def percentiles(sm,y0):
    out=np.full(len(sm),np.nan)
    for p in range(1,74):
        ix=np.where((pp==p)&(yr>=y0))[0]; out[ix]=rankdata(sm[ix],method='average')/len(ix)*100
    return out
sm0=S.ERA5_SM_0_100_mean_mm.values
def run(sm):
    # OVERLAP26: 2000-2025 sequence; LONG45: 1981-2025 sequence, onsets >=2000
    s26=(yr>=2000); o26=detect(percentiles(sm,2000)[s26]); off=np.where(s26)[0][0]
    ons26=[e['onset']+off for e in o26]
    l45=detect(percentiles(sm,1981)); ons45=[e['onset'] for e in l45]; ons45r=[x for x in ons45 if yr[x]>=2000]
    return dict(o26=ons26,l45=ons45,l45r=ons45r,o26ev=o26,l45ev=l45)
base=run(sm0); print('baseline OVERLAP26',len(base['o26']),'LONG45',len(base['l45']),'LONG45>=2000',len(base['l45r']))
def agree(ons): return [match(list(G),ons,t) for t in (0,1,2)]
print('baseline agreement OVERLAP26 (0,±1,±2):',agree(base['o26']),' LONG45r:',agree(base['l45r']))
rng=np.random.default_rng(20261113)
def mc(sd,nrep):
    rows=[]
    for r in range(nrep):
        res=run(sm0+rng.normal(0,sd,len(sm0)))
        b26,p26=set(base['o26']),set(res['o26']); b45,p45=set(base['l45r']),set(res['l45r'])
        rows.append(dict(n26=len(p26),n45r=len(p45),n45=len(res['l45']),chg26=len(b26^p26),chg45=len(b45^p45),exact_same26=(b26==p26),exact_same45=(b45==p45),
          a26=agree(res['o26']),a45=agree(res['l45r']),
          dur_med26=np.median([e['dur'] for e in res['o26ev']]) if res['o26ev'] else np.nan))
    return pd.DataFrame(rows)
out={}
for lbl,sd in [('1x pooled year-to-year SD (0.56 mm)',0.5638),('3x (1.69 mm)',3*0.5638),('max observed |B-A| (3.25 mm)',3.2477)]:
    D=mc(sd,100)
    a26=np.array(D.a26.tolist()); a45=np.array(D.a45.tolist())
    out[lbl]=dict(sd_mm=sd,OVERLAP26_n_mean=D.n26.mean(),OVERLAP26_n_range=[int(D.n26.min()),int(D.n26.max())],OVERLAP26_changed_onsets_mean=D.chg26.mean(),OVERLAP26_changed_max=int(D.chg26.max()),OVERLAP26_identical_frac=D.exact_same26.mean(),
      LONG45r_n_range=[int(D.n45r.min()),int(D.n45r.max())],LONG45r_changed_mean=D.chg45.mean(),LONG45r_identical_frac=D.exact_same45.mean(),
      agree26_mean=a26.mean(0).round(2).tolist(),agree26_min=a26.min(0).tolist(),agree26_max=a26.max(0).tolist(),agree45_mean=a45.mean(0).round(2).tolist(),agree45_min=a45.min(0).tolist(),agree45_max=a45.max(0).tolist())
    print(lbl); print(json.dumps(out[lbl],default=float))
json.dump(out,open(OUT+'era5_catalogue_mc.json','w'),indent=1,default=float)
json.dump(dict(base_n26=len(base['o26']),base_n45=len(base['l45']),base_n45r=len(base['l45r']),agree26=agree(base['o26']),agree45r=agree(base['l45r'])),open(OUT+'era5_baseline.json','w'))
