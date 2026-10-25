#!/usr/bin/env python3
"""Exports the app's own pictures into the site.

Skies: the evening photograph, the one sky the site still shows (by day the
ground is paper, and the other dark hours are drawn), once sharp for the hero
and once blurred back to a ground, the way MushafGround draws it. Screens: the 3.0 shots at 2x for a 330pt phone, and the iPad's
two-page spread at 1920 wide. Wide: the open iPhone Duo cut to its own round
screen, and the pen on an iPad. Icons: the rosette, cut from the app icon.

    python3 tools/export_assets.py [skies] [screens] [wide] [icons]

With no names it exports all three. After a reshoot, `screens` is enough.
"""
import os, sys
from PIL import Image, ImageFilter, ImageOps

# The app's main branch, checked out in ~/hifz-wt-merge. Its shots are where
# AppStore/shoot.sh writes them: the phone's in shots/, the iPad's in
# shots/ipad/, the open iPhone Duo's in shots/duo-inner/.
WT = os.path.expanduser("~/hifz-wt-merge")
SHOTS = f"{WT}/AppStore/shots"
CAT = f"{WT}/HifzQuran/Assets.xcassets"
# 3.0 no longer ships the sky photographs, so the skies still come from the
# worktree that had them.
SKY_CAT = os.path.expanduser("~/hifz-wt-sky/HifzQuran/Assets.xcassets")
SITE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
SITE = os.path.normpath(SITE)
# The pen on an iPad, from the 3.2 review sheets (no store shot has writing).
PEN = os.path.expanduser("~/Desktop/Blue Tomato Studio/Hifz/Quran Pages 3.2 Duo preview/pen-and-saved-ui/ipad/02-pen-on-bar.png")
# The open iPhone Duo's screen outline, from the simulator's device profile.
DUO_MASK = "/Library/Developer/CoreSimulator/Profiles/DeviceTypes/iPhone Duo.simdevicetype/Contents/Resources/BF0DC480-5EE2-4EC1-B02B-C75E94759832.pdf"
PARTS = set(sys.argv[1:]) or {"skies", "screens", "wide", "icons"}
if "screens" in PARTS:
    PARTS.add("widgets")

os.makedirs(f"{SITE}/sky", exist_ok=True)
os.makedirs(f"{SITE}/shots", exist_ok=True)
os.makedirs(f"{SITE}/img", exist_ok=True)

def save_jpg(im, path, q=84):
    im.convert("RGB").save(path, quality=q, optimize=True, progressive=True, subsampling=1)
    print(f"  {os.path.relpath(path, SITE):40s} {os.path.getsize(path)//1024:5d} KB  {im.size}")

def save_pair(im, base, q=85):
    im = im.convert("RGBA" if im.mode == "RGBA" else "RGB")
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
           "04_indopak": "indopak"}

def clear_dock(im):
    """The simulator's Home Screen has an empty dock: a pale bar with no apps
    in it. It is iOS's, not the app's, so it goes: each row of it takes the
    night sky from the screen's two edges, blended across."""
    im = im.copy(); px = im.load(); W, H = im.size
    top, x0, x1 = round(H * 0.886), round(W * 0.015), round(W * 0.985)
    for y in range(top, H):
        left = [sum(px[x, y][c] for x in range(2, x0 - 2)) / (x0 - 4) for c in range(3)]
        right = [sum(px[x, y][c] for x in range(x1 + 2, W - 2)) / (W - x1 - 4) for c in range(3)]
        for x in range(x0, x1):
            t = (x - x0) / (x1 - x0)
            px[x, y] = tuple(round(left[c] * (1 - t) + right[c] * t) for c in range(3))
    return im

if "screens" in PARTS:
    print("screens (2x for a 330pt phone)")
    W = 660
    for src, dst in screens.items():
        im = Image.open(f"{SHOTS}/{src}.png").convert("RGB")
        h = round(im.height * W / im.width)
        save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/{dst}")
if "widgets" in PARTS:
    print("widgets (2x for a 330pt phone, the empty dock taken out)")
    W = 660
    im = clear_dock(Image.open(f"{SHOTS}/09_widgets.png").convert("RGB"))
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/widgets")
if "screens" in PARTS:
    # The iPad on its side, two pages open: 2x for the 960pt column it fills.
    print("ipad (2x for a 960pt column)")
    W = 1920
    im = Image.open(f"{SHOTS}/ipad/pad_spread.png").convert("RGB")
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/ipad-spread")

# ---- wide: iPhone Duo and the pen ------------------------------------------
if "wide" in PARTS:
    import subprocess, tempfile
    print("duo (2x for a 960pt column, cut to the screen's own corners)")
    W = 1920
    im = Image.open(f"{SHOTS}/duo-inner/pad_spread.png").convert("RGBA")
    # The outline is drawn upright; the open phone lies on its side. Its four
    # corners are the same, so either quarter turn fits.
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["sips", "-s", "format", "png", DUO_MASK, "--out", f"{tmp}/mask.png"],
                       check=True, capture_output=True)
        mask = Image.open(f"{tmp}/mask.png").getchannel("A")
    mask = mask.resize((im.height, im.width), Image.LANCZOS).rotate(90, expand=True)
    im.putalpha(mask)
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/duo-spread")
    print("pen (2x for a 380pt column)")
    W = 760
    im = Image.open(PEN).convert("RGB")
    # iPadOS draws a window's resize handle in the lower corner; it is not the
    # app's, so it goes, under the page's own warm white.
    from PIL import ImageDraw
    ImageDraw.Draw(im).rectangle((im.width - 96, im.height - 96, im.width, im.height), fill=im.getpixel((im.width - 120, im.height - 40)))
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/pen")

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
