"""Eq. (7) full-record checks (S1-S7): stored series vs the offline per-pixel recomputation, pathway comparison for 35 pentads, step/drift and trend tests.
Written 2026-11-15/16 for the Eq. 6/7 closure; NOT part of the original analysis code. Inputs: zone-level files released in data/eq6_eq7_verification/eq7_fullrecord/ (the per-pixel exports themselves are withheld). Outputs: results/eq6_eq7_rerun/eq7_fullrecord/.
Paths: ROOT is the folder holding scripts/ and data/ (software release and dataset record unzipped side by side)."""
import pathlib, os
HERE=pathlib.Path(__file__).resolve().parent; ROOT=HERE.parents[1]
V=ROOT/'data'/'eq6_eq7_verification'; FR=V/'eq7_fullrecord'
OUT=ROOT/'results'/'eq6_eq7_rerun'/'eq7_fullrecord'; OUT.mkdir(parents=True,exist_ok=True); os.chdir(OUT)
STORED=ROOT/'data'/'pentad_indicators'/'AEZ26_Robustness_ERA5Land_Pentad_Indicators_1981_2025.csv'

# ===== part 1 (S1-S3) =====
import pandas as pd, numpy as np, json
st=pd.read_csv(STORED)
st=st[['year','pentad_of_year','n_days','t2m_mean_C','t2m_max_C','relative_humidity_mean_pct','VPD_mean_kPa','VPD_dailymean_max_kPa','ERA5_SM_0_100_mean_mm']]
rc=pd.read_csv(FR/'AEZ26_Eq7_Recomputed_3285pentads.csv',parse_dates=['start','end'])
m=rc.merge(st,on=['year','pentad_of_year'],suffixes=('','_st')); assert len(m)==3285 and (m.n_days==m.n_days_st).all()
R={}
def stats(x,y):
    d=x-y; return dict(n=len(d),bias=d.mean(),MAE=d.abs().mean(),RMSE=float(np.sqrt((d**2).mean())),maxabs=d.abs().max(),r=float(np.corrcoef(x,y)[0,1]))
pairs={'T':('t2m_mean_C','S_T','N_T'),'RH':('relative_humidity_mean_pct','S_RH','N_RH'),'VPD':('VPD_mean_kPa','S_VPD','N_VPD'),'VPDmax':('VPD_dailymean_max_kPa','S_VPDmax','N_VPDmax'),'Tmax':('t2m_max_C','S_Tmax','N_Tmax')}
S1={}
for k,(sc,sw,nw) in pairs.items():
    for lab,col in [('sampleW',sw),('nativeW',nw)]:
        S1[f'{k}|{lab}|all']=stats(m[sc],m[col])
        S1[f'{k}|{lab}|1981-99']=stats(m[sc][m.year<2000],m[col][m.year<2000])
        S1[f'{k}|{lab}|2000-25']=stats(m[sc][m.year>=2000],m[col][m.year>=2000])
R['S1']=S1
pd.set_option('display.width',250)
print(pd.DataFrame(S1).T.round(5).to_string())
# stored Tmax definition check: which matches?
print('Tmax stored vs max of zone-mean-of-pixel-max:',(m.t2m_max_C-m.S_Tmax).abs().max())
m['month']=m.start.dt.month
# --- DIAG validation
D=pd.read_csv(FR/'AEZ26_Eq7FR_ABC_12pentads.csv'); P23=pd.read_csv(V/'eq7'/'AEZ26_Eq7_Temporal_Robustness_23pentads_v02.csv')
exp=[(1982,33),(1985,40),(1991,64),(1997,70),(2001,46),(2004,36),(2007,65),(2009,71),(2015,41),(2018,47),(2020,66),(2025,34)]
print('DIAG pentads as expected:',list(zip(D.year,D.pentad_of_year))==exp,'overlap with 23:',len(set(zip(D.year,D.pentad_of_year))&set(zip(P23.year,P23.pentad_of_year))))
num=D.select_dtypes('number'); print('cols',D.shape[1],'nulls',int(D.isna().sum().sum()),'dups',int(D.duplicated(['year','pentad_of_year']).sum()))
print('n_days/images',D.n_days.unique(),(D.n_days==D.era5_images).all(),'n_count',D[['A_n_count','B_n_count','C_n_count']].drop_duplicates().values.tolist(),'n_sum A,B,C',D.A_n_sum.unique(),D.B_n_sum.unique(),D.C_n_sum.unique())
# ranges
for v in ['t2m_C','td_C','RH_pct','VPD_mean_kPa','VPD_max_kPa','SM_0_100_mm']:
    print(v,{p:(round(D[f'{p}_{v}'].min(),3),round(D[f'{p}_{v}'].max(),3)) for p in 'ABC'})
