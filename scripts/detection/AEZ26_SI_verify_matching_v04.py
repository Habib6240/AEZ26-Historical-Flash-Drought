#!/usr/bin/env python3
"""Standalone check of the onset-matching algorithm (Supplementary Text S1.3).

Question answered: do the greedy one-to-one counts used in the manuscript equal the size of a
maximum one-to-one matching? The script compares the two for
  * the observed GLDAS (39 events) vs ERA5-Land OVERLAP26 (44 events) onsets at +-0, +-1, +-2 pentads,
  * the observed GLDAS vs ERA5-Land LONG45 onsets restricted to 2000-2025 (43 events) at the same tolerances,
  * the 25 whole-year shifts of the OVERLAP26 onsets (k x 73 pentads, k = 1..25, modulus 1,898) at the same
    tolerances (75 comparisons).
Inputs (released dataset, Zenodo record of the derived data; read-only):
  AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv
  AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv   (OVERLAP26; "SOURCE26" in file names)
  AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv
Three implementations are compared: (1) greedy matching in increasing absolute onset difference, ties by
event order (the algorithm of the manuscript); (2) maximum bipartite matching by augmenting paths;
(3) scipy.sparse.csgraph.maximum_bipartite_matching when SciPy is installed (independent check).
Usage:  python3 AEZ26_SI_verify_matching_v04.py --dataset-root <folder containing the dataset 'data' directory> [--out <dir>]
In the software release (scripts/detection/) the dataset record is unzipped so that data/ sits next to scripts/;
then --dataset-root may be omitted.  A matching_verification_output/ folder is written to the current directory.
Exit status 0 only if every comparison agrees and every documented value is reproduced.
"""
import argparse, csv, hashlib, json, pathlib, sys

NAMES = {
    "gldas": "AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv",
    "overlap26": "AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv",
    "long45": "AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv",
}
BASE_YEAR, NPENT, NYEARS = 2000, 73, 26
N = NPENT * NYEARS            # 1,898 pentads in 2000-2025
TOLS = (0, 1, 2)
# values stated in Supplementary Text S1.3 and the manuscript (Section 3.3, 4.2)
DOC_OBS = {"overlap26": {0: 7, 1: 11, 2: 15}, "long45": {0: 6, 1: 13, 2: 16}}
DOC_NULL_MEAN = {0: 1.16, 1: 4.28, 2: 6.96}
DOC_NULL_RANGE = {0: (0, 4), 1: (2, 7), 2: (3, 11)}


def find(root, name):
    # The dataset keeps each file in a topic folder; scripts/stage_flat_inputs.py of the software release
    # adds byte-identical copies in data/derived/. Identical copies are accepted; differing copies are an error.
    hits = sorted(p for p in pathlib.Path(root).rglob(name) if "historical_inputs" not in p.parts)
    if not hits:
        sys.exit(f"{name} not found under {root}")
    if len({hashlib.sha256(p.read_bytes()).hexdigest() for p in hits}) != 1:
        sys.exit(f"{len(hits)} different files named {name} under {root}")
    return hits[0]


def index_of(label):            # '2000_P55' -> 0-based pentad index within 2000-2025
    y, p = label.split("_P")
    return (int(y) - BASE_YEAR) * NPENT + int(p) - 1


def read_onsets(path, restrict_2000_2025=False):
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8")))
    out = []
    for r in rows:
        y = int(r["onset_pentad"].split("_P")[0])
        if restrict_2000_2025 and not (BASE_YEAR <= y <= BASE_YEAR + NYEARS - 1):
            continue
        out.append(r["onset_pentad"])
    return out


def greedy(a, b, tol):
    cand = sorted((abs(x - y), i, j) for i, x in enumerate(a) for j, y in enumerate(b) if abs(x - y) <= tol)
    ua, ub, n = set(), set(), 0
    for _, i, j in cand:
        if i not in ua and j not in ub:
            ua.add(i); ub.add(j); n += 1
    return n


def augmenting(a, b, tol):
    adj = [[j for j, y in enumerate(b) if abs(x - y) <= tol] for x in a]
    match_b = {}

    def try_(u, seen):
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                if v not in match_b or try_(match_b[v], seen):
                    match_b[v] = u
                    return True
        return False
    return sum(try_(u, set()) for u in range(len(a)))


