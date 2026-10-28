#!/usr/bin/env python3
"""Exports the app's own pictures into the site, for 4.0, the illuminated release.

Screens: the 4.0 shots at 2x for a 330pt phone, as WebP with a JPEG behind it.
Art: the app's paintings with the maps that grow them in and light their gold
(the shamsa, the crown, twelve surah paintings), the ground's rosettes and
paper grain, and two pieces cut from the
store banner: its painted border, as a nine-slice for CSS border-image, and
the gold rule with a rosette under its caption. Icons: icon A, the gilded
night, and its mark.

    python3 tools/export_assets.py [screens] [art] [icons] [wide]

With no names it exports screens, art and icons. After a reshoot, `screens`
is enough. `wide` makes the open iPhone Duo and the pen on an iPad
(shots/duo-spread, shots/pen); it waits for the 4.0 iPad and Duo shots, and
until then the site shows the 3.2 pictures there (README, Going live).
"""
import os, sys
import numpy as np
from PIL import Image

# The store kit: the raw 4.0 shots and the banner (feature/illuminated-store).
STORE = os.path.expanduser("~/hifz-wt-store-illum")
SHOTS = f"{STORE}/AppStore/shots"
BANNER = f"{STORE}/AppStore/creative/illuminated/e_repeat-universal-5244x2950.png"
ICON = f"{STORE}/Icon/out-illum/a"
# The paintings, as the app ships them (feature/illuminated).
ART = os.path.expanduser("~/hifz-wt-illuminated/HifzQuran/Resources/Illumination")
SURAHS = os.path.expanduser("~/hifz-wt-illuminated/HifzQuran/Resources/surahs.json")
SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets"))
PARTS = set(sys.argv[1:]) or {"screens", "art", "icons"}
# The open iPhone Duo's screen outline, from the simulator's device profile,
# and the 4.0 wide shots the store kit is to make: the open Duo's first two
# pages, and a page on the iPad with the pen out.
DUO_MASK = "/Library/Developer/CoreSimulator/Profiles/DeviceTypes/iPhone Duo.simdevicetype/Contents/Resources/BF0DC480-5EE2-4EC1-B02B-C75E94759832.pdf"
DUO = f"{SHOTS}/duo-inner/pad_indopak.png"   # the Mughal Indopak opening, the 4.0 Duo set's spread
PEN = f"{SHOTS}/ipad/pad_pen.png"

for d in ("shots", "art", "img"):
    os.makedirs(f"{SITE}/{d}", exist_ok=True)

def kb(path):
    return os.path.getsize(path) // 1024

def save_webp(im, path, q=82, lossless=False):
    im.save(path, quality=q, method=6, lossless=lossless)
    print(f"  {os.path.relpath(path, SITE):34s} {kb(path):4d} KB  {im.size}")

def save_png(im, path):
    im.save(path, optimize=True)
    print(f"  {os.path.relpath(path, SITE):34s} {kb(path):4d} KB  {im.size}")

def fit_width(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)

# ---- screens -------------------------------------------------------------
# Raw shots from AppStore/shoot.sh on the store kit, 1320 x 2868. The 4.0 set
# was shot from 4.0 (36). Indopak is the pre-Mughal page until the reshoot.
SCREENS = {
    "01_quran": "quran-day", "12_night": "quran-night",
    "14_opening": "fatihah", "15_opening2": "baqarah",
    "01_mushaf": "mushaf", "02_repeat": "repeat",
    "06_salah": "salah", "07_qibla": "qibla", "08_dua": "dua",
    "04_indopak": "indopak",
}
# 15_opening2 (Al-Baqarah) was shot from 4.0 (36) and is still the store kit's.
if "screens" in PARTS:
    print("screens (2x for a 330pt phone)")
    for src, dst in SCREENS.items():
        im = fit_width(Image.open(f"{SHOTS}/{src}.png").convert("RGB"), 660)
        save_webp(im, f"{SITE}/shots/{dst}.webp", 80)
        im.save(f"{SITE}/shots/{dst}.jpg", quality=80, optimize=True, progressive=True)
        print(f"  {'shots/' + dst + '.jpg':34s} {kb(f'{SITE}/shots/{dst}.jpg'):4d} KB")