print('Td<=T',all((D[f'{p}_td_C']<=D[f'{p}_t2m_C']).all() for p in 'ABC'),'VPDmax>=mean',all((D[f'{p}_VPD_max_kPa']>=D[f'{p}_VPD_mean_kPa']).all() for p in 'ABC'),'RH in 0..100',all(D[f'{p}_RH_pct'].between(0,100).all() for p in 'ABC'))
# B vs C
vars_=['t2m_C','td_C','RH_pct','VPD_mean_kPa','VPD_max_kPa','SM_0_100_mm']
print('max |B-C| by var:',{v:float((D['B_'+v]-D['C_'+v]).abs().max()) for v in vars_})
# combined 35
for X in (D,P23): X['key']=list(zip(X.year,X.pentad_of_year))
C=pd.concat([P23.assign(set='23'),D.assign(set='12')],ignore_index=True); print('35 unique',C.key.nunique())
C=C.merge(m[['year','pentad_of_year','t2m_mean_C','relative_humidity_mean_pct','VPD_mean_kPa','VPD_dailymean_max_kPa','ERA5_SM_0_100_mean_mm','S_T','S_Td','S_RH','S_VPD','S_VPDmax','N_T','N_Td','N_RH','N_VPD','N_VPDmax','start']],on=['year','pentad_of_year'])
mp={'t2m_C':('t2m_mean_C','T'),'RH_pct':('relative_humidity_mean_pct','RH'),'VPD_mean_kPa':('VPD_mean_kPa','VPD'),'VPD_max_kPa':('VPD_dailymean_max_kPa','VPDmax'),'SM_0_100_mm':('ERA5_SM_0_100_mean_mm',None)}
# S3: EE A vs stored
S3={}
for sub,lab in [(C[C.set=='12'],'12 new'),(C[C.set=='23'],'23 earlier'),(C,'35')]:
    for v,(sc,_) in mp.items():
        d=sub['A_'+v]-sub[sc]; S3[f'{lab}|{v}']=dict(n=len(d),maxabs=d.abs().max(),MAE=d.abs().mean(),bias=d.mean())
print('S3 (EE A minus stored):'); print(pd.DataFrame(S3).T.to_string())
R['S3']=S3
# S2: offline vs EE B
S2={}
for lab,pre in [('sampleW','S_'),('nativeW','N_')]:
    for sub,sl in [(C[C.set=='12'],'12'),(C[C.set=='23'],'23'),(C,'35')]:
        for v,(sc,off) in mp.items():
            if off is None: continue
            d=sub[pre+off]-sub['B_'+mp[v][1] if False else 'B_'+v]; S2[f'{lab}|{sl}|{v}']=dict(n=len(d),bias=d.mean(),MAE=d.abs().mean(),maxabs=d.abs().max())
        d=sub[pre+'Td']-sub['B_td_C']; S2[f'{lab}|{sl}|td_C']=dict(n=len(d),bias=d.mean(),MAE=d.abs().mean(),maxabs=d.abs().max())
print('S2 (offline minus EE B):'); print(pd.DataFrame(S2).T.round(5).to_string()); R['S2']=S2
# offsets B-A (EE) per variable, by set/season/period
rows=[]
for v in vars_:
    d=C['B_'+v]-C['A_'+v]; rows.append((v,len(d),d.mean(),d.std(),d.abs().max(),d.min(),d.max()))
