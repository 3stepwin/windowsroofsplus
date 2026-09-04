#!/usr/bin/env python3
"""
Windows Roofs Plus — static site builder.

Holds the shared shell (head, nav, footer, form) so every page stays consistent,
and generates the service hubs, financing, service-areas, thank-you page,
per-city service pages, sitemap.xml and llms.txt.

    python3 build.py
"""
import json, os, re, datetime

ROOT   = os.path.dirname(os.path.abspath(__file__))
DOMAIN = "https://windowsroofsplus.com"
PHONE  = "(954) 706-8028"
TEL    = "+19547068028"
BIZ    = "Windows Roofs Plus Inc."
LIC    = "CCC1333631"
ADDR   = "1700 Banks Rd, Unit 50-B, Margate, FL 33063"
TODAY  = datetime.date.today().isoformat()

# ─────────────────────────────────────────────────────────── shell ──

def head(title, desc, path, keywords="", extra_ld=None, og_title=None):
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(b, separators=(",", ":"))}</script>'
                   for b in (extra_ld or []))
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<link rel="canonical" href="{DOMAIN}{path}">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Margate, Broward County, Florida">
{f'<meta name="keywords" content="{keywords}">' if keywords else ''}
<meta property="og:type" content="website">
<meta property="og:title" content="{og_title or title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{DOMAIN}{path}">
<meta property="og:image" content="{DOMAIN}/assets/brand/wrp-social-share.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{DOMAIN}/assets/brand/wrp-social-share.jpg">
<link rel="icon" href="/assets/brand/wrp-icon.png" type="image/png">
<link rel="apple-touch-icon" href="/assets/brand/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/InstrumentSerif-italic-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/Barlow-400-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/fonts/fonts.css">
<link rel="stylesheet" href="/assets/fonts/remixicon-subset.css">
<link rel="stylesheet" href="/_ds/fdme-design-system-78336979-7a54-41e8-b9f6-e66e8cb27e16/colors_and_type.css">
<link rel="stylesheet" href="/_ds/fdme-design-system-78336979-7a54-41e8-b9f6-e66e8cb27e16/shared/fdme.css">
<link rel="stylesheet" href="/assets/css/wrp.css">
{ld}
</head>
<body>
'''

NAV = f'''
<div class="nav-wrap">
  <nav class="nav">
    <a href="/" class="nav-logo" aria-label="{BIZ} home">
      <img src="/assets/brand/wrp-nav.webp" alt="{BIZ} — Roofing, Impact Windows, Impact Doors" width="640" height="279">
    </a>
    <div class="nav-links">
      <a href="/services/roofing.html">Roofing</a>
      <a href="/services/impact-windows.html">Impact Windows</a>
      <a href="/services/impact-doors.html">Impact Doors</a>
      <a href="/financing.html">Financing</a>
      <a href="/service-areas.html">Service Areas</a>
      <a href="#estimate" class="fdme-cta btn btn-sm" style="margin-left:6px">Free Estimate</a>
    </div>
    <button class="nav-toggle" id="navToggle" aria-label="Open menu" aria-expanded="false"><i class="ri-menu-line"></i></button>
  </nav>
  <div class="mobile-menu" id="mobileMenu">
    <a href="/services/roofing.html">Roofing</a>
    <a href="/services/impact-windows.html">Impact Windows</a>
    <a href="/services/impact-doors.html">Impact Doors</a>
    <a href="/financing.html">Financing</a>
    <a href="/service-areas.html">Service Areas</a>
    <a href="tel:{TEL}" style="color:var(--violet-500)"><i class="ri-phone-fill"></i> {PHONE}</a>
  </div>
</div>
'''

def page_hero(eyebrow, h1_chrome, h1_violet, lead, crumbs=None):
    bc = ""
    if crumbs:
        items = " <span style='opacity:.4'>/</span> ".join(
            f'<a href="{u}" style="color:var(--muted)">{t}</a>' if u else f'<span style="color:var(--ink-2)">{t}</span>'
            for t, u in crumbs)
        bc = f'<nav aria-label="Breadcrumb" style="font-size:13px;margin-bottom:22px">{items}</nav>'
    return f'''
<header class="page-hero">
  <div class="container">
    {bc}
    <span class="eyebrow blur-in">{eyebrow}</span>
    <h1 class="h-display blur-in" style="animation-delay:.12s;margin-top:20px">
      {h1_chrome}<br><span class="violet-text">{h1_violet}</span>
    </h1>
    <p class="lead blur-in" style="animation-delay:.26s;max-width:720px;margin-top:22px">{lead}</p>
    <div class="hero-cta blur-in" style="animation-delay:.38s">
      <a href="#estimate" class="fdme-cta btn btn-lg">Free Estimate <i class="ri-arrow-right-up-line"></i></a>
      <a href="tel:{TEL}" class="btn btn-ghost btn-lg"><i class="ri-phone-line" style="color:var(--violet-500)"></i>{PHONE}</a>
    </div>
  </div>
</header>
'''

def faq_block(title, pairs):
    rows = "".join(
        f'<details{" open" if i == 0 else ""}><summary>{q}</summary><p>{a}</p></details>'
        for i, (q, a) in enumerate(pairs))
    return f'''
<section class="sec sec-alt" id="faq">
  <div class="container" style="max-width:880px">
    <div class="sec-head">
      <span class="eyebrow reveal">Straight Answers</span>
      <h2 class="h-display reveal"><span class="chrome">{title}</span></h2>
    </div>
    <div class="faq glass round-2xl reveal" style="padding:clamp(20px,3vw,36px)">{rows}</div>
  </div>
