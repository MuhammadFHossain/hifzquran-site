# Hifz Quran — website

The marketing + legal site for **Hifz Quran**, at **hifzquran.org**. Plain static
HTML/CSS, no build step, no framework, no tracking. The Arabic is set in the app's own
KFGQPC Uthmanic Hafs font and the screenshots are real captures, so the site matches the
app exactly.

```
index.html        landing page
privacy.html      Privacy Policy   (Apple requires a Privacy Policy URL)
terms.html        Terms of Use / EULA
support.html      Support page     (Apple requires a Support URL)
404.html          not-found page
og-render.html    source for assets/img/og.png (re-render if the tagline changes)
sitemap.xml, robots.txt
CNAME             the custom domain (used by GitHub Pages; ignored elsewhere)
assets/
  styles.css      the whole design system (brand teal #28ABC2 from the app icon)
  fonts/          Fraunces (headings, OFL) + UthmanicHafsV22 (the mushaf face, KFGQPC)
  img/            app-icon, mark (the open-mushaf logo), apple-touch-icon, favicon-64, og.png
  shots/          the five landing-page screenshots (web-optimized, 684×1486)
appstore-screenshots/
  6.9-inch-light/ full-res 1320×2868 (iPhone 16 Pro Max), light mode
  6.9-inch-dark/  full-res 1320×2868, dark mode
  6.5-inch-light/ 1284×2778, scaled from the 6.9" masters and trimmed 6px top and bottom
  6.5-inch-dark/  1284×2778, same treatment
```

Every screenshot set is a capture of **1.0.0 build 2** (2026-07-30) and holds the same
five screens: `01_mushaf`, `04_memorize`, `05_repeat`, `03_test`, `06_tajweed`. The old
`02_recite` and `03_finish` shots are gone, along with the recite-from-memory feature
they showed. Nothing on this site may imply the app listens to you: it has no microphone
access and no speech recognition, and it asks for no permissions at all.

## For the App Store submission

In App Store Connect, use these URLs:

- **Privacy Policy URL** → `https://hifzquran.org/privacy.html`
- **Support URL** → `https://hifzquran.org/support.html`
- **Marketing URL** (optional) → `https://hifzquran.org`
- **EULA**: either leave Apple's standard EULA, or paste `https://hifzquran.org/terms.html`

**Screenshots** in `appstore-screenshots/` are the exact 6.9" size (1320×2868) App Store
Connect wants for the primary set, plus a 6.5" set (1284×2778) because ASC's upload slots
ask for one in practice. They cover, in upload order: the page-exact mushaf with a range
selected, the Memorize tab (what is due for review and what you are working on), the
repeat sheet, the hide-and-reveal test, and the tajwīd-colored mushaf. Light and dark
sets are both included; supply one set per size, not a light/dark pair.

Captions, in the same order: *The page you memorize from* · *Pick a surah, see your
progress* · *Set the counts, then repeat* · *Hide it, then check yourself* · *Every rule
in color*.

Store copy (name, subtitle, description, keywords) lives in
`../HifzQuran/APPSTORE.md`.

## Hosting — free, static

Everything here is static, so any static host works.

### Cloudflare Pages (recommended — free, easy apex domain)
1. **dash.cloudflare.com → Workers & Pages → Create → Pages → Upload assets**, drag in
   this folder. No build command, no framework.
2. After it deploys, **Custom domains → Set up a domain** and add `hifzquran.org`
   (and `www.hifzquran.org`). Apex domains work here with zero fuss.

### GitHub Pages (also free)
1. Push these files to a repo's `main`.
2. **Settings → Pages → Deploy from a branch → main / (root)**.
3. **Custom domain** → `hifzquran.org` (the `CNAME` file already sets this), then point the
   apex `A` records at GitHub's IPs and add a `www` CNAME. Tick **Enforce HTTPS**.

### Netlify
Drag the folder onto **app.netlify.com/drop**, then add the custom domain.

All three give free HTTPS. Cloudflare Pages is the smoothest for an apex domain.

## When the app goes live

Open `index.html` and replace the "Coming soon on the App Store" `<span class="btn btn-solid" …>`
in the hero with a real link, e.g.:

```html
<a class="btn btn-solid" href="https://apps.apple.com/app/idYOURAPPID">
  <svg class="appleglyph" …></svg> Download on the App Store
</a>
```

## Notes

- Fonts are bundled (no external requests). Fraunces is OFL; the KFGQPC Uthmanic Hafs font is
  free to use and distribute (not to modify or sell) — the same terms under which the app ships it.
- No analytics, no cookies, no third-party requests. The site respects `prefers-color-scheme`
  and `prefers-reduced-motion`.