print('EE B-A offsets (35 pentads): var n mean sd maxabs min max'); [print(r) for r in rows]
C['month']=C.start.dt.month; C['period']=np.where(C.year<2000,'1981-99','2000-25')
for v in ['t2m_C','td_C','RH_pct','VPD_mean_kPa','VPD_max_kPa','SM_0_100_mm']:
    C['dBA_'+v]=C['B_'+v]-C['A_'+v]
print(C.groupby('period')[[f'dBA_{v}' for v in vars_]].agg(['mean','std','count']).round(4).T.to_string())
C['season']=C.month.map(lambda x:'DJF' if x in(12,1,2) else 'MAM' if x in(3,4,5) else 'JJAS' if x in(6,7,8,9) else 'ON')
print(C.groupby('season')[[f'dBA_{v}' for v in vars_]].agg(['mean','count']).round(4).T.to_string())
# B-A vs stored-vs-offline (A-offline) at 35 pentads: does stored - offline = -(B-A)?
d1=C['t2m_mean_C']-C['S_T']; d2=C['A_t2m_C']-C['B_t2m_C']; print('stored-offline(T) vs A-B(T) corr',np.corrcoef(d1,d2)[0,1],'mean',d1.mean(),d2.mean())
d1=C['VPD_mean_kPa']-C['S_VPD']; d2=C['A_VPD_mean_kPa']-C['B_VPD_mean_kPa']; print('same for VPD corr',np.corrcoef(d1,d2)[0,1],'mean',d1.mean(),d2.mean())
C.to_csv('AEZ26_Eq7_ABC_35pentads_with_offline.csv',index=False)
json.dump(R,open('eq7_fullrecord_checks_part1.json','w'),indent=1,default=float)
m.to_csv('AEZ26_Eq7_Recomputed_vs_Stored_3285pentads.csv',index=False)

# ===== part 2 (S4-S7) =====
import pandas as pd, numpy as np, json
from scipy import stats
m=pd.read_csv('AEZ26_Eq7_Recomputed_vs_Stored_3285pentads.csv',parse_dates=['start','end'])
C=pd.read_csv('AEZ26_Eq7_ABC_35pentads_with_offline.csv'); print('35-pentad years:',sorted(C.year.unique().tolist()),'| in 2000:',int((C.year==2000).sum()))
def wann(df,col): return df.groupby('year').apply(lambda g:(g[col]*g.n_days).sum()/g.n_days.sum(),include_groups=False)
V={'T':('t2m_mean_C','S_T','N_T'),'RH':('relative_humidity_mean_pct','S_RH','N_RH'),'VPD':('VPD_mean_kPa','S_VPD','N_VPD')}
ann={}
for k,(sc,s,n) in V.items():
    ann[k]=pd.DataFrame({'stored':wann(m,sc),'sample':wann(m,s),'native':wann(m,n)})
    ann[k].to_csv(f'annual_{k}_offsets.csv')
def ts(y,x):
    r=stats.theilslopes(y,x,alpha=0.95); kt=stats.kendalltau(x,y); return dict(slope10=r[0]*10,lo10=r[2]*10,hi10=r[3]*10,tau=kt.statistic,p=kt.pvalue)
def bh(ps):
    ps=np.array(ps); o=np.argsort(ps); m_=len(ps); q=np.empty(m_); prev=1
    for rank,i in list(enumerate(o,1))[::-1]:
        prev=min(prev,ps[i]*m_/rank); q[i]=prev
    return q
# ---------- offsets (stored - offline), annual
OFF={}
for k in V:
    for w in ['sample','native']:
        OFF[(k,w)]=ann[k]['stored']-ann[k][w]
