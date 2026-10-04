# Hifz Quran, the website

The marketing and legal site for **Hifz Quran** (iPhone and iPad, Android coming
soon), at **hifzquran.org**. Plain static
HTML, CSS and one small script. No build step, no framework, no tracking, no
external requests.

The site follows the app's design. The ground under every page is one of the
app's own sky photographs, blurred back to its light, with the hour's gradient
over it, the way `MushafGround` draws it in the app. Cards are glass over that.
The chrome is light while the sky is and dark once it is not, read off the
visitor's clock. `?sky=maghrib` forces a window and `?clock=21:30` a time, for
checking the page at any hour.

```
index.html        landing page
privacy.html      Privacy Policy   (Apple and Google Play both require a Privacy Policy URL;
                  it covers the iPhone and iPad app, the Android app, their widgets and this site)
terms.html        Terms of Use / EULA
support.html      Support page     (Apple requires a Support URL)
404.html          not-found page
og-render.html    source for assets/img/og.png (the command to render it is inside)
sitemap.xml, robots.txt
CNAME             the custom domain (used by GitHub Pages; ignored elsewhere)
assets/
  styles.css      the design system: tokens, the ground, glass, the type scale
  sky.js          picks the sky from the clock and paints it
  sky/            three of the app's photographs, sharp for the hero and blurred for the ground
  fonts/          Fraunces (headings, OFL) + UthmanicHafsV22 (the mushaf face, KFGQPC)
  img/            app-icon, mark (the gold rosette), apple-touch-icon, favicons, og.png
  shots/          screens of the app at 2x for a 330pt phone, and the iPad's two-page
                  spread at 1920 wide, each as WebP with PNG behind it
appstore-screenshots/
  6.9-inch/       the 1320x2868 pages that went up to the store on 26 August 2026
  6.5-inch/       the same at 1284x2778
```

`tools/export_assets.py` exports the screens in `assets/shots/` from the 3.0
shots in `~/hifz-wt-polish/AppStore/shots/` (the iPad's in `shots/ipad/`), the
icon set from the app icon, and the sky grounds from `~/hifz-wt-sky`'s asset
catalogue, since 3.0 no longer ships the photographs. After a reshoot,
`python3 tools/export_assets.py screens` is enough. The share card,
`assets/img/og.png`, shows no screens, so a reshoot does not touch it.
`tools/shoot_site.py` photographs the site with headless Chrome over the DevTools
protocol (the Browser pane cannot screenshot while it is hidden):
`python3 tools/shoot_site.py out "top|http://localhost:8765/index.html?sky=asr|1440|900|0|0,900"`.
Nothing on this site may imply the app listens to you: it has no microphone
access and no speech recognition. Location, notifications and alarms are
optional and asked for only when a feature is turned on, and the site says so.

## For the App Store submission

In App Store Connect, use these URLs:

- **Privacy Policy URL**: `https://hifzquran.org/privacy.html`
- **Support URL**: `https://hifzquran.org/support.html`
- **Marketing URL**: `https://hifzquran.org`
- **EULA**: either leave Apple's standard EULA, or paste `https://hifzquran.org/terms.html`

Store copy for 3.0 (What's New, promotional text, description) lives in
`~/hifz-wt-polish/ASO/APPSTORE_LISTING_3.0.md`. The site's claims should match it.

## Hosting

Everything here is static, so any static host works. It is on GitHub Pages:
push to `main`, and the `CNAME` file sets the domain.

The stylesheet and the script are linked with `?v=YYYYMMDD` because GitHub
Pages caches them hard and a stale copy reads as the change never landing.
Bump the number on any edit to either file.

## Notes

- Fonts are bundled. Fraunces is OFL; the KFGQPC Uthmanic Hafs font is free to
  use and distribute (not to modify or sell), the same terms under which the
  app ships it.
- No analytics, no cookies, no third-party requests. The site respects
  `prefers-reduced-motion`, and with no script it follows the system's
  light or dark setting instead of the clock.
