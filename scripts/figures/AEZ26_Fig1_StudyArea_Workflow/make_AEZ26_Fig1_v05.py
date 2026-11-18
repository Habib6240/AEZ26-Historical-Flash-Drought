#!/usr/bin/env python3
"""
make_AEZ26_Fig1_v05.py
FIGURE 1 (v05, grid and panel alignment correction of v04) - Study area and analytical workflow (AEZ-26, High Barind Tract, Bangladesh).

Panel (a): AEZ-26 boundary in WGS 84 / UTM zone 45N (EPSG:32645), straight 10 km UTM grid (grid lines coincide with the frame edges; geographic coordinates as ticks on the top and right edges), segmented scale bar
whose length is computed in projected metres (with the UTM point-scale factor at the map centre), grid-north arrow,
Bangladesh locator inset.  Panel (b): analytical workflow of the historical study (v05 shows the historical workflow only; the earlier CMIP6 branch is not shown).

Geometry sources (see README_AEZ26_Fig1.md): data/AEZ26_HBT_boundary_recovered.geojson (vertices recovered from the
vector SVG of Fig. 1 v02 and validated against the stored QA values: 6 parts; 27/34/39/42/112/1641 vertices; bounds;
geodesic perimeter), data/BGD_locator_outline_recovered_simplified.json (locator only).
No GIS library is needed: the Transverse Mercator (Kruger series) and the Vincenty geodesic are implemented in geo.py.
Usage: python make_AEZ26_Fig1_v05.py [--out-dir DIR]
"""
import argparse, io, json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, PathPatch, Rectangle, Polygon
from matplotlib.path import Path
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from geo import utm, perimeter_km

ap = argparse.ArgumentParser(); ap.add_argument("--out-dir", default=None); ap.add_argument("--stem", default="AEZ26_Fig1_StudyArea_Workflow_v05")
args = ap.parse_args(); OUT = args.out_dir or HERE; os.makedirs(OUT, exist_ok=True)

gj = json.load(open(os.path.join(HERE, "data", "AEZ26_HBT_boundary_recovered.geojson")))
geom = gj["features"][0]["geometry"]
assert len(gj["features"]) == 1 and geom["type"] == "MultiPolygon"
rings = [np.array(p[0]) for p in geom["coordinates"]]
assert all(len(p) == 1 for p in geom["coordinates"])
assert sorted(len(r) for r in rings) == [27, 34, 39, 42, 112, 1641] and all(np.allclose(r[0], r[-1]) for r in rings)
allpts = np.vstack(rings); lon_min, lat_min = allpts.min(0); lon_max, lat_max = allpts.max(0)
assert np.allclose([lon_min, lon_max, lat_min, lat_max], [88.280422, 88.678887, 24.366669, 25.215561], atol=2e-6)
perim = sum(perimeter_km(r) for r in rings)
assert abs(perim - 537.156) < 0.005, perim
AREA_SRC = 1545.546                      # source-reported (Earth Engine) area, km2
bgd = [np.array(r) for r in json.load(open(os.path.join(HERE, "data", "BGD_locator_outline_recovered_simplified.json")))]
bpts = np.vstack(bgd)
print(f"AEZ QA: {len(rings)} parts, {len(allpts)} vertices, geodesic perimeter {perim:.3f} km (source 537.156), "
      f"bounds {lon_min:.6f}-{lon_max:.6f}E {lat_min:.6f}-{lat_max:.6f}N")

LON0 = 87.0                              # UTM zone 45N central meridian
proj = lambda lo, la: utm(np.asarray(lo, float), np.asarray(la, float), LON0)

# ------------------------------------------------------------------ style
plt.rcParams.update({
    "font.family": "sans-serif", "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "svg.fonttype": "none", "pdf.fonttype": 42, "svg.hashsalt": "AEZ26_Fig1", "font.size": 6,
    "axes.linewidth": 0.6, "xtick.major.width": 0.6, "ytick.major.width": 0.6, "xtick.major.size": 2.2,
    "ytick.major.size": 2.2, "xtick.labelsize": 5.8, "ytick.labelsize": 5.8,
    "figure.facecolor": "white", "axes.facecolor": "white", "savefig.facecolor": "white"})
INK = "#222222"
W_MM, H_MM = 4134 / 600 * 25.4, 118.0
fig = plt.figure(figsize=(W_MM / 25.4, H_MM / 25.4), dpi=600)
axmm = lambda l, b, w, h: fig.add_axes([l / W_MM, b / H_MM, w / W_MM, h / H_MM])
AEZ_FILL, AEZ_EDGE = "#4F86B3", "#16384F"


def patch(ax, ring_list, **kw):
    ax.add_patch(PathPatch(Path(np.vstack(ring_list), np.concatenate([[1] + [2] * (len(r) - 2) + [79] for r in ring_list])), **kw))



