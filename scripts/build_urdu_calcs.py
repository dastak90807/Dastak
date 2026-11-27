"""Build the Urdu fee calculator pages (/ur/calculators/tools/<slug>.html).

The English calculator page stays the single source. This script copies it and:
  * switches the page to Urdu (lang="ur", dir="rtl") with Urdu title, meta tags,
    canonical, hreflang and JSON-LD (WebApplication + BreadcrumbList);
  * translates the visible text and accessibility labels using
    scripts/ur_hubs/calculator-tools.json (numbers are written as # in the keys);
  * hides English paragraphs that already have an Urdu twin on the page;
  * generates assets/calculator-ur.js, which translates text the calculator
    writes while it runs (results, totals, dates) with the same dictionary.

Fee logic, the PKR 950 facilitation fee and the PDF slip (with the Dastak 90807
watermark) are not touched. The PDF stays English because the built-in PDF fonts
have no Urdu letters. The footer brand line stays English because the calculator
locks itself if it is removed.

Run: python3 scripts/build_urdu_calcs.py
"""
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.dastak90807.com"
DICT_FILE = os.path.join(ROOT, "scripts", "ur_hubs", "calculator-tools.json")
JS_VER = "1"
CSS_VER = "1"

PAGES = {
    "punjab-driving-license-fee-calculator": dict(
        title="پنجاب ڈرائیونگ لائسنس فیس کیلکولیٹر | DLIMS 2.0 اور دستک 90807",
        desc="پنجاب ڈرائیونگ لائسنس کی تجدید، نئے، ڈپلیکیٹ اور انٹرنیشنل پرمٹ (IDP) کی تخمینی فیس معلوم کریں۔ گھر پر سہولت: محمد عثمان، دستک کوڈ 90807، 0345-5583530۔",
        name="پنجاب ڈرائیونگ لائسنس فیس کیلکولیٹر (DLIMS 2.0)",
        app_desc="پنجاب ڈرائیونگ لائسنس کی تجدید، نئے لائسنس، ڈپلیکیٹ لائسنس اور انٹرنیشنل ڈرائیونگ پرمٹ کی تخمینی فیس کا مفت آن لائن کیلکولیٹر، 1 سے 5 سال کی میعاد کے ساتھ۔ یہ صرف اندازہ ہے؛ حتمی سرکاری فیس (PSID) مریم کی دستک پورٹل پر بنتی ہے۔",
        crumb="ڈرائیونگ لائسنس فیس کیلکولیٹر",
    ),
    "punjab-car-token-tax-transfer-fee-calculator": dict(
        title="پنجاب کار ٹوکن ٹیکس اور ٹرانسفر فیس کیلکولیٹر | دستک 90807",
        desc="پنجاب میں کار/جیپ کا سالانہ اور لائف ٹائم ٹوکن ٹیکس (فائلر/نان فائلر) اور ملکیت کی منتقلی کی تخمینی فیس معلوم کریں۔ گھر پر سہولت: دستک کوڈ 90807، 0345-5583530۔",
        name="پنجاب کار ٹوکن ٹیکس اور ٹرانسفر فیس کیلکولیٹر",
        app_desc="پنجاب میں کار اور جیپ کے سالانہ اور لائف ٹائم ٹوکن ٹیکس (فائلر/نان فائلر) اور ملکیت کی منتقلی کی تخمینی فیس کا مفت آن لائن کیلکولیٹر۔ یہ صرف اندازہ ہے؛ حتمی سرکاری چالان (PSID) سرکاری سسٹم بناتا ہے۔",
        crumb="کار ٹوکن ٹیکس اور ٹرانسفر کیلکولیٹر",
    ),
    "punjab-bike-registration-transfer-fee-calculator": dict(
        title="پنجاب موٹر سائیکل رجسٹریشن اور ٹرانسفر فیس کیلکولیٹر | دستک 90807",
        desc="پنجاب میں نئی موٹر سائیکل کی رجسٹریشن، ملکیت کی منتقلی اور لائف ٹائم ٹوکن ٹیکس کی تخمینی فیس معلوم کریں۔ الیکٹرک بائیک بھی شامل۔ دستک کوڈ 90807، 0345-5583530۔",
        name="پنجاب موٹر سائیکل رجسٹریشن اور ٹرانسفر فیس کیلکولیٹر",
        app_desc="پنجاب میں نئی موٹر سائیکل کی رجسٹریشن، ملکیت کی منتقلی اور لائف ٹائم ٹوکن ٹیکس کی تخمینی فیس کا مفت آن لائن کیلکولیٹر، الیکٹرک بائیک سمیت۔ یہ صرف اندازہ ہے؛ حتمی سرکاری چالان (PSID) سرکاری سسٹم بناتا ہے۔",
        crumb="موٹر سائیکل رجسٹریشن اور ٹرانسفر کیلکولیٹر",
    ),
}

