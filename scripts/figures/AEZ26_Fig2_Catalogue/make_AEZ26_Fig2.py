#!/usr/bin/env python3
"""
make_AEZ26_Fig2.py
FIGURE 2 - Primary flash-drought catalogue and event characteristics
AEZ-26 High Barind Tract (Bangladesh), 2000-2025.

Descriptive historical figure. Not a trend figure; no spatial footprints; no causal attribution.

Usage:
    python make_AEZ26_Fig2.py [--data-dir DIR] [--out-dir DIR] [--yscale log|linear]
Defaults: data-dir = script folder (falls back to CWD),
          out-dir  = script folder, yscale = log (decision documented in README).

All plotted values are read from the uploaded CSVs. No event rows are typed by hand.
The script STOPS (AssertionError / SystemExit) on catalogue-version mismatch,
unmatched joins, or any locked QA mismatch.
"""
import argparse
import io
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd
from PIL import Image

# ----------------------------------------------------------------------------- arguments
ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default=None)
ap.add_argument("--out-dir", default=None)
ap.add_argument("--yscale", default="log", choices=["log", "linear"])
ap.add_argument("--stem", default="AEZ26_Fig2_Catalogue")
args = ap.parse_args()

HERE = os.path.dirname(os.path.abspath(__file__))
FN_CAT = "AEZ26_Flash_Drought_Event_Catalogue_Primary_2000_2025.csv"
FN_DRV = "AEZ26_Phase2D_Event_Driver_Characterization.csv"
FN_SEA = "AEZ26_Phase2D_Seasonal_Onset_Summary.csv"
FN_CLS = "AEZ26_Phase2D_Driver_Class_Summary.csv"


def find_dir():
    cands = [args.data_dir, HERE, os.getcwd()]
    for c in cands:
        if c and all(os.path.exists(os.path.join(c, f)) for f in (FN_CAT, FN_DRV, FN_SEA, FN_CLS)):
            return c
    sys.exit("BLOCKING SOURCE PROBLEM: required CSVs not found")


DATA = find_dir()
OUT = args.out_dir or HERE
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------------------- load
cat = pd.read_csv(os.path.join(DATA, FN_CAT))
drv = pd.read_csv(os.path.join(DATA, FN_DRV))
sea = pd.read_csv(os.path.join(DATA, FN_SEA))
cls = pd.read_csv(os.path.join(DATA, FN_CLS))

# ----------------------------------------------------------------------------- VERSION QA
SUPERSEDED_V2_ONSETS = ["2003_P49", "2017_P47", "2019_P34", "2022_P45", "2023_P26", "2024_P48"]
if len(cat) != 39:
    sys.exit(f"STOP: primary catalogue has {len(cat)} rows (expected 39; 45 = superseded v2).")
if cat["onset_pentad"].isin(SUPERSEDED_V2_ONSETS).any():
    sys.exit("STOP: superseded v2 onset cases present in primary catalogue.")
assert cat["event_id"].is_unique and cat["event_id"].duplicated().sum() == 0
assert cat["right_censored_flag"].sum() == 0, "right-censored primary events present"
needed = ["onset_start_date", "onset_mid_date", "event_end_date", "total_duration_pentads",
          "total_duration_actual_days", "severity_40pct_deficit_pp_pentads",
          "intensification_duration_pentads", "mean_intensification_rate_pp_per_pentad",
          "onset_pentad", "onset_month", "prolonged_after_flash_flag"]
assert cat[needed].notna().all().all(), "missing values in required catalogue fields"

# ----------------------------------------------------------------------------- SOURCE / JOIN QA
assert len(drv) == 39 and drv["event_id"].is_unique
assert drv["primary_driver_class"].notna().all()
assert set(cat["event_id"]) == set(drv["event_id"]), "event_id sets differ -> STOP"
df = cat.merge(drv, on="event_id", how="inner", suffixes=("", "_drv"), validate="one_to_one")
assert len(df) == 39, "event join is not 39/39"
# the SAME chronology in both files: all shared event-level fields must agree
SHARED = ["onset_pentad", "onset_mid_date", "onset_year", "onset_month", "threshold_crossing_pentad",
          "intensification_duration_pentads", "total_duration_pentads",
          "severity_40pct_deficit_pp_pentads", "mean_intensification_rate_pp_per_pentad",
          "prolonged_after_flash_flag"]
