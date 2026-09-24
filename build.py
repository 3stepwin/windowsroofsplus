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
LIC2   = "21-CRP-22416-X"  # Broward Structural Carpentry Specialty Contractor
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
<a class="skip-link" href="#main">Skip to content</a>
'''

NAV = f'''
<div class="nav-wrap">
  <nav class="nav glass">
    <a href="/" class="nav-logo" aria-label="{BIZ} home">
      <img src="/assets/brand/wrp-nav.webp" alt="{BIZ} — Roofing, Impact Windows, Impact Doors" width="620" height="226">
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
  <div class="mobile-menu glass-strong" id="mobileMenu">
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
<main id="main">
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
          <div class="footer-logo"><img src="/assets/brand/wrp-mark.webp" alt="{BIZ}" width="900" height="328"></div>
          <p style="font-size:14.5px;font-weight:300;max-width:320px">Licensed South Florida roofing, impact window and gutter contractor. In business since 2013. Protect · Enhance · Add Value — built for Florida.</p>
          <p style="font-size:12.5px;color:var(--muted);margin-top:14px">FL Certified Roofing Contractor <strong style="color:var(--ink-2)">{LIC}</strong><br>Broward Structural Carpentry <strong style="color:var(--ink-2)">{LIC2}</strong><br>BBB Accredited · A+ Rating · 5★ Google</p>
        </div>
        <div>
          <h4>Services</h4>
          <ul>
            <li><a href="/services/roofing.html">Roofing</a></li>
            <li><a href="/services/impact-windows.html">Impact Windows</a></li>
            <li><a href="/services/impact-doors.html">Impact Doors</a></li>
            <li><a href="/#services">Seamless Gutters</a></li>
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
          <ul><li>Jupiter to Miami</li><li>Palm Beach County</li><li>Broward County</li><li>Miami-Dade County</li><li>Residential &amp; Commercial</li></ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© <span id="yr">2026</span> {BIZ} · Margate, FL</span>
        <span>Licensed &amp; Insured · Verify at myfloridalicense.com</span>
      </div>
    </div>
  </div>
