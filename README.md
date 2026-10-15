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

`api/lead.js` stores estimate requests in the existing Supabase `fb_leads` table when `SUPABASE_QUEUE_URL` and `SUPABASE_QUEUE_KEY` are configured. Production metadata checked on 2026-10-11 shows these two variables only. No Formspree or notification webhook is configured. A successful CRM insert counts as delivered; it does not prove a notification reached Mike. Do not submit fake production leads to test it.

Optional existing notification paths are `FORMSPREE_ID` and `LEAD_WEBHOOK`. With no usable delivery route the endpoint returns an error and the browser offers click-to-call. The unused GHL example is not active.

## Brand assets

`assets/brand/wrp-logo-polished.svg` is the owner-approved October 11 candidate, used in every navigation/footer and structured-data logo. It preserves all 40 path attributes and colors of `wrp-logo-classic.svg`, with balanced clear space and scalable output. The original remains unchanged. Existing favicon and social-card art retain the same classic identity.

Provenance distinction: the old domain still serves `https://windowsroofsplus.com/wp-content/uploads/2022/08/win-roof-logo.png`, which has the same purple-roof/gray-window icon but an uppercase “WINDOWS ROOFS PLUS INC.” wordmark. The repository classic vector and approved candidate use title-case “Windows Roofs Plus”. Do not claim exact wordmark parity with that older PNG. The prior dramatic WRP badge is obsolete.

The homepage background remains the existing `hero-bg.jpg`; layout and design are unchanged.

## October 11 launch checks

- Logo approved before integration; DNS cutover remains separately held for mail-safe coordination.
- Roof-copy correction source: https://www.flsenate.gov/Laws/Statutes/2025/553.844, subsection (5). The 25% rule has a code-history exception; avoid categorical replacement claims.
- BBB accreditation and A+ were reconfirmed at https://www.bbb.org/us/fl/margate/profile/roofing-contractors/windows-roofs-plus-inc-0633-92024925. That profile lists incorporation in 2013 and business start in 2021; Mike's supplied since-2013 history remains subject to reconciliation.
- Google rating, insurance, current license standing and financing eligibility need current supporting evidence before claiming a complete business-fact audit.

## Company facts used on the site

Everything asserted on these pages is sourced, not invented — no fabricated review
counts, prices, or years in business. If you change any of the below, grep for it:

- Phone: **(954) 914-3586** (matches the number on the existing site)
- Address: 1700 Banks Rd, Unit 50-B, Margate, FL 33063
- License: Florida Certified Roofing Contractor **CCC1333631**
- License: Broward County Structural Carpentry Specialty Contractor **21-CRP-22416-X** (Mike, 9/22/2026 email)
- In business since **2013** (Mike: BBB shows 2013, the year of the name change); BBB A+
- 5-star Google rating (Mike, 9/22/2026 email — no review count stated, so none shown)
- Service area: **Jupiter to Miami** (Mike, 9/22/2026)
- Windows & doors: "High impact rated" — NOT "Florida-made"; Mike uses multiple manufacturers. Do not name a manufacturer.
- Crew: "installed by our own crew" — never "licensed local crew" (reads like subbing out)
- Seamless gutters, 6-inch and 7-inch
- Financing: Ygrene Certified (PACE, not based on credit score) and GoodLeap (conventional). PACE
  programs have advertising rules — no $0-down / term-length claims until Mike's GoodLeap/Ygrene rep signs off.
- Do not claim we do insurance paperwork for the homeowner (Mike: insurers are funny about that)
- Logo: Mike's classic house logo (`assets/brand/wrp-logo-classic.svg`). The WRP badge art is on hold —
  Mike doesn't want to change the logo yet because it's on everything he has.

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