</section>
'''

def faq_ld(pairs):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}}
        for q, a in pairs]}

ESTIMATE = f'''
<section class="sec" id="estimate">
  <div class="container" style="max-width:820px">
    <div class="sec-head">
      <span class="eyebrow reveal">Free · No Obligation</span>
      <h2 class="h-display reveal"><span class="chrome">Let's protect</span> <span class="violet-text">your home.</span></h2>
      <p class="lead reveal">Tell us what you need. We'll come measure, put a real number on it, and show you exactly what financing looks like for your address.</p>
    </div>
    <form class="glass-strong round-2xl reveal" id="estimateForm" style="padding:clamp(24px,4vw,42px)" novalidate>
      <div class="form-grid">
        <label class="fld">Full name<input name="name" required autocomplete="name" placeholder="Jane Rodriguez"></label>
        <label class="fld">Phone<input name="phone" type="tel" required autocomplete="tel" placeholder="(954) 555-0142"></label>
        <label class="fld">Email<input name="email" type="email" autocomplete="email" placeholder="you@email.com"></label>
        <label class="fld">City<input name="city" autocomplete="address-level2" placeholder="Fort Lauderdale"></label>
        <label class="fld span-2">What do you need?
          <select name="service" required>
            <option value="Impact windows">Impact windows</option>
            <option value="Impact doors">Impact doors</option>
            <option value="Impact windows + doors">Impact windows + doors</option>
            <option value="Roof replacement">Roof replacement</option>
            <option value="Roof repair / leak">Roof repair / leak</option>
            <option value="Roof + impact package">Roof + impact package</option>
            <option value="Commercial project">Commercial project</option>
            <option value="Not sure yet">Not sure yet — need advice</option>
          </select>
        </label>
        <label class="fld span-2">Anything we should know? <span style="text-transform:none;letter-spacing:0;font-weight:400;color:#5F657A">(optional)</span>
          <textarea name="details" rows="3" placeholder="Roof is 22 years old and insurance is asking for a replacement…"></textarea>
        </label>
      </div>
      <input type="hidden" name="page_url">
      <input type="text" name="_gotcha" tabindex="-1" autocomplete="off" style="position:absolute;left:-9999px" aria-hidden="true">
      <button type="submit" class="fdme-cta btn btn-lg" style="width:100%;margin-top:22px">Request My Free Estimate <i class="ri-arrow-right-up-line"></i></button>
      <p class="form-note" id="formStatus" role="status" aria-live="polite">Prefer to talk? Call <a href="tel:{TEL}" style="color:var(--violet-500);font-weight:600">{PHONE}</a>.</p>
    </form>
  </div>
</section>
'''

FOOTER = f'''
<footer class="footer">
  <div class="container">
    <div class="glass round-2xl footer-inner">
      <div class="footer-grid">
        <div>
          <div class="footer-logo"><img src="/assets/brand/wrp-nav.webp" alt="{BIZ}" width="640" height="279"></div>
          <p style="font-size:14.5px;font-weight:300;max-width:320px">Licensed South Florida roofing and impact window contractor. Protect · Enhance · Add Value — built for Florida.</p>
          <p style="font-size:12.5px;color:var(--muted);margin-top:14px">FL Certified Roofing Contractor <strong style="color:var(--ink-2)">{LIC}</strong><br>BBB Accredited · A+ Rating</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="/services/roofing.html">Roofing</a></li>
            <li><a href="/services/impact-windows.html">Impact Windows</a></li>
            <li><a href="/services/impact-doors.html">Impact Doors</a></li>
            <li><a href="/financing.html">Financing &amp; PACE</a></li>
            <li><a href="/service-areas.html">Service Areas</a></li>
          </ul>
        </div>
        <div>
          <h4>Contact</h4>
          <ul>
            <li><a href="tel:{TEL}"><i class="ri-phone-line"></i>{PHONE}</a></li>
            <li><i class="ri-map-pin-line"></i> 1700 Banks Rd, Unit 50-B<br>&nbsp;&nbsp;&nbsp;Margate, FL 33063</li>
            <li><i class="ri-time-line"></i> Mon–Sat, 8am–6pm</li>
          </ul>
        </div>
        <div>
          <h4>Coverage</h4>
          <ul><li>Broward County</li><li>Miami-Dade County</li><li>Palm Beach County</li><li>Residential &amp; Commercial</li></ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="yr">2026</span> {BIZ} · Margate, FL</span>
        <span>Licensed &amp; Insured · Verify at myfloridalicense.com</span>
      </div>
    </div>
  </div>
