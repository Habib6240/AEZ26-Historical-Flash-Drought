#!/usr/bin/env python3
"""
make_AEZ26_Fig3.py
FIGURE 3 - Source and record-length robustness of regional flash-drought detection (AEZ-26, High Barind Tract).

(a) inventory sizes (common 2000-2025 period vs extended 1981-2025 record), (b) cumulative onset agreement with the
GLDAS primary catalogue, (c) onset-season shares, (d) 15-year event rates + trend / continuous-state summary.

Robustness / sensitivity figure. ERA5-Land does not validate GLDAS; source disagreement is not error; absence of an
FDR-supported frequency trend is not evidence of no climate change. All plotted values come from the uploaded CSVs.

Usage: python make_AEZ26_Fig3.py [--data-dir DIR] [--out-dir DIR]
"""
import argparse, io, os, sys, textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import pandas as pd
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument("--data-dir", default=None)
ap.add_argument("--out-dir", default=None)
ap.add_argument("--stem", default="AEZ26_Fig3_Source_Record_Robustness")
args = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__))
F = dict(gl="AEZ26_Phase7A_Audit_Reconstructed_GLDAS_v3_Primary_39.csv",
         s26="AEZ26_Robustness_ERA5Land_Source26_Event_Catalogue_2000_2025.csv",
         l45="AEZ26_Robustness_ERA5Land_Long45_Event_Catalogue_1981_2025.csv",
         agr="AEZ26_Robustness_Event_Onset_Agreement.csv", sea="AEZ26_Robustness_Long45_Seasonality.csv",
         rate="AEZ26_Robustness_Long45_Period_Event_Rates.csv", cont="AEZ26_Robustness_Continuous_State_Agreement.csv",
         trend="AEZ26_Robustness_Long_Record_Trend_Diagnostics.csv", qc="AEZ26_Robustness_QC.csv")
DATA = next((c for c in (args.data_dir, HERE, os.getcwd())
             if c and all(os.path.exists(os.path.join(c, f)) for f in F.values())), None)
if DATA is None:
    sys.exit("BLOCKING SOURCE PROBLEM: required CSVs not found")
OUT = args.out_dir or HERE
os.makedirs(OUT, exist_ok=True)
D = {k: pd.read_csv(os.path.join(DATA, f)) for k, f in F.items()}
gl, s26, l45 = D["gl"], D["s26"], D["l45"]

# ------------------------------------------------------------------ catalogue QA
assert len(gl) == 39 and len(s26) == 44 and len(l45) == 74, "catalogue sizes differ"
for n, d in (("GLDAS", gl), ("OVERLAP26", s26), ("LONG45", l45)):
    assert d["event_id"].is_unique and d["onset_pentad"].is_unique and not d.duplicated().any(), f"{n}: duplicate keys"
    assert d["catalogue"].nunique() == 1
assert gl["catalogue"].iloc[0] == "PRIMARY_SM0_100" and s26["catalogue"].iloc[0] == "ERA5_SOURCE26" and l45["catalogue"].iloc[0] == "ERA5_LONG45"
assert s26["onset_year"].between(2000, 2025).all() and gl["onset_year"].between(2000, 2025).all()
l45c = l45[l45["onset_year"].between(2000, 2025)].reset_index(drop=True)   # LONG45 restricted to the common 2000-2025 period
assert len(l45c) == 43 and l45["onset_year"].min() == 1981 and l45["onset_year"].max() <= 2025
qc = D["qc"]; assert (qc["status"] == "PASS").all() and int(qc.set_index("check").loc["Locked GLDAS v3 reconstructed events", "value"]) == 39