# ---- wide: iPhone Duo and the pen ------------------------------------------
if "wide" in PARTS:
    import subprocess, tempfile
    print("duo (2x for a 960pt column, cut to the screen's own corners)")
    im = Image.open(DUO).convert("RGBA")
    # The outline is drawn upright; the open phone lies on its side. Its four
    # corners are the same, so either quarter turn fits.
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["sips", "-s", "format", "png", DUO_MASK, "--out", f"{tmp}/mask.png"],
                       check=True, capture_output=True)
        mask = Image.open(f"{tmp}/mask.png").getchannel("A")
    im.putalpha(mask.resize((im.height, im.width), Image.LANCZOS).rotate(90, expand=True))
    im = fit_width(im, 1920)
    # WebP only: a PNG of this, for browsers without WebP, would be 2.4 MB
    save_webp(im, f"{SITE}/shots/duo-spread.webp", 82)
    if os.path.exists(PEN):
        print("pen (2x for a 380pt column)")
        im = fit_width(Image.open(PEN).convert("RGB"), 760)
        save_webp(im, f"{SITE}/shots/pen.webp", 82)
        im.save(f"{SITE}/shots/pen.png", optimize=True)
    else:
        print(f"  no pen shot yet at {PEN}: shots/pen stays as it is")

# ---- art -----------------------------------------------------------------
PAPER = np.array([249, 245, 235], float)   # the banner's paper

def key_paper(rgb, keep=None, reach=34.0):
    """The banner's paper taken out, as the app's illumKeyPaper does: what is
    near the paper's colour goes clear, softly, and the paper's tint is taken
    back out of the soft edges so nothing carries a pale rim. `keep` is a mask
    of pixels kept whole (the band's white blossoms are near the paper's
    colour, and must stay)."""
    a = np.asarray(rgb, float)
    d = np.sqrt(((a - PAPER) ** 2).sum(2))
    alpha = np.clip((d - reach * 0.5) / (reach * 0.5), 0, 1)
    alpha = alpha * alpha * (3 - 2 * alpha)
    if keep is not None:
        alpha = np.maximum(alpha, keep)
    safe = np.maximum(alpha, 1e-3)[..., None]
    col = np.clip((a - (1 - alpha[..., None]) * PAPER) / safe, 0, 255)
    out = np.dstack([col, alpha * 255]).round().astype(np.uint8)
    return Image.fromarray(out, "RGBA")

def frame_nine_slice(banner):
    """The banner's border as a nine-slice: its top-left corner (the rays, the
    lapis rule, the tooled gold, the lapis band of blossoms and the corner
    rosette) and four periods of the band on each side, mirrored into the
    other three corners. Measured on the 5244 x 2950 banner: the outer lapis
    rule at y 403 and x 461, the rays 70 beyond it, the corner square to 534 /
    592, a blossom and a red point every 114.67 along the band."""
    T, P4 = 201, 459                    # slice thickness, four periods of the band
    y0, x0 = 333, 391                   # the corner's top-left, rays included
    corner = banner.crop((x0, y0, x0 + T, y0 + T))
    top = banner.crop((x0 + T, y0, x0 + T + P4, y0 + T))
    left = banner.crop((x0, y0 + T, x0 + T, y0 + T + P4))
    S = T + P4 + T
    sheet = Image.new("RGB", (S, S), tuple(int(v) for v in PAPER))
    sheet.paste(corner, (0, 0))
    sheet.paste(top, (T, 0))
    sheet.paste(left, (0, T))
    sheet.paste(corner.transpose(Image.FLIP_LEFT_RIGHT), (T + P4, 0))
    sheet.paste(left.transpose(Image.FLIP_LEFT_RIGHT), (T + P4, T))
    sheet.paste(corner.transpose(Image.FLIP_TOP_BOTTOM), (0, T + P4))
    sheet.paste(top.transpose(Image.FLIP_TOP_BOTTOM), (T, T + P4))
    sheet.paste(corner.transpose(Image.ROTATE_180), (T + P4, T + P4))
    # Kept whole: the band itself, from the outer lapis rule (70 in) to the
    # inner gold rule (70 + 116), which holds the white blossoms. The corner
    # squares' gold reaches a little further in and keys out by itself.
    keep = np.zeros((S, S))
    b0, b1 = 70, 70 + 117
    for lo, hi in ((b0, b1), (S - b1, S - b0)):
        keep[lo:hi, b0:S - b0] = 1
        keep[b0:S - b0, lo:hi] = 1
    return key_paper(sheet, keep)