OG_ALT = "دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807): گوجرخان، راولپنڈی اور پورے پنجاب میں ڈرائیونگ لائسنس، گاڑی کی منتقلی اور پولیس سرٹیفیکیٹ کی سہولت"

NAV_UR = ('<nav aria-label="مرکزی مینو" style="text-align:center;padding:10px">'
          '<a href="/ur/">ہوم</a> | <a href="/ur/services/">خدمات</a> | '
          '<a href="/ur/calculators/">فیس کیلکولیٹر</a> | <a href="/ur/guides/">رہنمائی اور تازہ ترین معلومات</a> | '
          '<a href="/ur/about/">ہمارے بارے میں</a> | <a href="/ur/contact/">رابطہ کریں</a></nav>')

# English paragraphs that already have an Urdu twin on the page. They get
# class "ur-hide" (display:none) so the Urdu text is not shown twice.
# Each rule: (regex matching the opening tag, which group to add the class to).
HIDE = [
    # small Urdu duplicates of headings that are now translated
    r'(<p lang="ur" dir="rtl" class="urdu-text urdu-subtitle")',
    r'(<span lang="ur" dir="rtl" class="urdu-text") (style="font-size:13px; font-weight:700; color:#146336;")',
    r'(<span lang="ur" dir="rtl" class="urdu-text") (style="font-size:12\.5px; font-weight:700; color:#146336;")',
    # English twins next to an Urdu paragraph
    r'(<p) (style="font-size:13\.5px; color:#475569; max-width:540px; margin:6px auto 0;")',
    r'(<p) (style="font-size:12px; color:#334155; margin-bottom:12px;")',
    r'(<p id="nonDastakEngText")',
    r'(<p) (style="border-top:1px solid #e2e8f0; padding-top:8px; font-size:11\.5px;")',
    r'(<p) (style="font-size:13px; font-weight:700; color:#146336; margin-top:4px;")',
]
# Notice boxes: hide the first English <p> right after the Urdu notice paragraph.
NOTICE_TWIN = re.compile(r'(<p lang="ur" dir="rtl" class="urdu-text notice-urdu-inner">.*?</p>\s*)<p\b', re.S)
NO_BIO_TWIN = re.compile(r'(<div class="no-bio-banner">\s*)<span>')

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
URDU = re.compile(r"[؀-ۿ]")
MONTHS = dict(January="جنوری", February="فروری", March="مارچ", April="اپریل", May="مئی", June="جون",
              July="جولائی", August="اگست", September="ستمبر", October="اکتوبر", November="نومبر", December="دسمبر",
              Jan="جنوری", Feb="فروری", Mar="مارچ", Apr="اپریل", Jun="جون", Jul="جولائی", Aug="اگست",
              Sep="ستمبر", Oct="اکتوبر", Nov="نومبر", Dec="دسمبر",
              Mon="پیر", Tue="منگل", Wed="بدھ", Thu="جمعرات", Fri="جمعہ", Sat="ہفتہ", Sun="اتوار")
DATE_WORD = re.compile(r"\b(" + "|".join(sorted(MONTHS, key=len, reverse=True)) + r")\b")


def translate(text, d):
    """Translate one text value. Returns None when nothing should change."""
    core = re.sub(r"\s+", " ", text).strip()
    if not core or not re.search(r"[A-Za-z]", core):
        return None
    nums = NUM.findall(core)
    key = NUM.sub("#", core)
    u = d.get(key)
    if u is None:
        if re.fullmatch(r"[#\s,().\-–/]*", DATE_WORD.sub("", key)):
            u = DATE_WORD.sub(lambda m: MONTHS[m.group(1)], key)
        else:
            return None
    it = iter(nums)
    u = re.sub(r"\{(\d)\}|#", lambda m: nums[int(m.group(1)) - 1] if m.group(1) else next(it, "#"), u)
    if u.rstrip().endswith(")"):
        u += "\u200f"  # right-to-left mark: keeps "(Rs. 0)" brackets in place in RTL, also inside <option>
    lead = " " if text[:1].isspace() else ""
    trail = " " if text[-1:].isspace() else ""
    return lead + u + trail


