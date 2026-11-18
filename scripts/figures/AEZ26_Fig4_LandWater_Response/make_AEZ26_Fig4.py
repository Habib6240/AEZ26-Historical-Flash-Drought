#!/usr/bin/env python3
"""
make_AEZ26_Fig4.py
FIGURE 4 - Land-water responses and multiplicity-aware event-level inference (AEZ-26, High Barind Tract).

(a) response depth (z_base - z_min) per event, (b) onset-to-minimum lag per event,
(c) BH/FDR q-values for every source-backed association test (46 tests, 5 families),
(d) seasonal-normal recovery observed vs not observed within the finite window (right-censored).

Descriptive, event-level analysis. No causal cascade is inferred; GRACE TWSA is not groundwater;
JRC surface-water extent is not storage; right-censored != permanent non-recovery.
All plotted values are read from the Phase 2F / 2G CSVs.

Usage: python make_AEZ26_Fig4.py [--data-dir DIR] [--out-dir DIR]
"""
import argparse, io, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default=None)
ap.add_argument("--out-dir", default=None)
ap.add_argument("--stem", default="AEZ26_Fig4_LandWater_Response")
args = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__))
F2F = {"MOD16": "AEZ26_Phase2F_MOD16_Event_Response_Metrics.csv", "MOD13": "AEZ26_Phase2F_MOD13_Event_Response_Metrics.csv",
       "GRACE": "AEZ26_Phase2F_GRACE_TWSA_Event_Response_Metrics.csv",
       "JRC": "AEZ26_Phase2F_JRC_SurfaceWater_Event_Response_Metrics.csv"}
F2F_SYN, F2F_QC = "AEZ26_Phase2F_Cross_Response_Event_Synthesis.csv", "AEZ26_Phase2F_QC.csv"
F2G = {"primary": "AEZ26_Phase2G_Primary_Driver_Response_Associations.csv",
       "secondary": "AEZ26_Phase2G_Secondary_Atmospheric_Response_Associations.csv",
       "physics": "AEZ26_Phase2G_EventPhysics_Response_Associations.csv",
       "class": "AEZ26_Phase2G_DriverClass_Response_Comparisons.csv",
       "cross": "AEZ26_Phase2G_Cross_Response_Coupling.csv"}
F2G_COH, F2G_QC = "AEZ26_Phase2G_Response_Cohort_Summary.csv", "AEZ26_Phase2G_QC.csv"
ALL = list(F2F.values()) + list(F2G.values()) + [F2F_SYN, F2F_QC, F2G_COH, F2G_QC]
DATA = next((c for c in (args.data_dir, HERE, os.getcwd())
             if c and all(os.path.exists(os.path.join(c, f)) for f in ALL)), None)
if DATA is None:
    sys.exit("BLOCKING SOURCE PROBLEM: required CSVs not found")
OUT = args.out_dir or HERE
os.makedirs(OUT, exist_ok=True)
rd = lambda f: pd.read_csv(os.path.join(DATA, f))

PRODUCTS = ["MOD16", "MOD13", "JRC", "GRACE"]                       # fixed display order
PNAME = {"MOD16": "MOD16\nET/PET", "MOD13": "MOD13\nNDVI", "JRC": "JRC surface-\nwater extent", "GRACE": "GRACE\nTWSA"}
PCOL = {"MOD16": "#D55E00", "MOD13": "#009E73", "JRC": "#0072B2", "GRACE": "#CC79A7"}
PMARK = {"MOD16": "o", "MOD13": "s", "JRC": "^", "GRACE": "D"}

