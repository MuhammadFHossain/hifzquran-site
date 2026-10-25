# Quran Pages, the website

> **3.2 is live.** Quran Pages 3.2 went out on the App Store on 25 October 2026,
> with iPhone Duo, the pen and Saved recitations. Branch `site-3.2` brings the
> site up to it, with the first two App Store reviews. It goes live only on the
> owner's word: merge it into `main` and push.

The marketing and legal site for **Quran Pages** (iPhone, iPhone Duo, iPad and
Android), at **hifzquran.org**. Plain static
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
  shots/          screens of the app at 2x for a 330pt phone, the open iPhone Duo at
                  1920 wide, cut to its own round screen (duo-spread), the pen on an
                  iPad (pen), and the iPad's two-page spread (no longer shown), each
                  as WebP with PNG behind it
appstore-screenshots/
  6.9-inch/       the 1320x2868 pages that went up to the store on 26 August 2026
  6.5-inch/       the same at 1284x2778
```

`tools/export_assets.py` exports the screens in `assets/shots/` from the shots
on the app's main branch in `~/hifz-wt-merge/AppStore/shots/` (the iPad's in
`shots/ipad/`, the open Duo's in `shots/duo-inner/`), the icon set from the app
icon, and the sky grounds from `~/hifz-wt-sky`'s asset catalogue, since 3.0 no
longer ships the photographs. After a reshoot,
`python3 tools/export_assets.py screens` is enough; `wide` makes the Duo and
pen pictures. The Duo is cut with the simulator's own outline of its screen,
and the pen picture comes from the 3.2 review sheets, since no store shot has
writing on it. The share card,
`assets/img/og.png`, shows no screens, so a reshoot does not touch it.
`tools/shoot_site.py` photographs the site with headless Chrome over the DevTools
protocol (the Browser pane cannot screenshot while it is hidden):
`python3 tools/shoot_site.py out "top|http://localhost:8765/index.html?sky=asr|1440|900|0|0,900"`
(a position can also be a section's `#id`).
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

Store copy for 3.2 (What's New, promotional text, description) lives in
`ASO/APPSTORE_LISTING_3.2.md` on the app's main branch. The site's claims should
match it.

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

## Reviews

"In their own words" on the home page quotes App Store reviews word for word,
with the name the store shows, the storefront and the month. Only real ones,
chosen by the owner; nothing is ever invented or paraphrased into a quote. An
Arabic review keeps its own words and gets an English version under it, marked
as such. The two there now (26 October 2026, both 5 stars) were the only
written reviews then: runnerboy67 (Canada, 5 October) and ناقد اسطوري (Saudi
Arabia, 9 September). Apple's public feed shows a storefront's reviews:
`https://itunes.apple.com/<country>/rss/customerreviews/id=6792413377/sortby=mostrecent/json`.

## Later

- **The App Store rating:** the real star rating and count, read from the
  store, shown only once it is worth showing. Held by the owner on 26 October
  2026, at 4.7 from 15 ratings.
- **A note from the maker:** a few honest lines from the owner on why the app
  exists, written or approved by them.

## Going live (once 3.0 is approved)

1. Check the App Store page shows 3.0, and that the store link in `index.html`
   (`https://apps.apple.com/us/app/hifz-quran/id6792413377`) opens it.
2. If any screen in the app changed since 4 October, run
   `python3 tools/export_assets.py screens` and look at the page again.
3. Merge `release-3.0` into `main` and push. GitHub Pages publishes it in a
   minute or two. Open https://hifzquran.org on a phone and a computer.
4. In App Store Connect, keep Apple's standard EULA; the privacy and support
   links stay as listed above.
5. Done 18 Oct 2026: Quran Pages is public on Google Play. Every page shows
   the App Store badge and a Google Play badge side by side (Android visitors
   see only Google Play), and the "coming soon" lines are gone.
