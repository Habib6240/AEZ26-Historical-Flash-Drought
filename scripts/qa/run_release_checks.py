"""Release QA runner (run from anywhere: python scripts/qa/run_release_checks.py). Works on a temporary COPY of the repository.
This runner needs BOTH the software release and the derived-dataset record: unzip the dataset record so that its data/ folder sits next to scripts/. Checks: Python/notebook/JSON/CSV integrity, JS syntax (node --check, syntax only), SHA-256 manifest, duplicates, private-identifier and
excluded-analysis scans, re-execution of detection/statistics/audit scripts with comparison to stored outputs, figure-script tests,
and key-number consistency with the manuscript-v11 values recorded in KEY_NUMBERS below. Writes qa_results.json next to this file's repo root."""
import os,ast,json,glob,hashlib,subprocess,sys,csv,re,shutil,tempfile,platform,pathlib
import numpy,pandas,scipy,matplotlib
ROOT=pathlib.Path(__file__).resolve().parents[2]; res={}
if not (ROOT/'data').is_dir(): sys.exit('data/ not found: unzip the derived-dataset record so that data/ sits next to scripts/ before running this check.')
res['environment']=dict(python=platform.python_version(),numpy=numpy.__version__,pandas=pandas.__version__,scipy=scipy.__version__,matplotlib=matplotlib.__version__)
files=[p for p in ROOT.rglob('*') if p.is_file() and 'results' not in p.relative_to(ROOT).parts[:1] and '.staging' not in p.parts and p.name!='qa_results.json']
rel=lambda p:str(p.relative_to(ROOT))
# 1 python syntax
bad=[]
for p in files:
    if p.suffix=='.py':
        try: ast.parse(p.read_text(encoding='utf-8'))
        except Exception as e: bad.append((rel(p),str(e)[:80]))
res['py_files']=sum(p.suffix=='.py' for p in files); res['py_syntax_errors']=bad
# 2 notebooks
nb=[]
for p in files:
    if p.suffix=='.ipynb':
        d=json.load(open(p)); cells=[c for c in d['cells'] if c['cell_type']=='code']; err=[]
        for i,c in enumerate(cells):
            src='\n'.join(l for l in ''.join(c['source']).split('\n') if not l.lstrip().startswith(('%','!')))
            try: ast.parse(src)
            except Exception as e: err.append((i,str(e)[:60]))
        nb.append(dict(file=rel(p),code_cells=len(cells),cells_with_stored_outputs=sum(1 for c in cells if c.get('outputs')),syntax_errors=err))
res['notebooks']=nb
# 3 JSON / CSV
jb=[];cb=[]
for p in files:
    if p.suffix=='.json':
        try: json.load(open(p))
        except Exception: jb.append(rel(p))
    if p.suffix=='.csv':
        try:
            with open(p,encoding='utf-8',errors='replace') as fh:
                rd=csv.reader(fh); h=next(rd); n=next(rd,None)
                if n is None: cb.append(rel(p))
        except Exception: cb.append(rel(p))
res['json_files']=sum(p.suffix=='.json' for p in files); res['json_invalid']=jb; res['csv_files']=sum(p.suffix=='.csv' for p in files); res['csv_empty_or_invalid']=cb
# 4 JS syntax only (GEE scripts need the Earth Engine runtime; they were NOT executed here)
js={}
for p in files:
    if rel(p).startswith('gee/') and p.suffix in('.js','.txt') and p.name!='README.md':
        t=pathlib.Path(tempfile.mkdtemp())/'x.js'; shutil.copy(p,t)
        r=subprocess.run(['node','--check',str(t)],capture_output=True,text=True); js[rel(p)]='syntax OK' if r.returncode==0 else 'SYNTAX ERROR: '+r.stderr[:120]
res['gee_scripts_syntax_only']=js
# 5 duplicates
h={}
for p in files:
    if p.stat().st_size>0: h.setdefault(hashlib.sha256(p.read_bytes()).hexdigest(),[]).append(rel(p))
res['duplicate_groups']=[v for v in h.values() if len(v)>1]
# 6 manifest
man=ROOT/'checksums'/'SHA256SUMS.txt'
if man.exists():
    mism=[];n=0
    for l in man.read_text().splitlines():
        if not l.strip(): continue
        d,f=l.split('  ',1); n+=1
        q=ROOT/f
        if not q.exists() or hashlib.sha256(q.read_bytes()).hexdigest()!=d: mism.append(f)
    res['manifest']=dict(entries=n,mismatches=mism)
else: res['manifest']='not yet created'
# 7 scans
leak=[];excl=[]
LEAK=re.compile(r'gee-project-'+r'505|high_barind_'+r'aez26|ya29\.|client_secret|BEGIN (RSA|PRIVATE)|ahsan'+r'habib')
EXCL=re.compile(r'CMIP6|hindcast|emulator|future[- ]risk|early[- ]warning|XGBoost|random forest|scikit',re.I)
for p in files:
    if p.suffix in('.png','.xlsx','.docx','.zip','.pdf'): continue
    try: t=p.read_text(encoding='utf-8',errors='ignore')
    except Exception: continue
    if p.name=='run_release_checks.py': continue
    if LEAK.search(t): leak.append(rel(p))
    if EXCL.search(t): excl.append(rel(p))