# ------------------------------------------------------------------ Phase 2F: event-response tables
R = {p: rd(F2F[p]) for p in PRODUCTS}
syn = rd(F2F_SYN)
COL = {  # product -> (drop-from-prebaseline col, lag col, censored flag, SN recovery days, PB recovery days, SN before end, availability)
    "MOD16": ("minimum_ETPET_drop_from_prebaseline_z", "lag_onset_to_minimum_ETPET_days",
              "MOD16_seasonal_normal_recovery_censored_flag", "MOD16_relative_days_from_event_end_to_seasonal_normal_recovery",
              "MOD16_relative_days_from_event_end_to_prebaseline_recovery",
              "MOD16_seasonal_normal_recovery_before_event_end_flag", None),
    "MOD13": ("minimum_NDVI_drop_from_prebaseline_z", "lag_onset_to_minimum_NDVI_days",
              "MOD13_seasonal_normal_recovery_censored_flag", "MOD13_relative_days_from_event_end_to_seasonal_normal_recovery",
              "MOD13_relative_days_from_event_end_to_prebaseline_recovery",
              "MOD13_seasonal_normal_recovery_before_event_end_flag", None),
    "GRACE": ("minimum_TWSA_drop_from_prebaseline_z", "lag_onset_to_minimum_TWSA_days",
              "GRACE_seasonal_normal_recovery_censored_flag", "GRACE_relative_days_from_event_end_to_seasonal_normal_recovery",
              "GRACE_relative_days_from_event_end_to_prebaseline_recovery",
              "GRACE_seasonal_normal_recovery_before_event_end_flag", "GRACE_response_metric_available_flag"),
    "JRC": ("minimum_water_fraction_drop_from_prebaseline_z", "lag_onset_to_minimum_water_fraction_days",
            "JRC_seasonal_normal_recovery_censored_flag", "JRC_relative_days_from_event_end_to_seasonal_normal_recovery",
            "JRC_relative_days_from_event_end_to_prebaseline_recovery",
            "JRC_seasonal_normal_recovery_before_event_end_flag", "JRC_response_metric_available_flag")}
EV = set(syn["event_id"])
assert len(syn) == 39 and syn["event_id"].is_unique
for p in PRODUCTS:
    r = R[p]
    assert len(r) == 39 and r["event_id"].is_unique and set(r["event_id"]) == EV, f"{p}: event keys inconsistent"
qc2f = rd(F2F_QC); qc2g = rd(F2G_QC)
assert (qc2f["status"].isin(["PASS", "RESULT"])).all() and (qc2g["status"].isin(["PASS", "RESULT"])).all()

depth, lag, rec = {}, {}, {}
for p in PRODUCTS:
    r = R[p]; dcol, lcol, ccol, sncol, pbcol, bcol, acol = COL[p]
    valid = r if acol is None else r[r[acol] == 1]
    # response depth = z_base - z_min = -(source "drop_from_prebaseline" column, which stores z_min - z_base); NOT clipped
    depth[p] = (-valid[dcol]).dropna().reset_index(drop=True)
    lag[p] = valid[lcol].dropna().reset_index(drop=True)
    cen = valid[ccol].dropna()
    rec[p] = dict(obs=int((cen == 0).sum()), cens=int((cen == 1).sum()), n=len(cen),
                  pb_obs=int(valid[pbcol].notna().sum()), pb_not=int(valid[pbcol].isna().sum()),
                  before_end=int(valid[bcol].sum()))
    # consistency: seasonal-normal recovery date/time present iff not censored
    assert int(valid[sncol].notna().sum()) == rec[p]["obs"], f"{p}: recovery-time presence != uncensored count"

# ------------------------------------------------------------------ locked QA (targets only)
assert {p: len(depth[p]) for p in PRODUCTS} == {"MOD16": 39, "MOD13": 39, "JRC": 31, "GRACE": 34}
assert {p: len(lag[p]) for p in PRODUCTS} == {"MOD16": 39, "MOD13": 39, "JRC": 32, "GRACE": 35}
for p, v in {"MOD16": 1.486, "MOD13": 1.014, "GRACE": 0.808, "JRC": 0.863}.items():
    assert round(float(depth[p].median()), 3) == v, f"depth median {p}"
for p, v in {"MOD16": 37, "MOD13": 45, "JRC": 107, "GRACE": 193}.items():
    assert float(lag[p].median()) == v, f"lag median {p}"
assert {p: (rec[p]["obs"], rec[p]["cens"]) for p in PRODUCTS} == {"MOD16": (28, 11), "MOD13": (28, 11), "JRC": (16, 16), "GRACE": (15, 20)}
assert {p: rec[p]["n"] for p in PRODUCTS} == {"MOD16": 39, "MOD13": 39, "JRC": 32, "GRACE": 35}
assert {p: (rec[p]["pb_obs"], rec[p]["pb_not"]) for p in PRODUCTS} == {"MOD16": (28, 11), "MOD13": (29, 10), "GRACE": (23, 12), "JRC": (14, 18)}
assert {p: rec[p]["before_end"] for p in PRODUCTS} == {"MOD16": 7, "MOD13": 4, "GRACE": 1, "JRC": 1}
neg = {p: int((depth[p] < 0).sum()) for p in PRODUCTS}
assert all(neg[p] >= 1 for p in PRODUCTS), "expected negative depths retained in every product"
# cohort summary cross-check
coh = rd(F2G_COH).set_index("cohort")["median_response_depth_z"]
for p, k in {"MOD16": "MOD16 primary", "MOD13": "MOD13 primary", "GRACE": "GRACE baseline-relative", "JRC": "JRC baseline-relative"}.items():
    assert abs(float(depth[p].median()) - coh[k]) < 1e-9