for col in SHARED:
    a, b = df[col], df[col + "_drv"]
    ok = np.allclose(a, b) if pd.api.types.is_numeric_dtype(a) else bool((a == b).all())
    assert ok, f"shared field disagrees between files: {col}"
JOIN_KEY = "event_id"  # one-to-one; onset_pentad is also unique and agrees (verified above)
assert df["onset_pentad"].is_unique

# no overlapping primary events (interval = onset start -> onset start + actual days)
df["t0"] = pd.to_datetime(df["onset_start_date"])
df["t1"] = df["t0"] + pd.to_timedelta(df["total_duration_actual_days"], unit="D")
df = df.sort_values("t0").reset_index(drop=True)
assert (df["t0"].iloc[1:].values >= df["t1"].iloc[:-1].values).all(), "overlapping primary events"

# ----------------------------------------------------------------------------- derived season
# season derived from onset_month; cross-checked with the source onset_season label
SEASON_OF_MONTH = {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM",
                   6: "JJAS", 7: "JJAS", 8: "JJAS", 9: "JJAS", 10: "ON", 11: "ON"}
SRC_LABEL = {"Winter_DJF": "DJF", "PreMonsoon_MAM": "MAM", "Monsoon_JJAS": "JJAS", "PostMonsoon_ON": "ON"}
df["season"] = df["onset_month"].map(SEASON_OF_MONTH)
assert (df["season"] == df["onset_season"].map(SRC_LABEL)).all(), "derived season != source season label"
SEASONS = ["MAM", "JJAS", "ON", "DJF"]
scount = df["season"].value_counts().reindex(SEASONS).fillna(0).astype(int)
sea_src = sea.set_index(sea["onset_season"].map(SRC_LABEL))["event_count"].reindex(SEASONS)
assert (scount.values == sea_src.values).all(), "season counts differ from Seasonal_Onset_Summary"
spct = 100 * scount / len(df)

# ----------------------------------------------------------------------------- forcing classes
CLASSES = {  # source label -> (display, colour, marker)   Okabe-Ito colour-blind-safe + shape redundancy
    "compound_Pdeficit_highPE": ("Compound", "#D55E00", "o"),
    "precipitation_deficit_only": ("Precipitation-only", "#0072B2", "s"),
    "high_PE_only": ("High-PE-only", "#E69F00", "^"),
    "neither_large_anomaly": ("Neither", "#FFFFFF", "D"),
}
ccount = df["primary_driver_class"].value_counts()
cls_src = cls.set_index("primary_driver_class")["event_count"]
for k in CLASSES:
    assert ccount[k] == cls_src[k], f"class count differs from Driver_Class_Summary: {k}"
assert int(ccount.sum()) == 39

# ----------------------------------------------------------------------------- recomputed stats
dur = df["total_duration_pentads"].astype(float)
sev = df["severity_40pct_deficit_pp_pentads"].astype(float)
rid = df["intensification_duration_pentads"].astype(float)
rate = df["mean_intensification_rate_pp_per_pentad"].astype(float)
q = lambda s: tuple(np.percentile(s, [25, 75]))
STATS = dict(
    dur_min=dur.min(), dur_max=dur.max(), dur_med=dur.median(), dur_iqr=q(dur), dur_eq3=int((dur == 3).sum()),
    sev_min=sev.min(), sev_max=sev.max(), sev_med=sev.median(), sev_iqr=q(sev),
    rid_min=rid.min(), rid_max=rid.max(), rid_med=rid.median(),
    rate_min=rate.min(), rate_max=rate.max(), rate_med=rate.median())

