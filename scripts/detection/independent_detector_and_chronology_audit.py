"""Independent re-implementation of the first-crossing percentile detector (Section 3.1). Asserts exact reproduction of the stored 39-event GLDAS catalogue and the stored ERA5-Land OVERLAP26 catalogue, then runs the chronology audit (one-to-one matching, year-shift null, non-match classification, percentile resolution, LONG45 matching)."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=str(ROOT/'data'/'derived')+'/'
OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
OUT=lambda n: str(OUTD/n)
import pandas as pd,numpy as np,json
g=pd.read_csv(R+'AEZ26_Pentad_Hydroclimate_Indicators_2000_2025.csv').sort_values(['year','pentad_of_year']).reset_index(drop=True)
e=pd.read_csv(R+'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv')
e=e[e.year.between(2000,2025)].sort_values(['year','pentad_of_year']).reset_index(drop=True)
assert (g.year.values==e.year.values).all() and (g.pentad_of_year.values==e.pentad_of_year.values).all()
ord_=lambda s:int(s.split('_P')[0])*73+int(s.split('_P')[1])
base=2000*73+1
def detect(pct,log=None):
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
                ok=r>=5 and du>=3
                rec=dict(anchor=i,onset=on,cross=j,end=end,rate=r,dur=du,accepted=ok,reason='accepted' if ok else ('rate<5 and duration<3' if (r<5 and du<3) else ('rate<5' if r<5 else 'duration<3')))
                ev.append(rec);i=n if cens else k;done=True;break
            j+=1
        if not done:i+=1
    return ev
gp=g.SM_0_100_pct.to_numpy(float); ep=e.ERA5_SM_pct_OVERLAP26.to_numpy(float)
G=[x for x in detect(gp) if x['accepted']]; Eall=detect(ep); E=[x for x in Eall if x['accepted']]
print(len(G),len(E),len(Eall))
# check vs stored catalogues
cat=pd.read_csv(R+'AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv')
lab=lambda ix:f"{int(g.year[ix])}_P{int(g.pentad_of_year[ix]):02d}"
assert [lab(x['onset']) for x in E]==cat.onset_pentad.tolist()
gcat=pd.read_csv(R+'AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv')
assert [lab(x['onset']) for x in G]==gcat.onset_pentad.tolist()
def match(a,b,tol):
    c=sorted((abs(x-y),i,j) for i,x in enumerate(a) for j,y in enumerate(b) if abs(x-y)<=tol)
    ua,ub,pr=set(),set(),[]
    for d,i,j in c:
        if i not in ua and j not in ub: ua.add(i);ub.add(j);pr.append((i,j,d))
    return pr
go=[x['onset'] for x in G]; eo=[x['onset'] for x in E]
res={'n_gldas':len(G),'n_era5':len(E),'rejected_era5_episodes':len(Eall)-len(E)}
for t in (0,1,2): res[f'matches_tol{t}']=len(match(go,eo,t))
# per-event diagnosis for GLDAS events not matched at +-2
pr2=match(go,eo,2); mi={i:(j,d) for i,j,d in pr2}
rows=[]
for k,x in enumerate(G):
    o,c,en=x['onset'],x['cross'],x['end']; lo,hi=max(0,o-3),min(len(ep)-1,en+3)
    nearest=min(eo,key=lambda y:abs(y-o)); dnear=nearest-o
    rej=[r for r in Eall if not r['accepted'] and abs(r['onset']-o)<=2]
    win=ep[max(0,c-2):min(len(ep),c+3)]
    # classify
    if k in mi: cl='matched +-2'; why=''
    else:
        if len(rej): cl='ERA5 candidate rejected'; why=rej[0]['reason']
        elif ep[max(0,o-1):en+2].min()>20: cl='ERA5 never reaches <=20 percentile'; why=''
        elif abs(dnear)<=5 and abs(dnear)>2: cl='ERA5 event, timing offset 3-5 pentads'; why=''
        elif ep[max(0,o-4):o+1].max()<=40: cl='ERA5 no >40 anchor before crossing'; why=''
        else: cl='other (ERA5 episode consumed by a neighbouring event or different anchor)'; why=''
    rows.append(dict(event=gcat.event_id[k],onset=lab(o),gldas_cross_pct=gp[c],gldas_end=lab(en),gldas_rate=x['rate'],gldas_dur=x['dur'],era5_pct_at_gldas_cross=ep[c],era5_min_pct_cross_pm2=win.min(),era5_pct_at_anchor=ep[x['anchor']],gldas_pct_at_anchor=gp[x['anchor']],nearest_era5_onset=lab(nearest),offset_pentads=dnear,matched_pm2=k in mi,class_=cl,reject_reason=why,gldas_cross_margin_below20=20-gp[c]))
D=pd.DataFrame(rows); D.to_csv(OUT('chron_event_diagnosis.csv'),index=False)
res['class_counts']=D.class_.value_counts().to_dict()
res['reject_reasons']=D[D.reject_reason!=''].reject_reason.value_counts().to_dict()
# series agreement
from scipy.stats import spearmanr
res['spearman_pct']=float(spearmanr(gp,ep)[0]); d=ep-gp
res['pct_diff_mean']=float(d.mean());res['pct_diff_sd']=float(d.std());res['pct_absdiff_median']=float(np.median(abs(d)));res['pct_absdiff_p90']=float(np.percentile(abs(d),90))
# near-threshold fragility
res['gldas_events_cross_pct_ge15']=int((D.gldas_cross_pct>=15).sum()); res['gldas_events_cross_pct_ge10']=int((D.gldas_cross_pct>=10).sum())
res['gldas_cross_pct_median']=float(D.gldas_cross_pct.median())
# percentile resolution
res['crossing_rank_counts']=D.gldas_cross_pct.round(2).value_counts().to_dict()
res['n_cross_at_max_rank5']=int((D.gldas_cross_pct.round(2)==19.23).sum())
# year-shift null
Ee=np.array(eo)-base; n=len(ep); out={}
for t in (0,1,2):
    obs=len(match(go,eo,t)); nulls=[]
    for k in range(1,26):
        sh=sorted((x+k*73)%n for x in eo); nulls.append(len(match(go,sh,t)))
    out[t]=dict(observed=obs,null_mean=float(np.mean(nulls)),null_min=int(min(nulls)),null_max=int(max(nulls)),p=(1+sum(1 for v in nulls if v>=obs))/26)
res['yearshift_null']=out
# same for LONG45 restricted
lc=pd.read_csv(R+'AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv')
lc=lc[lc.onset_year.between(2000,2025)]; lo=[ord_(s)-base for s in lc.onset_pentad]; go0=list(go)
res['long45_n']=len(lo); res['long45_matches']={t:len(match(go0,lo,t)) for t in (0,1,2)}
# which GLDAS events matched in both
json.dump(res,open(OUT('chron_res.json'),'w'),indent=1,default=str); print(json.dumps(res,indent=1,default=str)); print(D[['onset','gldas_cross_pct','era5_pct_at_gldas_cross','nearest_era5_onset','offset_pentads','class_','reject_reason']].to_string())