# ------------------------------------------------------------------ Phase 2G: statistical families
OUTC = {"MOD16_ETPET_response_depth_z": "MOD16", "MOD13_NDVI_response_depth_z": "MOD13",
        "JRC_water_response_depth_z": "JRC", "GRACE_TWSA_response_depth_z": "GRACE"}


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n); m = 1.0
    for rk, i in zip(range(n, 0, -1), o[::-1]):
        m = min(m, p[i] * n / rk); q[i] = m
    return q


FAM = {}
for k in ("primary", "secondary", "physics"):
    t = rd(F2G[k]); t["key"] = t["family"] + "|" + t["predictor"] + "|" + t["outcome"]; t["product"] = t["outcome"].map(OUTC)
    FAM[k] = t
t = rd(F2G["class"]); t["key"] = "driver_class_omnibus|" + t["outcome"]; t["product"] = t["outcome"].map(OUTC); FAM["class"] = t
t = rd(F2G["cross"]); t["key"] = "cross_response|" + t["pair_label"]; FAM["cross"] = t
EXPECT = {"primary": 16, "secondary": 12, "physics": 8, "class": 4, "cross": 6}
assert {k: len(v) for k, v in FAM.items()} == EXPECT, "statistical-family row counts differ"
N_TESTS = sum(len(v) for v in FAM.values()); assert N_TESTS == 46
allkeys = pd.concat([v["key"] for v in FAM.values()]); assert allkeys.is_unique, "duplicate test keys"
for k, v in FAM.items():
    assert v[["p_perm", "p_fdr_bh"]].notna().all().all()
    assert np.allclose(bh(v["p_perm"]), v["p_fdr_bh"], atol=1e-9), f"{k}: stored q != BH(p) within family"
    assert ((v["p_fdr_bh"] <= 0.05).astype(int) == v["fdr_0_05_flag"]).all()
    assert (v["p_fdr_bh"] <= 0.05).sum() == 0, f"{k}: a q <= 0.05 exists"
for k in ("primary", "secondary", "physics"):
    assert FAM[k]["product"].notna().all()
cr = FAM["cross"].set_index("pair_label")
assert [int(cr.loc[x, "n"]) for x in ("MOD16 vs NDVI", "TWSA vs JRC")] == [39, 29]
assert abs(cr.loc["MOD16 vs NDVI", "p_fdr_bh"] - 0.0576) < 1e-9 and abs(cr.loc["TWSA vs JRC", "p_fdr_bh"] - 0.0576) < 1e-9
assert abs(cr.loc["MOD16 vs NDVI", "p_perm"] - 0.0192) < 1e-9 and abs(cr.loc["TWSA vs JRC", "p_perm"] - 0.0098) < 1e-9
assert abs(cr.loc["MOD16 vs NDVI", "rho"] - 0.383) < 5e-4 and abs(cr.loc["TWSA vs JRC", "rho"] - 0.476) < 5e-4
assert (cr.drop(["MOD16 vs NDVI", "TWSA vs JRC"])["p_perm"] >= 0.119).all()
assert (FAM["class"]["p_fdr_bh"] == 0.8754).all()
eps = FAM["class"].set_index("product")["epsilon2"]
assert [round(float(eps[p]), 4) for p in ("MOD16", "MOD13", "GRACE", "JRC")] == [0.0, 0.0, 0.0126, 0.0]
print("ALL SOURCE / LOCKED-VALUE / MULTIPLICITY QA PASSED:", N_TESTS, "tests; q<=0.05 count = 0")

# ------------------------------------------------------------------ style
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none", "svg.hashsalt": "AEZ26_Fig4", "font.size": 7,
    "axes.labelsize": 6.8, "xtick.labelsize": 6.3, "ytick.labelsize": 6.3,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.major.size": 2.5, "ytick.major.size": 0, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white"})
INK, MID, GREY = "#222222", "#6B6B6B", "#9A9A9A"
W_MM, H_MM = 4134 / 600 * 25.4, 140.0
fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4), dpi=600)
axmm = lambda l, b, w, h: fig.add_axes([l / W_MM, b / H_MM, w / W_MM, h / H_MM])
plabel = lambda s, x, y: fig.text(x / W_MM, y / H_MM, s, fontsize=10, fontweight="bold", ha="left", va="top")
rng = np.random.default_rng(4)   # deterministic jitter


