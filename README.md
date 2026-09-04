# windowsroofsplus.com

Static marketing site for **Windows Roofs Plus Inc.** (WRP) — licensed South Florida
roofing, impact window, and impact door contractor based in Margate, FL.

Built on the same pattern as `speedyremodelingcompany` — hand-authored static HTML,
a small Python builder for the repeated pages, one shared CSS design system, and a
Vercel Edge Function for lead capture. No framework, no build step required to serve.

---

## Stack

| Piece | What it is |
|---|---|
| Pages | Static HTML, served as-is |
| Styling | One file: `assets/css/wrp.css` (light theme — white ground, graphite type, violet brand accent) |
| Behavior | One file: `assets/js/wrp.js` (scroll reveal, mobile menu, form) |
| Fonts | Self-hosted Barlow + Barlow Condensed (`assets/fonts/`) — no Google Fonts request |
| Icons | Remixicon **subset** — 54 icons, 4 KB woff2, generated from the icons actually used |
| Forms | `POST /api/lead` → Vercel Edge Function |
| Hosting | Vercel (static + edge function) |

## Layout

```
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

`assets/brand/wrp-logo.png` is the master logo (1536×1024). The rest are derived:

| File | Use |
|---|---|
| `wrp-nav.webp` | nav + footer lockup, composited onto a rounded dark plate so the dark logo art reads as a deliberate badge on the white page |
| `wrp-mark.webp` | hero mark, full lockup including *Built for Florida*, same rounded-plate treatment |
| `wrp-social-share.jpg` | 1200×630 Open Graph card (white ground) |
| `wrp-icon.png` / `apple-touch-icon.png` | favicon + iOS home screen |

Regenerate them from the master with the Pillow snippet in the commit that added them.

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
