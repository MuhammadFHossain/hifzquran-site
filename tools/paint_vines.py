#!/usr/bin/env python3
"""Paints the vines that grow across the site's pages, with the app's own
illumination engine, and the maps that let site.js grow them in as the app
grows its paintings.

The engine is the one the store kit paints with (`Icon/illum` on the app's
feature/illuminated-store branch, `~/hifz-wt-store-illum`). It is only read
from here, never changed. Its scroll records when every stem point and every
blossom grows; the engine's own copy has no step that turns that into a
picture, so this file does: each painted pixel takes the time of the nearest
point of its stem, and a blossom opens from its middle once its stem reaches
it. Gold and lapis come from the painter's own record of what it laid.

    PYTHONDONTWRITEBYTECODE=1 python3 tools/paint_vines.py

Writes assets/art/vine-a, -b and -c (.webp, -time.png, -mat.png): bands of
gold stems with lapis, red and white blossoms on no ground, grown from the
middle out to both ends and mirrored, as an illuminator turns a stencil over.
Three, each from its own seed and its own breath of trunk, so the page never
repeats one stamp.
"""
import math, os, random, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.spatial import cKDTree
from shapely.geometry import box

ENGINE = os.path.expanduser("~/hifz-wt-store-illum/Icon/illum")
sys.path.insert(0, ENGINE)
sys.dont_write_bytecode = True
from engine import bez                              # noqa: E402
from illum import Page                              # noqa: E402
from tezhip import (SpiralField, GOLD, LAPIS, RED, WHITE, GREEN)  # noqa: E402

SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "art"))

W, H = 200.0, 26.0           # units; the band is drawn 1600pt wide on the page, 8pt a unit
PX = 2400                    # 1.5x, enough for a painting that sits behind nothing
CX, CY = W / 2, H / 2
VINES = {"a": (11, 7.5), "b": (23, 6.0), "c": (37, 8.5)}   # seed, the trunk's rise


def paint(seed=11, rise=7.5):
    rnd = random.Random(seed)
    half = box(0.6, 0.8, CX - 0.2, H - 0.8)
    F = SpiralField(half, rnd, keep=0.36, scale=1.0)
    # one trunk from the middle to the left end, rising and falling like a
    # breath; the right half is its mirror image
    pts = bez((CX - 0.2, CY), (CX - 14, CY - rise), (CX - 30, CY - rise), (CX - 44, CY), 40)
    pts += bez(pts[-1], (CX - 58, CY + rise), (CX - 72, CY + rise), (CX - 86, CY), 40)[1:]
    pts += bez(pts[-1], (CX - 92, CY - 3.5), (CX - 96, CY - 4.5), (CX - 98.5, CY - 3.0), 16)[1:]
    F.add_stem(pts, 0.42, 0.0)
    cols = {"hatayi": (LAPIS, RED, WHITE), "penc": (RED, WHITE, LAPIS), "rumi": GOLD, "leaf": GREEN}
    F.grow(n=7, min_r=3.0, max_r=5.0, cols=cols, w=0.36)
    F.grow(n=26, min_r=1.5, max_r=2.8, cols=cols, w=0.28)
    F.halkar(n=180, min_r=0.5)
    F.mirror(CX)

    P = Page(W, H, PX, seed=seed, ss=1)
    stem0 = F.stem_geom(0)
    P.gold(stem0, outline=False)
    P.line(stem0.boundary.buffer(0.05))
    for c in F.colours(0):
        g = F.fills(0, c)
        if c == GOLD:
            P.gold(g, outline=False)
        else:
            P.colour(g, c)
    P.line(F.outlines(0, 0.085))
    P.gold(F.stem_geom(1), outline=False)
    P.gold(F.fills(1, GOLD), outline=False)
    return F, P


def time_map(F, P):
    """When each painted pixel appears: the time of the nearest point of its
    stem; inside a blossom, the blossom's own time and a little more towards
    its rim, so it opens from the middle. Worked out on the left half, where
    the scroll was grown, and turned over for the right, as the painting was."""
    h, w = P.alpha.shape
    half = w // 2
    ys, xs = np.mgrid[0:h, 0:half]
    ux = (xs + 0.5) / w * W
    uy = (ys + 0.5) / h * H
    left = [p for p in F.points if p[0] <= CX + 0.01]
    pts = np.array([(p[0], p[1]) for p in left])
    tms = np.array([p[4] for p in left])
    painted = P.alpha[:, :half] > 0.01
    T = np.zeros((h, half), np.float32)
    _, idx = cKDTree(pts).query(np.c_[ux[painted], uy[painted]])
    T[painted] = tms[idx]
    for m in sorted(F.motifs, key=lambda m: m["t"]):
        if m["x"] > CX:
            continue
        mk = (P.mask(m["u"].buffer(0.12)) > 0.3)[:, :half]
        if not mk.any():
            continue
        d = np.hypot(ux[mk] - m["x"], uy[mk] - m["y"]) / max(m["r"], 0.3)
        T[mk] = m["t"] + 0.6 * np.clip(d, 0, 1.5)
    t0, t1 = T[painted].min(), T[painted].max()
    out = np.zeros((h, half), np.float32)
    out[painted] = 0.02 + 0.96 * (T[painted] - t0) / max(t1 - t0, 1e-6)
    # each time spreads a few pixels past its shape, so a soft edge never
    # shows before the stroke it belongs to
    out = ndi.grey_dilation(out, size=(5, 5))
    full = np.hstack([out, out[:, ::-1]]) if w % 2 == 0 else np.hstack([out, out[:, -1:], out[:, ::-1]])
    return Image.fromarray((full * 255).round().astype(np.uint8), "L")


if __name__ == "__main__":
    for name, (seed, rise) in VINES.items():
        F, P = paint(seed, rise)
        a = np.clip(P.alpha, 0, 1)
        rgb = np.clip(P.img, 0, 1) * (a[..., None] > 0.003)       # nothing kept under the clear
        im = Image.fromarray(np.dstack([(rgb * 255).astype(np.uint8), (a * 255).astype(np.uint8)]), "RGBA")
        im.save(f"{SITE}/vine-{name}.webp", quality=75, method=6, alpha_quality=80)
        t = time_map(F, P)
        t.resize((t.width // 2, t.height // 2), Image.BOX).save(f"{SITE}/vine-{name}-time.png", optimize=True)
        mat = np.dstack([P.goldm, P.lapism, np.zeros_like(P.goldm)])
        mat = Image.fromarray((np.clip(mat, 0, 1) * 255).astype(np.uint8), "RGB")
        # the light only needs to know roughly where the gold is: a quarter is enough
        mat.resize((mat.width // 4, mat.height // 4), Image.LANCZOS).save(f"{SITE}/vine-{name}-mat.png", optimize=True)
        for n in (f"vine-{name}.webp", f"vine-{name}-time.png", f"vine-{name}-mat.png"):
            print(f"art/{n} {os.path.getsize(f'{SITE}/{n}') // 1024} KB")
