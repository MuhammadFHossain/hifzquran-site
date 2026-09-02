#!/usr/bin/env python3
"""Exports the app's own pictures into the site.

Skies: the three photographs the app grades into five daylight windows, once
sharp for the hero and once blurred back to a ground, the way MushafGround
draws them. Screens: today's shots at 2x for a 330pt phone. Crops: the five
details the feature cards show. Icons: the rosette, cut from the app icon.
"""
import os, sys
from PIL import Image, ImageFilter, ImageOps

WT = "/Users/farhanhossain/hifz-wt-sky"
SITE = "/Users/farhanhossain/Desktop/Side Projects/App Projects/hifzquran-site/assets"
SHOTS = f"{WT}/AppStore/shots"
CAT = f"{WT}/HifzQuran/Assets.xcassets"

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
print("skies")
frames = {"morning": "SkyMorning", "golden": "SkyGoldenHour", "evening": "SkyEvening"}
for name, asset in frames.items():
    im = Image.open(f"{CAT}/{asset}.imageset/{asset}@2x.jpg").convert("RGB")
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
print("screens (2x for a 330pt phone)")
screens = {"01_quran": "quran-day", "12_night": "quran-night", "01_mushaf": "mushaf",
           "02_repeat": "repeat", "05_tajweed": "tajweed",
           "06_salah": "salah", "08_dua": "dua"}
W = 660
for src, dst in screens.items():
    im = Image.open(f"{SHOTS}/{src}.png").convert("RGB")
    h = round(im.height * W / im.width)
    save_pair(im.resize((W, h), Image.LANCZOS), f"{SITE}/shots/{dst}")

# ---- icons ---------------------------------------------------------------
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