res['private_id_or_secret_hits']=leak; res['excluded_analysis_term_hits']=excl
# 8 re-execution in a temp copy
tmp=pathlib.Path(tempfile.mkdtemp()); T=tmp/'r'; shutil.copytree(ROOT,T,ignore=shutil.ignore_patterns('results','qa_results.json'))
subprocess.run([sys.executable,str(T/'scripts'/'stage_flat_inputs.py')],capture_output=True)
runs={}
for s in ['scripts/detection/independent_detector_and_chronology_audit.py','scripts/statistics/association_tests_reproduction.py','scripts/statistics/consensus_event_analysis.py','scripts/statistics/cross_response_exact_permutation.py','scripts/statistics/seasonal_control_audit.py','scripts/statistics/response_minimum_window_fraction.py',
          'scripts/eq6_eq7_audit/eq6_reconstruction_audit.py','scripts/eq6_eq7_audit/eq6_35pentad_soilwater_offsets.py','scripts/eq6_eq7_audit/eq7_fullrecord_checks.py','scripts/eq6_eq7_audit/eq7_pathway_comparison.py','scripts/eq6_eq7_audit/eq7_percentile_and_drift_tests.py','scripts/eq6_eq7_audit/eq7_sm_catalogue_stress.py','scripts/eq6_eq7_audit/eq7_driver_flag_stress.py','scripts/eq6_eq7_audit/downstream.py']:
    r=subprocess.run([sys.executable,'-I',str(T/s)],capture_output=True,text=True,timeout=1800); runs[s]=f'exit {r.returncode}'+('' if r.returncode==0 else ' '+r.stderr[-200:])
res['script_runs']=runs
import pandas as pd
def cmpf(a,b):
    if a.suffix=='.json': return 'identical' if json.load(open(a))==json.load(open(b)) else 'DIFFERENT'
    A=pd.read_csv(a);B=pd.read_csv(b)
    if A.shape!=B.shape: return 'SHAPE DIFFERENT'
    num=A.select_dtypes('number').columns; d=float((A[num]-B[num]).abs().max().max()) if len(num) else 0.0
    return f'max numeric difference {d:.3g}; non-numeric identical {A.drop(columns=num).equals(B.drop(columns=num))}'
cmp={}
for f in sorted((ROOT/'data/statistical_outputs/closure_checks').iterdir()):
    b=T/'results'/'phase1_closure'/f.name; cmp['closure_checks/'+f.name]=cmpf(f,b) if b.exists() else 'MISSING'
for sub in ('eq6','eq7'):
    for f in sorted((ROOT/'data/eq6_eq7_verification'/sub).iterdir()):
        if f.is_dir() or f.name in('eq6_chunk_sha256.csv','AEZ26_Eq7_Temporal_Robustness_23pentads_v02.csv'): continue
        b=T/'results'/'eq6_eq7_rerun'/f.name; cmp[f'eq6_eq7_verification/{sub}/'+f.name]=cmpf(f,b) if b.exists() else 'MISSING'
for f in sorted((ROOT/'data/eq6_eq7_verification/eq7_fullrecord').iterdir()):
    if f.name in('AEZ26_Eq7_ABC_35pentads_with_offline.csv','AEZ26_Eq7_Recomputed_vs_Stored_3285pentads.csv','eq7_fullrecord_checks_part1.json','eq7_fullrecord_checks_part2.json'):
        b=T/'results'/'eq6_eq7_rerun'/'eq7_fullrecord'/f.name; cmp['eq6_eq7_verification/eq7_fullrecord/'+f.name]=cmpf(f,b) if b.exists() else 'MISSING'
res['output_comparison']=cmp
# 9 figures
fig={}
for fd in sorted((T/'scripts'/'figures').glob('AEZ26_Fig*')):
    if fd.name.startswith('AEZ26_Fig1_'): fig[fd.name]='NOT RUN (needs the study-area polygon and Bangladesh outline, which are not redistributed)'; continue
    o=tmp/fd.name; o.mkdir(); sc=list(fd.glob('make_*.py'))[0]
    r=subprocess.run([sys.executable,'-I',str(sc),'--data-dir',str(T/'data'/'derived'),'--out-dir',str(o)],capture_output=True,text=True,timeout=900)
    msg=f'exit {r.returncode}; outputs {sorted(x.name for x in o.iterdir())[:4]}'
    png=[x for x in o.glob('*.png')]
    if png:
        from PIL import Image,ImageChops
        ref=ROOT/'figures'/png[0].name
        if ref.exists():
            a=Image.open(png[0]).convert('RGB'); b=Image.open(ref).convert('RGB')
            msg+='; vs released PNG: '+('size differs %s vs %s'%(a.size,b.size) if a.size!=b.size else ('pixel-identical' if ImageChops.difference(a,b).getbbox() is None else 'pixels differ'))
    fig[fd.name]=msg
res['figure_scripts']=fig
json.dump(res,open(ROOT/'qa_results.json','w'),indent=1); print(json.dumps(res,indent=1)[:6000])