yrs=np.arange(1981,2026)
R={'offset':{},'drift':{},'shift':{},'S4':{}}
pre=lambda s:s[s.index<2000]; post=lambda s:s[s.index>=2000]
print('\n== Annual offset (stored - offline), mean / SD / min / max by period; Welch, MWU; segmented level shift at 2000')
for (k,w),s in OFF.items():
    a,b=pre(s),post(s); wt=stats.ttest_ind(a,b,equal_var=False); mw=stats.mannwhitneyu(a,b)
    # segmented regression with level shift + slope change
    t=(s.index.values-2000.0); D=(s.index.values>=2000).astype(float)
    X=np.column_stack([np.ones_like(t),t,D,D*t]); beta,res,_,_=np.linalg.lstsq(X,s.values,rcond=None)
    resid=s.values-X@beta; dof=len(s)-4; sig2=resid@resid/dof; cov=sig2*np.linalg.inv(X.T@X); se=np.sqrt(np.diag(cov)); tc=stats.t.ppf(.975,dof)
    # level shift without slope-change term (common slope)
    X2=X[:,:3]; b2=np.linalg.lstsq(X2,s.values,rcond=None)[0]; r2=s.values-X2@b2; cov2=(r2@r2/(len(s)-3))*np.linalg.inv(X2.T@X2); se2=np.sqrt(np.diag(cov2)); tc2=stats.t.ppf(.975,len(s)-3)
    d_all=ts(s.values,s.index.values); d_pre=ts(a.values,a.index.values); d_post=ts(b.values,b.index.values)
    R['offset'][f'{k}|{w}']=dict(pre_mean=a.mean(),pre_sd=a.std(),pre_min=a.min(),pre_max=a.max(),post_mean=b.mean(),post_sd=b.std(),post_min=b.min(),post_max=b.max(),diff=a.mean()-b.mean(),welch_p=wt.pvalue,mwu_p=mw.pvalue,
       seg_shift=beta[2],seg_shift_lo=beta[2]-tc*se[2],seg_shift_hi=beta[2]+tc*se[2],shift_common_slope=b2[2],sc_lo=b2[2]-tc2*se2[2],sc_hi=b2[2]+tc2*se2[2])
    R['drift'][f'{k}|{w}']=dict(all=d_all,pre=d_pre,post=d_post)
rows=[]
for key,v in R['offset'].items():
    rows.append([key,v['pre_mean'],v['pre_sd'],v['pre_min'],v['pre_max'],v['post_mean'],v['post_sd'],v['post_min'],v['post_max'],v['diff'],v['welch_p'],v['mwu_p'],v['shift_common_slope'],v['sc_lo'],v['sc_hi'],v['seg_shift'],v['seg_shift_lo'],v['seg_shift_hi']])
O=pd.DataFrame(rows,columns=['var|w','pre_mean','pre_sd','pre_min','pre_max','post_mean','post_sd','post_min','post_max','pre-post','welch_p','mwu_p','shift_cs','lo','hi','shift_seg','lo_seg','hi_seg']).set_index('var|w')
pd.set_option('display.width',300); print(O.round(5).T.to_string())
print('\n== Drift in offset (Theil-Sen per decade, 95% CI, Kendall p)')
for key,v in R['drift'].items():
    for per in ['all','pre','post']:
        d=v[per]; print(f"{key:14s} {per:4s} slope {d['slope10']:+.5f} CI [{d['lo10']:+.5f}, {d['hi10']:+.5f}] p={d['p']:.4f}")
# S4: against plan thresholds
print('\n== S4: pre-2000 annual offsets vs plan ranges (stored - native/offline)')
for k,rng,sd3 in [('T',(-0.055,-0.029),0.026),('VPD',(-0.0101,-0.0003),0.0075)]:
    for w in ['sample','native']:
        s=pre(OFF[(k,w)]); lo,hi=rng
        out=((s<lo-sd3)|(s>hi+sd3)).sum(); outside=((s<lo)|(s>hi)).sum()
        print(k,w,'pre-2000 min/max %.4f / %.4f'%(s.min(),s.max()),'| outside plan range:',int(outside),'of',len(s),'| beyond range+-3SD:',int(out),'| post-2000 min/max %.4f / %.4f'%(post(OFF[(k,w)]).min(),post(OFF[(k,w)]).max()))
