# Hifz Quran, the website

The marketing and legal site for **Hifz Quran** (iPhone and iPad, Android coming
soon), at **hifzquran.org**. Plain static
HTML, CSS and one small script. No build step, no framework, no tracking, no
external requests.

The site follows the app's design and its measure, `Design/GEOMETRY.md`
(Mizan). By day the ground is paper with al-Fatihah's lattice as a grain, and
the hour's sky sits at the head of the page at 22%, the way `MushafGround`
draws it in the app. Cards are paper on paper; glass is only for the floating
bar; the button is lapis with cream on it, and gold is only lines and points.
After Maghrib the page turns dark and the sky is the whole ground, read off
the visitor's clock. The words follow `Design/WORDS.md`: plain enough for a
grandmother who reads English as her second language. `?sky=maghrib` forces a window and `?clock=21:30` a time, for
checking the page at any hour.

```
index.html        landing page
privacy.html      Privacy Policy   (Apple and Google Play both require a Privacy Policy URL;
                  it covers the iPhone and iPad app, the Android app, their widgets and this site)
terms.html        Terms of Use (sit alongside Apple's standard EULA and Google Play's terms)
support.html      Support page     (Apple requires a Support URL)
404.html          not-found page
og-render.html    source for assets/img/og.png (the command to render it is inside)
sitemap.xml, robots.txt
CNAME             the custom domain (used by GitHub Pages; ignored elsewhere)
assets/
  styles.css      the design system: tokens, the ground, glass, the type scale
  sky.js          picks the sky from the clock and paints it
  sky/            the app's evening photograph, sharp for the hero and blurred for the ground
  fonts/          Fraunces (headings, OFL) + UthmanicHafsV22 (the mushaf face, KFGQPC)
  img/            Apple's App Store badges (black for day, white after dark, from
                  toolbox.marketingtools.apple.com, never redrawn), app-icon, mark (the gold rosette), apple-touch-icon, favicons, og.png
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
- **EULA**: leave Apple's standard EULA. terms.html is written to sit beside it, not
  replace it; a custom EULA would also have to give a postal address and phone number.

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

## Later

Proof that people trust the app, parked by the owner on 4 October 2026. Each
must be real; nothing is ever invented or paraphrased into a quote.

- **The App Store rating:** the real star rating and count, read from the
  store, shown only once it is worth showing.
- **Real reviews:** two or three App Store reviews, quoted word for word with
  the reviewer's name as the store shows it, chosen by the owner.
- **A note from the maker:** a few honest lines from the owner on why the app
  exists, written or approved by them.
