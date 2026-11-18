"""Independent re-implementation of the 46 association tests (Spearman + Monte Carlo permutation p, percentile bootstrap, Kruskal-Wallis H, eta2_H, Benjamini-Hochberg within five families) from the event-level table. Seeds: permutation 20261112, bootstrap 20260826. Output: results/phase1_closure/assoc_reproduction.csv."""
import pathlib
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=str(ROOT/'data'/'derived')+'/'
OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
OUT=lambda n: str(OUTD/n)
import pandas as pd,numpy as np,json
from scipy.stats import spearmanr,rankdata
st=pd.read_csv(R+'AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv')
NP=4999;NB=2000;SEED_PERM=20261112;SEED_BOOT=20260826
def rho(x,y): return np.corrcoef(rankdata(x),rankdata(y))[0,1]
def bh(p):
    p=np.asarray(p,float);n=len(p);o=np.argsort(p);q=np.empty(n);prev=1.0
    for rank,i in zip(range(n,0,-1),o[::-1]): prev=min(prev,p[i]*n/rank);q[i]=prev
    return q
fam=[('primary_driver_response','AEZ26_Phase2G_Primary_Driver_Response_Associations.csv'),('secondary_atmospheric_response','AEZ26_Phase2G_Secondary_Atmospheric_Response_Associations.csv'),('event_physics_response','AEZ26_Phase2G_EventPhysics_Response_Associations.csv')]
rows=[]; rngp=np.random.default_rng(SEED_PERM); rngb=np.random.default_rng(SEED_BOOT)
fc={'severity_40pct_deficit_pp_pentads':'severity_40pct_deficit_pp_pentads'}
for fname,f in fam:
    S=pd.read_csv(R+f)
    for r in S.itertuples():
        d=st[[r.predictor,r.outcome]].dropna(); x=d[r.predictor].values;y=d[r.outcome].values;n=len(d)
        ro=rho(x,y); ry=rankdata(y); rx=rankdata(x)
        cnt=0
        for _ in range(NP):
            if abs(np.corrcoef(rx,rngp.permutation(ry))[0,1])>=abs(ro)-1e-12: cnt+=1
        p=(cnt+1)/(NP+1)
        bs=[]
        for _ in range(NB):
            ix=rngb.integers(0,n,n)
            if len(set(x[ix]))>1 and len(set(y[ix]))>1: bs.append(rho(x[ix],y[ix]))
        lo,hi=np.percentile(bs,[2.5,97.5])
        rows.append(dict(family=fname,predictor=r.predictor,outcome=r.outcome,n=n,n_stored=r.n,rho=ro,rho_stored=r.rho,p_perm=p,p_stored=r.p_perm,ci_low=lo,ci_low_stored=r.ci_low,ci_high=hi,ci_high_stored=r.ci_high,q_stored=r.p_fdr_bh))
C=pd.read_csv(R+'AEZ26_Phase2G_Cross_Response_Coupling.csv')
for r in C.itertuples():
    d=st[[r.response_x,r.response_y]].dropna(); x=d[r.response_x].values;y=d[r.response_y].values;n=len(d)
    ro=rho(x,y);rx=rankdata(x);ry=rankdata(y)
    cnt=sum(abs(np.corrcoef(rx,rngp.permutation(ry))[0,1])>=abs(ro)-1e-12 for _ in range(NP)); p=(cnt+1)/(NP+1)
    bs=[]
    for _ in range(NB):
        ix=rngb.integers(0,n,n)
        if len(set(x[ix]))>1 and len(set(y[ix]))>1: bs.append(rho(x[ix],y[ix]))
    lo,hi=np.percentile(bs,[2.5,97.5])
    rows.append(dict(family='cross_response',predictor=r.response_x,outcome=r.response_y,n=n,n_stored=r.n,rho=ro,rho_stored=r.rho,p_perm=p,p_stored=r.p_perm,ci_low=lo,ci_low_stored=r.ci_low,ci_high=hi,ci_high_stored=r.ci_high,q_stored=r.p_fdr_bh))
# driver class KW
K=pd.read_csv(R+'AEZ26_Phase2G_DriverClass_Response_Comparisons.csv')
kw=[]
for r in K.itertuples():
    d=st[['primary_driver_class',r.outcome]].dropna(); g=d.primary_driver_class.values; y=d[r.outcome].values; n=len(d); ks=sorted(set(g))
    def H(y,g):
        rk=rankdata(y); h=12/(n*(n+1))*sum((rk[g==k].sum()**2)/(g==k).sum() for k in ks)-3*(n+1)
        # tie correction
        _,c=np.unique(y,return_counts=True); return h/(1-(c**3-c).sum()/(n**3-n))
    h=H(y,g); cnt=sum(H(y,rngp.permutation(g))>=h-1e-12 for _ in range(NP)); p=(cnt+1)/(NP+1)
    e2=max(0,(h-len(ks)+1)/(n-len(ks)))
    kw.append(dict(family='driver_class_KW',predictor='primary_driver_class',outcome=r.outcome,n=n,n_stored=r.n,rho=h,rho_stored=r.H,p_perm=p,p_stored=r.p_perm,ci_low=e2,ci_low_stored=r.epsilon2,ci_high=np.nan,ci_high_stored=np.nan,q_stored=r.p_fdr_bh))
A=pd.DataFrame(rows+kw)
A['q_from_own_p']=np.nan; A['q_from_stored_p']=np.nan
for f in A.family.unique():
    i=A.family==f; A.loc[i,'q_from_own_p']=bh(A.loc[i,'p_perm']); A.loc[i,'q_from_stored_p']=bh(A.loc[i,'p_stored'])
A['rho_diff']=A.rho-A.rho_stored; A['p_diff']=A.p_perm-A.p_stored
A['mc_se']=np.sqrt(A.p_stored*(1-A.p_stored)/NP)
A['p_within_3se']=A.p_diff.abs()<=3*A.mc_se+0.0005
A['q_own_le_0.05']=A.q_from_own_p<=0.05; A['q_stored_le_0.05']=A.q_stored<=0.05
A.to_csv(OUT('assoc_reproduction.csv'),index=False)
pd.set_option('display.width',250)
print(len(A),A.family.value_counts().to_dict())
print('max |rho diff| (Spearman rows):',A[A.family!='driver_class_KW'].rho_diff.abs().max(),' KW H diff:',A[A.family=='driver_class_KW'].rho_diff.abs().max(),' eta2 diff:',(A[A.family=='driver_class_KW'].ci_low-A[A.family=='driver_class_KW'].ci_low_stored).abs().max())
print('p within 3 SE:',int(A.p_within_3se.sum()),'of',len(A),' max |p diff|:',A.p_diff.abs().max())
print('n differs:',int((A.n!=A.n_stored).sum()))
print('q (own p) vs stored q: max abs diff',(A.q_from_own_p-A.q_stored).abs().max(),' q(from stored p) vs stored q',(A.q_from_stored_p-A.q_stored).abs().max())
print('FDR flags own/stored:',int(A['q_own_le_0.05'].sum()),int(A['q_stored_le_0.05'].sum()),'min q own',A.q_from_own_p.min())
print('CI max abs diff lo/hi:',(A.ci_low-A.ci_low_stored)[A.family!='driver_class_KW'].abs().max(),(A.ci_high-A.ci_high_stored).abs().max())
print(A[~A.p_within_3se][['family','predictor','outcome','p_perm','p_stored']].round(4).to_string())