</footer>
</main>
<a href="tel:{TEL}" class="fdme-cta btn float-call"><i class="ri-phone-fill"></i> Call {PHONE}</a>
<script src="/assets/js/wrp.js" defer></script>
</body>
</html>
'''

def biz_ld(path, extra=None):
    d = {"@context": "https://schema.org", "@type": ["RoofingContractor", "HomeAndConstructionBusiness"],
         "name": BIZ, "alternateName": "WRP", "url": DOMAIN + path, "telephone": TEL,
         "logo": DOMAIN + "/assets/brand/wrp-mark.png",
         "address": {"@type": "PostalAddress", "streetAddress": "1700 Banks Rd, Unit 50-B",
                     "addressLocality": "Margate", "addressRegion": "FL",
                     "postalCode": "33063", "addressCountry": "US"},
         "priceRange": "$$",
         "hasCredential": [f"Florida Certified Roofing Contractor {LIC}", f"Broward County Structural Carpentry Specialty Contractor {LIC2}"],
         "foundingDate": "2013",
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
                  "Shingle, tile, metal and flat — repairs, full replacements and new construction."),
      "impact-windows": ("/services/impact-windows.html", "ri-window-2-fill", "Impact Windows",
                  "High impact rated hurricane glass, in every style and shape your house has."),
      "impact-doors": ("/services/impact-doors.html", "ri-door-open-fill", "Impact Doors",
                  "Patio sliders, French doors and entry doors built to take a hit."),
      "financing": ("/financing.html", "ri-bank-card-fill", "Financing &amp; PACE",
                  "Ygrene PACE and GoodLeap conventional financing."),
    }
    picks = [v for k, v in cards.items() if k != current][:3]
    inner = "".join(f'''<a href="{u}" class="glass card hover-lift reveal" style="display:block">
        <div class="icon-pill"><i class="{ic}"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">{t}</span></h3>
        <p style="font-size:14.5px">{d}</p>
        <span style="color:var(--violet);font-weight:600;font-size:14px;display:inline-block;margin-top:14px">Learn more <i class="ri-arrow-right-line"></i></span>
      </a>''' for u, ic, t, d in picks)
    return f'''<section class="sec"><div class="container">
      <div class="sec-head"><span class="eyebrow reveal">We Also Do</span>
      <h2 class="h-display reveal"><span class="chrome">One company for<br>the whole outside.</span></h2></div>
      <div class="grid-3">{inner}</div></div></section>'''


# ═══════════════════════════════════════════════════ PAGE: ROOFING ══

def build_roofing():
    path = "/services/roofing.html"
    faqs = [
      ("How do I know if I need a repair or a whole new roof?",
       "It comes down to how much of the roof is affected, what shape the wood underneath is in, and how much life the roof has left. There's also a Florida rule that once repairs pass about a quarter of a section, that whole section has to be brought up to code. We look, we tell you in writing what we found and why, and you decide before anything comes off."),
      ("What kinds of roof do you do?",
       "Shingle, tile, metal, and flat. Shingle is the most affordable and the most common. Tile looks classic and keeps the house cooler. Metal lasts the longest and handles wind the best but costs more up front. Flat roofing is for flat sections, additions and commercial buildings. We'll tell you which makes sense for your house and your budget."),
      ("Does South Florida have stricter roofing rules?",
       "Yes. Broward and Miami-Dade have the toughest building requirements in the country for wind — stricter materials, stricter fastening, stricter inspections than almost anywhere else. That's a good thing for you as a homeowner, and every roof we put on is permitted and inspected to those standards."),
      ("Can you help with a storm damage claim?",
       "We photograph and document what we find on your roof. To be clear about what we are: we're roofers, not public adjusters. We record honestly what we find — your insurance company makes the decision."),
      ("How many days will my house be torn up?",
       "Most homes are stripped and watertight again within a day or two, with the whole job usually running several days depending on size and whether there's wood to replace underneath. Tile takes longer than shingle. Rain and inspection scheduling can move things, and we'll tell you the moment they do."),
      ("Can I pay for a roof monthly?",
       "Yes. We're Ygrene Certified for PACE financing, which isn't based on your credit score, and we offer conventional financing through GoodLeap. We check what your address qualifies for and show you the real payment before you agree to anything."),
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
      "Roofing · Jupiter to Miami",
      "Roofs built",
      "for Florida weather.",
      "Leaks, storm damage, or a roof that has simply reached the end of its life. Shingle, tile, metal and flat — we look at what you have, tell you straight whether it needs a repair or a replacement, and handle the permit with your city.",
      [("Home","/"),("Roofing",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass stats reveal">
    <div class="stat"><div class="stat-value chrome">4</div><div class="stat-label">Kinds Of Roof We Work On</div></div>
    <div class="stat"><div class="stat-value violet-text">Free</div><div class="stat-label">Roof Inspection</div></div>
    <div class="stat"><div class="stat-value chrome">A+</div><div class="stat-label">BBB Accredited</div></div>
    <div class="stat"><div class="stat-value violet-text">$0</div><div class="stat-label">Cost For An Estimate</div></div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Systems</span>
    <h2 class="h-display reveal"><span class="chrome">Every kind of roof<br>South Florida has.</span></h2>
    <p class="lead reveal">The right one depends on your house, your budget, and how long you plan to stay — not on what a contractor happens to have on the truck that week.</p>
  </div>
  {feature_grid([
    ("ri-stack-line","Shingle","The most common choice, and usually the most affordable. Plenty of colors and styles, and today's shingles hold up far better than the twenty-year-old roof they're replacing."),
    ("ri-shapes-line","Tile","The classic Florida look, and it actually keeps the house cooler — the air space under tile slows the heat coming into your attic. Costs more and takes longer to install, and on the right house it's worth it."),
    ("ri-shield-flash-line","Metal","Lasts the longest of anything we install and handles wind the best. It costs more up front, so it makes the most sense if you plan on staying in the house a long time."),
    ("ri-layout-row-line","Flat Roofs","For flat sections, additions and commercial buildings. Flat roofs almost always fail at the edges, seams and drains rather than in the middle — which is why who installs it matters more here than anywhere else."),
    ("ri-drop-line","Finding The Leak","Water almost never comes in directly above the stain on your ceiling. We track down where it's actually getting in and fix that, instead of patching the spot you can see and hoping."),
    ("ri-building-2-line","Additions &amp; Commercial","New construction, room additions and commercial buildings, coordinated with your builder and permitted with the city."),
  ])}
</div></section>

{spec_table([
  ("Why a patch can turn into a roof", "Florida has a rule: once repairs cover more than about a quarter of a section of roof within a year, that whole section has to be brought up to today's code. It catches a lot of homeowners by surprise mid-job. We tell you which side of that line you're on before anyone starts pulling shingles off."),
  ("The wood underneath", "On older homes there's often soft or rotted wood under the shingles that nobody sees until the roof comes off. We check for it and put it on the written estimate up front, so it isn't a phone call halfway through the job asking you for more money."),
  ("We deal with the city, not you", "Every city in Broward runs its own permits and inspections, and they don't all move at the same speed. We pull the permit and meet the inspector, so you don't have to."),
  ("If your insurance sent you a letter", "A lot of our calls start with a renewal notice or a non-renewal letter about the age of the roof. Tell us that up front — it changes what actually solves your problem, and sometimes there's a deadline attached."),
], "What homeowners actually ask us")}

{faq_block("Roofing questions,<br>answered straight.", faqs)}
{cross_links("roofing")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ══════════════════════════════════════════ PAGE: IMPACT WINDOWS ══

def build_windows():
    path = "/services/impact-windows.html"
    faqs = [
      ("Will this lower my insurance?",
       "Usually, yes. Protecting your windows and doors earns one of the bigger discounts Florida insurers give. Once the work is inspected, an inspector fills out a form your insurance company uses to apply it. How much depends on your policy and your roof, and covering every opening is worth more than covering some. We won't promise you a number we don't control."),
      ("How is this different from hurricane shutters?",
       "Somebody has to put shutters up. That means being home, being able to climb a ladder, and having the warning to do it — and then living in the dark until you take them down. Impact windows are just your windows. Nothing to store, nothing to install at the last minute, nothing to do if a storm forms while you're out of town. And they're working on the noise and your power bill the other 360 days."),
      ("What windows do you use?",
       "High impact rated windows. We work with more than one manufacturer, so we pick the right product for your house and your budget instead of forcing one brand on every job."),
      ("What styles can I get?",
       "Single-hung, which is the most common here. Sliders that go side to side. Casements that crank all the way open for a breeze. Big fixed picture windows, and arches or angled shapes if your house has them. Most homes end up with a mix, and we'll walk the house with you and work out what goes where."),
      ("Is the quieter-and-cooler part real, or just sales talk?",
       "It's real. The same layer inside the glass that stops debris also deadens sound, and it's obvious if you live near a road or under a flight path. And swapping out old single-pane aluminum windows takes a real load off your air conditioning in the summer. Neither is the reason people call us — but they're what people mention a year later."),
      ("How long does the whole thing take?",
       "Most of the wait is on the window order, not at your house. Once everything's measured, permitted and built, a typical home takes one to three days depending on how many windows there are and whether there's stucco work around them. We give you a real date up front and tell you right away if it changes."),
      ("Can I pay monthly?",
       "Yes. We're Ygrene Certified for PACE financing, which isn't based on your credit score, and we offer conventional financing through GoodLeap. We check what your address qualifies for and show you the actual payment first."),
    ]
    ld = [biz_ld(path), {"@context":"https://schema.org","@type":"Service","serviceType":"Impact Window Installation",
        "provider":{"@type":"RoofingContractor","name":BIZ,"telephone":TEL},
        "areaServed":{"@type":"AdministrativeArea","name":"Broward County, Florida"},
        "description":"Hurricane-rated impact window installation across South Florida — single-hung, horizontal slider and XOX, casement, and architectural shapes. High impact rated, installed by our own crew."},
        faq_ld(faqs)]

    html = head(
      "Impact Windows Broward County FL | Hurricane-Rated Glass",
      f"High impact rated hurricane windows installed by our own crew from Jupiter to Miami. Single-hung, slider, casement and custom shapes. Free estimate: {PHONE}.",
      path,
      "impact windows Broward County, hurricane windows Fort Lauderdale, impact windows Coral Springs, single hung impact window Margate, hurricane impact glass South Florida, impact window financing PACE",
      ld, og_title=f"Impact Windows — High Impact Rated | {BIZ}")

    html += NAV
    html += page_hero(
      "Impact Windows · High Impact Rated · Jupiter to Miami",
      "Glass that holds",
      "when the wind doesn't.",
      "Windows built to take a hit from whatever the storm throws at them — and in the meantime, a quieter house, lower power bills, and floors that stop fading. High impact rated, installed by our own crew.",
      [("Home","/"),("Impact Windows",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass stats reveal">
    <div class="stat"><div class="stat-value chrome">365</div><div class="stat-label">Days A Year You Benefit</div></div>
    <div class="stat"><div class="stat-value violet-text">2013</div><div class="stat-label">In Business Since</div></div>
    <div class="stat"><div class="stat-value chrome">0</div><div class="stat-label">Shutters To Put Up</div></div>
    <div class="stat"><div class="stat-value violet-text">$0</div><div class="stat-label">Estimate Cost</div></div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Why Impact Glass</span>
    <h2 class="h-display reveal"><span class="chrome">Storm protection is<br>only half the reason.</span></h2>
    <p class="lead reveal">Everybody buys them for hurricane season. What homeowners actually talk about afterward is how much quieter and cooler the house got.</p>
  </div>
  {feature_grid([
    ("ri-shield-flash-fill","It Doesn't Blow Through","There's a tough clear layer bonded inside the glass. Something hits it hard enough, the glass cracks — but it stays in the frame. The wind and rain stay outside, which is the whole point."),
    ("ri-shield-keyhole-line","Harder To Break Into","The same layer that stops a flying roof tile also stops a crowbar. It takes a long, loud effort to get through impact glass — long enough that most people give up. That protection is there every night, not just in September."),
    ("ri-volume-down-line","A Quieter House","If you live near a busy road, a school, or under a flight path, this is the one people notice first. Close the window and the outside gets a lot further away."),
    ("ri-temp-cold-line","Cooler In Summer","Old single-pane windows let the heat pour in and the cold air you paid for leak out. New ones mean the A/C runs less, the house stays evenly cool, and the August bill stops being a shock."),
    ("ri-sun-cloudy-line","Your Floors Stop Fading","Impact glass blocks most of the sunlight that bleaches wood floors, rugs and furniture on the sunny side of the house. If you've got a faded stripe across the living room, that's what did it."),
    ("ri-money-dollar-circle-line","A Discount On Your Policy","Protecting your windows and doors earns one of the bigger discounts Florida insurers offer. Ask your insurance agent how much it could take off your premium."),
  ], violet_first=True)}
</div></section>

{spec_table([
  ("Single-hung", "The most common window in South Florida. The bottom half slides up, the top half stays put. Comes in the widest range of sizes and it's the most affordable way to do a whole house at once."),
  ("Sliders", "Slides side to side instead of up and down. Good for wide openings and for windows over a counter or a sink where reaching up to lift one would be awkward."),
  ("Casement", "Opens all the way out on a hinge with a crank handle, so you get the whole opening for a breeze instead of half of it. Nice where you actually want air moving through."),
  ("Arches &amp; custom shapes", "Half-rounds, arches, angled tops and big fixed picture windows. If your house has an unusual shape up high, it can still be done — and matched to the windows around it."),
], "Which kind goes where")}

<section class="sec"><div class="container">
  <div class="glass-violet reveal" style="padding:clamp(28px,4.5vw,54px)">
    <span class="eyebrow">Doing Some vs. Doing All</span>
    <h2 class="h-display" style="margin:18px 0 16px"><span class="chrome">One window left out<br>undoes the rest.</span></h2>
    <p class="lead">Wind only needs one way in. If it finds a single window or door that gave way, it gets inside and starts pushing on the roof and walls from within — while the storm is still pushing from outside. The eleven windows you did protect don't help much at that point. Insurance discounts work the same way: covering everything is worth more than covering most things.</p>
    <p style="margin-top:14px">If the budget means doing it in stages, we'll tell you honestly which ones to do first — the biggest and most exposed — instead of quoting whatever happens to be easiest for us to install.</p>
    <a href="#estimate" class="fdme-cta btn" style="margin-top:24px">Get my price <i class="ri-arrow-right-up-line"></i></a>
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
      ("Why do the doors if I already did the windows?",
       "Because the slider is usually the biggest piece of glass in the house. If it goes, the wind is inside — and the windows you already paid for don't change that. It's the one opening that can undo all the others."),
      ("What kinds of doors do you do?",
       "Patio sliders, including the wide multi-panel ones. French doors that open in or out. Front and side entry doors. All high impact rated, and matched to your windows so it looks like one job."),
      ("Do you replace the frame too, or just the glass?",
       "The whole thing — frame, glass and locks. It has to be, because strong glass in a weak frame won't hold and won't count toward your insurance discount. If someone offers you a cheap price to swap only the glass, now you know why it's cheap."),
      ("Will I notice a difference day to day?",
       "More than with the windows, usually. Old sliders are the leakiest thing in most Florida houses — that draft along the floor is real. Replacing one is often the single biggest change in comfort and noise anywhere in the house."),
      ("Can I do the doors now and windows later?",
       "You can, and plenty of people do it that way for budget reasons. We'll tell you honestly which to do first. One thing to know going in: the insurance discount generally rewards protecting everything, so you may not see the premium change until the last opening is done."),
      ("Can doors be financed too?",
       "Yes, the same way as windows and roofing — including the option you repay through your property tax bill. We check what your address qualifies for before anything gets signed."),
    ]
    ld = [biz_ld(path), {"@context":"https://schema.org","@type":"Service","serviceType":"Impact Door Installation",
        "provider":{"@type":"RoofingContractor","name":BIZ,"telephone":TEL},
        "areaServed":{"@type":"AdministrativeArea","name":"Broward County, Florida"},
        "description":"Hurricane-rated impact door installation across South Florida — sliding glass, French and entry doors, high impact rated and installed by our own crew."},
        faq_ld(faqs)]

    html = head(
      "Impact Doors Broward County FL | Sliding, French &amp; Entry",
      f"Hurricane-rated impact doors from Jupiter to Miami — sliding glass, French and entry, high impact rated. Free estimates. Call {PHONE}.",
      path,
      "impact doors Broward County, impact sliding glass doors Fort Lauderdale, hurricane French doors South Florida, impact entry door Margate FL, impact door installation Coral Springs",
      ld, og_title=f"Impact Doors — Sliding Glass, French &amp; Entry | {BIZ}")

    html += NAV
    html += page_hero(
      "Impact Doors · High Impact Rated · Jupiter to Miami",
      "The biggest opening",
      "deserves the strongest door.",
      "Your patio slider is usually the largest piece of glass in the house, and the one people forget after they've done the windows. We replace the whole thing — frame, glass and locks — so the weakest spot stops being the weakest spot.",
      [("Home","/"),("Impact Doors",None)])

    html += f'''