</footer>
<a href="tel:{TEL}" class="fdme-cta btn float-call"><i class="ri-phone-fill"></i> Call {PHONE}</a>
<script src="/assets/js/wrp.js" defer></script>
</body>
</html>
'''

def biz_ld(path, extra=None):
    d = {"@context": "https://schema.org", "@type": ["RoofingContractor", "HomeAndConstructionBusiness"],
         "name": BIZ, "alternateName": "WRP", "url": DOMAIN + path, "telephone": TEL,
         "logo": DOMAIN + "/assets/brand/wrp-logo.png",
         "address": {"@type": "PostalAddress", "streetAddress": "1700 Banks Rd, Unit 50-B",
                     "addressLocality": "Margate", "addressRegion": "FL",
                     "postalCode": "33063", "addressCountry": "US"},
         "priceRange": "$$",
         "hasCredential": f"Florida Certified Roofing Contractor {LIC}",
         "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in
                        ("Broward County, Florida", "Miami-Dade County, Florida", "Palm Beach County, Florida")]}
    if extra: d.update(extra)
    return d

def write(path, html):
    full = os.path.join(ROOT, path.lstrip("/"))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  ✓ {path}  ({len(html)//1024} KB)")


# ───────────────────────────────────────────────────────── content ──

CITIES = [
    ("Fort Lauderdale", "fort-lauderdale"), ("Margate", "margate"), ("Coral Springs", "coral-springs"),
    ("Pompano Beach", "pompano-beach"), ("Hollywood", "hollywood"), ("Pembroke Pines", "pembroke-pines"),
    ("Plantation", "plantation"), ("Sunrise", "sunrise"), ("Tamarac", "tamarac"),
    ("Coconut Creek", "coconut-creek"), ("Deerfield Beach", "deerfield-beach"), ("Davie", "davie"),
    ("Weston", "weston"), ("Miramar", "miramar"), ("Parkland", "parkland"),
    ("Lauderhill", "lauderhill"), ("Oakland Park", "oakland-park"), ("North Lauderdale", "north-lauderdale"),
    ("Dania Beach", "dania-beach"), ("Hallandale Beach", "hallandale-beach"), ("Wilton Manors", "wilton-manors"),
    ("Cooper City", "cooper-city"), ("Lighthouse Point", "lighthouse-point"),
    ("Southwest Ranches", "southwest-ranches"), ("Lauderdale Lakes", "lauderdale-lakes"),
    ("Lauderdale-by-the-Sea", "lauderdale-by-the-sea"), ("West Park", "west-park"),
    ("Pembroke Park", "pembroke-park"), ("Hillsboro Beach", "hillsboro-beach"),
    ("Sea Ranch Lakes", "sea-ranch-lakes"),
]


def feature_grid(items, violet_first=True):
    out = []
    for i, (icon, h, p) in enumerate(items):
        pill = "icon-pill" if (i % 2 == 0) == violet_first else "icon-pill chrome-pill"
        out.append(f'''<div class="glass card hover-lift reveal">
        <div class="{pill}"><i class="{icon}"></i></div>
        <h3 class="h-display" style="margin:18px 0 10px"><span class="chrome">{h}</span></h3>
        <p>{p}</p></div>''')
    return f'<div class="grid-3">{"".join(out)}</div>'


def spec_table(rows, title):
    trs = "".join(
        f'<div class="glass card reveal" style="padding:22px"><h4 class="h-display" style="font-size:1.15rem;margin-bottom:8px">'
        f'<span class="chrome">{a}</span></h4><p style="font-size:14.5px">{b}</p></div>' for a, b in rows)
    return f'''<section class="sec"><div class="container">
    <div class="sec-head"><h2 class="h-display reveal"><span class="chrome">{title}</span></h2></div>
    <div class="grid-2">{trs}</div></div></section>'''


def cross_links(current):
    cards = {
      "roofing": ("/services/roofing.html", "ri-home-4-fill", "Roofing",
                  "Shingle, tile, metal and flat systems — repair, replacement and new construction."),
      "impact-windows": ("/services/impact-windows.html", "ri-window-2-fill", "Impact Windows",
                  "Florida-made hurricane-rated glass in single-hung, slider, casement and architectural shapes."),
      "impact-doors": ("/services/impact-doors.html", "ri-door-open-fill", "Impact Doors",
                  "Sliding glass, French and entry doors rated for wind-borne debris."),
      "financing": ("/financing.html", "ri-bank-card-fill", "Financing &amp; PACE",
                  "PACE assessments, conventional lending and credit-flexible programs."),
    }
    picks = [v for k, v in cards.items() if k != current][:3]
    inner = "".join(f'''<a href="{u}" class="glass card hover-lift reveal" style="display:block">
        <div class="icon-pill"><i class="{ic}"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">{t}</span></h3>
        <p style="font-size:14.5px">{d}</p>
        <span style="color:var(--violet);font-weight:600;font-size:14px;display:inline-block;margin-top:14px">Learn more <i class="ri-arrow-right-line"></i></span>
      </a>''' for u, ic, t, d in picks)
    return f'''<section class="sec"><div class="container">
      <div class="sec-head"><span class="eyebrow reveal">Also From WRP</span>
      <h2 class="h-display reveal"><span class="chrome">One contractor,<br>the whole envelope.</span></h2></div>
      <div class="grid-3">{inner}</div></div></section>'''


# ═══════════════════════════════════════════════════ PAGE: ROOFING ══

def build_roofing():
    path = "/services/roofing.html"
    faqs = [
      ("How do I know whether my roof needs repair or full replacement?",
       "Three things decide it: how much of the roof section is affected, the condition of the decking underneath, and how much service life the covering has left. Florida's 25% rule sets a hard limit — once more than a quarter of a roof section is repaired or replaced inside a twelve-month period, that whole section generally has to be brought up to current code. We give you the assessment in writing, with the reason, before anything is torn off."),
      ("Which roofing systems do you install?",
       "Asphalt shingle, concrete and clay tile, metal, and flat or low-slope membrane. Each suits a different building and budget: shingle is the cost-effective default, tile carries thermal benefits and the classic South Florida look, metal offers the longest service life with excellent wind and impact resistance, and membrane systems handle flat sections and commercial decks."),
      ("What is the High-Velocity Hurricane Zone and does it apply to me?",
       "Broward and Miami-Dade counties sit inside Florida's High-Velocity Hurricane Zone. Roofing in the HVHZ has to meet the strictest wind-uplift and wind-borne-debris provisions in the Florida Building Code — specific underlayment, rated fasteners, and inspection requirements that don't apply in most of the country. Every roof we install is permitted and inspected to those standards."),
      ("Do you handle storm damage and insurance documentation?",
       "Yes. We photograph and document conditions thoroughly so your adjuster has what they need, and we complete the wind-mitigation form that can reduce your premium. We are contractors, not public adjusters — we document what we find accurately and let the carrier make its determination."),
      ("How long does a roof replacement take?",
       "Most single-family homes are torn off and dried in within a day or two, with the full job typically running several days depending on size, system, and whether decking repairs are needed. Tile takes longer than shingle. Weather and inspection scheduling affect the calendar, and we tell you when either moves."),
      ("Can I finance a roof replacement?",
       "Yes. Roofing is one of the upgrades PACE was built to fund — repaid through a property tax assessment rather than a conventional loan, with approval leaning on equity and repayment ability rather than a credit-score minimum. Conventional financing and credit-flexible programs are also available. We confirm what your address qualifies for before you commit."),
    ]
    ld = [biz_ld(path), {"@context":"https://schema.org","@type":"Service","serviceType":"Roofing",
        "provider":{"@type":"RoofingContractor","name":BIZ,"telephone":TEL},
        "areaServed":{"@type":"AdministrativeArea","name":"Broward County, Florida"},
        "description":"Roof repair, replacement and new construction across South Florida — asphalt shingle, concrete and clay tile, metal, and flat membrane systems, permitted to Florida High-Velocity Hurricane Zone standards."},
        faq_ld(faqs)]

    html = head(
      "Roofing Contractor Broward County FL | Repair &amp; Replacement",
      f"Licensed Florida roofing contractor in Margate. Shingle, tile, metal and flat roof repair and replacement across Broward County. Free estimates. {PHONE}.",
      path,
      "roofing contractor Broward County, roof replacement Fort Lauderdale, tile roof Margate FL, metal roofing South Florida, flat roof repair Broward, roof leak repair Coral Springs",
      ld, og_title=f"Roofing — Repair, Replacement &amp; New Construction | {BIZ}")

    html += NAV
    html += page_hero(
      "Roofing · Broward · Miami-Dade · Palm Beach",
      "Roofs engineered",
      "for Florida weather.",
      f"Shingle, tile, metal and flat systems — repaired, replaced and permitted to High-Velocity Hurricane Zone standards by a Florida Certified Roofing Contractor (license {LIC}).",
      [("Home","/"),("Roofing",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass stats reveal">
    <div class="stat"><div class="stat-value chrome">4</div><div class="stat-label">Roof Systems Installed</div></div>
    <div class="stat"><div class="stat-value violet-text">HVHZ</div><div class="stat-label">Code Compliant</div></div>
    <div class="stat"><div class="stat-value chrome">A+</div><div class="stat-label">BBB Accredited</div></div>
    <div class="stat"><div class="stat-value violet-text">$0</div><div class="stat-label">Estimate Cost</div></div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Systems</span>
    <h2 class="h-display reveal"><span class="chrome">Every roof South Florida uses.</span></h2>
    <p class="lead reveal">The right system depends on your building, your budget, and how long you plan to own the home — not on what a contractor happens to have on the truck.</p>
  </div>
  {feature_grid([
    ("ri-stack-line","Asphalt Shingle","The cost-effective South Florida default, available across a wide range of colors and architectural profiles. Modern shingle systems paired with HVHZ-rated underlayment and fastening perform far better than the 20-year-old roofs they replace."),
    ("ri-shapes-line","Concrete &amp; Clay Tile","The classic Florida look, with real thermal benefit — tile's air gap and mass slow heat transfer into the attic. Heavier and slower to install than shingle, and worth it on the right home."),
    ("ri-shield-flash-line","Metal","The longest service life of anything we install, with excellent wind uplift and impact resistance. Higher up-front cost, lowest lifetime cost per year on a home you intend to keep."),
    ("ri-layout-row-line","Flat &amp; Low-Slope","Membrane systems for flat sections, additions, and commercial decks. Flat roofs fail at details — seams, drains, penetrations — so this is where installation quality matters most."),
    ("ri-drop-line","Leak Diagnosis &amp; Repair","Water rarely enters where it appears inside. We trace the actual entry point — flashing, pipe boots, valleys, failed sealant — rather than patching the ceiling stain and hoping."),
    ("ri-building-2-line","New Construction","Roofing for additions, new builds and commercial projects, coordinated with your GC and permitted through the local building department."),
  ])}
</div></section>

{spec_table([
  ("The 25% rule, plainly", "Florida Building Code limits how much of a roof section can be repaired before the entire section must be brought current. Cross 25% inside twelve months and a patch becomes a code-required section replacement. Knowing where you stand <em>before</em> the tear-off is the difference between a planned expense and a surprise."),
  ("Decking is the part nobody quotes", "On older Broward homes, the sheathing under the covering has absorbed decades of South Florida rain. We probe and inspect the deck on every opened roof and put any required replacement on the written estimate rather than discovering it mid-job."),
  ("Permits and inspections", "Each Broward municipality issues its own roofing permits and runs its own inspections, so timelines differ city to city. We pull the permit under our license and carry the job through final inspection — including the wind-mitigation form your insurer wants."),
  ("Roof age and your policy", "Florida carriers increasingly price, condition, or decline coverage based on roof age and condition. If a renewal notice is what brought you here, tell us — it changes which options actually solve your problem."),
], "What actually decides your roof job")}

{faq_block("Roofing questions,<br>answered straight.", faqs)}
{cross_links("roofing")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ══════════════════════════════════════════ PAGE: IMPACT WINDOWS ══

def build_windows():
    path = "/services/impact-windows.html"
    faqs = [
      ("Do impact windows lower my homeowners insurance?",
       "In most cases yes. Florida carriers price wind-mitigation credits into premiums, and opening protection is one of the largest single credits available. After installation and permitting, a wind-mitigation inspection documents the upgrade for your carrier. The size of the credit depends on your policy, your roof, and how much of the home's openings are protected — protecting every opening generally earns more than protecting some."),
      ("What is the difference between impact glass and hurricane shutters?",
       "Shutters have to be deployed. Impact windows are always in place — which matters when a storm forms fast, when you are out of town, and every ordinary day of the year for noise, UV, security, and energy. Laminated impact glass is designed to crack and hold on the interlayer rather than breaking through, keeping the building envelope sealed."),
      ("Are your impact windows made in Florida?",
       "Yes. Our windows and doors are manufactured in Florida and installed factory direct. That means shorter lead times, product built to Florida's High-Velocity Hurricane Zone requirements rather than a generic national spec, and one fewer layer of markup between the plant and your home."),
      ("Which window styles do you install?",
       "Single-hung, horizontal sliders including XOX three-panel configurations, casements that open fully for ventilation, and architectural shapes and picture units for arches and feature openings. Most South Florida homes end up with a mix — sliders and single-hungs through the main elevations, casements where airflow matters."),
      ("Do impact windows really reduce noise and energy bills?",
       "Both are real, measurable secondary benefits. The laminated interlayer that stops debris also damps sound transmission, which is noticeable near a busy road or a flight path. And replacing old single-pane aluminum units reduces the heat load your air conditioning fights all summer. Neither benefit is the reason to buy them — but you get them every day, not just during a named storm."),
      ("How long does the whole process take?",
       "Manufacturing lead time is the long pole. Once measured, permitted and built, a typical single-family home installs in one to three days depending on opening count and whether stucco or trim repair is involved. We give you the real schedule at estimate time and tell you if the plant's queue moves."),
      ("Can impact windows be financed?",
       "Yes — impact windows are a qualifying PACE upgrade, repaid through a property tax assessment rather than a conventional loan, with approval based on equity and ability to repay rather than a credit-score minimum. Conventional and credit-flexible financing are also available. We confirm what your specific address qualifies for."),
    ]
    ld = [biz_ld(path), {"@context":"https://schema.org","@type":"Service","serviceType":"Impact Window Installation",
        "provider":{"@type":"RoofingContractor","name":BIZ,"telephone":TEL},
        "areaServed":{"@type":"AdministrativeArea","name":"Broward County, Florida"},
        "description":"Hurricane-rated impact window installation across South Florida — single-hung, horizontal slider and XOX, casement, and architectural shapes. Florida-manufactured and installed factory direct."},
        faq_ld(faqs)]

    html = head(
      "Impact Windows Broward County FL | Hurricane-Rated Glass",
      f"Florida-made hurricane impact windows installed factory direct across Broward County. Single-hung, slider, casement and custom shapes. Free estimate: {PHONE}.",
      path,
      "impact windows Broward County, hurricane windows Fort Lauderdale, impact windows Coral Springs, single hung impact window Margate, hurricane impact glass South Florida, impact window financing PACE",
      ld, og_title=f"Impact Windows — Florida-Made, Factory Direct | {BIZ}")

    html += NAV
    html += page_hero(
      "Impact Windows · Florida-Made · Factory Direct",
      "Glass that holds",
      "when the wind doesn't.",
      "Hurricane-rated laminated impact windows that stop wind-borne debris, cut outside noise, block UV, and reduce cooling load — manufactured in Florida and installed factory direct.",
      [("Home","/"),("Impact Windows",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass stats reveal">
    <div class="stat"><div class="stat-value chrome">HVHZ</div><div class="stat-label">Rated For Broward &amp; Dade</div></div>
    <div class="stat"><div class="stat-value violet-text">FL</div><div class="stat-label">Manufactured In Florida</div></div>
    <div class="stat"><div class="stat-value chrome">24/7</div><div class="stat-label">Protection, No Deployment</div></div>
    <div class="stat"><div class="stat-value violet-text">$0</div><div class="stat-label">Estimate Cost</div></div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Why Impact Glass</span>
    <h2 class="h-display reveal"><span class="chrome">Five benefits.<br>One installation.</span></h2>
    <p class="lead reveal">Storm protection is the headline. The reasons homeowners say they'd do it again are usually the other four.</p>
  </div>
  {feature_grid([
    ("ri-shield-flash-fill","Storm Protection","Laminated glass is engineered to crack and stay bonded to its interlayer rather than blow through. The envelope stays sealed, interior pressure stays normal, and the roof isn't fighting an internal push from below."),
    ("ri-shield-keyhole-line","Forced-Entry Resistance","The same interlayer that resists a flying roof tile resists a crowbar. Impact glass is markedly harder to breach than standard annealed or tempered glass — a security upgrade that runs year-round."),
    ("ri-volume-down-line","Noise Reduction","The laminate damps sound transmission. Near a busy road, a school, or an approach path, the difference in a bedroom is immediately obvious."),
    ("ri-temp-cold-line","Energy Efficiency","Replacing old single-pane aluminum units cuts the heat gain your A/C works against all summer. Lower load, steadier indoor temperature, less runtime."),
    ("ri-sun-cloudy-line","UV Blocking","Impact laminate blocks the great majority of ultraviolet light, which is what fades flooring, art and upholstery on the sun-facing side of a Florida home."),
    ("ri-money-dollar-circle-line","Insurance Credits","Opening protection is one of the largest wind-mitigation credits available to Florida homeowners. Once permitted and inspected, the upgrade is documented for your carrier."),
  ], violet_first=True)}
</div></section>

{spec_table([
  ("Single-hung", "The South Florida workhorse — bottom sash operates, top sash fixed. Clean sightlines, the widest size range, and the most cost-effective way to protect a lot of openings at once."),
  ("Horizontal slider &amp; XOX", "Two-panel sliders and three-panel XOX configurations for wide openings. Ideal on long elevations and where a taller unit would be awkward to operate."),
  ("Casement", "Cranks fully open on a side hinge, so you get the entire opening for ventilation rather than half of it. The right choice where cross-breeze matters or where a window sits above a counter."),
  ("Architectural shapes", "Arches, half-rounds, trapezoids and fixed picture units for feature openings and gable walls — impact-rated, matched to the operable units beside them."),
], "Styles we install")}

<section class="sec"><div class="container">
  <div class="glass-violet reveal" style="padding:clamp(28px,4.5vw,54px)">
    <span class="eyebrow">Whole-Home vs. Partial</span>
    <h2 class="h-display" style="margin:18px 0 16px"><span class="chrome">Protecting some openings<br>is not protecting the home.</span></h2>
    <p class="lead">Wind doesn't dismantle a house from the outside. It finds one unprotected opening, gets inside, pressurizes the interior, and pushes outward on the roof and walls at the same moment the storm is pushing in. A single unprotected slider or garage-adjacent window can undo the protection everywhere else — and insurance credits generally scale with how completely the openings are covered.</p>
    <p style="margin-top:14px">If budget means phasing the work, we'll tell you honestly which openings to do first — largest, most exposed, most likely to be struck — rather than quoting whatever is easiest to install.</p>
    <a href="#estimate" class="fdme-cta btn" style="margin-top:24px">Price my openings <i class="ri-arrow-right-up-line"></i></a>
  </div>
</div></section>

{faq_block("Impact window questions,<br>answered straight.", faqs)}
{cross_links("impact-windows")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ════════════════════════════════════════════ PAGE: IMPACT DOORS ══

def build_doors():
    path = "/services/impact-doors.html"
    faqs = [
      ("Why do doors matter more than windows for storm protection?",
       "A door is usually the largest single opening in the building envelope, and sliding glass doors are the largest of all. That makes them the highest-consequence failure point: the bigger the breach, the faster the interior pressurizes. Homes with excellent impact windows and an unprotected slider are protected everywhere except where it matters most."),
      ("What types of impact doors do you install?",
       "Sliding glass doors including multi-panel and pocket configurations, French doors in both in-swing and out-swing, and impact-rated entry doors with rated hardware. All are Florida-manufactured and installed factory direct, matched to the impact windows around them."),
      ("Does an impact door include the frame and hardware?",
       "It has to. An impact door assembly is rated as a system — glass, frame, anchoring, and hardware together. Rated glass in an unrated frame, or an impact door hung on ordinary hardware, is not an impact-rated opening and will not be documented as one on a wind-mitigation inspection."),
      ("Will impact doors reduce noise and energy loss the way windows do?",
       "Yes, and often more noticeably — because doors are large and older sliders are frequently the leakiest openings in a Florida home. Replacing a worn aluminum slider typically produces the single biggest change in comfort and outside noise of any opening in the house."),
      ("Can I do doors now and windows later, or vice versa?",
       "You can, and sometimes budget requires it. We'll tell you honestly which openings to protect first based on size and exposure. Just know that insurance wind-mitigation credits generally reward complete opening protection, so a phased plan may not produce the premium change until the last openings are done."),
      ("Are impact doors covered by financing?",
       "Yes — impact doors qualify under PACE alongside windows and roofing, repaid through a property tax assessment rather than a conventional loan. Conventional and credit-flexible programs are also available. We confirm eligibility for your specific address before anything is signed."),
    ]
    ld = [biz_ld(path), {"@context":"https://schema.org","@type":"Service","serviceType":"Impact Door Installation",
        "provider":{"@type":"RoofingContractor","name":BIZ,"telephone":TEL},
        "areaServed":{"@type":"AdministrativeArea","name":"Broward County, Florida"},
        "description":"Hurricane-rated impact door installation across South Florida — sliding glass, French and entry doors, Florida-manufactured and installed factory direct."},
        faq_ld(faqs)]

    html = head(
      "Impact Doors Broward County FL | Sliding, French &amp; Entry",
      f"Hurricane-rated impact doors across Broward County — sliding glass, French and entry, Florida-made and factory direct. Free estimates. Call {PHONE}.",
      path,
      "impact doors Broward County, impact sliding glass doors Fort Lauderdale, hurricane French doors South Florida, impact entry door Margate FL, impact door installation Coral Springs",
      ld, og_title=f"Impact Doors — Sliding Glass, French &amp; Entry | {BIZ}")

    html += NAV
    html += page_hero(
      "Impact Doors · Florida-Made · Factory Direct",
      "The biggest opening",
      "deserves the strongest door.",
      "Impact-rated sliding glass, French and entry door systems — glass, frame, anchoring and hardware rated together, so the largest opening in your home stops being the weakest one.",
      [("Home","/"),("Impact Doors",None)])

    html += f'''
