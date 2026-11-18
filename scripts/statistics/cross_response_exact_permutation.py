"""2,000,000-permutation re-estimate of the six cross-response Spearman pairs (seed 20261113) and BH q within the six-test family. Output: results/phase1_closure/cross_exact.csv."""
import pathlib, numpy as np, pandas as pd
from scipy.stats import rankdata
ROOT=pathlib.Path(__file__).resolve().parents[2]
R=ROOT/'data'/'derived'; OUTD=ROOT/'results'/'phase1_closure'; OUTD.mkdir(parents=True,exist_ok=True)
st=pd.read_csv(R/'AEZ26_Phase2G_Event_Statistical_Analysis_Table.csv')
C=pd.read_csv(R/'AEZ26_Phase2G_Cross_Response_Coupling.csv')
NP=2_000_000; rng=np.random.default_rng(20261113)
def bh(p):
    p=np.asarray(p,float);n=len(p);o=np.argsort(p);q=np.empty(n);prev=1.0
    for rank,i in zip(range(n,0,-1),o[::-1]): prev=min(prev,p[i]*n/rank);q[i]=prev
    return q
rows=[]
for r in C.itertuples():
    d=st[[r.response_x,r.response_y]].dropna(); rx=rankdata(d[r.response_x].values); ry=rankdata(d[r.response_y].values); n=len(d)
    ro=np.corrcoef(rx,ry)[0,1]; rxc=(rx-rx.mean())/rx.std(); ryc=(ry-ry.mean())/ry.std(); cnt=0; B=200_000
    for _ in range(NP//B):
        perm=np.argsort(rng.random((B,n)),axis=1); ys=ryc[perm]
        cnt+=int((np.abs(ys@rxc/n)>=abs(ro)-1e-12).sum())
    p=(cnt+1)/(NP+1)
    rows.append(dict(pair=f'{r.response_x} vs {r.response_y}',n=n,rho=ro,p_stored=r.p_perm,p_2M=p,se=np.sqrt(p*(1-p)/NP),q_stored=r.p_fdr_bh))
A=pd.DataFrame(rows); A['q_2M']=bh(A.p_2M); A.to_csv(OUTD/'cross_exact.csv',index=False); print(A.round(5).to_string())
