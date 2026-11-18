"""Consensus-event sensitivity analysis defined in documentation/PRESPEC_consensus_analysis.md (written before the analysis)."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=str(ROOT/'data'/'derived')+'/'
OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
OUT=lambda n: str(OUTD/n)
import pandas as pd,numpy as np,json,hashlib
from scipy.stats import mannwhitneyu,fisher_exact,spearmanr
_b=open(str(ROOT/'documentation'/'PRESPEC_consensus_analysis.md'),'rb').read()
# the pre-specification section (before the later addenda) must match the hash recorded before the analysis was run
spec_hash=hashlib.sha256(_b[:_b.index(b'## Addendum A')-1]).hexdigest()
assert spec_hash.startswith('e2e996dabb14')
st=pd.read_csv(R+'AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv')
gc=pd.read_csv(R+'AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv')
assert (st.event_id==gc.event_id).all()
ordn=lambda s:int(s.split('_P')[0])*73+int(s.split('_P')[1])
sc=pd.read_csv(R+'AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv')
lc=pd.read_csv(R+'AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv'); lc=lc[lc.onset_year.between(2000,2025)]
go=[ordn(s) for s in gc.onset_pentad]
def match(a,b,tol):
    c=sorted((abs(x-y),i,j) for i,x in enumerate(a) for j,y in enumerate(b) if abs(x-y)<=tol)
    ua,ub,pr=set(),set(),[]
    for d,i,j in c:
        if i not in ua and j not in ub: ua.add(i);ub.add(j);pr.append((i,j,d))
    return pr
sets={'C_primary (OVERLAP26, +-2)':(sc,2),'C_pm1 (OVERLAP26, +-1)':(sc,1),'C_exact (OVERLAP26, 0)':(sc,0),'C_LONG45 (+-2)':(lc,2)}
masks={k:np.array([i in {a for a,_,_ in match(go,[ordn(s) for s in cat.onset_pentad],t)} for i in range(39)]) for k,(cat,t) in sets.items()}
vars_c=['total_duration_pentads_driver','severity_40pct_deficit_pp_pentads','mean_intensification_rate_pp_per_pentad','P_deficit_strength_z','VPD_excess_strength_z','temperature_excess_strength_z',
 'MOD16_ETPET_response_depth_z','MOD13_NDVI_response_depth_z','GRACE_TWSA_response_depth_z','JRC_water_response_depth_z',
 'event_weighted_ETPET_z','event_weighted_NDVI_z','event_weighted_TWSA_z','event_weighted_water_fraction_z',
 'minimum_ETPET_z_onset_to_post64','minimum_NDVI_z_onset_to_post96','minimum_TWSA_z_onset_to_post365','minimum_water_fraction_z_onset_to_post180',
 'lag_onset_to_minimum_ETPET_days','lag_onset_to_minimum_NDVI_days','lag_onset_to_minimum_TWSA_days','lag_onset_to_minimum_water_fraction_days']
st['jjas']=(st.onset_season_driver=='Monsoon_JJAS').astype(int)
out=[]
for name,m in masks.items():
    C,N=st[m],st[~m]
    for v in vars_c:
        a,b=C[v].dropna(),N[v].dropna()
        p=mannwhitneyu(a,b,alternative='two-sided').pvalue if len(a)>=3 and len(b)>=3 else np.nan
        out.append(dict(set=name,variable=v,nC=len(a),nN=len(b),medianC=a.median() if len(a) else np.nan,medianN=b.median() if len(b) else np.nan,p_MWU=p))
    ct=[[C.jjas.sum(),len(C)-C.jjas.sum()],[N.jjas.sum(),len(N)-N.jjas.sum()]]
    out.append(dict(set=name,variable='JJAS onset count (C: JJAS/other | N: JJAS/other)',nC=len(C),nN=len(N),medianC=C.jjas.mean(),medianN=N.jjas.mean(),p_MWU=fisher_exact(ct)[1]))
O=pd.DataFrame(out)
def bh(p):
    p=np.asarray(p,float);n=len(p);o=np.argsort(p);q=np.empty(n);prev=1.0
    for rank,i in zip(range(n,0,-1),o[::-1]):
        prev=min(prev,p[i]*n/rank);q[i]=prev
    return q
O['q_BH_within_set']=np.nan
for s in O.set.unique():
    i=O.set==s; pv=O.loc[i,'p_MWU']; ok=pv.notna()
    q=pd.Series(np.nan,index=pv.index); q[ok]=bh(pv[ok].values); O.loc[i,'q_BH_within_set']=q
O.to_csv(OUT('consensus_comparisons.csv'),index=False)
# driver classes
dc=pd.crosstab(masks['C_primary (OVERLAP26, +-2)'],st.primary_driver_class); print(dc)
dc.to_csv(OUT('consensus_driver_classes.csv'))
# primary associations
pa=pd.read_csv(R+'AEZ26_Phase2G_Primary_Driver_Response_Associations.csv')
rng_seed=20260826
rows=[]
m=masks['C_primary (OVERLAP26, +-2)']
for r in pa.itertuples():
    x,y=r.predictor,r.outcome
    full=st[[x,y]].dropna(); rho_full=spearmanr(full[x],full[y])[0]
    sub=st[m][[x,y]].dropna(); 
    if len(sub)>=5:
        rho_c=spearmanr(sub[x],sub[y])[0]; rng=np.random.default_rng(rng_seed); bs=[]
        for _ in range(2000):
            ix=rng.integers(0,len(sub),len(sub)); s=sub.iloc[ix]
            if s[x].nunique()>1 and s[y].nunique()>1: bs.append(spearmanr(s[x],s[y])[0])
        lo,hi=np.percentile(bs,[2.5,97.5])
    else: rho_c=lo=hi=np.nan
    nm=st[~m][[x,y]].dropna(); rho_n=spearmanr(nm[x],nm[y])[0] if len(nm)>=5 else np.nan
    holds=('n/a' if np.isnan(rho_c) else ('unchanged' if (np.sign(rho_c)==np.sign(rho_full) and lo<=rho_full<=hi) else 'not reproduced'))
    rows.append(dict(predictor=x,outcome=y,n_full=len(full),rho_full=rho_full,rho_stored=r.rho,nC=len(sub),rho_C=rho_c,ciC_low=lo,ciC_high=hi,nN=len(nm),rho_N=rho_n,C_interval_includes_zero=(lo<=0<=hi) if not np.isnan(lo) else None,rule_outcome=holds))
A=pd.DataFrame(rows); A.to_csv(OUT('consensus_associations.csv'),index=False)
print(A.round(3).to_string())
print(O[O.set.str.startswith('C_primary')].round(3).to_string())
print({k:int(v.sum()) for k,v in masks.items()})
json.dump({k:[int(i) for i in np.where(v)[0]] for k,v in masks.items()},open(OUT('consensus_masks.json'),'w'))