<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Door Systems</span>
    <h2 class="h-display reveal"><span class="chrome">Three ways to close the gap.</span></h2>
  </div>
  {feature_grid([
    ("ri-layout-right-line","Sliding Glass Doors","Multi-panel and pocket configurations for patios, lanais and rear elevations. Modern impact sliders operate more smoothly than the worn aluminum units they replace and seal far better against air and water."),
    ("ri-door-lock-line","French Doors","In-swing and out-swing, single or paired, with impact-rated glass and rated multi-point hardware. The classic look with none of the structural compromise."),
    ("ri-door-open-line","Impact Entry Doors","Front and side entries with rated glass, frames and hardware. The opening most visitors — and most intruders — approach first."),
    ("ri-shield-check-line","System-Rated Assemblies","Glass, frame, anchoring and hardware are approved as one assembly. We install the complete rated system, which is what a wind-mitigation inspection actually credits."),
    ("ri-links-line","Matched To Your Windows","Doors specified alongside your impact windows so finishes, glass tint and sightlines read as one package rather than a patchwork of jobs."),
    ("ri-flashlight-line","Everyday Payoff","Security, sound damping, UV blocking and reduced air leakage — the same benefits as impact windows, on the largest openings in the house."),
  ], violet_first=False)}
</div></section>

