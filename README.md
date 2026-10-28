# Quran Pages, the website

> **Branch `release-4.0`: the site for Quran Pages 4.0, the app painted in
> gold and blue.** Ready to go live the day Apple approves 4.0; the steps are under
> "Going live" at the end. `main` is still the 3.2 site, live since 26 October
> 2026.

The marketing and legal site for **Quran Pages** (iPhone, iPhone Duo, iPad and
Android), at **hifzquran.org**. Plain static HTML, CSS and one small script.
No build step, no framework, no tracking, no external requests.

The site follows the app, which in 4.0 is painted in gold and blue.
By day the ground is the app's bright cream paper, lit from the top, with a
touch of burnished grain and the rosette lattice pressed in tone on tone; in
the dark it is the app's lapis night with the same rosettes in cream. The bar
and the footer are lapis bands under a gold rule, like the app's tab band.
Buttons are cartouches with pointed ends, cards are square and ruled in gold,
and the closing panel wears the store banner's painted border. Light or dark
follows the visitor's system setting; there is no sky any more, as in the app.
`?theme=dark` or `?theme=light` forces one, for checking.

The painted pieces are the app's own paintings, played the way the app plays
them: each grows in as it comes into view, and the light moves on its gold
(with the mouse, or the phone's tilt or the page's scroll). That is the app's
paint shader (`Illumination.metal`, `IllumLight.h`) ported to WebGL in
`assets/site.js`, on the design page's player. With Reduce Motion, or with no
WebGL, the still painting shows.

The words follow `Design/WORDS.md`: plain enough for a grandmother who reads
English as her second language. Say "painted in gold and blue", never
"illuminated": the owner found nobody knows the word (27 October 2026). The
site says plainly that the app is free forever, with no ads and no account
(owner, 27 October 2026); the App Store text never does, by Apple's rules.
Nothing in our own words ranks the app above others, and no em dashes.
`tools/check_site.py` checks these.

```
index.html        landing page
privacy.html      Privacy Policy   (Apple and Google Play both require a Privacy Policy URL;
                  it covers the iPhone and iPad app, the Android app, their widgets and this site)
terms.html        Terms of Use (they go beside Apple's standard EULA and Google Play's terms)
support.html      Support page     (Apple requires a Support URL)
404.html          not-found page
og-render.html    source for assets/img/og.jpg, the share card (the command is inside)
sitemap.xml, robots.txt
CNAME             the custom domain (used by GitHub Pages; ignored elsewhere)
assets/
  styles.css      the design: tokens, the grounds, the bands, cartouches, ruled cards
  site.js         the theme, the Android badge rule, the fade-in, and the paintings' player
  fonts/          Fraunces (headings, OFL) + UthmanicHafsV22 (the mushaf face, KFGQPC)
  img/            Apple's App Store badges (black for day, white in the dark, from
                  toolbox.marketingtools.apple.com, never redrawn), icon A (app-icon,
                  apple-touch-icon, favicons), its mark for the wordmark, og.jpg
  art/            the app's paintings with their maps (-base, -time, -mat): the shamsa,
                  the crown, twelve surahs, three vines; the banner's border (frame) and its gold
                  rule (rule); the ground's rosettes (ground-day.svg, ground-night.svg)
                  and grain
  shots/          screens of the app at 2x for a 330pt phone, as WebP with a JPEG behind;
                  the open iPhone Duo (duo-spread) and the pen on an iPad (pen)
appstore-screenshots/   the 3.0 store pages of 26 August 2026 (not linked)
preview/                pictures of the 3.0 site (not linked)
tools/
  export_assets.py  the screens, the art and the icons, from the app and its store kit
  paint_vines.py    paints the vines with the app's illumination engine, and their maps
  subset_fonts.py   cuts Fraunces down to what the site uses
  check_site.py     ranking words, em dashes, "illuminated", and the Quran text
  shoot_site.py     photographs the site with headless Chrome
```

`tools/export_assets.py` reads the 4.0 store kit (`~/hifz-wt-store-illum`,
branch `feature/illuminated-store`: the raw shots in `AppStore/shots`, the
banner, icon A) and the paintings in `~/hifz-wt-illuminated` (branch
`feature/illuminated`, `HifzQuran/Resources/Illumination`). After a reshoot,
`python3 tools/export_assets.py screens` is enough; `wide` makes the Duo and
the pen pictures once the 4.0 iPad and Duo shots exist. If those worktrees are
gone after the merge, point `STORE` and `ART` at the app's main checkout. The
share card shows the Al-Fatihah screen, so a reshoot of that screen means
rendering `og-render.html` again.