def strip(ax, data, xlabel, fmt, xlim, ticks, zero=False):
    for i, p in enumerate(PRODUCTS):
        v = data[p].values
        q1, q3 = np.percentile(v, [25, 75])
        ax.add_patch(plt.Rectangle((q1, i - 0.30), q3 - q1, 0.60, fill=False, ec=GREY, lw=0.6, zorder=1))
        jit = rng.uniform(-0.2, 0.2, len(v))
        ax.scatter(v, i + jit, s=6.5, marker=PMARK[p], color=PCOL[p], alpha=0.8, edgecolor="none", zorder=3)
        med = float(np.median(v))
        ax.plot([med, med], [i - 0.36, i + 0.36], color=INK, lw=1.5, zorder=5, solid_capstyle="butt")
        ax.text(1.03, i, f"n = {len(v)}\nmedian {fmt(med)}", transform=ax.get_yaxis_transform(), fontsize=5.6,
                va="center", ha="left", color=INK)
    if zero:
        ax.axvline(0, color=MID, lw=0.6, ls=(0, (3, 2)), zorder=0)
    ax.set_ylim(len(PRODUCTS) - 0.4, -0.6); ax.set_yticks(range(4)); ax.set_yticklabels([PNAME[p] for p in PRODUCTS])
    ax.set_xlim(*xlim); ax.set_xticks(ticks); ax.set_xlabel(xlabel)


# ------------------------------------------------------------------ a
axa = axmm(25.0, 98.0, 40.0, 36.0)
strip(axa, depth, "Response depth, z_base − z_min (z)", lambda m: f"{m:.2f}", (-1.2, 4.6), [-1, 0, 1, 2, 3, 4], zero=True)
# ------------------------------------------------------------------ b
axb = axmm(112.0, 98.0, 40.0, 36.0)
strip(axb, lag, "Onset-to-minimum lag (days)", lambda m: f"{m:.0f} d", (-10, 470), [0, 100, 200, 300, 400], zero=False)
axb.set_yticks(range(4)); axb.set_yticklabels([PNAME[p] for p in PRODUCTS])

# ------------------------------------------------------------------ c
axc = axmm(36.0, 11.0, 62.0, 66.0)
FAMS = [("Primary drivers (16 tests)", "primary", "predictor_label"),
        ("Secondary atmospheric (12)", "secondary", "predictor_label"),
        ("Event physics (8)", "physics", "predictor_label"),
        ("Driver-class omnibus (4)", "class", None),
        ("Cross-response coupling (6)", "cross", None)]
SHORT = {"Precipitation deficit strength": "Precip. deficit", "Potential evaporation excess": "PE excess",
         "VPD excess": "VPD excess", "Temperature excess": "Temperature excess", "Net radiation excess": "Net radiation excess",
         "Low-RH / dry-air strength": "Low RH / dry air", "Wind excess": "Wind excess",
         "Flash-drought severity": "Event severity", "Flash-drought intensification rate": "Intensification rate"}
OFFS = dict(zip(PRODUCTS, (-0.3, -0.1, 0.1, 0.3)))
r = 0; yt, yl = [], []
for head, k, plab in FAMS:
    axc.text(0.07, r, head, fontsize=6.2, fontweight="bold", color=INK, va="center", ha="left"); r += 1
    t = FAM[k]
    if plab:
        for pl in dict.fromkeys(t[plab]):                 # predictor order as stored in the source
            for _, row in t[t[plab] == pl].iterrows():
                axc.plot([row["p_fdr_bh"]], [r + OFFS[row["product"]]], marker=PMARK[row["product"]], ms=2.3,
                         color=PCOL[row["product"]], mec="none", ls="none", zorder=3)
            yt.append(r); yl.append(SHORT[pl]); r += 1
    elif k == "class":
        for _, row in t.iterrows():
            axc.plot([row["p_fdr_bh"]], [r + OFFS[row["product"]]], marker=PMARK[row["product"]], ms=2.3,
                     color=PCOL[row["product"]], mec="none", ls="none", zorder=3)
        yt.append(r); yl.append("Driver class (4 groups)"); r += 1
    else:
        for _, row in t.iterrows():
            axc.plot([row["p_fdr_bh"]], [r], marker="o", ms=2.8, color="#444444", mec="none", ls="none", zorder=3)
            if row["pair_label"] in ("MOD16 vs NDVI", "TWSA vs JRC"):   # nominal p < 0.05 pairs: annotated, not marked
                axc.text(row["p_fdr_bh"] + 0.045, r, f"nominal p = {row['p_perm']:.4f}; q = {row['p_fdr_bh']:.4f}",
                         fontsize=5.4, color=MID, va="center", ha="left", style="italic")
            yt.append(r); yl.append(row["pair_label"].replace("MOD16 vs NDVI", "MOD16 vs NDVI")); r += 1
