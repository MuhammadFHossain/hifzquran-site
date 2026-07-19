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
  shots/          the six landing-page screenshots (web-optimized)
appstore-screenshots/
  6.9-inch-light/ 01..06  full-res 1320×2868 (iPhone 16 Pro Max), light mode
  6.9-inch-dark/  01..05  full-res 1320×2868, dark mode
```

## For the App Store submission

In App Store Connect, use these URLs:

- **Privacy Policy URL** → `https://hifzquran.org/privacy.html`
- **Support URL** → `https://hifzquran.org/support.html`
- **Marketing URL** (optional) → `https://hifzquran.org`
- **EULA**: either leave Apple's standard EULA, or paste `https://hifzquran.org/terms.html`

**Screenshots** in `appstore-screenshots/` are the exact 6.9" size (1320×2868) App Store
Connect wants for the primary set. They cover: the page-exact mushaf, reciting with the
live reveal + a soft crimson slip, finishing a portion, the Memorize cockpit (due for
review + weak spots), the repeat drill sheet, and the tajwīd-colored mushaf. Both a light
and a dark set are included; upload whichever you prefer as the primary. (Apple derives the
6.5" set from these, so a separate 6.5" capture is optional.)

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