# ------------------------------------------------------------------ panel a: map (WGS 84 / UTM 45N)
# Frame = rectangle in projected metres whose edges lie on 10 km UTM grid lines (610-680 km E, 2690-2800 km N);
# it contains the former lon/lat window (88.17-88.80 E, 24.30-25.25 N) and the whole AEZ-26 boundary.
GRID_M = 10000.0
xmin, xmax, ymin, ymax = 610000.0, 680000.0, 2690000.0, 2800000.0
MAP_H = 100.0; MAP_W = MAP_H * (xmax - xmin) / (ymax - ymin)      # equal aspect: 1 mm = same ground distance in E and N
axa = axmm(10.5, 8.0, MAP_W, MAP_H)
axa.set_xlim(xmin, xmax); axa.set_ylim(ymin, ymax); axa.set_aspect("equal", adjustable="box")
GRAT = "#B9B9B9"
gx = np.arange(xmin, xmax + 1, GRID_M); gy = np.arange(ymin, ymax + 1, GRID_M)
for x_ in gx[1:-1]: axa.plot([x_, x_], [ymin, ymax], color=GRAT, lw=0.35, zorder=1, solid_capstyle="butt")
for y_ in gy[1:-1]: axa.plot([xmin, xmax], [y_, y_], color=GRAT, lw=0.35, zorder=1, solid_capstyle="butt")
for r in rings:
    E_, N_ = proj(r[:, 0], r[:, 1]); patch(axa, [np.c_[E_, N_]], fc=AEZ_FILL, ec=AEZ_EDGE, lw=0.45, zorder=2)
# geographic coordinates: ticks where meridians cross the top edge and parallels cross the right edge
lons = np.round(np.arange(88.2, 88.79, 0.1), 1); lats = np.round(np.arange(24.4, 25.21, 0.2), 1)
tl = np.linspace(24.0, 25.6, 800); tn = np.linspace(87.9, 89.0, 800)
tx, tlab, ty, tylab = [], [], [], []
for lo in lons:
    E_, N_ = proj(np.full_like(tl, lo), tl); e_ = np.interp(ymax, N_, E_)
    if xmin < e_ < xmax: tx.append(e_); tlab.append(f"{lo:.1f}\u00b0E")
for la in lats:
    E_, N_ = proj(tn, np.full_like(tn, la)); n_ = np.interp(xmax, E_, N_)
    if ymin < n_ < ymax: ty.append(n_); tylab.append(f"{la:.1f}\u00b0N")
xt, xl = list(gx), [f"{v / 1000:.0f}" for v in gx]; yt, yl = list(gy), [f"{v / 1000:.0f}" for v in gy]
axa.set_xticks(xt); axa.set_xticklabels(xl); axa.set_yticks(yt); axa.set_yticklabels(yl)
axa.tick_params(length=2.2, width=0.6, pad=1.5)
plt.setp(axa.get_yticklabels(), rotation=90, va="center")
_yl = axa.get_yticklabels(); _yl[0].set_va("bottom"); _yl[-1].set_va("top")   # keep the corner labels clear of each other and of the frame
axt = axa.secondary_xaxis("top"); axt.set_xticks(tx); axt.set_xticklabels(tlab); axt.tick_params(length=2.2, width=0.6, pad=1.5)
axr = axa.secondary_yaxis("right"); axr.set_yticks(ty); axr.set_yticklabels(tylab); axr.tick_params(length=2.2, width=0.6, pad=1.5)
plt.setp(axr.get_yticklabels(), rotation=-90, va="center")
for a_ in (axt, axr):
    for sp in a_.spines.values(): sp.set_visible(False)
axa.set_xlabel("Easting (km), UTM zone 45N", fontsize=5.8, labelpad=1.5); axa.set_ylabel("Northing (km)", fontsize=5.8, labelpad=1.5)
lx, ly = proj(88.56, 24.71)
axa.text(lx, ly, "AEZ-26\nHigh Barind\nTract", fontsize=6.0, fontweight="bold", color=INK, ha="left", va="top", linespacing=1.2, zorder=5)
axa.text(lx, ly - 0.105 * (ymax - ymin), f"{AREA_SRC:,.2f} km²", fontsize=5.6, color=INK, ha="left", va="top", zorder=5)
# scale bar: ground distance -> grid distance with the UTM point scale factor at the map centre
cE = 0.5 * (xmin + xmax)
k0 = 0.9996 * (1 + ((cE - 500000.0) ** 2) / (2 * 6371008.8 ** 2))
sb_x0 = xmin + 0.64 * (xmax - xmin); sb_y0 = ymin + 0.045 * (ymax - ymin); seg = 10000.0 * k0; sb_h = 0.011 * (ymax - ymin)
for i in range(2):
    axa.add_patch(Rectangle((sb_x0 + i * seg, sb_y0), seg, sb_h, fc=INK if i % 2 == 0 else "white", ec=INK, lw=0.5, zorder=5))