<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Door Systems</span>
    <h2 class="h-display reveal"><span class="chrome">Three doors people<br>usually forget about.</span></h2>
  </div>
  {feature_grid([
    ("ri-layout-right-line","Patio Sliders","For the back of the house and the lanai, including the really wide ones. A nice side effect: new sliders actually slide. If you've been shoving yours with two hands for years, you'll notice that first."),
    ("ri-door-lock-line","French Doors","Single or double, opening in or out, with heavy locks that catch in several places instead of just one. Same classic look, far stronger than it used to be."),
    ("ri-door-open-line","Front &amp; Side Doors","The door everyone walks up to — including the people you don't want walking up to it. Stronger glass, stronger frame, stronger locks."),
    ("ri-shield-check-line","The Whole Door, Not Just Glass","A door is only as strong as its frame, its anchors and its locks. We replace all of it together, because that's the only way it counts — with the storm and with your insurance company."),
    ("ri-links-line","Matches Your Windows","We spec the doors alongside your windows so the color, the tint and the frames all match. It should look like one job, not three jobs done in different years."),
    ("ri-flashlight-line","You Feel It Daily","Quieter, cooler, more secure, and no more draft along the floor by the slider — the same benefits as the windows, on the biggest opening you have."),
  ], violet_first=False)}