def scipy_max(a, b, tol):
    try:
        import numpy as np
        from scipy.sparse import csr_matrix
        from scipy.sparse.csgraph import maximum_bipartite_matching
    except ImportError:
        return None
    m = np.array([[1 if abs(x - y) <= tol else 0 for y in b] for x in a])
    return int((maximum_bipartite_matching(csr_matrix(m), perm_type="column") >= 0).sum())


def main():
    ap = argparse.ArgumentParser()
    default_root = pathlib.Path(__file__).resolve().parents[2]      # software release: data/ sits next to scripts/
    ap.add_argument("--dataset-root", default=str(default_root) if (default_root / "data").is_dir() else None,
                    help="folder containing the dataset record (its data/ directory); default: the software-release root if data/ is there")
    ap.add_argument("--out", default="matching_verification_output")
    args = ap.parse_args()
    if not args.dataset_root:
        ap.error("--dataset-root is required (folder containing the dataset record's data/ directory)")
    files = {k: find(args.dataset_root, v) for k, v in NAMES.items()}
    sha = {k: hashlib.sha256(p.read_bytes()).hexdigest() for k, p in files.items()}
    g = [index_of(s) for s in read_onsets(files["gldas"])]
    o = [index_of(s) for s in read_onsets(files["overlap26"])]
    l = [index_of(s) for s in read_onsets(files["long45"], restrict_2000_2025=True)]
    assert (len(g), len(o), len(l)) == (39, 44, 43), (len(g), len(o), len(l))
    rows, bad = [], []

    def compare(tag, a, b, tol, extra=""):
        gr, au, sp = greedy(a, b, tol), augmenting(a, b, tol), scipy_max(a, b, tol)
        ok = gr == au and (sp is None or sp == au)
        rows.append(dict(comparison=tag, tolerance=tol, greedy=gr, maximum_augmenting=au,
                         maximum_scipy="" if sp is None else sp, identical=ok, note=extra))
        if not ok:
            bad.append((tag, tol, gr, au, sp))
        return gr

    obs = {"overlap26": {}, "long45": {}}
    for t in TOLS:
        obs["overlap26"][t] = compare("observed OVERLAP26", g, o, t)
        obs["long45"][t] = compare("observed LONG45 (2000-2025)", g, l, t)
    null = {t: [] for t in TOLS}
    for k in range(1, 26):
        shifted = sorted((x + k * NPENT) % N for x in o)
        for t in TOLS:
            null[t].append(compare(f"OVERLAP26 shifted by {k} year(s)", g, shifted, t))
    problems = []
    for key in obs:
        for t in TOLS:
            if obs[key][t] != DOC_OBS[key][t]:
                problems.append(f"observed {key} tol {t}: {obs[key][t]} != documented {DOC_OBS[key][t]}")
    summary = {"inputs_sha256": sha, "n_events": {"gldas": len(g), "overlap26": len(o), "long45_2000_2025": len(l)},
               "observed": obs, "shifts": {}, "comparisons_run": len(rows),
               "year_shift_comparisons": sum(1 for r in rows if "shifted" in r["comparison"]),
               "scipy_check_available": scipy_max([0], [0], 0) is not None}
    for t in TOLS:
        v = null[t]
        mean, rng = round(sum(v) / len(v), 2), (min(v), max(v))
        p = (1 + sum(1 for x in v if x >= obs["overlap26"][t])) / 26
        summary["shifts"][t] = {"mean": mean, "range": rng, "p_min_possible_1_over_26": round(1 / 26, 4), "p": round(p, 4)}
        if mean != DOC_NULL_MEAN[t]:
            problems.append(f"null mean tol {t}: {mean} != documented {DOC_NULL_MEAN[t]}")
        if rng != DOC_NULL_RANGE[t]:
            problems.append(f"null range tol {t}: {rng} != documented {DOC_NULL_RANGE[t]}")
    if summary["year_shift_comparisons"] != 75:
        problems.append("expected 75 year-shift comparisons")
    if bad:
        problems.append(f"greedy and maximum matching differ in {len(bad)} comparison(s): {bad[:3]}")
    out = pathlib.Path(args.out); out.mkdir(parents=True, exist_ok=True)
    with open(out / "matching_comparisons.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    summary["problems"] = problems
    (out / "matching_summary.json").write_text(json.dumps(summary, indent=1), encoding="utf-8")
    print(json.dumps(summary, indent=1))
    print("RESULT:", "ALL COMPARISONS IDENTICAL AND DOCUMENTED VALUES REPRODUCED" if not problems else "PROBLEMS FOUND")
    sys.exit(0 if not problems else 1)


if __name__ == "__main__":
    main()