for i, lab in enumerate(["0", "10", "20 km"]):
    axa.text(sb_x0 + i * seg, sb_y0 + sb_h + 0.006 * (ymax - ymin), lab, fontsize=5.4, ha="center", va="bottom", color=INK, zorder=5)
# north arrow (UTM grid north = up); standard split-kite symbol
nx = xmin + 0.09 * (xmax - xmin); ny0 = ymin + 0.10 * (ymax - ymin); nh = 0.10 * (ymax - ymin); nw = 0.075 * (xmax - xmin)
axa.add_patch(Polygon([[nx, ny0 + nh], [nx - nw / 2, ny0], [nx, ny0 + 0.28 * nh]], closed=True, fc=INK, ec=INK, lw=0.5, zorder=5))
axa.add_patch(Polygon([[nx, ny0 + nh], [nx + nw / 2, ny0], [nx, ny0 + 0.28 * nh]], closed=True, fc="white", ec=INK, lw=0.5, zorder=5))
axa.text(nx, ny0 + nh + 0.012 * (ymax - ymin), "N", fontsize=6.2, fontweight="bold", ha="center", va="bottom", color=INK, zorder=5)
axa.text(0.99, 0.012, "WGS 84 / UTM zone 45N (EPSG:32645); 10 km grid", transform=axa.transAxes, fontsize=4.6, ha="right", va="bottom", color="#555555", zorder=5)

# locator inset (Bangladesh outline; AEZ-26 highlighted), plain WGS 84 lon/lat with cos-corrected aspect
bl, bb, br, bt = 87.86, 20.59, 92.82, 26.78
INS_W = 19.5; INS_H = INS_W * (bt - bb) / ((br - bl) * np.cos(np.radians(23.7)))
axi = axmm(11.2, 8.0 + MAP_H - INS_H - 0.8, INS_W, INS_H)
for r in bgd:
    patch(axi, [r], fc="#EDEDED", ec="#555555", lw=0.4, zorder=1)
for r in rings:
    patch(axi, [r], fc=AEZ_FILL, ec=AEZ_EDGE, lw=0.5, zorder=3)
axi.add_patch(Rectangle((lon_min - 0.12, lat_min - 0.12), lon_max - lon_min + 0.24, lat_max - lat_min + 0.24, fill=False, ec=AEZ_EDGE, lw=0.6, zorder=4))
axi.set_xlim(bl, br); axi.set_ylim(bb, bt); axi.set_aspect(1 / np.cos(np.radians(23.7)), adjustable="box")
axi.set_xticks([]); axi.set_yticks([])
for s_ in axi.spines.values():
    s_.set_linewidth(0.6); s_.set_color("#444444")
axi.patch.set_facecolor("white"); axi.patch.set_zorder(0)
axi.text(0.5, 0.03, "Bangladesh", transform=axi.transAxes, fontsize=5.4, ha="center", va="bottom", color=INK)
fig.text(1.0 / W_MM, 117.5 / H_MM, "a", fontsize=10, fontweight="bold", ha="left", va="top")


# ------------------------------------------------------------------ panel b: workflow (coordinates in mm)
BX0 = 10.5 + MAP_W + 9.0
axb = axmm(BX0, 0, W_MM - BX0 - 1.5, H_MM); axb.set_xlim(0, W_MM - BX0 - 1.5); axb.set_ylim(0, H_MM); axb.axis("off")
WB = W_MM - BX0 - 1.5
HC, FC = "#E6EDF3", "#7A93A8"                      # historical branch: muted cool
PC, PE = "#FBEBDD", "#D9A074"                      # future pre-steps: pale warm
CW = (WB - 6.0) / 2; XL0, XR0 = 0.0, CW + 6.0       # column x0
FS = 5.7