</div></section>

{spec_table([
  ("Why the frame matters as much as the glass", "Strong glass in a weak frame is a weak door. It won't hold in a storm, and it won't count when the inspector comes out to document your discount. If someone quotes you a cheap price to swap only the glass, that's why."),
  ("Do the slider first", "It's the biggest piece of glass in most houses, so it's the one with the most to lose. If you're doing this in stages because of budget, start there."),
  ("Installation matters more than brand", "A good door installed carelessly leaks air, water, or both — and no manufacturer warranty covers a bad install. Anchored properly, sealed properly, level. It isn't glamorous but it's the whole job."),
  ("We deal with the city", "Replacing doors needs a permit in Broward. We pull it and we meet the inspector — that part is on us, not you."),
], "What actually matters here")}

{faq_block("Impact door questions,<br>answered straight.", faqs)}
{cross_links("impact-doors")}
{ESTIMATE}
{FOOTER}'''
    write(path, html)


# ═══════════════════════════════════════════════ PAGE: FINANCING ══

def build_financing():
    path = "/financing.html"
    faqs = [
      ("What financing do you offer?",
       "Two options. We're Ygrene Certified for PACE financing, and we offer conventional financing through GoodLeap. We'll go over both with you at the free estimate."),
      ("What is PACE?",
       "PACE is a program that pays for improvements like a roof, impact windows or impact doors, and you pay it back through your property tax bill instead of a regular loan. PACE approval isn't based on your credit score."),
      ("Is PACE right for everyone?",
       "No. PACE attaches to the property and shows up on your tax bill, and every program has its own rules. We'll put the options side by side for your actual job so you can decide with the real numbers in front of you."),
      ("Does my house qualify?",
       "PACE isn't offered in every city, so it comes down to your exact address. We check it for you when we come out to do the free estimate, before you've committed to anything."),
    ]
    ld = [biz_ld(path), faq_ld(faqs)]
    html = head(
      "Roof &amp; Impact Window Financing FL | Ygrene PACE &amp; GoodLeap",
      f"Financing for a new roof, impact windows or doors in South Florida — Ygrene Certified PACE, not based on credit score, and conventional financing through GoodLeap. Call {PHONE}.",
      path,
      "PACE financing Florida roof, Ygrene PACE roofing, GoodLeap roof financing, impact window financing South Florida, PACE roofing Broward County",
      ld, og_title=f"Financing For Your Roof, Windows Or Doors | {BIZ}")

    html += NAV
    html += page_hero(
      "Financing · Ygrene Certified · GoodLeap",
      "Financing for your",
      "roof, windows &amp; doors.",
      "Almost nobody has a new roof or a house full of windows sitting in the bank. We offer Ygrene PACE financing and conventional financing through GoodLeap, and we'll walk you through what you qualify for.",
      [("Home","/"),("Financing",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="grid-2" style="gap:24px">
    <div class="glass card reveal" style="padding:clamp(24px,3.5vw,40px);text-align:center">
      <img src="/assets/brand/partner-ygrene.webp" alt="Ygrene Certified — 100% Financing" width="386" height="188" loading="lazy" style="width:100%;max-width:300px;margin:0 auto 16px;border-radius:12px">
      <h3 class="h-display" style="font-size:1.6rem;margin-bottom:10px"><span class="chrome">Ygrene PACE</span></h3>
      <p style="font-size:15px">We're Ygrene Certified. PACE is repaid through your property tax bill, and approval isn't based on your credit score.</p>
    </div>
    <div class="glass card reveal" style="padding:clamp(24px,3.5vw,40px);text-align:center">
      <img src="/assets/brand/partner-goodleap.webp" alt="GoodLeap" width="515" height="220" loading="lazy" style="width:100%;max-width:300px;margin:0 auto 16px;border-radius:12px">
      <h3 class="h-display" style="font-size:1.6rem;margin-bottom:10px"><span class="chrome">GoodLeap</span></h3>
      <p style="font-size:15px">Conventional financing for your roof, impact windows and impact doors.</p>
    </div>
  </div>
</div></section>

{spec_table([
  ("How we handle it", "We check what's offered at your address, put the options side by side with real numbers for your actual job, and answer your questions. Then it's your call, not ours."),
  ("Every program has its own rules", "PACE and conventional financing each have their own requirements and terms. We'll go over them with you before you sign anything."),
], "How it works")}

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
      "Service Areas | Jupiter to Miami — Palm Beach, Broward &amp; Miami-Dade",
      f"Windows Roofs Plus works from Jupiter to Miami — Palm Beach, Broward and Miami-Dade, including Fort Lauderdale, Coral Springs, Pompano Beach, Hollywood and more. {PHONE}.",
      path,
      "roofing contractor Broward County service area, impact windows Fort Lauderdale, impact windows Coral Springs, roofer Pompano Beach, impact doors Hollywood FL",
      ld)

    html += NAV
    html += page_hero(
      "Service Areas",
      "Based in Margate.",
      "Working Jupiter to Miami.",
      "We're on Banks Road in Margate, right in the middle of it — and we work from Jupiter all the way down to Miami, across Palm Beach, Broward and Miami-Dade.",
      [("Home","/"),("Service Areas",None)])

    html += f'''
