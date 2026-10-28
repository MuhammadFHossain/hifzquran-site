#!/usr/bin/env python3
"""Checks the site before it goes live.

1. No price words and no ranking claims anywhere a visitor can read: free,
   price, cost, buy, ads, paid, purchase, subscription, discount, best, #1,
   top rated. The legal pages keep a few fixed phrases where the word is not
   about price (a warranty "free of errors", the indemnity's "legal costs",
   and the refund line Apple asks every developer's terms to carry); each is
   listed below, and nothing else passes.
2. No em dashes, and not the word "illuminated" (say "painted in gold and
   blue": the owner found nobody knows the word).
3. The Quran shown on the site is the app's own text: the footer's Al-Qamar
   54:17, letter for letter against ayahs.json, and its English against
   Saheeh International (tr_en-saheeh.json), both in the app.

    python3 tools/check_site.py

Exits 1 on any failure.
"""
import glob, html, json, os, re, sys

SITE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
APP = os.path.expanduser("~/hifz-wt-illuminated/HifzQuran/Resources")

WORDS = r"\b(free|freely|price[sd]?|pricing|cost|costs|buy|buying|(?<!-)ads?(?!-)|paid|purchases?|subscriptions?|discounts?|best|top[- ]rated)\b|#1\b"
# Fixed legal phrases, by page. The word in each is not a price claim.
ALLOWED = {
    "terms.html": [
        "free of errors",                                   # 10, the warranty disclaimer
        "any claim, loss or cost (including reasonable legal costs)",   # 12, the indemnity
        "Apple may refund the price you paid (if any)",     # 15, Apple's required terms
        "any other claim, loss or cost from such a failure",  # 15, Apple's required terms
        "the amount you paid us for the app",               # 11, the cap on liability
    ],
}

def visible(text):
    """Page text a visitor can read or a share card can show: everything but
    tags and comments, with attribute values kept (alt, content, aria-label)."""
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    text = re.sub(r"<script\b(?![^>]*ld\+json)[^>]*>.*?</script>", " ", text, flags=re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.S)
    attrs = " ".join(re.findall(r'(?:alt|content|aria-label|title)="([^"]*)"', text))
    body = re.sub(r"<[^>]+>", " ", text)
    return html.unescape(re.sub(r"\s+", " ", body + " " + attrs))

failed = False
def fail(msg):
    global failed
    failed = True
    print("FAIL", msg)

pages = sorted(glob.glob(f"{SITE}/*.html")) + [f"{SITE}/README.md"]
for path in pages:
    name = os.path.basename(path)
    raw = open(path, encoding="utf-8").read()
    if "—" in raw:
        fail(f"{name}: an em dash")
    if name.endswith(".html") and re.search(r"illuminat", visible(raw), flags=re.I):
        fail(f"{name}: the word illuminated (say painted in gold and blue)")
    if name in ("og-render.html",):
        continue
    text = visible(raw) if name.endswith(".html") else raw
    for phrase in ALLOWED.get(name, []):
        flat = re.sub(r"\s+", " ", phrase)
        if flat not in text:
            fail(f"{name}: allowed phrase no longer there, take it off the list: {phrase!r}")
        text = text.replace(flat, " ")
    for m in re.finditer(WORDS, text, flags=re.I):
        ctx = text[max(0, m.start() - 50):m.end() + 50]
        fail(f"{name}: {m.group(0)!r} in ...{ctx}...")

# The footer's ayah, on every page that shows it.
ayahs = json.load(open(f"{APP}/ayahs.json", encoding="utf-8"))
i = next(k for k, d in enumerate(ayahs) if d["s"] == 54 and d["a"] == 17)
arabic = ayahs[i]["u"].strip()
english = json.load(open(f"{APP}/tr_en-saheeh.json", encoding="utf-8"))["verses"][i]
for path in sorted(glob.glob(f"{SITE}/*.html")):
    raw = open(path, encoding="utf-8").read()
    for m in re.finditer(r'<figure class="foot-ayah">(.*?)</figure>', raw, flags=re.S):
        ar = re.search(r'<p class="ar"[^>]*>([^<]*)</p>', m.group(1)).group(1)
        en = re.search(r'<p class="en">([^<]*)</p>', m.group(1)).group(1)
        if ar != arabic:
            fail(f"{os.path.basename(path)}: the footer's Arabic is not the app's 54:17")
        if html.unescape(en) != english:
            fail(f"{os.path.basename(path)}: the footer's English is not Saheeh's 54:17")
    if re.search(r'lang="ar"[^>]*>[^<]*[ً-ْۡ][^<]*<', raw) and "foot-ayah" not in raw:
        fail(f"{os.path.basename(path)}: Quran-like Arabic outside the checked footer")

print("site check:", "FAILED" if failed else "all clear")
sys.exit(1 if failed else 0)