# ------------------------------------------------------------------ onset agreement: stored values + independent re-derivation
agr = D["agr"]
CMP = {"s26": "GLDAS_primary_vs_ERA5_source26", "l45": "GLDAS_primary_vs_ERA5_long45_overlap"}
M = {k: agr[agr["comparison"] == v].sort_values("tolerance_pentads") for k, v in CMP.items()}
for k in M:
    assert list(M[k]["tolerance_pentads"]) == [0, 1, 2] and (M[k]["primary_total"] == 39).all()
    assert (np.diff(M[k]["matched_primary_events"]) >= 0).all(), "matches must be cumulative (non-decreasing)"
assert (M["s26"]["sensitivity_total"] == 44).all() and (M["l45"]["sensitivity_total"] == 43).all()
assert list(M["s26"]["matched_primary_events"]) == [7, 11, 15] and list(M["l45"]["matched_primary_events"]) == [6, 13, 16]
pidx = lambda d: (d["onset_pentad"].str[:4].astype(int) * 73 + d["onset_pentad"].str[-2:].astype(int)).values


def max_one_to_one(a, b, k):
    """size of a maximum one-to-one matching of onsets within +-k pentads (bipartite augmenting paths)"""
    adj = [[j for j in range(len(b)) if abs(a[i] - b[j]) <= k] for i in range(len(a))]
    mt = {}

    def aug(u, seen):
        for v in adj[u]:
            if v not in seen:
                seen.add(v)
                if v not in mt or aug(mt[v], seen):
                    mt[v] = u; return True
        return False
    return sum(aug(u, set()) for u in range(len(a)))


for key, cat in (("s26", s26), ("l45", l45c)):
    rec = [max_one_to_one(pidx(gl), pidx(cat), k) for k in (0, 1, 2)]
    assert rec == list(M[key]["matched_primary_events"]), f"{key}: stored matches differ from re-derived one-to-one matches {rec}"

# ------------------------------------------------------------------ seasons (shares from counts)
SEAS = ["MAM", "JJAS", "ON", "DJF"]
SRC = {"PreMonsoon_MAM": "MAM", "Monsoon_JJAS": "JJAS", "PostMonsoon_ON": "ON", "Winter_DJF": "DJF"}
mon2s = {12: "DJF", 1: "DJF", 2: "DJF", 3: "MAM", 4: "MAM", 5: "MAM", 6: "JJAS", 7: "JJAS", 8: "JJAS", 9: "JJAS", 10: "ON", 11: "ON"}
cnt_gl = gl["onset_month"].map(mon2s).value_counts().reindex(SEAS).fillna(0).astype(int)
cnt_l45 = D["sea"].assign(s=D["sea"]["season"].map(SRC)).set_index("s")["events"].reindex(SEAS)
assert (l45["onset_month"].map(mon2s).value_counts().reindex(SEAS).fillna(0).astype(int).values == cnt_l45.values).all(), "LONG45 catalogue vs seasonality CSV"
assert cnt_gl.to_dict() == {"MAM": 9, "JJAS": 24, "ON": 5, "DJF": 1} and cnt_l45.to_dict() == {"MAM": 23, "JJAS": 44, "ON": 7, "DJF": 0}
assert cnt_gl.sum() == 39 and cnt_l45.sum() == 74
sh_gl, sh_l45 = 100 * cnt_gl / cnt_gl.sum(), 100 * cnt_l45 / cnt_l45.sum()

# ------------------------------------------------------------------ 15-year rates (stored; re-derived from the catalogue)
rate = D["rate"]
assert list(rate["period"]) == ["1981-1995", "1996-2010", "2011-2025"] and (rate["years"] == 15).all()
assert np.allclose(rate["events_per_year"], rate["events"] / rate["years"])
for (lo, hi), n in zip(((1981, 1995), (1996, 2010), (2011, 2025)), rate["events"]):
    assert int(l45["onset_year"].between(lo, hi).sum()) == int(n)
assert [round(x, 2) for x in rate["events_per_year"]] == [1.67, 1.67, 1.60]