def box(x0, y0, w, h, txt, fc, ec, fs=FS, bold=False, tc=INK, lw=0.6, ls="-", ha="center", style="normal"):
    axb.add_patch(FancyBboxPatch((x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.8", fc=fc, ec=ec, lw=lw, ls=ls, zorder=2))
    axb.text(x0 + (w / 2 if ha == "center" else 1.6), y0 + h / 2, txt, fontsize=fs, ha=ha, va="center", color=tc,
             fontweight="bold" if bold else "normal", linespacing=1.18, zorder=3, style=style)


def arrow(x, y0, y1, color="#555555", lw=0.8, ls="-"):
    axb.annotate("", xy=(x, y1), xytext=(x, y0), arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, mutation_scale=5,
                                                                shrinkA=0, shrinkB=0), zorder=1)


TOP = 8.0 + MAP_H                                   # top of workflow = top edge of the map frame
box(WB / 2 - 27, TOP - 7, 54, 7, "High Barind Tract (AEZ-26)", "#F2F2F2", "#444444", fs=6.4, bold=True, lw=0.8)
ymid = TOP - 7 - 2.6
axb.plot([XL0 + CW / 2, XR0 + CW / 2], [ymid, ymid], color="#555555", lw=0.8, zorder=1)
axb.plot([WB / 2, WB / 2], [TOP - 7, ymid], color="#555555", lw=0.8, zorder=1)
arrow(XL0 + CW / 2, ymid, ymid - 2.0); arrow(XR0 + CW / 2, ymid, ymid - 2.0)
y_hdr = ymid - 2.0 - 5.4
RC, RE = "#E4EFE7", "#6E9A7B"                      # response branch: muted green
box(XL0, y_hdr, CW, 5.4, "A  Detection, drivers and source sensitivity", "#C9D6E2", FC, fs=5.6, bold=True)
box(XR0, y_hdr, CW, 5.4, "B  Land–water responses", "#CFE3D5", RE, fs=5.9, bold=True)

BH = 6.4
BOT = 8.0                                            # bottom of workflow = bottom edge of the map frame
y_top = y_hdr - 2.6
PITCH = (y_top - BOT - BH) / 7.0                     # eight left-column boxes span exactly from y_top to the map-frame bottom
left = ["CHIRPS + ERA5-Land + GLDAS:\ndaily hydroclimate backbone", "73-pentad processing",
        "GLDAS soil-moisture percentile detection", "39-event regional flash-drought catalogue",
        "Driver characterization:\nprecipitation, PE, VPD, temperature",
        "ERA5-Land source / record-length sensitivity\n(OVERLAP26, LONG45)",
        "Chronology agreement and\nyear-shift (seasonal-coincidence) benchmark",
        "Consensus-event sensitivity\n(events matched within \u00b12 pentads)"]
ys = []
for i, t in enumerate(left):
    yb = y_top - BH - i * PITCH; ys.append(yb)
    box(XL0, yb, CW, BH, t, HC, FC, bold=(i == 3))
    arrow(XL0 + CW / 2, y_hdr if i == 0 else ys[i - 1], yb + BH)
right = ["Native-time responses: MOD16 \u00b7 MOD13 \u00b7\nGRACE TWSA \u00b7 JRC (seasonal z-scores)", "Response depth, lag to minimum, recovery",
         "Association tests: Spearman + permutation,\nBH within 5 families (46 tests)", "Seasonal-control audit:\nselection reference, pre-event control",
         "Independent reproduction of tests\nfrom the event-level table"]
yr = []
for j, t in enumerate(right):
    yb = ys[3] - j * PITCH; yr.append(yb)
    box(XR0, yb, CW, BH, t, RC, RE)
    if j > 0: arrow(XR0 + CW / 2, yr[j - 1], yb + BH)
# catalogue -> responses (events are the unit of analysis)
axb.annotate("", xy=(XR0, ys[3] + BH / 2), xytext=(XL0 + CW, ys[3] + BH / 2),
             arrowprops=dict(arrowstyle="-|>", color="#555555", lw=0.8, mutation_scale=5, shrinkA=0, shrinkB=0), zorder=1)
# driver anomalies -> association tests (dashed)
axb.annotate("", xy=(XR0, yr[2] + BH / 2), xytext=(XL0 + CW, ys[4] + BH / 2),
             arrowprops=dict(arrowstyle="-|>", color=FC, lw=0.7, ls=(0, (3, 2)), mutation_scale=5, shrinkA=0, shrinkB=0), zorder=1)
fig.text((BX0 - 2.5) / W_MM, 117.5 / H_MM, "b", fontsize=10, fontweight="bold", ha="left", va="top")

# ------------------------------------------------------------------ save
png = os.path.join(OUT, args.stem + ".png"); svg = os.path.join(OUT, args.stem + ".svg")
buf = io.BytesIO(); fig.savefig(buf, format="png", dpi=600); buf.seek(0)
Image.open(buf).convert("RGB").save(png, dpi=(600, 600), optimize=True)
fig.savefig(svg, format="svg", metadata={"Date": None, "Creator": "make_AEZ26_Fig1_v05.py"})
fig.savefig(os.path.join(OUT, args.stem + ".pdf"), format="pdf", metadata={"Creator": "make_AEZ26_Fig1_v05.py", "CreationDate": None})
chk = Image.open(png)
print("PNG", chk.size, chk.mode, chk.info.get("dpi"))
print("sources: data/AEZ26_HBT_boundary_recovered.geojson | data/BGD_locator_outline_recovered_simplified.json")
print("versions: python", sys.version.split()[0], "| matplotlib", matplotlib.__version__, "| numpy", np.__version__, "| Pillow", Image.__version__)