{spec_table([
  ("Why the frame matters as much as the glass", "An impact door is rated as a complete assembly. Rated glass in an unrated frame — or a rated door on ordinary hardware — is not an impact opening, will not perform like one, and will not be documented as one on a wind-mitigation inspection."),
  ("Sliders are the highest-consequence opening", "A multi-panel slider can be the largest single area of glass in the building. If storm protection is being phased, the slider is almost always the opening to do first."),
  ("Installation is where doors are won or lost", "Anchoring into sound substrate, correct shimming, proper flashing and sealing at the sill. A perfectly good door assembly installed carelessly leaks air, water, or both — and no warranty covers that."),
  ("Permits and inspection", "Impact door replacement is permitted work in Broward. We pull the permit under our license and carry the job through final inspection, then provide the documentation your insurer needs."),
], "What separates a good door job")}

{faq_block("Impact door questions,<br>answered straight.", faqs)}
{cross_links("impact-doors")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ═══════════════════════════════════════════════ PAGE: FINANCING ══

def build_financing():
    path = "/financing.html"
    faqs = [
      ("What exactly is PACE financing?",
       "P.A.C.E. stands for Property Assessed Clean Energy. It funds qualifying resilience and efficiency upgrades — roofing, impact windows, impact doors and related work — and is repaid through an assessment added to your property tax bill rather than through a conventional loan payment. Because the obligation attaches to the property rather than to a personal credit line, approval leans on home equity and ability to repay rather than a credit-score minimum."),
      ("Does PACE have a minimum credit score?",
       "PACE programs generally do not underwrite on a credit-score cutoff the way a conventional lender does. They weigh property equity, tax and mortgage payment history, and ability to repay. That is why PACE reaches homeowners who conventional lending turns away — but it also means it is not automatic, and it is not the right answer for everyone."),
      ("How long are PACE terms and is there money down?",
       "Terms commonly extend up to 20 years, and many programs require no money down for qualified applicants, with the first payment deferred until the next property tax cycle. The exact term, rate and structure depend on the program available in your county or city and on the scope of the work."),
      ("What is the catch with PACE?",
       "It is worth understanding before you sign: the assessment attaches to the property and appears on your tax bill, which can affect refinancing or sale — some mortgage lenders require the assessment be paid off at closing. Total cost over a 20-year term can exceed a shorter conventional loan. We would rather you understand that up front than be surprised later. Read your program documents, and ask us anything that isn't clear."),
      ("What if I would rather use conventional financing?",
       "Then use it. Conventional home improvement lending, and credit-flexible programs for borrowers who don't qualify for prime rates, are both available through us. For homeowners with strong credit and equity, a conventional product or a HELOC through your own bank is often the cheaper path — and we will say so."),
      ("Is my property eligible?",
       "PACE availability depends on whether your specific county or municipality has adopted a program, so eligibility is address-specific. We check it for you as part of the free estimate, before you commit to anything."),
    ]
    ld = [biz_ld(path), faq_ld(faqs)]
    html = head(
      "Roof &amp; Impact Window Financing FL | PACE &amp; Conventional",
      f"PACE, conventional and credit-flexible financing for roofing and impact windows in South Florida. $0 down for qualified applicants. Call {PHONE}.",
      path,
      "PACE financing Florida roof, impact window financing Broward, roof financing no money down Florida, PACE roofing Broward County, hurricane window financing bad credit Florida",
      ld, og_title=f"Financing — PACE, Conventional &amp; Credit-Flexible | {BIZ}")

    html += NAV
    html += page_hero(
      "Financing · PACE · Conventional · Credit-Flexible",
      "Protection shouldn't",
      "wait for savings.",
      "Most homeowners don't have a roof or a whole-home window package sitting in a savings account. Financing exists so protection happens before the storm, not after the claim.",
      [("Home","/"),("Financing",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass stats reveal">
    <div class="stat"><div class="stat-value chrome">$0</div><div class="stat-label">Down, Qualified Applicants</div></div>
    <div class="stat"><div class="stat-value violet-text">20yr</div><div class="stat-label">Terms Commonly Available</div></div>
    <div class="stat"><div class="stat-value chrome">No</div><div class="stat-label">Credit-Score Minimum (PACE)</div></div>
    <div class="stat"><div class="stat-value violet-text">3</div><div class="stat-label">Financing Paths</div></div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Three Paths</span>
    <h2 class="h-display reveal"><span class="chrome">Different homeowners,<br>different right answers.</span></h2>
    <p class="lead reveal">We are a PACE-approved contractor, but PACE is not automatically the best product for every homeowner. Here is the honest comparison.</p>
  </div>
  {feature_grid([
    ("ri-government-line","P.A.C.E. Assessment","Funds roofing, impact windows and impact doors through an assessment on your property tax bill. Approval weighs equity and repayment ability rather than a credit score. Terms commonly up to 20 years, often no money down. Best for homeowners with equity whom conventional lending won't reach."),
    ("ri-bank-line","Conventional Financing","Standard home-improvement lending at conventional rates and terms. Usually the lowest total cost for borrowers with strong credit — and it doesn't attach anything to your property tax bill. Best for homeowners who qualify comfortably."),
    ("ri-user-heart-line","Credit-Flexible Programs","Lending options built for borrowers who don't clear prime-rate underwriting. Rates are higher than conventional; the trade is access. Best when PACE isn't available at your address and conventional says no."),
  ])}
</div></section>

{spec_table([
  ("What PACE is good at", "Reaching homeowners with equity but imperfect credit, spreading a large resilience project over a long term, and requiring nothing at signing. For a family facing a non-renewal notice and a 22-year-old roof, it is frequently the only path that closes the gap in time."),
  ("What you should know before signing", "The assessment attaches to the property and appears on your tax bill. Some mortgage lenders require it be paid off at refinance or sale. Total cost across a long term can exceed a shorter conventional loan. None of that makes PACE wrong — it makes it a decision you should make with the numbers in front of you."),
  ("How we handle it", "We check whether PACE is even available at your address, lay the options side by side with real numbers on your actual scope, and tell you when conventional lending through your own bank would cost you less. Then you decide."),
  ("Insurance interaction", "Financing the work is only half the arithmetic. Impact openings and a new roof can move your homeowners premium and, in some cases, your insurability. Factor the premium change into the monthly comparison — sometimes it materially changes which option is cheaper."),
], "The honest version")}

{faq_block("Financing questions,<br>answered straight.", faqs)}
{cross_links("financing")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ════════════════════════════════════════════ PAGE: SERVICE AREAS ══

def build_areas():
    path = "/service-areas.html"
    rows = "".join(
      f'''<div class="glass card reveal" style="padding:20px">
        <h3 class="h-display" style="font-size:1.25rem;margin-bottom:12px"><span class="chrome">{name}, FL</span></h3>
        <ul style="display:flex;flex-direction:column;gap:7px">
          <li><a href="/services/roofing.html" style="font-size:14px;color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> Roofing</a></li>
          <li><a href="/services/impact-windows.html" style="font-size:14px;color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> Impact Windows</a></li>
          <li><a href="/services/impact-doors.html" style="font-size:14px;color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> Impact Doors</a></li>
        </ul>
      </div>''' for name, slug in CITIES)

    ld = [biz_ld(path, {"areaServed": [{"@type": "City", "name": n + ", FL"} for n, _ in CITIES]})]
    html = head(
      "Service Areas | Broward, Miami-Dade &amp; Palm Beach FL",
      f"Windows Roofs Plus serves all of Broward plus Miami-Dade and Palm Beach — Fort Lauderdale, Coral Springs, Pompano Beach, Hollywood and more. {PHONE}.",
      path,
      "roofing contractor Broward County service area, impact windows Fort Lauderdale, impact windows Coral Springs, roofer Pompano Beach, impact doors Hollywood FL",
      ld)

    html += NAV
    html += page_hero(
      "Service Areas",
      "Based in Margate.",
      "Working the whole county.",
      "1700 Banks Rd sits near the center of Broward, which is why we can run a Coral Springs estimate and a Hollywood install in the same day. Service extends into Miami-Dade and Palm Beach County.",
      [("Home","/"),("Service Areas",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass reveal" style="padding:clamp(24px,4vw,44px)">
    <div class="grid-3" style="gap:24px">
      <div><div class="icon-pill"><i class="ri-map-pin-2-fill"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Broward County</span></h3>
        <p style="font-size:14.5px">Our home county and the core of our work — every municipality, residential and commercial.</p></div>
      <div><div class="icon-pill chrome-pill"><i class="ri-road-map-line"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Miami-Dade County</span></h3>
        <p style="font-size:14.5px">Also inside the High-Velocity Hurricane Zone, with its own product-approval requirements we build to.</p></div>
      <div><div class="icon-pill"><i class="ri-compass-3-line"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Palm Beach County</span></h3>
        <p style="font-size:14.5px">Service extends north into Palm Beach for roofing and impact projects.</p></div>
    </div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Broward Municipalities</span>
    <h2 class="h-display reveal"><span class="chrome">Every city we serve.</span></h2>
    <p class="lead reveal">Same crews, same licensing, same pricing across the county. Each municipality issues its own permits and runs its own inspections — we handle that end of it.</p>
  </div>
  <div class="grid-4">{rows}</div>
</div></section>

<section class="sec"><div class="container" style="max-width:820px">
  <div class="glass-violet reveal" style="padding:clamp(28px,4.5vw,50px);text-align:center">
    <h2 class="h-display"><span class="chrome">Not sure if you're in range?</span></h2>
    <p class="lead" style="margin-top:16px">Call and ask. If we're not the right fit for your address, we'll say so rather than waste your afternoon.</p>
    <div class="hero-cta" style="margin-top:26px">
      <a href="tel:{TEL}" class="fdme-cta btn btn-lg"><i class="ri-phone-fill"></i> {PHONE}</a>
      <a href="#estimate" class="btn btn-ghost btn-lg">Request an estimate</a>
    </div>
  </div>
</div></section>

{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ═════════════════════════════════════════════ PAGE: THANK YOU ══

def build_thanks():
    path = "/thank-you.html"
    html = head(
      f"Request Received | {BIZ}",
      "Your estimate request has been received. Windows Roofs Plus will be in touch shortly.",
      path)
    html = html.replace('<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">',
                        '<meta name="robots" content="noindex,follow">')
    html += NAV
    html += f'''
<section class="hero" style="min-height:70vh;display:flex;align-items:center">
  <div class="container" style="max-width:720px;text-align:center">
    <div class="icon-pill blur-in" style="width:74px;height:74px;flex:0 0 74px;font-size:34px;margin:0 auto 26px">
      <i class="ri-check-double-line"></i>
    </div>
    <h1 class="h-display blur-in" style="animation-delay:.12s;font-size:clamp(2.3rem,5.4vw,4rem)">
      <span class="chrome">Request received.</span><br><span class="violet-text">We'll be in touch.</span>
    </h1>
    <p class="lead blur-in" style="animation-delay:.26s;margin-top:22px">
      Thanks for reaching out to {BIZ}. Someone from our team will contact you shortly to schedule your free
      on-site estimate. If it's urgent — an active leak or storm damage — call us directly and we'll move you up.
    </p>
    <div class="hero-cta blur-in" style="animation-delay:.38s">
      <a href="tel:{TEL}" class="fdme-cta btn btn-lg"><i class="ri-phone-fill"></i> {PHONE}</a>
      <a href="/" class="btn btn-ghost btn-lg">Back to home</a>
    </div>
    <div class="glass reveal" style="padding:26px;margin-top:44px;text-align:left">
      <h3 class="h-display" style="font-size:1.3rem;margin-bottom:12px"><span class="chrome">While you wait</span></h3>
      <ul style="display:flex;flex-direction:column;gap:10px">
        <li style="font-size:14.5px"><a href="/financing.html" style="color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> How PACE and conventional financing compare</a></li>
        <li style="font-size:14.5px"><a href="/services/impact-windows.html" style="color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> What impact windows actually do for your insurance</a></li>
        <li style="font-size:14.5px"><a href="/services/roofing.html" style="color:var(--ink-2)"><i class="ri-arrow-right-s-line" style="color:var(--violet-2)"></i> Florida's 25% roof rule, explained</a></li>
      </ul>
    </div>
  </div>
</section>
{FOOTER}'''
    write(path, html)


# ════════════════════════════════════════════════ SITEMAP / MISC ══

def build_sitemap():
    urls = ["/", "/services/roofing.html", "/services/impact-windows.html",
            "/services/impact-doors.html", "/financing.html", "/service-areas.html"]
    prio = {"/": "1.0"}
    body = "".join(
      f'<url><loc>{DOMAIN}{u if u != "/" else "/"}</loc><lastmod>{TODAY}</lastmod>'
      f'<changefreq>weekly</changefreq><priority>{prio.get(u, "0.8")}</priority></url>\n' for u in urls)
    write("/sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + body + '</urlset>\n')

    write("/robots.txt", f"""User-agent: *
Allow: /
Disallow: /thank-you.html

# AI crawlers welcome
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
""")

    write("/llms.txt", f"""# {BIZ}

> Licensed South Florida exterior contractor specializing in roofing, impact windows,
> and impact doors. Based in Margate, FL. Serving Broward County primarily, with service
> into Miami-Dade and Palm Beach County.

## Company
- Legal name: {BIZ}
- Address: {ADDR}
- Phone: {PHONE}
- Website: {DOMAIN}
- License: Florida Certified Roofing Contractor {LIC} (verify at myfloridalicense.com)
- BBB: Accredited, A+ rating
- Tagline: Protect · Enhance · Add Value — Built for Florida

## Services
- Roofing: repair, replacement, new construction. Asphalt shingle, concrete and clay tile,
  metal, flat and low-slope membrane. Permitted to Florida High-Velocity Hurricane Zone code.
- Impact windows: single-hung, horizontal slider and XOX, casement, architectural shapes.
  Manufactured in Florida, installed factory direct.
- Impact doors: sliding glass (multi-panel and pocket), French (in-swing and out-swing),
  impact-rated entry doors. Florida-manufactured, factory direct.

## Financing
- P.A.C.E. (Property Assessed Clean Energy): repaid via property tax assessment, approval
  based on equity and ability to repay rather than a credit-score minimum, terms commonly
  up to 20 years, $0 down for qualified applicants. Availability is address-specific.
- Conventional home-improvement financing.
- Credit-flexible programs for borrowers outside prime underwriting.

## Pages
- {DOMAIN}/ — overview, services, financing, service areas, FAQ, estimate request
- {DOMAIN}/services/roofing.html — roofing systems, 25% rule, HVHZ code, permits
- {DOMAIN}/services/impact-windows.html — styles, insurance credits, energy, noise, UV
- {DOMAIN}/services/impact-doors.html — sliding glass, French, entry; system ratings
- {DOMAIN}/financing.html — PACE vs conventional vs credit-flexible, honest tradeoffs
- {DOMAIN}/service-areas.html — Broward municipalities served

## Notes for AI assistants
- Estimates are free. The fastest path for a homeowner is calling {PHONE}.
- We are contractors, not public adjusters or insurance agents. We document conditions
  accurately; carriers make coverage determinations.
- Warranty terms are stated in the written contract: manufacturer coverage on products,
  workmanship coverage stated explicitly. Ask for it in writing.
""")

    write("/vercel.json", json.dumps({
        "framework": None, "cleanUrls": True, "trailingSlash": False,
        "redirects": [
            {"source": "/roofing", "destination": "/services/roofing.html", "permanent": True},
            {"source": "/impact-windows", "destination": "/services/impact-windows.html", "permanent": True},
            {"source": "/impact-doors", "destination": "/services/impact-doors.html", "permanent": True},
            {"source": "/windows", "destination": "/services/impact-windows.html", "permanent": True},
            {"source": "/doors", "destination": "/services/impact-doors.html", "permanent": True},
            {"source": "/contact", "destination": "/#estimate", "permanent": False},
            {"source": "/estimate", "destination": "/#estimate", "permanent": False},
        ],
        "headers": [
            {"source": "/sitemap.xml", "headers": [
                {"key": "Content-Type", "value": "application/xml; charset=utf-8"},
                {"key": "Cache-Control", "value": "public, max-age=3600"}]},
            {"source": "/assets/(.*)", "headers": [
                {"key": "Cache-Control", "value": "public, max-age=31536000, immutable"}]},
            {"source": "/(.*)", "headers": [
                {"key": "X-Content-Type-Options", "value": "nosniff"},
                {"key": "Referrer-Policy", "value": "strict-origin-when-cross-origin"},
                {"key": "X-Frame-Options", "value": "SAMEORIGIN"}]},
        ],
    }, indent=2) + "\n")


if __name__ == "__main__":
    print("Building windowsroofsplus.com …")
    build_roofing(); build_windows(); build_doors()
    build_financing(); build_areas(); build_thanks()
    build_sitemap()
    print("Done.")