<section class="sec" style="padding-top:0"><div class="container">
  <div class="glass reveal" style="padding:clamp(24px,4vw,44px)">
    <div class="grid-3" style="gap:24px">
      <div><div class="icon-pill"><i class="ri-map-pin-2-fill"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Broward County</span></h3>
        <p style="font-size:14.5px">Where our shop is. Every city in the county, houses and businesses both.</p></div>
      <div><div class="icon-pill chrome-pill"><i class="ri-road-map-line"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Miami-Dade County</span></h3>
        <p style="font-size:14.5px">All the way down to Miami. Same strict wind requirements as Broward, with a few rules of its own — we build to them.</p></div>
      <div><div class="icon-pill"><i class="ri-compass-3-line"></i></div>
        <h3 class="h-display" style="margin:16px 0 8px;font-size:1.4rem"><span class="chrome">Palm Beach County</span></h3>
        <p style="font-size:14.5px">All the way up to Jupiter — roofing, windows, doors and gutters.</p></div>
    </div>
  </div>
</div></section>

<section class="sec"><div class="container">
  <div class="sec-head">
    <span class="eyebrow reveal">Broward Municipalities</span>
    <h2 class="h-display reveal"><span class="chrome">Every city we serve.</span></h2>
    <p class="lead reveal">Same crews wherever you are. Every city handles permits and inspections a little differently — that part is ours to deal with, not yours.</p>
  </div>
  <div class="grid-4">{rows}</div>