def jsonld(slug, p):
    ur = f"{BASE}/ur/calculators/tools/{slug}"
    app = {
        "@context": "https://schema.org", "@type": "WebApplication", "name": p["name"],
        "alternateName": "Dastak 90807 Fee Calculator (Urdu)", "url": ur, "mainEntityOfPage": ur,
        "description": p["app_desc"], "applicationCategory": "FinanceApplication",
        "operatingSystem": "Any (web browser)", "browserRequirements": "Requires JavaScript",
        "inLanguage": "ur", "isAccessibleForFree": True,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "PKR"},
        "areaServed": [{"@type": "City", "name": "Gujar Khan"}, {"@type": "City", "name": "Rawalpindi"},
                       {"@type": "AdministrativeArea", "name": "Punjab"}],
        "provider": {"@type": "ProfessionalService", "name": "Dastak Online Document Facilitation",
                     "url": BASE, "telephone": "+92-345-5583530"},
    }
    crumbs = {
        "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "ہوم", "item": f"{BASE}/ur/"},
            {"@type": "ListItem", "position": 2, "name": "فیس کیلکولیٹر", "item": f"{BASE}/ur/calculators/"},
            {"@type": "ListItem", "position": 3, "name": p["crumb"], "item": ur},
        ]}
    return "\n".join('<script type="application/ld+json">' + json.dumps(x, ensure_ascii=False) + "</script>"
                     for x in (app, crumbs))


