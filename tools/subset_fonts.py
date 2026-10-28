#!/usr/bin/env python3
"""Makes the site's Fraunces from the full fonts in tools/fonts.

Fraunces is OFL, which allows this. The site needs Latin only, weights 400 to
700, and no SOFT axis, so each face is cut down to that and saved as WOFF:
about 190 KB for both instead of 757 KB. The optical size axis stays, so the
headings still draw with their display cut.

The KFGQPC Uthmanic Hafs font is never cut down or converted: its terms allow
using and sharing it, not changing it. The site loads it only when the footer's
ayah comes near (assets/site.js).

    python3 tools/subset_fonts.py
"""
import glob, html, os, tempfile
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools import subset

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
text = "".join(html.unescape(open(p, encoding="utf-8").read()) for p in glob.glob(f"{ROOT}/*.html"))
uni = set(range(0x20, 0x7F)) | set(range(0xA0, 0x180))
uni |= {0x2018, 0x2019, 0x201C, 0x201D, 0x2013, 0x2026, 0x00B7, 0x2022, 0x2039, 0x203A, 0x2122, 0x00A9}
uni |= {ord(c) for c in set(text) if ord(c) < 0x2100 and not 0x0590 <= ord(c) <= 0x08FF}

for name in ("Fraunces-VF", "Fraunces-Italic-VF"):
    font = TTFont(f"{ROOT}/tools/fonts/{name}.ttf", lazy=False)
    font = instancer.instantiateVariableFont(font, {"SOFT": 0, "wght": (400, 700)})
    with tempfile.TemporaryDirectory() as tmp:
        font.save(f"{tmp}/i.ttf")
        font = TTFont(f"{tmp}/i.ttf", lazy=False)
    opts = subset.Options()
    opts.layout_features = ["*"]; opts.name_IDs = ["*"]; opts.notdef_outline = True; opts.flavor = "woff"
    sub = subset.Subsetter(opts); sub.populate(unicodes=uni); sub.subset(font)
    out = f"{ROOT}/assets/fonts/{name}.woff"
    font.flavor = "woff"; font.save(out)
    print(f"assets/fonts/{name}.woff {os.path.getsize(out) // 1024} KB")