# ----------------------------------------------------------------------------- locked QA (targets only)
r2 = lambda x: round(float(x), 2)
assert scount.to_dict() == {"MAM": 9, "JJAS": 24, "ON": 5, "DJF": 1}
assert [r2(x) for x in spct.values] == [23.08, 61.54, 12.82, 2.56]
mc = df["onset_month"].value_counts()
assert mc.get(9, 0) == 8 and mc.get(4, 0) == 6 and mc.get(7, 0) == 6
assert all(mc.get(m, 0) == 0 for m in (1, 11, 12))
assert (STATS["dur_min"], STATS["dur_max"], STATS["dur_med"], STATS["dur_iqr"], STATS["dur_eq3"]) == (3, 58, 5, (3.0, 6.5), 16)
assert (r2(STATS["sev_min"]), r2(STATS["sev_max"]), r2(STATS["sev_med"])) == (31.54, 1958.46, 104.62)
assert tuple(r2(x) for x in STATS["sev_iqr"]) == (62.31, 158.08)
assert (STATS["rid_min"], STATS["rid_max"], STATS["rid_med"]) == (1, 8, 2)
assert (r2(STATS["rate_min"]), r2(STATS["rate_max"]), r2(STATS["rate_med"])) == (5.77, 53.85, 14.10)
PROLONGED = ["2011_P56", "2014_P55", "2015_P55", "2018_P53"]
assert sorted(df.loc[df["prolonged_after_flash_flag"] == 1, "onset_pentad"]) == PROLONGED
pd_ = df.set_index("onset_pentad")
assert [int(pd_.loc[p, "total_duration_pentads"]) for p in PROLONGED] == [19, 19, 58, 30]
top3 = pd_["severity_40pct_deficit_pp_pentads"].nlargest(3)
assert list(top3.index) == ["2015_P55", "2018_P53", "2011_P56"]
assert [r2(x) for x in top3.values] == [1958.46, 961.54, 544.62]
assert {k: int(v) for k, v in ccount.items()} == {"compound_Pdeficit_highPE": 10, "precipitation_deficit_only": 10,
                                                  "high_PE_only": 8, "neither_large_anomaly": 11}
FLAGS = {"low RH": "low_RH_anomaly_flag", "high VPD": "high_VPD_anomaly_flag",
         "high net radiation": "high_net_radiation_anomaly_flag",
         "high temperature": "high_temperature_anomaly_flag", "high wind": "high_wind_anomaly_flag"}
assert [int(df[v].sum()) for v in FLAGS.values()] == [20, 18, 16, 14, 10]
plot_cols = ["t0", "t1", "total_duration_pentads", "severity_40pct_deficit_pp_pentads", "primary_driver_class"]
assert df[plot_cols].notna().all().all()
print("ALL SOURCE / VERSION / LOCKED-VALUE QA PASSED (join key = %s, 39/39 matched)" % JOIN_KEY)

# ----------------------------------------------------------------------------- style
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none",          # keep SVG text editable
    "svg.hashsalt": "AEZ26_Fig2",    # deterministic SVG ids
    "pdf.fonttype": 42,
    "font.size": 7, "axes.labelsize": 7.5, "xtick.labelsize": 6.5, "ytick.labelsize": 6.5,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6,
    "xtick.minor.width": 0.4, "ytick.minor.width": 0.4,
    "xtick.major.size": 2.5, "ytick.major.size": 2.5, "xtick.minor.size": 1.5, "ytick.minor.size": 1.5,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white",
})
INK, MID, LIGHT = "#222222", "#6B6B6B", "#D9D9D9"

W_MM, H_MM = 4134 / 600 * 25.4, 124.0   # 175.006 mm -> exactly 4134 px at 600 dpi
fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4), dpi=600)


def axmm(l, b, w, h):
    """axes from mm coordinates (left, bottom, width, height) measured from the figure's bottom-left."""
    return fig.add_axes([l / W_MM, b / H_MM, w / W_MM, h / H_MM])


def plabel(letter, x_mm, y_mm):
    fig.text(x_mm / W_MM, y_mm / H_MM, letter, fontsize=10, fontweight="bold", ha="left", va="top")