axc.axvline(0.05, color=INK, lw=0.7, ls=(0, (2, 2)), zorder=1)
axc.text(0.05, 1.005, "q = 0.05", transform=axc.get_xaxis_transform(), fontsize=5.6, color=INK, ha="left", va="bottom")
axc.set_ylim(r - 0.4, -0.7); axc.set_yticks(yt); axc.set_yticklabels(yl)
axc.set_xlim(0, 1.0); axc.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); axc.set_xticklabels(["0", "0.25", "0.5", "0.75", "1"])
axc.set_xlabel("BH/FDR q-value (within family)")
axc.text(0.0, 1.07, f"No test satisfied q ≤ 0.05 ({N_TESTS} tests, 5 families)", transform=axc.transAxes, fontsize=6.6,
         fontweight="bold", color=INK, ha="left", va="bottom")

# ------------------------------------------------------------------ d
axd = axmm(126.0, 48.0, 36.0, 30.0)
for i, p in enumerate(PRODUCTS):
    o, c, n = rec[p]["obs"], rec[p]["cens"], rec[p]["n"]
    axd.barh(i, 100 * o / n, height=0.62, color=PCOL[p], ec=PCOL[p], lw=0.8, zorder=2)
    axd.barh(i, 100 * c / n, left=100 * o / n, height=0.62, color="white", ec=PCOL[p], lw=0.8, hatch="////", zorder=2)
    axd.text(100 * o / n / 2, i, str(o), ha="center", va="center", color="white", fontsize=6.4, fontweight="bold", zorder=4)
    axd.text(100 * o / n + 100 * c / n / 2, i, str(c), ha="center", va="center", color=INK, fontsize=6.4, fontweight="bold",
             zorder=4, bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none"))
    axd.text(1.03, i, f"of {n}", transform=axd.get_yaxis_transform(), fontsize=5.8, va="center", ha="left", color=INK)
axd.set_ylim(3.5, -0.6); axd.set_yticks(range(4)); axd.set_yticklabels([PNAME[p] for p in PRODUCTS])
axd.set_xlim(0, 100); axd.set_xticks([0, 25, 50, 75, 100]); axd.set_xlabel("Seasonal-normal recovery\n(% of events)")
axd.legend(handles=[Patch(fc="#7F7F7F", ec="#7F7F7F", label="Recovery observed"),
                    Patch(fc="white", ec="#7F7F7F", hatch="////", label="Not observed within finite window\n(right-censored)")],
           loc="upper left", bbox_to_anchor=(-0.02, -0.40), frameon=False, fontsize=5.8, handlelength=1.6,
           handletextpad=0.5, labelspacing=0.5, borderaxespad=0)

# shared product key (panels a-d)
LEG = {"MOD16": "MOD16 ET/PET", "MOD13": "MOD13 NDVI", "JRC": "JRC surface-water extent", "GRACE": "GRACE TWSA"}
hp = [Line2D([], [], marker=PMARK[p], ls="none", color=PCOL[p], ms=4.2, label=LEG[p]) for p in PRODUCTS]
hp.append(Line2D([], [], marker="o", ls="none", color="#444444", ms=4.2, label="Cross-response pair (c)"))
fig.legend(handles=hp, loc="lower left", bbox_to_anchor=(108.0 / W_MM, 4.0 / H_MM), ncol=1, frameon=False, fontsize=5.9,
           handletextpad=0.4, labelspacing=0.45, borderaxespad=0, title="Product key", title_fontsize=6.0, alignment="left")

plabel("a", 1.0, 139.5); plabel("b", 90.0, 139.5); plabel("c", 1.0, 87.0); plabel("d", 106.0, 87.0)

png = os.path.join(OUT, args.stem + ".png"); svg = os.path.join(OUT, args.stem + ".svg")
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=600); buf.seek(0)
Image.open(buf).convert("RGB").save(png, dpi=(600, 600), optimize=True)
fig.savefig(svg, format="svg", metadata={"Date": None, "Creator": "make_AEZ26_Fig4.py"})
chk = Image.open(png)
print("PNG", chk.size, chk.mode, chk.info.get("dpi"), "| data dir:", DATA)
print("negative depths retained:", neg, "| depth min:", {p: round(float(depth[p].min()), 3) for p in PRODUCTS})
print("versions: python", sys.version.split()[0], "| matplotlib", matplotlib.__version__, "| pandas", pd.__version__,
      "| numpy", np.__version__, "| Pillow", Image.__version__)