def divider(banner):
    """The gold rule under the banner's caption: a lobed rosette of lapis and
    white on gold, a rule on each side, a gold point at each end."""
    cx, cy = 2022, 1805
    im = banner.crop((1480, cy - 90, 2565, cy + 90))
    ys, xs = np.mgrid[0:im.height, 0:im.width]
    r2 = (xs - (cx - 1480)) ** 2 + (ys - 90) ** 2
    keep = (r2 < 52 ** 2).astype(float)
    out = key_paper(im, keep)
    # only the rosette and its rule: the vine's leaf tips below are not part of it
    a = np.asarray(out).copy()
    a[..., 3] = np.where((r2 < 84 ** 2) | (np.abs(ys - 90) < 14), a[..., 3], 0)
    out = Image.fromarray(a, "RGBA")
    return out.crop(out.getbbox())

def ground_tile(ink, line_alpha, fill_alpha):
    """GroundPattern.swift as an SVG tile: eight-petalled rosettes in
    eight-pointed stars at the corners, a small flower in the middle, a
    hairline lattice between, all tone on tone. 88pt, as in the app."""
    import math
    def f(v): return f"{v:.2f}".rstrip("0").rstrip(".")
    def petal(cx, cy, ang, length, width):
        ux, uy = math.cos(ang), math.sin(ang)
        tx, ty = cx + ux * length, cy + uy * length
        mx, my = cx + ux * length * .5, cy + uy * length * .5
        px, py = -uy * width, ux * width
        return f"M{f(cx)} {f(cy)}Q{f(mx+px)} {f(my+py)} {f(tx)} {f(ty)}Q{f(mx-px)} {f(my-py)} {f(cx)} {f(cy)}Z"
    t = 88.0; star = t * .22; flower = t * .10; gap = t * .035
    lines, fills, seeds = [], [], []
    c = (t / 2, t / 2)
    for (x, y) in [(0, 0), (t, 0), (0, t), (t, t)]:
        dx, dy = c[0] - x, c[1] - y; L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
        lines.append(f"M{f(x+ux*(star+gap))} {f(y+uy*(star+gap))}L{f(c[0]-ux*(flower+gap))} {f(c[1]-uy*(flower+gap))}")
        for turn in (0, math.pi / 4):
            pts = [(x + star * math.cos(turn + k * math.pi / 2), y + star * math.sin(turn + k * math.pi / 2)) for k in range(4)]
            lines.append("M" + "L".join(f"{f(a)} {f(b)}" for a, b in pts) + "Z")
        for k in range(8):
            fills.append(petal(x, y, k * math.pi / 4 + math.pi / 8, star * .62, star * .17))
        seeds.append((x, y, star * .11))
    for k in range(8):
        long = k % 2 == 0
        fills.append(petal(c[0], c[1], k * math.pi / 4 + math.pi / 4, flower if long else flower * .55, flower * .26 if long else flower * .18))
    seeds.append((c[0], c[1], flower * .16))
    return (f"<svg xmlns='http://www.w3.org/2000/svg' width='88' height='88'>"
            f"<g fill='none' stroke='{ink}' stroke-opacity='{line_alpha}' stroke-width='.6'><path d='{''.join(lines)}'/></g>"
            f"<path d='{''.join(fills)}' fill='{ink}' fill-opacity='{fill_alpha}' stroke='{ink}' stroke-opacity='{line_alpha}' stroke-width='.5'/>"
            f"<g fill='{ink}' fill-opacity='{line_alpha}'>" + "".join(f"<circle cx='{f(x)}' cy='{f(y)}' r='{f(r)}'/>" for x, y, r in seeds) + "</g></svg>")