# ------------------------------------------------------------------ continuous state, trends, FDR
cs = D["cont"].set_index("metric")["value"]
assert round(cs["Spearman percentile agreement"], 3) == 0.583 and round(cs["Spearman standardized-anomaly agreement"], 3) == 0.578
tr = D["trend"].set_index("metric")
assert len(tr) == 5
cnt = tr.loc["ERA5-Land flash-drought annual count"]
assert cnt["theil_sen_change_per_decade"] == 0 and cnt["theil_sen_95ci_low_per_decade"] == 0 and cnt["theil_sen_95ci_high_per_decade"] == 0


def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p); q = np.empty(n); m = 1.0
    for rk, i in zip(range(n, 0, -1), o[::-1]):
        m = min(m, p[i] * n / rk); q[i] = m
    return q


# The trend table stores nominal Kendall p only (no q). BH q is RECOMPUTED here over the five stored tests.
q_trend = pd.Series(bh(tr["kendall_p_value"].values), index=tr.index)
assert (q_trend > 0.05).all(), "a trend survives FDR"
assert abs(q_trend.min() - 0.0879) < 5e-4
assert abs(tr.loc["Annual mean temperature", "theil_sen_change_per_decade"] - 0.089) < 1e-3 and abs(tr.loc["Annual mean temperature", "kendall_p_value"] - 0.0439) < 5e-5
assert abs(tr.loc["Annual ERA5-Land potential evaporation", "kendall_p_value"] - 0.021) < 5e-4
print("ALL SOURCE / ONSET-MATCH / SEASON / RATE / TREND QA PASSED | min recomputed BH q =", round(q_trend.min(), 4))

# ------------------------------------------------------------------ style
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none", "svg.hashsalt": "AEZ26_Fig3", "font.size": 7,
    "axes.labelsize": 6.8, "xtick.labelsize": 6.3, "ytick.labelsize": 6.3,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.5,
    "ytick.major.size": 2.5, "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white"})
INK, MID = "#222222", "#6B6B6B"
SC = {"gl": ("#0072B2", "o"), "s26": ("#E69F00", "s"), "l45": ("#009E73", "^")}   # source encodings (not a ranking)
W_MM, H_MM = 4134 / 600 * 25.4, 122.0
fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4), dpi=600)
axmm = lambda l, b, w, h: fig.add_axes([l / W_MM, b / H_MM, w / W_MM, h / H_MM])
plabel = lambda s, x, y: fig.text(x / W_MM, y / H_MM, s, fontsize=10, fontweight="bold", ha="left", va="top")
MS = 4.8


def pt(ax, x, y, k, filled=True, **kw):
    c, m = SC[k]
    ax.plot([x], [y], marker=m, ms=MS if m != "^" else MS + 0.4, ls="none", mfc=c if filled else "white", mec=c, mew=1.0,
            zorder=4, clip_on=False, **kw)


# ------------------------------------------------------------------ a: inventory sizes
axa = axmm(40.0, 74.0, 40.0, 42.0)
rows = [(0, "hdr", "Common period 2000–2025"), (1, "gl", "GLDAS primary", len(gl)), (2, "s26", "ERA5-Land OVERLAP26", len(s26)),
        (3, "l45", "ERA5-Land LONG45,\nonsets 2000–2025", len(l45c)), (4.9, "hdr", "Extended record 1981–2025"),
        (5.9, "l45f", "ERA5-Land LONG45,\nfull record", len(l45))]
yt, yl = [], []
for r in rows:
    if r[1] == "hdr":
        axa.text(1.5, r[0], r[2], fontsize=6.2, fontweight="bold", color=INK, va="center", ha="left")
        continue
    y, k, lab, n = r
    kk = "l45" if k == "l45f" else k
    axa.plot([0, n], [y, y], color="#C8C8C8", lw=0.7, zorder=1)
    pt(axa, n, y, kk, filled=(k != "l45f"))
    axa.text(n + 2.2, y, f"{n}", fontsize=6.6, fontweight="bold", va="center", ha="left", color=INK)
    yt.append(y); yl.append(lab)