def build(slug, p, d):
    src = os.path.join(ROOT, "en", "calculators", "tools", slug + ".html")
    h = open(src, encoding="utf-8").read()
    en_url = f"{BASE}/en/calculators/tools/{slug}"
    ur_url = f"{BASE}/ur/calculators/tools/{slug}"

    h = h.replace('<html lang="en">', '<html lang="ur" dir="rtl">', 1)
    head_end = h.index("</head>")
    head, body = h[:head_end], h[head_end:]

    def meta(attr, name, value):
        nonlocal head
        pat = re.compile(rf'(<meta {attr}="{re.escape(name)}" content=")[^"]*(")')
        assert pat.search(head), name
        head = pat.sub(lambda m: m.group(1) + html.escape(value) + m.group(2), head, count=1)

    head = re.sub(r"<title>.*?</title>", "<title>" + html.escape(p["title"], quote=False) + "</title>", head, count=1)
    meta("name", "description", p["desc"])
    meta("property", "og:title", p["title"])
    meta("property", "og:description", p["desc"])
    meta("property", "og:url", ur_url)
    meta("property", "og:image:alt", OG_ALT)
    meta("name", "twitter:image:alt", OG_ALT)
    meta("property", "og:locale", "ur_PK")
    head = head.replace(f'<link rel="canonical" href="{en_url}" />',
                        f'<link rel="canonical" href="{ur_url}" />\n'
                        f'  <link rel="alternate" hreflang="en" href="{en_url}" />\n'
                        f'  <link rel="alternate" hreflang="ur" href="{ur_url}" />\n'
                        f'  <link rel="alternate" hreflang="x-default" href="{en_url}" />', 1)
    assert ur_url in head, "canonical"
    # Replace the English WebApplication JSON-LD with the Urdu one + breadcrumbs.
    blocks = re.findall(r'<script type="application/ld\+json">.*?</script>', head, re.S)
    web = [b for b in blocks if '"WebApplication"' in b]
    assert len(web) == 1
    head = head.replace(web[0], jsonld(slug, p))
    head += (f'<link rel="stylesheet" href="/assets/calculator-ur.css?v={CSS_VER}">\n'
             f'<script src="/assets/calculator-ur.js?v={JS_VER}" defer></script>\n')

    # Fine-period table headers ("Till 15 Jan<br/>2024"): Urdu word order puts تک / سے after the date.
    for en, ur in (("Till 15 Jan<br/>2024", "15 جنوری 2024<br/>تک"), ("From 16 Jan<br/>2024", "16 جنوری 2024<br/>سے")):
        body = body.replace(en, ur)
    body = body.replace('<div style="text-align:left; line-height:1.25;">', '<div style="text-align:right; line-height:1.25;">')

    # English twins of Urdu paragraphs: hide.
    for rule in HIDE:
        pat = re.compile(rule)
        if not pat.search(body):
            continue

        def add(m):
            tag = m.group(1)
            if 'class="' in tag:
                tag = tag.replace('class="', 'class="ur-hide ', 1)
            else:
                tag += ' class="ur-hide"'
            return tag + ("" if m.lastindex == 1 else " " + m.group(2))
        body = pat.sub(add, body)
    body = NOTICE_TWIN.sub(lambda m: m.group(1) + '<p class="ur-hide"', body)
    body = NO_BIO_TWIN.sub(lambda m: m.group(1) + '<span class="ur-hide">', body)

    # Translate text and labels outside scripts, styles and SVG.
    keep = []

    def stash(m):
        keep.append(m.group(0))
        return f"\x00{len(keep) - 1}\x00"
    body = re.sub(r"<(script|style|svg)\b.*?</\1>", stash, body, flags=re.S)
    body = re.sub(r"<noscript>\s*<nav\b.*?</nav>\s*</noscript>", "<noscript>" + NAV_UR + "</noscript>", body, flags=re.S)
    # "Smart Card Fee (<span lang="ur">سمارٹ کارڈ فیس</span>):" and "3. Exact 3 Clear Photos (<span ...>)":
    # keep the number and the Urdu, drop the English words in front.
    body = re.sub(r'>(\d+\.\s*)?([^<>(]*?[A-Za-z][^<>(]*?)\s*\(<span lang="ur">([^<]*)</span>\)',
                  lambda m: ">" + (m.group(1) or "") + '<span lang="ur">' + m.group(3) + "</span>", body)
    # Checklist lines that end with their own Urdu explanation: show only the Urdu.
    body = re.sub(r'^(\s*<li><strong>[^<]*</strong>)[^\n]*?\(<span lang="ur">([^<]*)</span>\)[.۔](</li>)',
                  r'\1 <span lang="ur">\2</span>۔\3', body, flags=re.M)
    body = re.sub(r'^(\s*)(?!<)([^\n]*?)\(<span lang="ur">([^<]*)</span>\)[.۔]\s*$',
                  r'\1<span lang="ur">\3</span>۔', body, flags=re.M)

    def text(m):
        raw = m.group(1)
        if "\x00" in raw:
            return m.group(0)
        u = translate(html.unescape(raw), d)
        return ">" + (html.escape(u, quote=False) if u is not None else raw) + "<"
    body = re.sub(r">([^<>]+)<", text, body)

    def attr(m):
        u = translate(html.unescape(m.group(3)), d)
        return m.group(1) + m.group(2) + (html.escape(u) if u is not None else m.group(3)) + m.group(2)
    body = re.sub(r'(\s(?:aria-label|placeholder|title|alt)=)(["\'])(.*?)\2', attr, body)
    body = re.sub(r'href="/en/(about|calculators|contact|guides|services)?/?"',
                  lambda m: f'href="/ur/{m.group(1) + "/" if m.group(1) else ""}"', body)
    body = re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], body)

    out_dir = os.path.join(ROOT, "ur", "calculators", "tools")
    os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, slug + ".html"), "w", encoding="utf-8").write(head + body)


def write_runtime(d):
    """assets/calculator-ur.js: same dictionary, applied to text the calculator writes."""
    tpl = open(os.path.join(ROOT, "scripts", "calculator-ur.template.js"), encoding="utf-8").read()
    js = tpl.replace("/*DICT*/{}", json.dumps(d, ensure_ascii=False, separators=(",", ":"))) \
            .replace("/*MONTHS*/{}", json.dumps(MONTHS, ensure_ascii=False, separators=(",", ":")))
    open(os.path.join(ROOT, "assets", "calculator-ur.js"), "w", encoding="utf-8").write(js)


def main():
    d = json.load(open(DICT_FILE, encoding="utf-8"))
    bad = [k for k, v in d.items() if v.count("#") + len(re.findall(r"\{\d\}", v)) > k.count("#")]
    if bad:
        sys.exit("Urdu values with more numbers than the English key: " + repr(bad[:5]))
    for slug, p in PAGES.items():
        build(slug, p, d)
    write_runtime(d)
    print(f"Built {len(PAGES)} Urdu calculator pages ({len(d)} dictionary entries)")


if __name__ == "__main__":
    main()