</div></section>

<section class="sec"><div class="container" style="max-width:820px">
  <div class="glass-violet reveal" style="padding:clamp(28px,4.5vw,50px);text-align:center">
    <h2 class="h-display"><span class="chrome">Not sure if you're in range?</span></h2>
    <p class="lead" style="margin-top:16px">Just call and ask. If you're outside what we cover, we'll tell you straight instead of sending someone out to waste your afternoon.</p>
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
> impact doors and seamless gutters. Based in Margate, FL. In business since 2013.
> Serving Jupiter to Miami (Palm Beach, Broward and Miami-Dade counties).

## Company
- Legal name: {BIZ}
- Address: {ADDR}
- Phone: {PHONE}
- Website: {DOMAIN}
- License: Florida Certified Roofing Contractor {LIC} (verify at myfloridalicense.com)
- License: Broward County Structural Carpentry Specialty Contractor {LIC2}
- BBB: Accredited, A+ rating
- Google: 5-star rating
- Tagline: Protect · Enhance · Add Value — Built for Florida

## Services
- Roofing: repair, replacement, new construction. Asphalt shingle, concrete and clay tile,
  metal, flat and low-slope membrane. Permitted to Florida High-Velocity Hurricane Zone code.
- Impact windows: single-hung, horizontal slider and XOX, casement, architectural shapes.
  High impact rated, installed by our own crew.
- Impact doors: sliding glass (multi-panel and pocket), French (in-swing and out-swing),
  impact-rated entry doors. High impact rated, installed by our own crew.
- Seamless gutters: 6-inch and 7-inch.

## Financing
- Ygrene Certified PACE financing: repaid via property tax assessment, approval not based
  on credit score. Availability is address-specific.
- Conventional financing through GoodLeap.

## Pages
- {DOMAIN}/ — overview, services, financing, service areas, FAQ, estimate request
- {DOMAIN}/services/roofing.html — roofing systems, 25% rule, HVHZ code, permits
- {DOMAIN}/services/impact-windows.html — styles, insurance credits, energy, noise, UV
- {DOMAIN}/services/impact-doors.html — sliding glass, French, entry; system ratings
- {DOMAIN}/financing.html — Ygrene PACE and GoodLeap financing
- {DOMAIN}/service-areas.html — Jupiter to Miami; Broward municipalities listed

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