axa.axhline(4.1, color="#9A9A9A", lw=0.6, ls=(0, (3, 2)), zorder=0)
axa.set_ylim(6.5, -0.6); axa.set_yticks(yt); axa.set_yticklabels(yl); axa.tick_params(axis="y", length=0)
axa.set_xlim(0, 85); axa.set_xticks([0, 20, 40, 60, 80]); axa.set_xlabel("Regional events (count)")
axa.text(0.99, 0.43, "different periods:\nnot directly comparable", transform=axa.transAxes, fontsize=5.4, style="italic", color=MID,
         ha="right", va="center")

# ------------------------------------------------------------------ b: cumulative onset agreement
axb = axmm(106.0, 74.0, 62.0, 42.0)
tx = np.arange(3)
for k, dx, ha in (("s26", -0.07, "right"), ("l45", 0.07, "left")):
    v = M[k]["matched_primary_events"].values
    axb.plot(tx + dx, v, color=SC[k][0], lw=0.9, zorder=2)
    for x, yv in zip(tx, v):
        pt(axb, x + dx, yv, k)
        axb.text(x + dx + (-0.1 if ha == "right" else 0.1), yv, str(yv), fontsize=6.4, color=INK, ha=ha, va="center")
axb.set_xlim(-0.5, 2.5); axb.set_ylim(0, 20); axb.set_yticks([0, 5, 10, 15, 20])
axb.set_xticks(tx); axb.set_xticklabels(["Exact", "±1 pentad", "±2 pentads"])
axb.set_xlabel("Onset-matching tolerance (cumulative: within tolerance)")
axb.set_ylabel("GLDAS onsets matched (of 39)")
axb.legend(handles=[Line2D([], [], marker=SC["s26"][1], color=SC["s26"][0], ms=MS - 0.6, label="ERA5-Land OVERLAP26 (44 events)"),
                    Line2D([], [], marker=SC["l45"][1], color=SC["l45"][0], ms=MS - 0.2, label="ERA5-Land LONG45, 2000–2025 (43)")],
           loc="upper left", frameon=False, fontsize=5.8, handletextpad=0.4, borderaxespad=0.1, labelspacing=0.35)
axb.text(0.99, 0.02, "y-axis truncated at 20 (n = 39)", transform=axb.transAxes, fontsize=5.4, style="italic", color=MID, ha="right", va="bottom")

# ------------------------------------------------------------------ c: season shares
axc = axmm(24.0, 12.0, 56.0, 38.0)
for i, sname in enumerate(SEAS):
    a, b = sh_gl[sname], sh_l45[sname]
    axc.plot([a, b], [i - 0.15, i + 0.15], color="#C8C8C8", lw=0.7, zorder=1)
    pt(axc, a, i - 0.15, "gl"); pt(axc, b, i + 0.15, "l45")
    axc.text(a + 2.2, i - 0.15, f"{a:.1f}%", fontsize=6.0, va="center", ha="left", color=INK)
    axc.text(b + 2.2, i + 0.15, f"{b:.1f}%", fontsize=6.0, va="center", ha="left", color=INK)
axc.set_ylim(3.6, -0.6); axc.set_yticks(range(4)); axc.set_yticklabels(["MAM", "JJAS", "ON", "DJF"]); axc.tick_params(axis="y", length=0)
axc.set_xlim(0, 80); axc.set_xticks([0, 20, 40, 60, 80]); axc.set_xlabel("Share of events by onset season (%)")
axc.legend(handles=[Line2D([], [], marker=SC["gl"][1], ls="none", color=SC["gl"][0], ms=MS - 0.6, label=f"GLDAS primary, 2000–2025 (n = {len(gl)})"),
                    Line2D([], [], marker=SC["l45"][1], ls="none", color=SC["l45"][0], ms=MS - 0.2, label=f"ERA5-Land LONG45, 1981–2025 (n = {len(l45)})")],
           loc="lower right", frameon=False, fontsize=5.8, handletextpad=0.2, borderaxespad=0.1, labelspacing=0.35)

