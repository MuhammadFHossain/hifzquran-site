#!/usr/bin/env python3
"""Exports the app's own pictures into the site.

Skies: the evening photograph, the one sky the site still shows (by day the
ground is paper, and the other dark hours are drawn), once sharp for the hero
and once blurred back to a ground, the way MushafGround draws it. Screens: the 3.0 shots at 2x for a 330pt phone, and the iPad's
two-page spread at 1920 wide. Icons: the rosette, cut from the app icon.

    python3 tools/export_assets.py [skies] [screens] [icons]

With no names it exports all three. After a reshoot, `screens` is enough.
"""
import os, sys
from PIL import Image, ImageFilter, ImageOps

# 3.0 lives on feature/ui-polish. Its shots are where AppStore/shoot.sh writes
# them: the phone's in shots/, the iPad's in shots/ipad/.
WT = os.path.expanduser("~/hifz-wt-polish")
SHOTS = f"{WT}/AppStore/shots"
CAT = f"{WT}/HifzQuran/Assets.xcassets"
# 3.0 no longer ships the sky photographs, so the skies still come from the
# worktree that had them.
SKY_CAT = os.path.expanduser("~/hifz-wt-sky/HifzQuran/Assets.xcassets")
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SITE = os.path.normpath(SITE)
PARTS = set(sys.argv[1:]) or {"skies", "screens", "icons"}

os.makedirs(f"{SITE}/sky", exist_ok=True)
os.makedirs(f"{SITE}/shots", exist_ok=True)
os.makedirs(f"{SITE}/img", exist_ok=True)

def save_jpg(im, path, q=84):
    im.convert("RGB").save(path, quality=q, optimize=True, progressive=True, subsampling=1)
    print(f"  {os.path.relpath(path, SITE):40s} {os.path.getsize(path)//1024:5d} KB  {im.size}")

def save_pair(im, base, q=85):
    im = im.convert("RGB")
    im.save(base + ".webp", quality=q, method=6)
    im.save(base + ".png", optimize=True)
    print(f"  {os.path.relpath(base, SITE):40s} webp {os.path.getsize(base+'.webp')//1024:4d} KB  png {os.path.getsize(base+'.png')//1024:4d} KB  {im.size}")

# ---- skies ---------------------------------------------------------------
frames = {"evening": "SkyEvening"}
if "skies" in PARTS:
    print("skies")
for name, asset in (frames.items() if "skies" in PARTS else ()):
    im = Image.open(f"{SKY_CAT}/{asset}.imageset/{asset}@2x.jpg").convert("RGB")
    # The hero: sharp, with the JPEG grain taken off so a 2.7x upscale reads as
    # atmosphere rather than as blocks.
    save_jpg(im.filter(ImageFilter.GaussianBlur(1.2)), f"{SITE}/sky/{name}.jpg", 86)
    # The ground: blurred until only its light and its texture survive. 3.5% of
    # the width, which is the app's 14pt on a 402pt phone.
    r = im.width * 0.035
    big = ImageOps.fit(im, (im.width, im.height))
    # Scale past the frame after blurring, or the blur pulls a pale rim in at
    # the edges (MushafGround does the same with scaleEffect 1.16).
    pad = int(im.width * 0.08)
    padded = ImageOps.expand(im, border=pad, fill=None)
    # mirror-pad so the blur has neighbours at the edge
    padded = Image.new("RGB", (im.width + 2*pad, im.height + 2*pad))
    padded.paste(im, (pad, pad))
    padded.paste(ImageOps.mirror(im).crop((im.width-pad, 0, im.width, im.height)), (0, pad))
    padded.paste(ImageOps.mirror(im).crop((0, 0, pad, im.height)), (pad+im.width, pad))
    top = padded.crop((0, pad, padded.width, 2*pad)); padded.paste(ImageOps.flip(top), (0, 0))
    bot = padded.crop((0, padded.height-2*pad, padded.width, padded.height-pad)); padded.paste(ImageOps.flip(bot), (0, padded.height-pad))
    ground = padded.filter(ImageFilter.GaussianBlur(r)).crop((pad, pad, pad+im.width, pad+im.height))
    save_jpg(ground, f"{SITE}/sky/{name}-ground.jpg", 80)

# ---- screens -------------------------------------------------------------
screens = {"01_quran": "quran-day", "12_night": "quran-night", "01_mushaf": "mushaf",
           "02_repeat": "repeat", "05_tajweed": "tajweed",
           "06_salah": "salah", "08_dua": "dua",
           "04_indopak": "indopak", "09_widgets": "widgets"}
if "screens" in PARTS:
    print("screens (2x for a 330pt phone)")
    W = 660
    for src, dst in screens.items():
        im = Image.open(f"{SHOTS}/{src}.png").convert("RGB")
        h = round(im.height * W / im.width)
        save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/{dst}")
    # The iPad on its side, two pages open: 2x for the 960pt column it fills.
    print("ipad (2x for a 960pt column)")
    W = 1920
    im = Image.open(f"{SHOTS}/ipad/pad_spread.png").convert("RGB")
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/ipad-spread")

# ---- icons ---------------------------------------------------------------
if "icons" not in PARTS:
    sys.exit(0)
print("icons")
icon = Image.open(f"{CAT}/AppIcon.appiconset/icon-1024.png").convert("RGBA")
for size, name in ((512, "app-icon.png"), (180, "apple-touch-icon.png"), (64, "favicon-64.png"), (32, "favicon-32.png")):
    out = icon.resize((size, size), Image.LANCZOS)
    out.save(f"{SITE}/img/{name}", optimize=True)
    print(f"  img/{name:22s} {os.path.getsize(f'{SITE}/img/{name}')//1024:4d} KB")

# The rosette alone, in one gold, so it reads on paper and on ink alike. The
# icon's own mark has a cream word inside a gold ring, and cream is invisible
# on paper.
ring = Image.open(f"{WT}/HifzQuran/AppIcon.icon/Assets/iqraring.png").convert("RGBA")
alpha = ring.getchannel("A")
gold = Image.new("RGBA", ring.size, (0xC4, 0x9F, 0x4E, 255))
gold.putalpha(alpha)
bbox = alpha.getbbox()
gold = gold.crop(bbox)
side = max(gold.size) + 24
sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
sq.paste(gold, ((side - gold.width)//2, (side - gold.height)//2))
sq.resize((512, 512), Image.LANCZOS).save(f"{SITE}/img/mark.png", optimize=True)
print(f"  img/mark.png {os.path.getsize(f'{SITE}/img/mark.png')//1024} KB")