# ============================================================================ PANEL a
axa = axmm(12.5, 77.0, 159.5, 41.5)
# one lane per calendar month of onset (Jan at top): shows when in each year events began and
# keeps the 39 non-overlapping events separated on a continuous 2000-2025 time axis
lane = df["onset_month"].astype(float)
axa.axhspan(5.5, 9.5, color="#F1F1F1", lw=0, zorder=0)           # JJAS rows, very light guide
for _, r in df.iterrows():
    y = r["onset_month"]
    axa.plot([r["t0"], r["t1"]], [y, y], color=INK, lw=3.0, solid_capstyle="butt", zorder=2)
    axa.plot(r["t0"], y, "o", ms=2.6, color=INK, mec="none", zorder=3)
# labels for the four prolonged events only: placed one lane below their own bar (hand-tuned anchors)
LAB = {"2011_P56": ("t0", "left"), "2014_P55": ("t1", "right"),
       "2015_P55": ("t0", "left"), "2018_P53": ("t0", "left")}
for p in PROLONGED:
    r = df.loc[df["onset_pentad"] == p].iloc[0]
    anchor, ha = LAB[p]
    axa.text(r[anchor], r["onset_month"] + 1.0, p, fontsize=6.5, fontweight="bold", color=INK, ha=ha, va="center",
             zorder=4)
axa.set_ylim(12.6, 0.4)
axa.set_yticks(range(1, 13))
axa.set_yticklabels(list("JFMAMJJASOND"))
axa.set_ylabel("Onset month")
axa.set_xlim(pd.Timestamp("2000-01-01"), pd.Timestamp("2026-12-31"))
axa.xaxis.set_major_locator(mdates.YearLocator(2))
axa.xaxis.set_minor_locator(mdates.YearLocator(1))
axa.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
axa.set_xlabel("Calendar year (flash-drought onset to event end)")
axa.tick_params(axis="y", length=2)
# key
axa.plot([pd.Timestamp("2000-04-01")], [11.4], "o", ms=2.6, color=INK, mec="none")
axa.plot([pd.Timestamp("2000-04-01"), pd.Timestamp("2000-12-01")], [11.4, 11.4], color=INK, lw=3.0,
         solid_capstyle="butt")
axa.text(pd.Timestamp("2001-02-15"), 11.4, "onset (dot) and event duration (line)", fontsize=6, color=MID,
         va="center", ha="left")
axa.text(pd.Timestamp("2026-12-15"), 5.55, "JJAS", fontsize=6, color=MID, ha="right", va="bottom")

# ============================================================================ PANEL b
axb = axmm(12.5, 10.5, 52.0, 52.0)
xs = np.arange(len(SEASONS))
cols = [INK if s == "JJAS" else "#A8A8A8" for s in SEASONS]
axb.bar(xs, scount.values, width=0.68, color=cols, edgecolor="none", zorder=2)
for x, n, pc in zip(xs, scount.values, spct.values):
    axb.text(x, n + 0.55, f"{n}", ha="center", va="bottom", fontsize=7.5, fontweight="bold", color=INK)
    axb.text(x, n + 2.6, f"{pc:.1f}%", ha="center", va="bottom", fontsize=6, color=MID)
axb.set_xticks(xs)
axb.set_xticklabels(["MAM\n(Mar–May)", "JJAS\n(Jun–Sep)", "ON\n(Oct–Nov)", "DJF\n(Dec–Feb)"])
axb.set_ylim(0, 30)
axb.set_yticks(range(0, 31, 5))
axb.set_xlim(-0.6, 3.6)
axb.set_ylabel("Primary events (count)")
axb.set_xlabel("Season of onset")

# ============================================================================ PANEL c
axc = axmm(86.0, 10.5, 85.5, 52.0)
xplot = dur.values.copy()
# display-only dodge for exactly coincident (duration, severity) points; data values are unchanged
key = list(zip(dur.values, np.round(sev.values, 6)))
dodge_log = []
for k in set(key):
    idx = [i for i, kk in enumerate(key) if kk == k]
    if len(idx) > 1:
        for j, i in enumerate(idx):
            off = (j - (len(idx) - 1) / 2) * 0.55
            xplot[i] += off
            dodge_log.append((df.loc[i, "onset_pentad"], off))