# ------------------------------------------------------------------ d: 15-year rates + trend / continuous-state summary
axd = axmm(106.0, 36.0, 62.0, 16.0)
labs = [p.replace("-", "–") for p in rate["period"]]
for i, (p, ev, r) in enumerate(zip(labs, rate["events"], rate["events_per_year"])):
    axd.plot([i, i], [0, r], color="#C8C8C8", lw=0.7, zorder=1)
    pt(axd, i, r, "l45")
    axd.text(i, r + 0.33, f"{r:.2f}", fontsize=6.4, fontweight="bold", ha="center", va="bottom", color=INK)
    axd.text(i + 0.16, r, f"({int(ev)} events)", fontsize=5.6, ha="left", va="center", color=MID)
axd.set_xlim(-0.5, 2.9); axd.set_ylim(0, 2.8); axd.set_yticks([0, 1, 2]); axd.set_xticks(range(3)); axd.set_xticklabels(labs)
axd.set_ylabel("Events yr$^{-1}$"); axd.set_xlabel("15-year period, ERA5-Land LONG45")
txt = axmm(106.0, 1.0, 66.0, 25.0); txt.axis("off"); txt.set_xlim(0, 1); txt.set_ylim(0, 1)
cnt_tau, cnt_p = cnt["kendall_tau"], cnt["kendall_p_value"]
TAU = f"−{abs(cnt_tau):.2f}" if cnt_tau < 0 else f"{cnt_tau:.2f}"
blocks = [
    ("No FDR-supported increase in event frequency, 1981–2025.",
     f"Annual event count: Theil–Sen slope 0.0 events/decade (95% CI 0.0–0.0); Kendall τ = {TAU}, nominal p = {cnt_p:.2f}."),
    ("No tested hydroclimate trend survives FDR.",
     f"Temperature, VPD, precipitation, potential evaporation: BH q ≥ {q_trend.min():.3f} (recomputed from the five stored p-values)."),
    ("Continuous-state agreement is moderate.",
     f"ERA5-Land vs GLDAS Spearman ρ = {cs['Spearman percentile agreement']:.3f} (percentile), {cs['Spearman standardized-anomaly agreement']:.3f} (standardized anomaly); not event-date agreement."),
]
y = 0.995
for head, body in blocks:
    txt.text(0.0, y, head, fontsize=5.9, fontweight="bold", color=INK, va="top", ha="left")
    bw = textwrap.fill(body, 64)
    txt.text(0.0, y - 0.075, bw, fontsize=5.6, color=INK, va="top", ha="left", linespacing=1.25)
    y -= 0.075 + 0.1 * (bw.count("\n") + 1) + 0.07

plabel("a", 1.0, 121.5); plabel("b", 90.0, 121.5); plabel("c", 1.0, 60.0); plabel("d", 90.0, 60.0)

# ------------------------------------------------------------------ save
png = os.path.join(OUT, args.stem + ".png"); svg = os.path.join(OUT, args.stem + ".svg")
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=600); buf.seek(0)
Image.open(buf).convert("RGB").save(png, dpi=(600, 600), optimize=True)
fig.savefig(svg, format="svg", metadata={"Date": None, "Creator": "make_AEZ26_Fig3.py"})
chk = Image.open(png)
print("PNG", chk.size, chk.mode, chk.info.get("dpi"), "| data dir:", DATA)
print("shares GLDAS:", sh_gl.round(1).to_dict(), "| LONG45:", sh_l45.round(1).to_dict())
print("BH q (recomputed):", q_trend.round(4).to_dict())
print("versions: python", sys.version.split()[0], "| matplotlib", matplotlib.__version__, "| pandas", pd.__version__,
      "| numpy", np.__version__, "| Pillow", Image.__version__)