# ---------- trends
other={'FD_count':0.7345552259086775,'CHIRPS_precip':0.2251268955817738,'ERA5_PE':0.020964262608188372}
print('\n== Trends (annual means weighted by n_days), Theil-Sen per decade')
TR={}
for k in V:
    for src in ['stored','sample','native']:
        TR[(k,src)]=ts(ann[k][src].values,ann[k].index.values)
tt=pd.DataFrame(TR).T; print(tt.round(5).to_string())
# BH families: five-test (Table 3), with T and VPD p replaced by src
print('\n== BH q, five-test family (Table 3 design), T and VPD from each source')
Q={}
for src in ['stored','sample','native']:
    ps=[other['FD_count'],TR[('T',src)]['p'],TR[('VPD',src)]['p'],other['CHIRPS_precip'],other['ERA5_PE']]; q=bh(ps)
    Q[src]=dict(qT=q[1],qVPD=q[2],qFD=q[0],qCH=q[3],qPE=q[4]); print(src,{k_:round(v_,4) for k_,v_ in Q[src].items()},'p T %.4f VPD %.4f'%(TR[('T',src)]['p'],TR[('VPD',src)]['p']))
print('six-test family adding RH (exploratory):')
for src in ['stored','sample','native']:
    ps=[other['FD_count'],TR[('T',src)]['p'],TR[('VPD',src)]['p'],other['CHIRPS_precip'],other['ERA5_PE'],TR[('RH',src)]['p']]; q=bh(ps); print(src,'qT %.4f qVPD %.4f qRH %.5f'%(q[1],q[2],q[5]))
# table3 reproduction check
t3={'T':(0.08893527221692354,0.0014727187188897282,0.1821233795539458,0.0438881101996406),'VPD':(-0.02471503990662468,-0.048718294192238686,0.0005208628449708819,0.05275765250271968)}
for k in ['T','VPD']:
    d=TR[(k,'stored')]; print('Table3 reproduction',k,'max abs diff',max(abs(d['slope10']-t3[k][0]),abs(d['lo10']-t3[k][1]),abs(d['hi10']-t3[k][2]),abs(d['p']-t3[k][3])))
# trend-difference (offline - stored) via annual diff trend already = drift. Also: difference in trend estimate
for k in ['T','VPD','RH']:
    print(k,'trend(offline sample) - trend(stored) per decade: %+.5f ; native: %+.5f'%(TR[(k,'sample')]['slope10']-TR[(k,'stored')]['slope10'],TR[(k,'native')]['slope10']-TR[(k,'stored')]['slope10']))
# drift thresholds needed to flip: from earlier sensitivity: VPD 0.006-0.008 kPa/dec, T 0.03 C/dec
json.dump({'offset':R['offset'],'drift':R['drift'],'TR':{f'{a}|{b}':v for (a,b),v in TR.items()},'Q':Q},open('eq7_fullrecord_checks_part2.json','w'),indent=1,default=float)
# monthly/seasonal offset (pentad level)
m['month']=m.start.dt.month
for k,(sc,s,n) in V.items(): m['off_'+k]=m[sc]-m[n]
print('\n== Seasonal offset (stored - native-weights offline), by month, mean')
print(m.groupby('month')[['off_T','off_RH','off_VPD']].mean().round(4).T.to_string())
print('by month std'); print(m.groupby('month')[['off_T','off_RH','off_VPD']].std().round(4).T.to_string())
m['season']=m.month.map(lambda x:'DJF' if x in(12,1,2) else 'MAM' if x in(3,4,5) else 'JJAS' if x in(6,7,8,9) else 'ON')
print(m.groupby(['season'])[['off_T','off_RH','off_VPD']].mean().round(4).to_string())
# is seasonal pattern same pre and post?
pp=m.assign(per=np.where(m.year<2000,'pre','post')).groupby(['month','per'])[['off_T','off_VPD']].mean().unstack().round(4); print(pp.to_string())
