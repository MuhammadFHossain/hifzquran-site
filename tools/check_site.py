#!/usr/bin/env python3
"""Checks the site before it goes live.

1. No ranking claims in our own words: best, #1, top rated. A review quoted
   word for word (inside <figure class="review">) is the reviewer's, and
   stays as they wrote it. The site does say free and no ads: the owner wants
   it said (27 October 2026). The App Store text never does; that is checked
   in the app's store copy scripts, not here.
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
# The app's text, read from its 4.0 branch in the app's repo (git show, so no
# checkout of it is needed; the 4.0 worktree may be gone after a merge).
APP_REPO = os.path.expanduser("~/Developer/HifzQuran")
APP_REFS = ("feature/illuminated", "main")

def app_json(name):
    import subprocess
    for ref in APP_REFS:
        r = subprocess.run(["git", "-C", APP_REPO, "show", f"{ref}:HifzQuran/Resources/{name}"], capture_output=True)
        if r.returncode == 0:
            return json.loads(r.stdout.decode("utf-8"))
    raise SystemExit(f"cannot read {name} from {APP_REPO} ({', '.join(APP_REFS)})")

WORDS = r"\b(best|top[- ]rated)\b|#1\b"


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
    if name.endswith(".html"):
        raw = re.sub(r'<figure class="review[^"]*">.*?</figure>', " ", raw, flags=re.S)
    text = visible(raw) if name.endswith(".html") else raw
    for m in re.finditer(WORDS, text, flags=re.I):
        ctx = text[max(0, m.start() - 50):m.end() + 50]
        fail(f"{name}: {m.group(0)!r} in ...{ctx}...")

# The footer's ayah, on every page that shows it.
ayahs = app_json("ayahs.json")
i = next(k for k, d in enumerate(ayahs) if d["s"] == 54 and d["a"] == 17)
arabic = ayahs[i]["u"].strip()
english = app_json("tr_en-saheeh.json")["verses"][i]
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