`tools/shoot_site.py` photographs the site with headless Chrome over the
DevTools protocol (the Browser pane cannot screenshot while it is hidden):
`python3 tools/shoot_site.py out "top|http://localhost:8765/index.html?theme=dark|1440|900|0|0,#painted"`
(a position can also be a section's `#id`).

Nothing on this site may imply the app listens to you: it has no microphone
access and no speech recognition. Location, notifications and alarms are
optional and asked for only when a feature is turned on, and the site says so.
The motion sensor moves only the light on the gold, and the site says that too.

## For the App Store submission

In App Store Connect, use these URLs:

- **Privacy Policy URL**: `https://hifzquran.org/privacy.html`
- **Support URL**: `https://hifzquran.org/support.html`
- **Marketing URL**: `https://hifzquran.org`
- **EULA**: leave Apple's standard EULA. terms.html is written to go beside it,
  not replace it; a custom EULA would also have to give a postal address and
  phone number.

Store copy for 4.0 (What's New, promotional text, description) lives in
`ASO/APPSTORE_LISTING_4.0.md` on the app's `feature/illuminated` branch. The
site's claims should match it.

## Hosting

Everything here is static, so any static host works. It is on GitHub Pages:
push to `main`, and the `CNAME` file sets the domain.

The stylesheet and the script are linked with `?v=YYYYMMDD` because GitHub
Pages caches them hard and a stale copy reads as the change never landing.
Bump the number on any edit to either file.

## Notes

- Fonts are bundled. Fraunces is OFL; the KFGQPC Uthmanic Hafs font may be
  used and shared (not changed or sold), the same terms under which the app
  ships it.
- No analytics, no cookies, no third-party requests. The site respects
  `prefers-reduced-motion`, and with no script it still follows the system's
  light or dark setting.
- The surahs' paintings are shown, not sold: a strip of tiles drifting past,
  with no heading (owner, 27 October 2026: "not a value prop"). Three vines
  painted for the site with the app's engine (`tools/paint_vines.py`) grow
  across the page between sections, as the app paints its pages in.
- The line is "Read, repeat, remember." (owner, 27 October 2026: "pray isn't
  something we make people do").
- The Quran on the site is one ayah, in the footer: Al-Qamar 54:17, taken
  letter for letter from the app's `ayahs.json`, with Saheeh International
  from the app's `tr_en-saheeh.json`. `tools/check_site.py` compares them.
  The surah names under the paintings are the app's own (`surahs.json`).

## Reviews

"In their own words" on the home page quotes App Store reviews word for word,
with the name the store shows, the storefront and the month. Only real ones,
chosen by the owner; nothing is ever invented or paraphrased into a quote. An
Arabic review keeps its own words and gets an English version under it, marked
as such. The owner asked for as many as there are (27 October 2026). On that
day every storefront's feed held three written reviews, all 5 stars, and all
three are on the page: runnerboy67 (Canada, 5 October), ناقد اسطوري (Saudi
Arabia, 9 September) and Izza_chockly (India, 24 October). Google Play shows
no reviews yet. Apple's public feed shows a storefront's reviews:
`https://itunes.apple.com/<country>/rss/customerreviews/id=6792413377/sortby=mostrecent/json`.

## Later

- **The App Store rating:** the real star rating and count, read from the
  store, shown only once it is worth showing. Put off by the owner on 26
  October 2026, at 4.7 from 15 ratings.
- **A note from the maker:** a few lines from the owner on why the app exists,
  written or approved by them.

## Going live (once 4.0 is approved)

Before the day:

1. Wait for the store session's final 4.0 shots (it reshoots every set once
   iPhone, iPad, Duo, Android and Indopak have all landed). On 28 October
   the site took the store kit's reshoot of 27 October (the calmer Quran tab,
   the Mughal Indopak page, Salah with no sky, the open Duo on the Indopak
   opening). One picture is still a stand-in: `shots/pen`, the 3.2 look, until
   there is a 4.0 iPad shot with the pen out.
   Then run `python3 tools/export_assets.py screens wide` (for the pen, the
   iPad shot must be at `AppStore/shots/ipad/pad_pen.png`, or change `PEN`).
   If the Al-Fatihah screen changed, render the share card again
   (`og-render.html`).
2. Read the page against the 4.0 build: every claim must be true of the build
   that ships, and the alt texts must still describe the pictures.
3. `python3 tools/check_site.py` must say "all clear".
4. Look at it at phone and desktop width, in light and dark (`?theme=dark`).
5. Set the "Last updated" line in `privacy.html` and `terms.html`, and the
   dates in `sitemap.xml`, to the day it goes live (they say 27 October 2026
   now). Privacy is new for 4.0 where it speaks of the motion sensor.

On the day:

6. Check the App Store page shows 4.0, and that the store link
   (`https://apps.apple.com/us/app/quran-pages-read-repeat/id6792413377`)
   opens it.
7. Merge `release-4.0` into `main` and push. Pushes over about 10 MB drop
   on this Mac: if `git count-objects` or the push says more, push the
   commits one at a time. GitHub Pages publishes it in a minute or two.
8. Open https://hifzquran.org on a phone and a computer, in light and dark,
   and paste the link in a chat to see the new share card.
9. In App Store Connect, keep Apple's standard EULA; the privacy and support
   links stay as listed above.
10. The Google Play listing changes on its own, in the Play Console.
