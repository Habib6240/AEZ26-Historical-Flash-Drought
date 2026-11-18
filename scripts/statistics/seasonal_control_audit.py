"""Seasonal-control audit of the land-water response analysis (checks 1-3 of Addendum A in documentation/PRESPEC_consensus_analysis.md). No random-date placebo is possible: raw native series are not archived."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=str(ROOT/'data'/'derived')+'/'
OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
OUT=lambda n: str(OUTD/n)
import pandas as pd,numpy as np,json
from scipy.stats import wilcoxon,binomtest
st=pd.read_csv(R+'AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv')
prod={'MOD16 ET/PET':('MOD16','ET_PET_ratio_primary_z','minimum_ETPET_z_onset_to_post64','event_weighted_ETPET_z'),
      'MOD13 NDVI':('MOD13','NDVI_standardQA_z','minimum_NDVI_z_onset_to_post96','event_weighted_NDVI_z'),
      'GRACE TWSA':('GRACE_TWSA','TWSA_z','minimum_TWSA_z_onset_to_post365','event_weighted_TWSA_z'),
      'JRC water fraction':('JRC_Qualified','water_fraction_z','minimum_water_fraction_z_onset_to_post180','event_weighted_water_fraction_z')}
rng=np.random.default_rng(20261112); cache={}
def emin(n):
    if n not in cache: cache[n]=rng.standard_normal((200000,n)).min(axis=1).mean() if n>0 else np.nan
    return cache[n]
rows=[];ev=[]
for name,(f,zc,mincol,ewcol) in prod.items():
    L=pd.read_csv(R+f'AEZ26_Phase2F_{f}_Seasonal_Anomaly_Links.csv')
    # 1 event-period mean anomaly vs 0
    ew=st[ewcol].dropna()
    w=wilcoxon(ew); sg=binomtest(int((ew<0).sum()),len(ew),0.5)
    rows.append(dict(product=name,check='event-weighted z vs 0',n=len(ew),median=ew.median(),n_negative=int((ew<0).sum()),p_wilcoxon=w.pvalue,p_sign=sg.pvalue))
    # 2/3 selection reference and pre-event control
    per=[]
    for eid,g in L.groupby('event_id'):
        pre=g[g.alignment_phase=='pre_event_context'][zc].dropna(); post=g[g.alignment_phase!='pre_event_context'][zc].dropna()
        if len(post)==0: continue
        sm=st.loc[st.event_id==eid,mincol].values[0]
        per.append(dict(event_id=eid,n_pre=len(pre),n_post=len(post),pre_min=pre.min() if len(pre) else np.nan,post_min_links=post.min(),post_min_stored=sm))
    P=pd.DataFrame(per)
    P['stored_match']=np.isclose(P.post_min_links,P.post_min_stored,equal_nan=True)
    P['E_post']=[emin(int(n)) for n in P.n_post]; P['E_pre']=[emin(int(n)) if n>0 else np.nan for n in P.n_pre]
    P['excess_post']=P.post_min_stored-P.E_post; P['excess_pre']=P.pre_min-P.E_pre
    P['product']=name; ev.append(P)
    d=P.dropna(subset=['excess_post','excess_pre'])
    wp=wilcoxon(d.excess_post-d.excess_pre) if len(d)>=6 else None
    rows.append(dict(product=name,check='selection reference (iid upper bound)',n=len(P),median_observed_min=P.post_min_stored.median(),median_iid_expected_min=P.E_post.median(),median_excess=P.excess_post.median(),median_n_records=P.n_post.median(),stored_min_reproduced_from_links=int(P.stored_match.sum())))
    rows.append(dict(product=name,check='pre-event control: excess pre vs post (paired)',n=len(d),median_excess_pre=d.excess_pre.median(),median_excess_post=d.excess_post.median(),median_n_pre=P.n_pre.median(),p_wilcoxon=(wp.pvalue if wp else np.nan)))
R_=pd.DataFrame(rows); R_.to_csv(OUT('seasctl_summary.csv'),index=False); pd.concat(ev).to_csv(OUT('seasctl_events.csv'),index=False)
pd.set_option('display.width',250); print(R_.round(3).to_string())