axc.axvline(STATS["dur_med"], color=MID, lw=0.5, ls=(0, (3, 2)), zorder=1)
axc.axhline(STATS["sev_med"], color=MID, lw=0.5, ls=(0, (3, 2)), zorder=1)
for ck, (nm, colr, mk) in CLASSES.items():
    m = (df["primary_driver_class"] == ck).values
    axc.scatter(xplot[m], sev.values[m], s=14 if mk != "D" else 11, marker=mk, facecolor=colr,
                edgecolor=INK, linewidth=0.5, zorder=3, label=f"{nm} (n = {int(m.sum())})")
axc.set_yscale(args.yscale)
if args.yscale == "log":
    axc.set_ylim(22, 3200)
    axc.set_yticks([30, 100, 300, 1000, 2000])
    axc.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, p: f"{int(v):,}"))
    axc.yaxis.set_minor_locator(mticker.LogLocator(base=10, subs=np.arange(2, 10), numticks=20))
    axc.yaxis.set_minor_formatter(mticker.NullFormatter())
    axc.set_ylabel("Severity (percentile-point pentads, log scale)")
else:
    axc.set_ylim(0, 2100)
    axc.set_ylabel("Severity (percentile-point pentads)")
axc.set_xlim(0, 61)
axc.set_xticks([3, 10, 20, 30, 40, 50, 58])
axc.xaxis.set_minor_locator(mticker.MultipleLocator(5))
axc.set_xlabel("Total duration (pentads)")
# median annotations (small, at axes edges)
ytop = axc.get_ylim()[1]
axc.text(STATS["dur_med"] + 0.6, ytop, f"median {STATS['dur_med']:.0f}", fontsize=5.5, color=MID, ha="left", va="top",
         rotation=90)
axc.text(60.6, STATS["sev_med"] * (1.07 if args.yscale == "log" else 1.0) + (0 if args.yscale == "log" else 25),
         f"median {STATS['sev_med']:.1f}", fontsize=5.5, color=MID, ha="right", va="bottom")
# labels for the four prolonged events only
LABC = {"2011_P56": (-1.3, 4.0, "right"), "2014_P55": (-1.3, -4.0, "right"),
        "2015_P55": (-1.8, 0.0, "right"), "2018_P53": (-1.8, 0.0, "right")}
for p in PROLONGED:
    r = df.loc[df["onset_pentad"] == p].iloc[0]
    dx, dyp, ha = LABC[p]
    axc.annotate(p, (r["total_duration_pentads"], r["severity_40pct_deficit_pp_pentads"]), xytext=(dx * 2.2, dyp),
                 textcoords="offset points", fontsize=6.5, fontweight="bold", color=INK, ha=ha, va="center",
                 zorder=5)
leg = axc.legend(loc="lower right", bbox_to_anchor=(1.0, -0.01), frameon=False, fontsize=6.3, handletextpad=0.3,
                 borderaxespad=0.2, labelspacing=0.35, title="Primary forcing class", title_fontsize=6.5)
leg._legend_box.align = "left"

plabel("a", 1.0, 123.5)
plabel("b", 1.0, 66.0)
plabel("c", 72.5, 66.0)

# ============================================================================ SAVE
png = os.path.join(OUT, args.stem + ".png")
svg = os.path.join(OUT, args.stem + ".svg")
buf = io.BytesIO()
fig.savefig(buf, format="png", dpi=600)
buf.seek(0)
im = Image.open(buf).convert("RGB")             # drop alpha channel -> plain RGB, white background
im.save(png, dpi=(600, 600), optimize=True)     # writes pHYs = 600 dpi
fig.savefig(svg, format="svg", metadata={"Date": None, "Creator": "make_AEZ26_Fig2.py"})
chk = Image.open(png)
print("PNG", chk.size, chk.mode, chk.info.get("dpi"))
print("dodged points (display only):", dodge_log)
print("yscale:", args.yscale, "| outputs:", png, svg)
print("versions: python", sys.version.split()[0], "| matplotlib", matplotlib.__version__, "| pandas", pd.__version__,
      "| numpy", np.__version__, "| Pillow", Image.__version__)