TILES = [1, 2, 18, 19, 36, 55, 67, 97, 103, 106, 112, 114]

if "art" in PARTS:
    print("art")
    a = f"{SITE}/art"
    # The ground: the rosettes in the paper's beige by day, in cream on the
    # lapis night (GroundPattern's dayInk and nightInk and their strengths),
    # and the burnished paper's grain (PaperGrainTexture).
    for name, ink, la, fa in (("day", "#9A8462", .06, .032), ("night", "#FBF5E6", .032, .018)):
        open(f"{a}/ground-{name}.svg", "w").write(ground_tile(ink, la, fa))
        print(f"  art/ground-{name}.svg {kb(f'{a}/ground-{name}.svg'):4d} KB")
    save_webp(Image.open(f"{ART}/il_paper_grain.png").convert("RGB"), f"{a}/grain.webp", 90)
    # The shamsa, with its ground, its clock and its gold and lapis.
    save_webp(Image.open(f"{ART}/il_shamsa.png").convert("RGBA"), f"{a}/shamsa.webp", 84)
    save_webp(Image.open(f"{ART}/il_shamsa_base.png").convert("RGBA"), f"{a}/shamsa-base.webp", 80)
    save_png(Image.open(f"{ART}/il_shamsa_time.png").convert("L"), f"{a}/shamsa-time.png")
    save_png(Image.open(f"{ART}/il_shamsa_mat.png").convert("RGB"), f"{a}/shamsa-mat.png")
    # The crown over a heading, which has no clock: it is there at once.
    save_webp(Image.open(f"{ART}/il_crown_rays.png").convert("RGBA"), f"{a}/crown.webp", 86)
    save_png(Image.open(f"{ART}/il_crown_rays_mat.png").convert("RGB"), f"{a}/crown-mat.png")
    # Twelve surahs, at 2x for a 240pt tile.
    for n in TILES:
        im = fit_width(Image.open(f"{ART}/il_tile_{n:03d}.jpg").convert("RGB"), 480)
        save_webp(im, f"{a}/tile-{n:03d}.webp", 80)
        save_png(Image.open(f"{ART}/il_tile_{n:03d}_mat.png").convert("RGB"), f"{a}/tile-{n:03d}-mat.png")
    # The banner's border and its rule, at 0.56 of the banner: the band is
    # 56pt deep at 2x.
    banner = Image.open(BANNER).convert("RGB")
    fr = frame_nine_slice(banner)
    fr = fr.resize((round(fr.width * 0.56), round(fr.height * 0.56)), Image.LANCZOS)
    save_webp(fr, f"{a}/frame.webp", 86)
    dv = divider(banner)
    dv = dv.resize((round(dv.width * 0.5), round(dv.height * 0.5)), Image.LANCZOS)
    save_webp(dv, f"{a}/rule.webp", 88)
    print(f"  frame slice: {round(201 * 0.56)} px of {fr.width}")

# ---- icons ---------------------------------------------------------------
if "icons" in PARTS:
    print("icons (icon A, the gilded night)")
    icon = Image.open(f"{ICON}/icon-1024.png").convert("RGB")
    for size, name in ((512, "app-icon.png"), (180, "apple-touch-icon.png"), (64, "favicon-64.png"), (32, "favicon-32.png")):
        save_png(icon.resize((size, size), Image.LANCZOS), f"{SITE}/img/{name}")
    save_webp(icon.resize((192, 192), Image.LANCZOS), f"{SITE}/img/app-icon.webp", 86)
    # The mark alone (the ring, the wings and Iqra, on no ground), for the
    # wordmark: it reads on paper and on the lapis night alike.
    mark = Image.open(f"{ICON}/mark.png").convert("RGBA")
    mark = mark.crop(mark.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox())
    side = max(mark.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
    save_png(sq.resize((128, 128), Image.LANCZOS), f"{SITE}/img/mark.png")
    save_webp(sq.resize((128, 128), Image.LANCZOS), f"{SITE}/img/mark.webp", 88)
