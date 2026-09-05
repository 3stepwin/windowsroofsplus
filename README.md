# windowsroofsplus.com

Static marketing site for **Windows Roofs Plus Inc.** (WRP) — licensed South Florida
roofing, impact window, and impact door contractor based in Margate, FL.

Built on the same pattern *and the same design system* as `speedyremodelingcompany` —
hand-authored static HTML, a small Python builder for the repeated pages, the FDME
glass design system, and a Vercel Edge Function for lead capture. No framework, no
build step required to serve.

`_ds/` holds the same FDME design system files Speedy runs on, copied verbatim
(`colors_and_type.css` and `shared/fdme.css` are md5-identical to Speedy's). Every page
loads them in the same order Speedy does, then `assets/css/wrp.css` on top:

```html
<link rel="stylesheet" href="/_ds/fdme-design-system-…/colors_and_type.css">
<link rel="stylesheet" href="/_ds/fdme-design-system-…/shared/fdme.css">
<link rel="stylesheet" href="/assets/css/wrp.css">
```

The system ships teal-primary / orange-CTA. Speedy overrides the teal with navy; WRP
overrides it with brand violet (`--violet-500 #7C22CE`, headings `--plum-900 #2A0F52`).
`.fdme-cta` — the orange CTA gradient — is a system constant and is used unmodified on
both sites. `wrp.css` does not redefine anything the system already provides identically
(`.blur-in`, `.blur-word`, `.float-y`, `.ken-burns`, `.pulse-ring`, `.reveal`,
`.icon-pill-orange`, `.stat-value-orange`, `.video-light-tint-soft`).

**One deviation from the upstream copy.** `colors_and_type.css` `@import`s Inter and
Poppins from Google Fonts. Those families back `--fdme-font-body` / `--fdme-font-display`,
which are only consumed by the `.fdme-h1` / `.fdme-h2` / `.fdme-lede` / `.fdme-body` type
roles — and no page here uses them (`.fdme-cta` is the only system class in the markup).
`fdme.css` sets the actually-rendered families to Barlow and Instrument Serif, both
self-hosted. The import was a render-blocking third-party request for two fonts that never
paint, so it is commented out with an explanatory note. Restore it if a page ever adopts
the `.fdme-*` type roles.

---

## Stack

| Piece | What it is |
|---|---|
| Pages | Static HTML, served as-is |
| Styling | The vendored FDME design system in `_ds/` + `assets/css/wrp.css` as the WRP colorway layer |
| Behavior | One file: `assets/js/wrp.js` (scroll reveal, mobile menu, form) |
| Fonts | Self-hosted Instrument Serif (display) + Barlow (body) in `assets/fonts/` — no Google Fonts request |
| Icons | Remixicon **subset** — 54 icons, 4 KB woff2, generated from the icons actually used |
| Forms | `POST /api/lead` → Vercel Edge Function |
| Hosting | Vercel (static + edge function) |

## Layout

```
_ds/fdme-design-system-…/       vendored FDME design system (byte-identical to Speedy's)
  colors_and_type.css             tokens
  shared/fdme.css                 primitives (.glass, .fdme-cta, .h-display, motion)
  _ds_bundle.js                   nav/footer injection + reveal — unused here, kept for parity
index.html                      homepage
services/roofing.html           roofing hub
services/impact-windows.html    impact window hub
services/impact-doors.html      impact door hub
financing.html                  PACE / conventional / credit-flexible
service-areas.html              30 Broward municipalities
thank-you.html                  post-submit (noindex)
api/lead.js                     edge function — estimate requests
build.py                        regenerates everything except index.html
assets/css/wrp.css              design system
assets/js/wrp.js                shared behavior
assets/fonts/                   self-hosted fonts + icon subset
assets/brand/                   logo derivatives
sitemap.xml robots.txt llms.txt vercel.json
```

## Rebuilding pages

`index.html` is hand-maintained. Everything else is generated:

```bash
python3 build.py
```

The builder holds the shared nav, footer, estimate form, and JSON-LD helpers, so a
change to the nav is one edit in `build.py` + one edit in `index.html` — not eight.

`CITIES` in `build.py` is the list of Broward municipalities. Per-city service pages
(e.g. `/services/impact-windows/fort-lauderdale.html`) are the natural next phase —
the list, the shell, and the sitemap writer are already in place.

## Lead capture

`api/lead.js` currently runs in **notification-only** mode. Set one of these in the
Vercel project's environment variables:

| Var | Effect |
|---|---|
| `FORMSPREE_ID` | POSTs the lead to `https://formspree.io/f/<id>` |
| `LEAD_WEBHOOK` | POSTs the raw JSON payload to that URL |

With neither set the endpoint returns `503` and the form tells the visitor to call.

A ready-to-fill GoHighLevel block is commented at the bottom of `api/lead.js`. To
switch on CRM capture later: create the WRP sub-account, set `GHL_WRP_LOCATION_PIT`,
`GHL_WRP_LOCATION_ID`, `GHL_WRP_PIPELINE_ID`, uncomment `sendToGHL()`, and call it
before the notification step. Nothing else changes.

## Brand assets

`assets/brand/wrp-logo-transparent.png` is the master (1722×832, alpha). It was made
from the flat-white-background artwork by flood-filling near-white **inward from the
image borders** rather than keying white globally — the logo's own white keylines around
the WRP letters are interior, so a global key would have eaten them. Everything else is
derived from that master:

| File | Use |
|---|---|
| `wrp-nav.webp/.png` | nav lockup — WRP badge + WINDOWS ROOFS PLUS, above the first divider rule |
| `wrp-mark.webp/.png` | footer + schema logo — the complete lockup including *Built for Florida* |
| `wrp-social-share.jpg` | 1200×630 Open Graph card, full lockup on white |
| `wrp-icon.png` / `apple-touch-icon.png` | favicon + iOS home screen — WRP monogram squared on white |
| `hero-bg.jpg` | hero background, from `wrp-logo-original-dark.png` (the earlier dark logo art), standing in for Speedy's hero video until WRP has real footage |
| `wrp-logo-original-dark.png` | the previous dark-background logo, kept only as the source for `hero-bg.jpg` |

Because the art is transparent, the nav and footer marks carry no plate or shadow — the
nav pill is a plain `.glass` surface from the design system.

## Company facts used on the site

Everything asserted on these pages is sourced, not invented — no fabricated review
counts, prices, or years in business. If you change any of the below, grep for it:

- Phone: **(954) 706-8028** (matches the number on the existing site)
- Address: 1700 Banks Rd, Unit 50-B, Margate, FL 33063
- License: Florida Certified Roofing Contractor **CCC1333631**
- BBB: Accredited since October 2022, A+ rating
- Products manufactured in Florida, installed factory direct
- Financing: P.A.C.E., conventional, credit-flexible programs

Warranty language is deliberately non-specific ("stated in your written contract")
because the public warranty terms aren't documented. Tighten it once the real terms
are confirmed.

## Local preview

```bash
python3 -m http.server 8899
# http://localhost:8899
```

The edge function does not run under `http.server`; use `vercel dev` to exercise
`/api/lead` locally.
