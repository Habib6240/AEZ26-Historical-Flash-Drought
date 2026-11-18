"""Create the flat input view data/derived/ that the statistics, detection, figure and audit scripts expect.
The released data are organised by topic; the scripts (kept as originally written) read data/derived/<file>.
Usage: python scripts/stage_flat_inputs.py   (copies files; safe to re-run)."""
import pathlib, shutil
ROOT=pathlib.Path(__file__).resolve().parents[1]
D=ROOT/'data'/'derived'; D.mkdir(exist_ok=True)
n=0
for k in ('event_catalogue','pentad_indicators','chronology_comparison','environmental_drivers','land_water_responses','statistical_outputs'):
    for f in (ROOT/'data'/k).glob('*'):
        if f.is_file(): shutil.copy2(f,D/f.name); n+=1
print(f'staged {n} files into {D}')
