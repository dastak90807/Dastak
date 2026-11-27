#!/usr/bin/env python3
"""Build the Urdu (/ur/) pages of www.dastak90807.com.

Run from the repository root:   python3 scripts/build_urdu.py
It writes ur/**/index.html. Edit the page content below, then run it again.

Rules followed on every page:
- Fees come only from the official Dastak training manual (V-5, 26 June 2025) or the
  official Dastak portal/app, as confirmed by the facilitator. The PSID shows the final amount.
- Independent-facilitator disclaimer (Code 90807), no government emblems, no 1202 helpline.
- Canonical, hreflang (en/ur/x-default), Open Graph, JSON-LD (WebPage, BreadcrumbList,
  Service or Article, FAQPage) with inLanguage "ur".
"""
import html
import json
import os
import re

SITE = "https://www.dastak90807.com"
UPDATED = "2026-11-25"
UPDATED_UR = "25 نومبر 2026"
WA = "https://wa.me/923455583530"
PHONE = '<span class="ltr">0345-5583530</span>'
CODE = '<span class="ltr">90807</span>'
APP_ANDROID = "https://play.google.com/store/apps/details?id=pk.pitb.gov.dastakHomeDelivery"
APP_IOS = "https://apps.apple.com/us/app/dastak-home-delivery/id6479348922"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CLARITY_SNIPPET = '<!-- Clarity tracking code for https://dastak90807.com/ -->\n<script>\n    (function(c,l,a,r,i,t,y){\n        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};\n        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i+"?ref=bwt";\n        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);\n    })(window, document, "clarity", "script", "zk4xin7ucw");\n</script>\n'

SAME_AS = ["https://facebook.com/Dastak90807", "https://instagram.com/dastak90807",
           "https://www.tiktok.com/@dastak90807", "https://x.com/dastak90807",
           "https://www.linkedin.com/in/dastak90807", "https://www.youtube.com/@Dastak90807",
           "https://www.snapchat.com/add/dastak90807", "https://www.pinterest.com/dastak90807",
           "https://share.google/nmpsQYND7NTAnZzqI",
           "https://whatsapp.com/channel/0029VbEdgGRAu3aLblsW5g0Y"]

DISCLAIMER = ("دستک آن لائن ڈاکومنٹ فیسیلیٹیشن محمد عثمان چلاتے ہیں، جو حکومتِ پنجاب کے مریم کی دستک پروگرام کے تحت "
              f"رجسٹرڈ فیسیلیٹیٹر ہیں (فیسیلیٹیٹر کوڈ {CODE})۔ یہ ویب سائٹ ایک آزاد فیسیلیٹیشن سروس ہے، کوئی سرکاری ویب سائٹ یا محکمہ نہیں۔ "
              "فیس سرکاری سسٹم خود بناتا ہے اور حتمی رقم آپ کے PSID پر لکھی ہوتی ہے۔ تفصیلات ہمیشہ سرکاری دستک پورٹل یا ایپ سے تصدیق کریں۔")

FEE_SOURCE = ("فیس کی معلومات کا ذریعہ: سرکاری دستک تربیتی مینول (ورژن 5، اپ ڈیٹ 26 جون 2025) اور سرکاری دستک پورٹل۔ "
              "سرکاری فیس کبھی بھی بدل سکتی ہے، اس لیے ادائیگی سے پہلے PSID پر لکھی رقم ضرور دیکھیں۔")

PAYMENT = ("فیس سرکاری سسٹم خود بناتا ہے۔ دستک ایپ میں ادائیگی کے طریقے: PSID (کسی بھی بینکنگ ایپ یا موبائل والٹ سے)، "
           "IBFT، جاز کیش، ایزی پیسہ اور کیش آن ڈیلیوری۔ ہر سروس میں طریقے مختلف ہو سکتے ہیں۔")

VERIFY = (f"میرا فیسیلیٹیٹر کوڈ {CODE} سرکاری <a href=\"https://dastak.punjab.gov.pk\" rel=\"noopener\">دستک پورٹل</a> یا سرکاری دستک ایپ میں چیک کریں، "
          "یا سرکاری دستک ہیلپ لائن <a href=\"tel:1202\" class=\"ltr\">1202</a> پر کال کر کے تصدیق کریں۔ "
          "نوٹ: 1202 حکومتِ پنجاب کے دستک پروگرام کی سرکاری ہیلپ لائن ہے، یہ ہمارا نمبر نہیں۔ ہم سے رابطے کے لیے صرف " + PHONE + " استعمال کریں۔")

AREAS = "گوجرخان، راولپنڈی، کلر سیداں، کہوٹہ، مندرہ، بیول، دولتالہ، جاتلی، سکھو اور قاضیاں"


def wa_link(service):
    from urllib.parse import quote
    return WA + "?text=" + quote(f"السلام علیکم۔ مجھے اس سروس میں مدد چاہیے: {service}")


def strip_tags(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- shared blocks
def booking_block(service):
    return f'''<div class="card book" id="book"><h2>{esc(service)} کی بکنگ کیسے کریں؟</h2><ol>
<li>سرکاری دستک سٹیزن ایپ کھولیں اور <b>Doorstep Delivery</b> منتخب کریں۔</li>
<li><b>Self</b> یا <b>On Behalf</b> منتخب کریں اور Facilitator Code کے خانے میں <b>{CODE}</b> لکھیں۔</li>
<li>یا براہِ راست واٹس ایپ یا کال کریں: {PHONE}</li></ol>
<p class="sd-tip"><b>اہم:</b> کوڈ {CODE} کے ساتھ بکنگ کے لیے <b>Doorstep Delivery</b> ہی منتخب کریں۔ Self Service میں فیسیلیٹیٹر کوڈ کا خانہ نہیں ہوتا۔</p>
<div class="row"><a class="btn y" data-ga-event="service_whatsapp_click" href="{wa_link(service)}">اس سروس کے بارے میں واٹس ایپ کریں</a><a class="btn g" data-ga-event="service_call_click" href="tel:+923455583530">کال کریں {PHONE}</a><a class="btn o" href="{APP_ANDROID}" rel="noopener">دستک ایپ (گوگل پلے)</a><a class="btn o" href="{APP_IOS}" rel="noopener">دستک ایپ (ایپ اسٹور)</a></div>
<p class="note">{PAYMENT}</p><p class="note ur-verify" id="verify"><b>فیسیلیٹیٹر کی تصدیق:</b> {VERIFY}</p></div>'''


def fee_table(rows):
    body = "".join(f"<tr><th scope=\"row\">{k}</th><td>{v}</td></tr>" for k, v in rows)
    return f'<table class="ur-fee"><caption class="sr-only">فیس اور وقت</caption><tbody>{body}</tbody></table>'


def faq_html(faqs):
    return "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faqs)


def home_faq(faqs):
    items = "".join(f'<details data-ga-event="home_faq_expand" data-faq-title="{html.escape(q)}"><summary>{q}</summary><p>{a}</p></details>' for q, a in faqs)
    return ('<section class="wrap home-faqs" id="faqs" aria-labelledby="home-faq-title"><h2 id="home-faq-title">پنجاب کی سرکاری خدمات سے متعلق آپ کے سوالات</h2>'
            f'<div class="faq-list">{items}</div><p><a class="btn o" href="/ur/faqs/">تمام سوالات دیکھیں ←</a></p></section>')


def cards(items):
    return '<ul class="ur-cards">' + "".join(
        f'<li><a href="{href}">{title}</a><p>{desc}</p></li>' for href, title, desc in items) + "</ul>"


# ---------------------------------------------------------------- page shell
FOOTER = open(os.path.join(ROOT, "assets", "footer-ur.html"), encoding="utf-8").read().strip()


def page(p):
    path = p["path"]                       # e.g. /services/token-tax/
    ur_url = SITE + "/ur" + path
    en_url = SITE + "/en" + path
    title, desc = p["title"], p["desc"]
    og_img = SITE + p.get("og", "/assets/og/default.jpg")
    og_alt = p.get("og_alt", f"{strip_tags(p['h1'])}، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی، پنجاب")
    crumbs = [("ہوم", "/ur/")] + p.get("crumbs", [])
    graph = [
        {"@type": "Organization", "@id": SITE + "/#org", "name": "Dastak Online Document Facilitation",
         "alternateName": ["Dastak 90807", "دستک آن لائن ڈاکومنٹ فیسیلیٹیشن"], "url": SITE + "/",
         "logo": SITE + "/assets/dastak-90807-transparent.png",
         "description": "مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر (کوڈ 90807) کی آزاد ڈاکومنٹ فیسیلیٹیشن سروس، گوجرخان، راولپنڈی اور پنجاب۔",
         "contactPoint": {"@type": "ContactPoint", "telephone": "+92-345-5583530", "contactType": "customer support",
                          "areaServed": "PK", "availableLanguage": ["Urdu", "English", "Punjabi"]},
         "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in ("Gujar Khan", "Rawalpindi", "Punjab")],
         "sameAs": SAME_AS},
        {"@type": "WebPage", "@id": ur_url + "#webpage", "url": ur_url, "name": title, "description": desc,
         "inLanguage": "ur", "isPartOf": {"@id": SITE + "/#website"}, "dateModified": UPDATED},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(crumbs)]},
    ]
    if p.get("kind") == "service":
        graph.append({"@type": "Service", "@id": ur_url + "#service", "name": strip_tags(p["h1"]),
                      "serviceType": "Document facilitation", "description": desc, "inLanguage": "ur",
                      "provider": {"@id": SITE + "/#org"}, "url": ur_url,
                      "areaServed": [{"@type": "AdministrativeArea", "name": n} for n in p.get("areas", ("Gujar Khan", "Rawalpindi", "Punjab"))]})
    if p.get("kind") == "guide":
        graph.append({"@type": "Article", "@id": ur_url + "#article", "headline": strip_tags(p["h1"]),
                      "description": desc, "inLanguage": "ur", "dateModified": UPDATED, "datePublished": UPDATED,
                      "author": {"@type": "Person", "@id": SITE + "/#person", "name": "Muhammad Usman",
                                 "alternateName": "محمد عثمان", "jobTitle": "Registered Dastak Facilitator (Code 90807)"},
                      "publisher": {"@id": SITE + "/#org"}, "image": og_img, "mainEntityOfPage": ur_url})
    if p.get("faqs"):
        graph.append({"@type": "FAQPage", "inLanguage": "ur", "mainEntity": [
            {"@type": "Question", "name": strip_tags(q), "acceptedAnswer": {"@type": "Answer", "text": strip_tags(a)}}
            for q, a in p["faqs"]]})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False).replace("</", "<\\/")

    crumb_html = " › ".join(f'<a href="{u}">{n}</a>' for n, u in crumbs[:-1]) + (" › " if len(crumbs) > 1 else "") + crumbs[-1][0]
    faq_block = (f'<section class="service-module questions-module"><h2>عام سوالات</h2>{faq_html(p["faqs"])}</section>'
                 if p.get("faqs") else "")
    main_class = p.get("main_class", "service-detail")
    en_note = f'<p class="ur-en-link">یہ صفحہ انگریزی میں پڑھیں: <a href="/en{path}" hreflang="en">انگریزی ورژن ←</a></p>'

    return f'''<!doctype html><html lang="ur" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{ur_url}"><link rel="alternate" hreflang="ur" href="{ur_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{en_url}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="{"article" if p.get("kind") == "guide" else "website"}"><meta property="og:site_name" content="Dastak 90807"><meta property="og:locale" content="ur_PK"><meta property="og:locale:alternate" content="en_PK"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{ur_url}"><meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(og_alt)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{og_img}"><meta name="twitter:image:alt" content="{esc(og_alt)}"><meta name="theme-color" content="#0A3F35"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{SITE}/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><link rel="preload" href="/assets/fonts/noto-sans-arabic-arabic-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/loader.css?v=1"><link rel="stylesheet" href="/assets/style.css"><link rel="stylesheet" href="/assets/site-update.css?v=20261122-ui"><link rel="stylesheet" href="/assets/site-polish.css?v=6"><link rel="stylesheet" href="/assets/services-design.css?v=1"><link rel="stylesheet" href="/assets/page-design.css?v=20261125a"><link rel="stylesheet" href="/assets/service-detail-v2.css?v=20261125a">{'<link rel="stylesheet" href="/assets/guide-hero.css?v=1">' if 'class="guide-hero"' in p["body"] else ""}{"".join(f'<link rel="stylesheet" href="{c}">' for c in p.get("css", []))}<link rel="stylesheet" href="/assets/urdu-rtl.css?v=26"><script type="application/ld+json">{ld}</script>{CLARITY_SNIPPET}</head><body id="top"><div id="dastak-loader" role="status" aria-live="polite" aria-label="صفحہ لوڈ ہو رہا ہے" aria-hidden="true"><span class="dastak-loader-status">صفحہ لوڈ ہو رہا ہے…</span><div class="dastak-loader-wrap"><span class="dastak-pulse-ring" aria-hidden="true"></span><span class="dastak-pulse-ring" aria-hidden="true"></span><span class="dastak-pulse-ring" aria-hidden="true"></span><img src="/assets/dastak-90807-transparent.png" alt="دستک 90807، گھر کی دہلیز پر سرکاری خدمات" class="dastak-loader-logo" width="175" height="61"></div></div><script src="/assets/loader.js?v=1"></script><a class="skip" href="#main">مواد پر جائیں</a>
<aside class="top" aria-label="سرکاری پورٹل اور رجسٹریشن"><p class="ur-top">مریم کی دستک (حکومتِ پنجاب کا اقدام) کے <b>رجسٹرڈ فیسیلیٹیٹر</b> · <b class="gold">کوڈ {CODE}</b> · سرکاری پورٹل: <a href="https://dastak.punjab.gov.pk" rel="noopener" class="ltr">dastak.punjab.gov.pk</a></p></aside>
<script src="/assets/shared-header.js?v=13"></script><noscript><nav aria-label="مرکزی مینو"><a href="/ur/">ہوم</a> <a href="/ur/services/">خدمات</a> <a href="/ur/calculators/">فیس کیلکولیٹر</a> <a href="/ur/guides/">گائیڈز</a> <a href="/ur/contact/">رابطہ</a> <a href="/en{path}" lang="en">English</a></nav></noscript>
{(lambda _b, _i: f'<main id="main" class="{main_class}">{_b[:_i]}{en_note}{_b[_i:]}</main>')(p["body"], max(p["body"].rfind("</div>"), p["body"].rfind("</section>"))) if p.get("hub_en") else (f'<main id="main" class="{main_class}">{p["body"].replace("<!--FAQ-->", home_faq(p["faqs"]))}<section class="wrap ur-page-end">{en_note}<p class="disc">{DISCLAIMER}</p></section></main>' if "<!--FAQ-->" in p["body"] else f'<main id="main" class="{main_class}">{p["body"]}<section class="wrap home-faqs">{faq_block}{en_note}<p class="disc">{DISCLAIMER}</p></section></main>') if p.get("raw") else f'''<main id="main" class="{main_class}"><section class="wrap"><header class="service-intro"><p class="crumb">{crumb_html}</p>{p.get("eyebrow", "")}<h1>{p["h1"]}</h1><p class="meta">{p.get("meta", f"آخری اپ ڈیٹ: {UPDATED_UR} · تحریر: محمد عثمان، فیسیلیٹیٹر کوڈ {CODE}")}</p></header>
{p["body"]}
{faq_block}
{en_note}
<p class="disc">{DISCLAIMER}</p></section></main>'''}
{FOOTER}
<aside aria-label="فوری رابطہ"><a class="wafloat btn g" href="{WA}">واٹس ایپ</a><div class="bar"><a class="btn g" href="{WA}">واٹس ایپ</a><a class="btn y" href="tel:+923455583530">کال کریں</a></div></aside>
<script src="/assets/app.js?v=3" defer></script><a class="back-to-top" href="#top" aria-label="اوپر جائیں" title="اوپر جائیں">↑</a><script src="/assets/site-update.js?v=20261122-ui" defer></script><script src="/assets/site-polish.js?v=4" defer></script><script src="/assets/chatbot.js?v=4" defer></script>{"".join(f'<script src="{j}" defer></script>' for j in p.get("js", []))}</body></html>
'''


# Parity with the English service pages: "Estimate the fee" box (sd-calc) linking to the Urdu calculators
_CALC = {"dl": ("/ur/calculators/tools/punjab-driving-license-fee-calculator", "Driving License Fee Calculator", "ڈرائیونگ لائسنس فیس کیلکولیٹر"),
         "car": ("/ur/calculators/tools/punjab-car-token-tax-transfer-fee-calculator", "Car Token Tax &amp; Transfer Fee Calculator", "کار ٹوکن ٹیکس اور ملکیت کی منتقلی کیلکولیٹر"),
         "bike": ("/ur/calculators/tools/punjab-bike-registration-transfer-fee-calculator", "Motorcycle Registration &amp; Transfer Fee Calculator", "موٹر سائیکل رجسٹریشن اور ملکیت کی منتقلی کیلکولیٹر")}
CALC_FOR = {"ٹوکن ٹیکس": ("car", "bike"), "گاڑی کی ملکیت کی منتقلی": ("car", "bike"), "ڈرائیونگ لائسنس کی تجدید": ("dl",)}
_ARR = '<svg class="btn-arrow" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>'


# Renewal: the calculator replaces the old 1-year category table, so its button sits inside the fee section
CALC_IN_FEE = {"ڈرائیونگ لائسنس کی تجدید"}


def calc_box(name, in_fee=False):
    if name not in CALC_FOR:
        return ""
    if in_fee:
        btns = "".join(f'<a class="btn y" href="{_CALC[k][0]}" data-ga-event="service_calculator_click" data-tool-name="{_CALC[k][1]}">{_CALC[k][2]} کھولیں {_ARR}</a>' for k in CALC_FOR[name])
        return (f'<div class="card sd-calc"><p><strong>اپنی کیٹیگری اور مدت (1 سے 5 سال) کے مطابق درست اندازہ کیلکولیٹر سے لگائیں۔</strong> '
                f'کیلکولیٹر تجدید فیس، تاخیر کا جرمانہ، کوریئر فیس اور فیسیلیٹیٹر چارجز ایک ساتھ دکھاتا ہے اور آپ اندازہ PDF میں ڈاؤن لوڈ کر سکتے ہیں۔ یہ صرف اندازہ ہے، حتمی رقم PSID پر لکھی ہوتی ہے۔</p>'
                f'<div class="row">{btns}</div></div>')
    btns = "".join(f'<a class="btn y" href="{_CALC[k][0]}" data-ga-event="service_calculator_click" data-tool-name="{_CALC[k][1]}">{_CALC[k][2]} {_ARR}</a>' for k in CALC_FOR[name])
    return (f'<div class="card sd-calc"><h2>{esc(name)} کی فیس کا اندازہ لگائیں</h2><p>ہمارے مفت کیلکولیٹر سے فوری اندازہ لگائیں اور PDF میں ڈاؤن لوڈ کریں۔ '
            f'یہ صرف اندازہ ہے۔ سرکاری فیس پنجاب کا سرکاری سسٹم بناتا ہے۔</p><div class="row">{btns}</div></div>\n')


def service_body(name, quick, glance, docs, steps, fees, extra="", related=()):
    glance_html = "".join(f"<div><small>{k}</small><b>{v}</b></div>" for k, v in glance)
    docs_html = "".join(f"<li>{d}</li>" for d in docs)
    steps_html = "".join(f"<li>{s}</li>" for s in steps)
    rel = ("<section class=\"service-module related-module\"><h2>متعلقہ صفحات</h2>" + cards(related) + "</section>") if related else ""
    return f'''<div class="sd-glance" aria-label="سروس ایک نظر میں">{glance_html}</div>
<div class="sd-actions"><a class="btn g" data-ga-event="service_whatsapp_click" href="{wa_link(name)}">واٹس ایپ: {PHONE}</a><a class="btn y" href="#book">بکنگ کا طریقہ</a><a class="btn o" data-ga-event="service_call_click" href="tel:+923455583530">کال کریں</a></div>
<p class="sd-trust">رجسٹرڈ فیسیلیٹیٹر کوڈ {CODE} · آزاد سروس، سرکاری دفتر نہیں · <a href="#verify">تصدیق کیسے کریں؟</a></p>
<div class="card quick"><b>مختصر جواب</b><p>{quick}</p></div>
<section class="service-module documents-module"><h2>{esc(name)} کے لیے کون سی دستاویزات چاہئیں؟</h2><ul class="docs">{docs_html}</ul></section>
<section class="service-module fee-module"><h2>{esc(name)} کی فیس کتنی ہے؟</h2>{fee_table(fees)}{calc_box(name, True) if name in CALC_IN_FEE else ""}<p class="ur-note">{FEE_SOURCE}</p></section>
<section class="service-module steps-module"><h2>{esc(name)} کا طریقہ، قدم بہ قدم</h2><ol>{steps_html}</ol></section>
{"" if name in CALC_IN_FEE else calc_box(name)}{extra}
{booking_block(name)}
{rel}'''


def guide_body(quick, sections, hero=None, related=(), sources=()):
    toc = "".join(f'<li><a href="#s{i+1}">{h}</a></li>' for i, (h, _) in enumerate(sections))
    secs = "".join(f'<section class="service-module" id="s{i+1}"><h2>{h}</h2>{b}</section>' for i, (h, b) in enumerate(sections))
    hero_html = (f'<figure class="guide-hero"><img src="{hero[0]}" width="1600" height="893" alt="{esc(hero[1])}" fetchpriority="high"></figure>' if hero else "")
    rel = ("<section class=\"service-module related-module\"><h2>یہ بھی پڑھیں</h2>" + cards(related) + "</section>") if related else ""
    rel += ("<section class=\"service-module guide-sources\"><h2>ذرائع اور مزید معلومات</h2><ul>" + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{t}</a></li>' for u, t in sources) + "</ul><p class=\"sub\">ضروری دستاویزات، فیس اور طریقہ بدل سکتے ہیں۔ درخواست سے پہلے متعلقہ سرکاری سروس ضرور چیک کریں۔ تصدیق اور منظوری کا فیصلہ متعلقہ سرکاری محکمہ کرتا ہے۔</p></section>") if sources else ""
    return f'''{hero_html}<div class="card quick answer-summary"><b>مختصر جواب</b><p>{quick}</p></div>
<nav class="guide-contents card" aria-label="اس صفحے میں"><strong>اس گائیڈ میں</strong><ul>{toc}</ul></nav>
{secs}
<div class="card book"><h2>مدد چاہیے؟</h2><p>پورے پنجاب میں واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ۔ {AREAS} میں گھر پر وزٹ پہلے سے وقت طے کر کے۔</p><div class="row"><a class="btn y" data-ga-event="guide_whatsapp_click" href="{WA}">واٹس ایپ {PHONE}</a><a class="btn g" href="tel:+923455583530">کال کریں</a><a class="btn o" href="/ur/calculators/">فیس کیلکولیٹر</a></div></div>
{rel}'''


# ---------------------------------------------------------------- related link sets
R = {
    "renew": ("/ur/services/renewal-of-regular-license/", "ڈرائیونگ لائسنس کی تجدید", "پنجاب میں لائسنس کی تجدید، دستاویزات اور فیس"),
    "learner": ("/ur/services/learner-driving-license/", "لرنر پرمٹ", "لرنر پرمٹ کیسے بنوائیں، فیس 500 روپے فی کیٹیگری"),
    "track": ("/ur/guides/how-to-track-driving-license-in-punjab/", "لائسنس ٹریک کرنے کا طریقہ", "DLIMS اور پاکستان پوسٹ سے اسٹیٹس دیکھیں"),
    "renew_guide": ("/ur/guides/punjab-driving-license-renewal-online/", "لائسنس کی تجدید آن لائن گائیڈ", "مکمل طریقہ، تیاری اور عام غلطیاں"),
    "character": ("/ur/services/character-certificate/", "پولیس کریکٹر سرٹیفیکیٹ", "بیرون ملک سفر اور نوکری کے لیے"),
    "character_guide": ("/ur/guides/punjab-police-character-certificate-online/", "کریکٹر سرٹیفیکیٹ گائیڈ", "دستاویزات، طریقہ اور تصدیق"),
    "transfer": ("/ur/services/transfer-of-motor-vehicle/", "گاڑی / موٹر سائیکل کی ملکیت کی منتقلی", "ملکیت اپنے نام کروانے کا طریقہ"),
    "token": ("/ur/services/token-tax/", "ٹوکن ٹیکس", "گھر بیٹھے سالانہ ٹوکن ٹیکس جمع کروائیں"),
    "vehicle_guide": ("/ur/guides/vehicle-transfer-token-tax-punjab/", "ملکیت کی منتقلی اور ٹوکن ٹیکس گائیڈ", "بائیومیٹرک، PSID اور عام سوالات"),
    "domicile": ("/ur/services/domicile-certificate/", "ڈومیسائل سرٹیفیکیٹ", "فیس 1,200 روپے، گوجرخان اور راولپنڈی"),
    "calc": ("/ur/calculators/", "فیس کیلکولیٹر", "لائسنس، گاڑی اور موٹر سائیکل فیس کا اندازہ"),
    "gk": ("/ur/gujar-khan/", "گوجرخان میں دستک سروس", "گھر پر دستاویزات کی سہولت"),
    "contact": ("/ur/contact/", "رابطہ", f"واٹس ایپ، کال اور دفتر کا پتہ"),
}


# Official renewal fee table, copied from the official Dastak portal "فیس کی تفصیلات" page
# (https://dastak.punjab.gov.pk/citizen/fee/stucture), checked 25 Nov 2026. Fee is for 1 year.
RENEW_ROWS = [("موٹر سائیکل", "450", "225", "450", "1,125", "930"), ("رکشہ", "400", "200", "400", "1,000", "880"),
              ("کار / جیپ", "1,350", "675", "1,350", "3,375", "1,830"), ("موٹر سائیکل + کار", "1,350", "675", "1,350", "3,375", "1,830"),
              ("ایل ٹی وی (LTV)", "1,850", "925", "1,850", "4,625", "2,330"), ("ایچ ٹی وی (HTV)", "1,850", "925", "1,850", "4,625", "2,330"),
              ("ٹریکٹر کمرشل", "1,400", "700", "1,400", "3,500", "1,880")]
RENEW_FEE_TABLE = ('<div class="ur-table-wrap"><table class="ur-fee ur-fee-grid"><caption>سرکاری تجدید فیس (1 سال)، سرکاری دستک پورٹل کے مطابق</caption>'
    '<thead><tr><th scope="col">کیٹیگری</th><th scope="col">تجدید فیس</th><th scope="col">جرمانہ 1 سے 3 ماہ</th><th scope="col">جرمانہ 3 ماہ سے 1 سال</th><th scope="col">جرمانہ 1 سال سے زیادہ</th><th scope="col">کل (کوریئر Rs 480 سمیت، جرمانے کے بغیر)</th></tr></thead><tbody>'
    + "".join(f'<tr><th scope="row">{c}</th>' + "".join(f'<td class="ltr">Rs {v}</td>' for v in vals) + "</tr>" for c, *vals in RENEW_ROWS)
    + '</tbody></table></div><ul><li>یہ فیس 1 سال کی ہے۔ لائسنس 1 سے 5 سال تک کے لیے بن سکتا ہے، اس لیے سرکاری فیس سالوں کے حساب سے بڑھتی ہے۔</li>'
    '<li>ایک سے زیادہ کیٹیگری ہوں تو سب سے زیادہ فیس والی کیٹیگری کی فیس لگتی ہے۔</li>'
    '<li>اصل لائسنس موجود نہ ہو تو ڈپلیکیٹ فیس بھی شامل ہوتی ہے۔</li>'
    '<li>اس کے علاوہ دستک فیسیلیٹیٹر چارجز Rs 950 اور پلیٹ فارم چارجز Rs 19 ہیں۔ حتمی رقم PSID پر لکھی ہوتی ہے۔</li></ul>'
    '<p class="ur-note">ذریعہ: سرکاری دستک پورٹل، فیس کی تفصیلات (25 نومبر 2026 کو چیک کیا گیا)۔</p>')

PAGES = []

# ================================================================ SERVICES
PAGES.append(dict(
    path="/services/renewal-of-regular-license/", kind="service", en_title="Renewal of Regular License",
    title="ڈرائیونگ لائسنس کی تجدید (رینیول) پنجاب: دستاویزات اور فیس | دستک 90807",
    desc="پنجاب میں ڈرائیونگ لائسنس کی تجدید کا طریقہ، دستاویزات، فیس اور وقت۔ 1 سے 5 سال کے لیے تجدید۔ رجسٹرڈ دستک فیسیلیٹیٹر کوڈ 90807، واٹس ایپ 0345-5583530۔",
    h1="ڈرائیونگ لائسنس کی تجدید (رینیول)، پنجاب", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈرائیونگ لائسنس کی تجدید", "/ur/services/renewal-of-regular-license/")],
    body=service_body(
        "ڈرائیونگ لائسنس کی تجدید",
        "پنجاب میں ریگولر ڈرائیونگ لائسنس کی تجدید (رینیول) دستک سروس کے ذریعے گھر بیٹھے ہو جاتی ہے۔ آپ کو اصل شناختی کارڈ، پرانا لائسنس اور سفید بیک گراؤنڈ والی تازہ تصویر چاہیے۔ لائسنس 1، 2، 3، 4 یا 5 سال کے لیے بن سکتا ہے اور تقریباً 10 دن میں کوریئر سے گھر پہنچ جاتا ہے۔ سرکاری فیس کیٹیگری اور مدت کے حساب سے بنتی ہے اور PSID پر لکھی ہوتی ہے۔",
        [("محکمہ", "ٹریفک پولیس پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 10 دن"), ("ڈیلیوری", "کوریئر کے ذریعے گھر پر")],
        ["اصل شناختی کارڈ (CNIC)", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)", "پرانا ڈرائیونگ لائسنس (اصل)",
         "میڈیکل سرٹیفیکیٹ، صرف اگر عمر 50 سال سے زیادہ ہو", "ایف آئی آر یا گمشدگی رپورٹ کی کاپی، اگر اصل لائسنس گم ہو گیا ہو"],
        ["واٹس ایپ پر اپنا شناختی کارڈ اور پرانا لائسنس بھیجیں تاکہ کیٹیگری اور اہلیت چیک ہو جائے۔",
         "طے کریں کہ لائسنس کتنے سال (1 سے 5) کے لیے بنوانا ہے۔ فیس کا اندازہ <a href=\"/ur/calculators/\">فیس کیلکولیٹر</a> سے لگائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا ہمیں کال کریں۔",
         "فیسیلیٹیٹر آپ کی لائیو تصویر لے کر درخواست جمع کرواتا ہے اور PSID بنتا ہے۔",
         "PSID کی ادائیگی بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے کریں۔",
         "تقریباً 10 دن میں نیا لائسنس کوریئر سے آپ کے پتے پر آ جاتا ہے۔ اسٹیٹس <a href=\"/ur/guides/how-to-track-driving-license-in-punjab/\">یہاں سے ٹریک کریں</a>۔"],
        [("سرکاری فیس", "لائسنس کی کیٹیگری اور مدت (1 سے 5 سال) کے مطابق مختلف"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"),
         ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"), ("ادائیگی", "PSID کے ذریعے"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        related=(R["renew_guide"], R["track"], R["learner"], R["calc"])),
    faqs=[
        ("لائسنس رینیو کیسے کریں؟ (License renew kaise karein)", "دستک ایپ میں Doorstep Delivery منتخب کر کے کوڈ 90807 لکھیں، یا واٹس ایپ 0345-5583530 پر رابطہ کریں۔ فیسیلیٹیٹر گھر آ کر تصویر لیتا ہے، درخواست جمع کرواتا ہے اور لائسنس کوریئر سے آپ کو مل جاتا ہے۔"),
        ("ڈرائیونگ لائسنس کی تجدید کی فیس کتنی ہے؟", "سرکاری فیس لائسنس کی کیٹیگری اور مدت کے حساب سے بنتی ہے۔ اس کے ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں (تربیتی مینول کے مطابق)۔ حتمی رقم PSID پر لکھی ہوتی ہے۔"),
        ("لائسنس کتنے سال کے لیے رینیو ہو سکتا ہے؟", "تربیتی مینول کے مطابق 1، 2، 3، 4 یا 5 سال کے لیے۔"),
        ("50 سال سے زیادہ عمر میں کیا چاہیے؟", "50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفیکیٹ بھی ضروری ہے۔"),
        ("لائسنس گم ہو گیا ہو تو کیا کریں؟", "گمشدگی کی ایف آئی آر یا لاسٹ رپورٹ کی کاپی ساتھ لگائیں۔ ہم لاسٹ رپورٹ بنوانے میں بھی مدد کرتے ہیں۔"),
        ("Kya Gujar Khan se bahar bhi madad milti hai?", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ ہوتی ہے۔ گھر پر وزٹ گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/learner-driving-license/", kind="service", en_title="Learner Driving License",
    title="لرنر پرمٹ (لرنر لائسنس) کیسے بنوائیں؟ فیس اور دستاویزات | دستک 90807",
    desc="پنجاب میں لرنر پرمٹ (لرنر ڈرائیونگ لائسنس) بنوانے کا طریقہ: صرف شناختی کارڈ اور تصویر، سرکاری فیس 500 روپے فی کیٹیگری، 180 دن کارآمد۔ دستک کوڈ 90807۔",
    h1="لرنر پرمٹ (لرنر ڈرائیونگ لائسنس)", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("لرنر پرمٹ", "/ur/services/learner-driving-license/")],
    body=service_body(
        "لرنر پرمٹ",
        "گاڑی یا موٹر سائیکل چلانا سیکھنے والے ہر شخص کے لیے لرنر پرمٹ ضروری ہے۔ پنجاب میں یہ دستک سروس کے ذریعے گھر بیٹھے بن جاتا ہے: صرف اصل شناختی کارڈ اور سفید بیک گراؤنڈ والی لائیو تصویر چاہیے۔ سرکاری فیس 500 روپے فی کیٹیگری ہے، پرمٹ کی PDF موقع پر مل جاتی ہے اور یہ 180 دن کارآمد رہتا ہے۔",
        [("محکمہ", "ٹریفک پولیس پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "زیادہ سے زیادہ 2 دن"), ("ملتا کیسے ہے", "PDF موقع پر")],
        ["اصل شناختی کارڈ (CNIC)", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)", "میڈیکل سرٹیفیکیٹ، صرف اگر عمر 50 سال سے زیادہ ہو"],
        ["طے کریں کہ کون سی کیٹیگری چاہیے، مثلاً موٹر سائیکل، کار یا دونوں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا واٹس ایپ کریں۔",
         "فیسیلیٹیٹر آپ کی لائیو تصویر لے کر درخواست جمع کرواتا ہے۔",
         "PSID پر لکھی فیس ادا کریں۔",
         "لرنر پرمٹ کی PDF موقع پر مل جاتی ہے۔ اسے سنبھال کر رکھیں اور 180 دن کے اندر پکا لائسنس بنوانے کی تیاری کریں۔"],
        [("سرکاری فیس", "Rs 500 فی کیٹیگری"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"), ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"),
         ("کارآمد مدت", "180 دن"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>اہم شرائط</h2><ul><li>کمرشل لائسنس کے لیے عمر 21 سال سے زیادہ ہونی چاہیے۔</li><li>لرنر پرمٹ 180 دن کے لیے کارآمد ہوتا ہے۔ مدت ختم ہو جائے تو لرنر پرمٹ کی تجدید بھی دستک کے ذریعے ہو جاتا ہے۔</li><li>شناختی کارڈ کارآمد ہو اور اس کی تفصیلات درخواست سے میل کھاتی ہوں۔</li></ul></section>',
        related=(R["renew"], R["renew_guide"], R["calc"], R["track"])),
    faqs=[
        ("لرنر پرمٹ کیسے بنوائیں؟ (Learner license kaise banaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھ کر بکنگ کریں یا واٹس ایپ 0345-5583530 کریں۔ صرف شناختی کارڈ اور لائیو تصویر چاہیے۔"),
        ("لرنر پرمٹ کی فیس کتنی ہے؟", "تربیتی مینول کے مطابق سرکاری فیس 500 روپے فی کیٹیگری ہے، ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے۔ حتمی رقم PSID پر ہوتی ہے۔"),
        ("لرنر پرمٹ کتنے دن چلتا ہے؟", "180 دن۔"),
        ("لرنر پرمٹ کتنی دیر میں ملتا ہے؟", "عام طور پر موقع پر ہی PDF مل جاتی ہے، زیادہ سے زیادہ 2 دن۔"),
        ("کیا ٹیسٹ دینا پڑتا ہے؟", "لرنر پرمٹ کے لیے ٹیسٹ نہیں ہوتا۔ پکے لائسنس کے لیے ٹریفک پولیس کے طریقہ کار کے مطابق ٹیسٹ ہوتا ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/character-certificate/", kind="service", en_title="Police Character Certificate",
    title="پولیس کریکٹر سرٹیفیکیٹ پنجاب: فیس اور دستاویزات | دستک 90807",
    desc="پنجاب پولیس کریکٹر سرٹیفیکیٹ بیرون ملک سفر، نوکری اور امیگریشن کے لیے۔ دستاویزات، سرکاری فیس 1,000 روپے، 3 دن میں کوریئر۔ رجسٹرڈ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="پولیس کریکٹر سرٹیفیکیٹ (پنجاب پولیس)", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("پولیس کریکٹر سرٹیفیکیٹ", "/ur/services/character-certificate/")],
    body=service_body(
        "پولیس کریکٹر سرٹیفیکیٹ",
        "پولیس کریکٹر سرٹیفیکیٹ بیرون ملک سفر، باہر نوکری اور امیگریشن کے لیے ضروری ہوتا ہے۔ دستک سروس کے ذریعے پنجاب پولیس کا کریکٹر سرٹیفیکیٹ گھر بیٹھے اپلائی ہو جاتا ہے۔ اصل شناختی کارڈ، پاسپورٹ اور لائیو تصویر چاہیے۔ سرکاری فیس 1,000 روپے ہے اور سرٹیفیکیٹ تقریباً 3 دن میں کوریئر سے آتا ہے۔",
        [("محکمہ", "پنجاب پولیس"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 3 دن"), ("ڈیلیوری", "کوریئر کے ذریعے")],
        ["اصل شناختی کارڈ (CNIC)", "اصل پاسپورٹ", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)",
         "اتھارٹی لیٹر، اگر درخواست گزار بیرون ملک ہو۔ اس پر متعلقہ ایمبیسی کی مہر ہو، ورنہ دو معزز افراد کی تصدیق ہو جو درخواست گزار کو جانتے ہوں۔ لیٹر میں بیرون ملک قیام کی مدت بھی لکھی ہو۔"],
        ["پہلے معلوم کریں کہ آپ کو کریکٹر سرٹیفیکیٹ چاہیے یا جنرل پولیس ویریفکیشن۔ دونوں الگ خدمات ہیں۔",
         "اگر سرٹیفیکیٹ کسی دوسرے ملک کے لیے ہے تو پاسپورٹ پر اس ملک کا ویزا لگا ہونا چاہیے، ورنہ درخواست آگے نہیں بڑھتی۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا واٹس ایپ کریں۔",
         "فیسیلیٹیٹر آپ کی دستاویزات چیک کر کے لائیو تصویر لیتا ہے اور درخواست جمع کرواتا ہے۔",
         "PSID پر لکھی رقم ادا کریں۔",
         "پنجاب پولیس کی منظوری کے بعد سرٹیفیکیٹ تقریباً 3 دن میں کوریئر سے آ جاتا ہے۔"],
        [("سرکاری فیس", "Rs 1,000"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"), ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"),
         ("ادائیگی", "PSID کے ذریعے"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>بیرون ملک موجود افراد کے لیے</h2><p>اگر درخواست گزار بیرون ملک ہے تو اس کا کوئی خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ اتھارٹی لیٹر پر ایمبیسی کی مہر ہو یا دو معزز افراد کی تصدیق۔ لیٹر بھیجنے سے پہلے واٹس ایپ پر چیک کروا لیں تاکہ درخواست مسترد نہ ہو۔</p></section>',
        related=(R["character_guide"], R["gk"], R["contact"])),
    faqs=[
        ("کریکٹر سرٹیفیکیٹ کیسے بنوائیں؟ (Character certificate kaise banwaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ شناختی کارڈ، پاسپورٹ اور لائیو تصویر چاہیے۔"),
        ("پولیس کریکٹر سرٹیفیکیٹ کی فیس کتنی ہے؟", "تربیتی مینول کے مطابق سرکاری فیس 1,000 روپے، دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے۔ حتمی رقم PSID پر ہوتی ہے۔"),
        ("کریکٹر سرٹیفیکیٹ کتنے دن میں ملتا ہے؟", "عام طور پر تقریباً 3 دن، پنجاب پولیس کی منظوری کے بعد کوریئر سے۔"),
        ("کیا ویزا ضروری ہے؟", "اگر سرٹیفیکیٹ کسی دوسرے ملک کے لیے چاہیے تو پاسپورٹ پر ویزا لگا ہونا ضروری ہے۔"),
        ("کریکٹر سرٹیفیکیٹ اور جنرل پولیس ویریفکیشن میں کیا فرق ہے؟", "یہ دو الگ خدمات ہیں۔ جس ادارے کو دستاویز چاہیے اس سے پوچھ لیں کہ اسے کون سی سروس چاہیے۔"),
        ("کیا فیسیلیٹیٹر سرٹیفیکیٹ منظور کرتا ہے؟", "نہیں۔ فیسیلیٹیٹر صرف درخواست تیار اور جمع کرواتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔"),
        ("ادائیگی کیسے کروں؟", "فیس سرکاری سسٹم خود بناتا ہے۔ دستک ایپ میں ادائیگی کے طریقوں میں PSID (کسی بھی بینکنگ ایپ یا موبائل والٹ سے)، IBFT، JazzCash، Easypaisa اور کیش آن ڈیلیوری شامل ہیں۔ دستیاب طریقے سروس کے لحاظ سے مختلف ہو سکتے ہیں۔"),
        ("کیا بیانِ حلفی ضروری ہے؟", "نہیں، اس وقت بیانِ حلفی ضروری نہیں۔ دستاویزات کی تازہ فہرست ہمیشہ دستک ایپ میں چیک کریں۔"),
        ("کیا یہ سرکاری ویب سائٹ ہے؟", "نہیں۔ یہ ایک رجسٹرڈ فیسیلیٹیٹر کی آزاد فیسیلیٹیشن سروس ہے۔ آپ ہمارے بارے میں صفحے پر میری تصدیق کر سکتے ہیں۔"),
        ("میری دستاویزات کا کیا ہوتا ہے؟", "درخواست مکمل اور ڈیلیور ہوتے ہی کسٹمر کی دستاویزات ڈیلیٹ کر دی جاتی ہیں۔ میں کبھی پاس ورڈ یا OTP نہیں مانگتا۔"),
    ]))

PAGES.append(dict(
    path="/services/transfer-of-motor-vehicle/", kind="service", en_title="Transfer of Motor Vehicle",
    title="گاڑی اور موٹر سائیکل کی ملکیت کی منتقلی (ٹرانسفر) پنجاب: طریقہ اور فیس | دستک 90807",
    desc="پنجاب میں گاڑی یا موٹر سائیکل اپنے نام منتقل کروانے کا طریقہ: دستاویزات، خریدار اور بیچنے والے کی بائیومیٹرک، PSID فیس اور 10 دن میں کوریئر۔ دستک کوڈ 90807۔",
    h1="گاڑی اور موٹر سائیکل کی ملکیت کی منتقلی (ٹرانسفر)", og="/assets/og/vehicles.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("گاڑی کی ملکیت کی منتقلی", "/ur/services/transfer-of-motor-vehicle/")],
    body=service_body(
        "گاڑی کی ملکیت کی منتقلی",
        "پنجاب میں رجسٹرڈ گاڑی یا موٹر سائیکل کی ملکیت نئے مالک کے نام کروانے کے لیے گاڑی کا نمبر، خریدار کا اصل شناختی کارڈ اور گاڑی کی اصل فائل اور بُک یا کارڈ چاہیے۔ خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق لازمی ہے۔ سرکاری فیس گاڑی کی قسم کے مطابق PSID پر بنتی ہے، اور نیا رجسٹریشن کارڈ تقریباً 10 دن میں کوریئر سے آتا ہے۔",
        [("محکمہ", "ایکسائز، ٹیکسیشن اینڈ نارکوٹکس کنٹرول، پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 10 دن"), ("ڈیلیوری", "کوریئر کے ذریعے کارڈ")],
        ["گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر", "خریدار کا اصل شناختی کارڈ (CNIC)", "گاڑی کی اصل فائل اور رجسٹریشن بُک یا اسمارٹ کارڈ",
         "خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق"],
        ["گاڑی کا نمبر اور کارڈ یا بُک کی تصویر واٹس ایپ پر بھیجیں تاکہ واجب الادا ٹوکن ٹیکس اور دیگر تفصیلات چیک ہو جائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا کال کریں۔",
         "فیسیلیٹیٹر درخواست جمع کرواتا ہے اور سرکاری PSID بنتا ہے۔",
         "PSID پر لکھی سرکاری فیس بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے ادا کریں۔",
         "خریدار اور بیچنے والا دونوں بائیومیٹرک تصدیق مکمل کریں۔",
         "تقریباً 10 دن میں نیا رجسٹریشن کارڈ کوریئر سے آ جاتا ہے۔"],
        [("سرکاری فیس", "گاڑی کی قسم اور انجن (سی سی) کے مطابق، PSID پر لکھی ہوتی ہے"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"),
         ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"), ("فیس کا اندازہ", '<a href="/ur/calculators/">کار اور موٹر سائیکل فیس کیلکولیٹر</a> (صرف اندازہ)'),
         ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>درخواست مسترد ہونے سے کیسے بچیں؟</h2><ul><li>گاڑی کا نمبر رجسٹریشن کے کاغذات سے بالکل ملتا ہو۔</li><li>خریدار کا شناختی کارڈ کارآمد اور واضح ہو۔</li><li>خریدار اور بیچنے والا دونوں بائیومیٹرک کے لیے دستیاب ہوں۔</li><li>پچھلا ٹوکن ٹیکس پہلے سے چیک کر لیں۔</li></ul></section>',
        related=(R["vehicle_guide"], R["token"], R["calc"])),
    faqs=[
        ("گاڑی کی ملکیت کی منتقلی کیسے کروائیں؟ (Gari transfer kaise karwayen)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ گاڑی کا نمبر، خریدار کا شناختی کارڈ اور فائل اور بُک یا کارڈ تیار رکھیں۔"),
        ("پنجاب میں گاڑی کی ملکیت کی منتقلی کی فیس کتنی ہے؟", "سرکاری فیس گاڑی کی قسم کے مطابق مختلف ہوتی ہے اور PSID پر لکھی ہوتی ہے۔ اس کے ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں۔ اندازے کے لیے فیس کیلکولیٹر دیکھیں۔"),
        ("موٹر سائیکل کی ملکیت کی منتقلی کیسے ہوتی ہے؟ (Bike transfer kaise karein)", "طریقہ گاڑی جیسا ہی ہے: بائیک کا نمبر، خریدار کا شناختی کارڈ، اصل فائل اور کارڈ، اور دونوں فریقوں کی بائیومیٹرک۔"),
        ("کیا بیچنے والے کی بائیومیٹرک ضروری ہے؟", "جی ہاں، خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق لازمی ہے۔"),
        ("نیا کارڈ کتنے دن میں آتا ہے؟", "عام طور پر تقریباً 10 دن میں کوریئر سے۔ ڈیلیوری کا وقت مختلف ہو سکتا ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/token-tax/", kind="service", en_title="Token Tax",
    title="ٹوکن ٹیکس پنجاب: گھر بیٹھے جمع کروائیں | دستک 90807",
    desc="پنجاب میں گاڑی اور موٹر سائیکل کا سالانہ ٹوکن ٹیکس گھر بیٹھے جمع کروائیں۔ صرف گاڑی کا نمبر چاہیے، PSID سے ادائیگی، کام موقع پر مکمل۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ٹوکن ٹیکس (گاڑی اور موٹر سائیکل)", og="/assets/og/vehicles.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ٹوکن ٹیکس", "/ur/services/token-tax/")],
    body=service_body(
        "ٹوکن ٹیکس",
        "ٹوکن ٹیکس گاڑی کا سالانہ سرکاری ٹیکس ہے جو سڑک پر قانونی طور پر گاڑی چلانے کے لیے ضروری ہے۔ دستک سروس سے صرف گاڑی کے نمبر کے ساتھ ٹوکن ٹیکس جمع ہو جاتا ہے۔ رقم گاڑی کے ماڈل، سال اور سرکاری پالیسی کے مطابق PSID پر بنتی ہے، اور کام عام طور پر موقع پر مکمل ہو جاتا ہے۔",
        [("محکمہ", "ایکسائز، ٹیکسیشن اینڈ نارکوٹکس کنٹرول، پنجاب"), ("علاقہ", "پورا پنجاب"), ("وقت", "موقع پر، زیادہ سے زیادہ 2 دن"), ("ضرورت", "صرف گاڑی کا نمبر")],
        ["گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر"],
        ["واٹس ایپ پر گاڑی کا نمبر بھیجیں یا دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807)۔",
         "فیسیلیٹیٹر سرکاری سسٹم سے واجب الادا ٹوکن ٹیکس چیک کر کے PSID بناتا ہے۔",
         "کمرشل گاڑیوں کے لیے 3، 6، 9 ماہ یا 1 سال کی مدت منتخب کریں۔",
         "PSID پر لکھی رقم بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے ادا کریں۔",
         "ادائیگی کے بعد سروس موقع پر مکمل ہو جاتی ہے۔ رسید سنبھال کر رکھیں۔"],
        [("سرکاری ٹوکن ٹیکس", "گاڑی کے ماڈل، سال اور سرکاری پالیسی کے مطابق، PSID پر لکھا ہوتا ہے"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"),
         ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"), ("کمرشل گاڑیاں", "3، 6، 9 ماہ یا 1 سال"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        related=(R["vehicle_guide"], R["transfer"], R["calc"])),
    faqs=[
        ("ٹوکن ٹیکس آن لائن کیسے جمع کروائیں؟ (Token tax online kaise jama karein)", "واٹس ایپ 0345-5583530 پر گاڑی کا نمبر بھیجیں یا دستک ایپ میں کوڈ 90807 کے ساتھ بکنگ کریں۔ PSID بنتا ہے اور آپ موبائل سے ادائیگی کر دیتے ہیں۔"),
        ("ٹوکن ٹیکس کتنا ہے؟", "رقم گاڑی کے ماڈل، سال اور سرکاری پالیسی کے مطابق ہوتی ہے اور PSID پر لکھی ہوتی ہے۔ ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں۔"),
        ("ٹوکن ٹیکس کے لیے کیا چاہیے؟", "صرف گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر۔"),
        ("کمرشل گاڑی کا ٹوکن ٹیکس کیسے ہوتا ہے؟", "کمرشل گاڑیوں کے لیے 3، 6، 9 ماہ یا 1 سال کی مدت منتخب کی جا سکتی ہے۔"),
        ("کیا گاڑی کی ملکیت کی منتقلی سے پہلے ٹوکن ٹیکس ضروری ہے؟", "منتقلی سے پہلے واجب الادا ٹوکن ٹیکس چیک کر لیں۔ ہم دونوں کام ساتھ کروا دیتے ہیں۔"),
    ]))

PAGES.append(dict(
    path="/services/domicile-certificate/", kind="service", en_title="Domicile Certificate", areas=("Gujar Khan", "Rawalpindi"),
    title="ڈومیسائل کیسے بنوائیں؟ فیس 1,200 روپے، گوجرخان | دستک 90807",
    desc="گوجرخان اور راولپنڈی میں ڈومیسائل سرٹیفیکیٹ: دستاویزات کی مکمل فہرست، فیس 1,200 روپے بذریعہ PSID، 300 روپے کا بیان حلفی الگ۔ گھر پر سہولت، دستک کوڈ 90807۔",
    h1="ڈومیسائل سرٹیفیکیٹ، گوجرخان اور راولپنڈی", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈومیسائل سرٹیفیکیٹ", "/ur/services/domicile-certificate/")],
    body=service_body(
        "ڈومیسائل سرٹیفیکیٹ",
        "ڈومیسائل یہ ثابت کرتا ہے کہ آپ کس ضلع کے رہائشی ہیں۔ یہ سرکاری نوکری، تعلیمی کوٹے اور کئی دفتری کاموں میں چاہیے ہوتا ہے۔ دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے جو PSID سے ادا ہوتی ہے۔ 300 روپے کا بیان حلفی (ای اسٹامپ) الگ سے چاہیے۔ دستاویزات تحصیل (اسسٹنٹ کمشنر) دفتر میں جمع ہوتی ہیں اور تیار ڈومیسائل فیسیلیٹیٹر آپ تک پہنچاتا ہے۔",
        [("محکمہ", "بورڈ آف ریونیو، پنجاب"), ("علاقہ", "گوجرخان، راولپنڈی اور قریبی علاقے"), ("وقت", "15 دن تک"), ("ملتا کیسے ہے", "اسسٹنٹ کمشنر دفتر سے لے کر گھر پر")],
        ["درخواست فارم P-1 (تصدیق شدہ)", "درخواست گزار کی تازہ تصویر (تصدیق شدہ)", "درخواست گزار کا شناختی کارڈ یا ب فارم (اصل، کاپی اور تصدیق)",
         "والد، والدہ یا شوہر کا شناختی کارڈ (اصل، کاپی اور تصدیق)", "300 روپے کا بیان حلفی (ای اسٹامپ)", "تازہ ترین تعلیمی سرٹیفیکیٹ (تصدیق شدہ)",
         "یوٹیلیٹی بل (اصل، کاپی اور تصدیق)"],
        ["واٹس ایپ پر اپنی دستاویزات کی تصاویر بھیجیں تاکہ کمی پہلے ہی پوری ہو جائے۔",
         "یقینی بنائیں کہ آپ کا موجودہ اور مستقل پتہ ایک ہی ضلع کا ہو۔",
         "300 روپے کا بیان حلفی (ای اسٹامپ) تیار کریں، یا یہ بھی دستک کے ذریعے بنوائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا کال کریں۔",
         "PSID پر لکھی 1,200 روپے کی رقم ادا کریں۔",
         "فیسیلیٹیٹر دستاویزات اسسٹنٹ کمشنر (تحصیل) دفتر میں جمع کرواتا ہے اور منظوری کے بعد ڈومیسائل آپ تک پہنچاتا ہے۔"],
        [("ڈومیسائل (دستک سروس)", "<b>کل Rs 1,200</b>، PSID کے ذریعے"), ("بیان حلفی (ای اسٹامپ)", "Rs 300 کا ای اسٹامپ الگ سے درکار ہے"),
         ("ای اسٹامپ دستک کے ذریعے", "کل Rs 1,250 (Rs 300 ای اسٹامپ + Rs 950 فیسیلیٹیٹر چارجز)"), ("وقت", "15 دن تک، محکمے کی منظوری پر منحصر")],
        extra='<section class="service-module"><h2>ڈومیسائل کی دیگر خدمات</h2><p>ہم ڈومیسائل سے متعلق یہ کام بھی کرواتے ہیں:</p><ul><li><a href="/ur/services/duplicate-domicile/">ڈپلیکیٹ ڈومیسائل</a>: ڈومیسائل گم یا خراب ہو جائے تو نیا ڈپلیکیٹ</li><li><a href="/ur/services/modification-domicile/">ڈومیسائل میں ترمیم</a>: ڈومیسائل میں غلطی کی درستی</li><li><a href="/ur/services/noc-for-domicile-transfer/">ڈومیسائل منتقلی کا این او سی</a>: ڈومیسائل دوسرے ضلع منتقل کرنے کے لیے</li></ul></section>',
        related=(R["gk"], R["contact"])),
    faqs=[
        ("ڈومیسائل کیسے بنوائیں؟ (Domicile kaise banaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ اوپر دی گئی دستاویزات تیار رکھیں۔ فیسیلیٹیٹر انہیں تحصیل دفتر میں جمع کرواتا ہے۔"),
        ("ڈومیسائل کی فیس کتنی ہے؟", "دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے جو PSID سے ادا ہوتی ہے۔ 300 روپے کا بیان حلفی (ای اسٹامپ) الگ سے چاہیے۔"),
        ("کیا ای اسٹامپ بھی آپ بنوا دیتے ہیں؟", "جی ہاں۔ دستک کے ذریعے 300 روپے کا ای اسٹامپ بنوانے کی کل رقم 1,250 روپے ہے۔"),
        ("ڈومیسائل کتنے دن میں بنتا ہے؟", "15 دن تک، محکمے کی منظوری پر منحصر۔"),
        ("کیا دوسرے ضلع کا پتہ چل سکتا ہے؟", "نہیں۔ موجودہ اور مستقل پتہ ایک ہی ضلع کا ہونا چاہیے۔ ضلع بدلنا ہو تو ڈومیسائل کی منتقلی کا این او سی لیں۔"),
        ("Domicile kahan jama hota hai?", "دستاویزات متعلقہ تحصیل یعنی اسسٹنٹ کمشنر دفتر میں جمع ہوتی ہیں۔ یہ کام فیسیلیٹیٹر خود کرتا ہے۔"),
    ]))

# ================================================================ GUIDES
PAGES.append(dict(
    path="/guides/punjab-driving-license-renewal-online/", kind="guide", main_class="service-detail page-shell", en_title="Punjab Driving License Renewal Online",
    title="ڈرائیونگ لائسنس کی آن لائن تجدید (رینیول) پنجاب: مکمل طریقہ | دستک 90807",
    desc="پنجاب میں ڈرائیونگ لائسنس آن لائن رینیو کرنے کا مکمل طریقہ: تیاری، دستاویزات، فیس، PSID، ٹریکنگ اور عام غلطیاں۔ پورے پنجاب میں واٹس ایپ رہنمائی، دستک کوڈ 90807۔",
    h1="پنجاب میں ڈرائیونگ لائسنس کی آن لائن تجدید کا مکمل طریقہ", eyebrow='<p class="eyebrow">ڈرائیونگ لائسنس گائیڈ</p>',
    og="/assets/punjab-driving-license-renewal-guide-dastak-90807-og.jpg",
    og_alt="پنجاب ڈرائیونگ لائسنس کی تجدید گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
    crumbs=[("گائیڈز", "/ur/guides/"), ("لائسنس کی تجدید گائیڈ", "/ur/guides/punjab-driving-license-renewal-online/")],
    body=guide_body(
        "پنجاب میں ڈرائیونگ لائسنس رینیو کروانے کے لیے اصل شناختی کارڈ، پرانا لائسنس اور سفید بیک گراؤنڈ والی تازہ تصویر چاہیے (50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفیکیٹ بھی)۔ دستک سروس کے ذریعے درخواست جمع ہوتی ہے، PSID پر سرکاری فیس ادا ہوتی ہے اور نیا لائسنس تقریباً 10 دن میں کوریئر سے گھر آ جاتا ہے۔ لائسنس 1 سے 5 سال کے لیے بن سکتا ہے۔",
        [
            ("تجدید سے پہلے کیا تیاری کریں؟", "<ul><li>اصل شناختی کارڈ، جس کی مدت ختم نہ ہوئی ہو۔</li><li>پرانا ڈرائیونگ لائسنس، چاہے اس کی مدت ختم ہو چکی ہو۔</li><li>سفید بیک گراؤنڈ والی لائیو تصویر، جو فیسیلیٹیٹر موقع پر لیتا ہے۔</li><li>50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفیکیٹ۔</li><li>لائسنس گم ہو گیا ہو تو ایف آئی آر یا لاسٹ رپورٹ کی کاپی۔</li><li>ایک فعال موبائل نمبر، کیونکہ ڈیلیوری والا رابطہ کر سکتا ہے۔</li></ul>"),
            ("آن لائن تجدید کیسے ہوتی ہے؟", f"<ol><li>دستک ایپ میں Doorstep Delivery منتخب کریں اور کوڈ {CODE} لکھیں، یا واٹس ایپ {PHONE} کریں۔</li><li>فیسیلیٹیٹر آپ کی کیٹیگری اور اہلیت چیک کرتا ہے۔</li><li>آپ لائسنس کی مدت (1 سے 5 سال) منتخب کرتے ہیں۔</li><li>لائیو تصویر اور دستاویزات کے ساتھ درخواست جمع ہوتی ہے اور PSID بنتا ہے۔</li><li>آپ PSID کی ادائیگی موبائل بینکنگ، جاز کیش یا ایزی پیسہ سے کرتے ہیں۔</li><li>تقریباً 10 دن میں لائسنس کوریئر سے آپ کے پتے پر پہنچ جاتا ہے۔</li></ol><p>کچھ کیٹیگریز یا بہت پرانے ختم شدہ لائسنس کے لیے لائسنسنگ سینٹر جانا پڑ سکتا ہے۔ بکنگ سے پہلے واٹس ایپ پر اپنی صورتحال چیک کروا لیں۔</p>"),
            ("تجدید پر کتنا خرچ آتا ہے؟", RENEW_FEE_TABLE + '<p>سرکاری فیس لائسنس کی کیٹیگری، مدت اور مدت ختم ہونے کی تاریخ کے حساب سے بنتی ہے، اور حتمی رقم PSID پر لکھی ہوتی ہے۔ دستک تربیتی مینول کے مطابق فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں۔ اندازے کے لیے ہمارا <a href="/ur/calculators/tools/punjab-driving-license-fee-calculator">ڈرائیونگ لائسنس فیس کیلکولیٹر</a> استعمال کریں۔</p>'),
            ("لائسنس کا اسٹیٹس کیسے دیکھیں؟", '<p>درخواست کے بعد DLIMS پر شناختی کارڈ نمبر سے پرنٹنگ اور ڈسپیچ کا اسٹیٹس دیکھیں، پھر پاکستان پوسٹ پر ٹریکنگ آئی ڈی سے ڈیلیوری ٹریک کریں۔ مکمل طریقہ: <a href="/ur/guides/how-to-track-driving-license-in-punjab/">ڈرائیونگ لائسنس ٹریک کرنے کا طریقہ</a>۔</p>'),
            ("عام غلطیاں جن سے درخواست رکتی ہے", "<ul><li>شناختی کارڈ کی مدت ختم ہونا۔</li><li>تصویر کا بیک گراؤنڈ سفید نہ ہونا۔</li><li>50 سال سے زیادہ عمر میں میڈیکل سرٹیفیکیٹ نہ لگانا۔</li><li>گمشدہ لائسنس کی ایف آئی آر کے بغیر درخواست دینا۔</li><li>غلط یا بند موبائل نمبر دینا۔</li></ul>"),
            ("مدد کہاں سے ملے گی؟", f"<p><b>پورے پنجاب میں:</b> واٹس ایپ {PHONE} پر رہنمائی اور دستاویزات کی جانچ۔</p><p><b>گوجرخان اور راولپنڈی:</b> {AREAS} میں گھر پر وزٹ، پہلے سے وقت طے کر کے۔</p><p>دستک 90807 ایک آزاد رجسٹرڈ فیسیلیٹیٹر ہے، سرکاری دفتر نہیں۔ منظوری اور ڈیلیوری لائسنسنگ اتھارٹی کے اختیار میں ہے۔</p>"),
        ],
        hero=("/assets/punjab-driving-license-renewal-guide-dastak-90807.webp", "پنجاب ڈرائیونگ لائسنس کی تجدید گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["renew"], R["track"], R["learner"]), sources=(("https://dlims.punjab.gov.pk/", "پنجاب DLIMS (سرکاری)"), ("https://dastak.punjab.gov.pk/", "سرکاری دستک پورٹل"), ("https://sites.google.com/view/dastakservices/latest-updates-guide/driving-license-renewal-gujar-khan", "ہماری اصل سروس گائیڈ (انگریزی)"))),
    faqs=[
        ("کیا میں گوجرخان سے باہر رہ کر بھی لائسنس رینیو کروا سکتا ہوں؟", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ ہوتی ہے۔ گھر پر وزٹ صرف گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
        ("کیا کیلکولیٹر کی فیس حتمی ہوتی ہے؟", "نہیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔ حتمی رقم سرکاری سسٹم کے PSID پر ہوتی ہے۔"),
        ("Expired license renew ho sakta hai?", "جی ہاں، عام طور پر ختم شدہ لائسنس بھی رینیو ہو جاتا ہے، مگر بہت پرانے لائسنس یا کچھ کیٹیگریز کے لیے سینٹر جانا پڑ سکتا ہے۔ پہلے واٹس ایپ پر چیک کروا لیں۔"),
        ("رینیو شدہ لائسنس کتنے دن میں ملتا ہے؟", "تربیتی مینول کے مطابق تقریباً 10 دن، کوریئر سے۔"),
    ]))

PAGES.append(dict(
    path="/guides/how-to-track-driving-license-in-punjab/", kind="guide", main_class="service-detail page-shell", en_title="How to Track Your Driving License in Punjab",
    title="ڈرائیونگ لائسنس ٹریک کیسے کریں؟ DLIMS اور پاکستان پوسٹ | دستک 90807",
    desc="پنجاب میں ڈرائیونگ لائسنس کا اسٹیٹس شناختی کارڈ نمبر سے DLIMS پر چیک کریں اور پاکستان پوسٹ پر ڈیلیوری ٹریک کریں۔ آسان اردو گائیڈ، دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="پنجاب میں ڈرائیونگ لائسنس ٹریک کرنے کا طریقہ", eyebrow='<p class="eyebrow">ڈرائیونگ لائسنس گائیڈ</p>',
    og="/assets/track-driving-license-punjab-dastak-90807-og.jpg",
    og_alt="پنجاب ڈرائیونگ لائسنس ٹریکنگ گائیڈ، DLIMS اور پاکستان پوسٹ، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
    crumbs=[("گائیڈز", "/ur/guides/"), ("لائسنس ٹریکنگ", "/ur/guides/how-to-track-driving-license-in-punjab/")],
    body=guide_body(
        "پنجاب میں ڈرائیونگ لائسنس دو مرحلوں میں ٹریک ہوتا ہے۔ پہلے سرکاری DLIMS ٹریکنگ صفحے پر شناختی کارڈ نمبر سے منظوری، پرنٹنگ اور ڈسپیچ کا اسٹیٹس دیکھیں۔ پھر وہاں ملنے والی ٹریکنگ آئی ڈی سے پاکستان پوسٹ (UMS) کی ویب سائٹ پر ڈیلیوری ٹریک کریں۔",
        [
            ("مرحلہ 1: DLIMS پر پرنٹنگ اور ڈسپیچ کا اسٹیٹس", '<ol><li>سرکاری <a href="https://dlims.punjab.gov.pk/track" rel="noopener">DLIMS ٹریکنگ صفحہ</a> کھولیں۔</li><li>اپنا 13 ہندسوں کا شناختی کارڈ نمبر بغیر ڈیش کے لکھیں، یا جو تفصیل صفحہ مانگے۔</li><li>سیکیورٹی چیک مکمل کر کے سرچ کریں۔</li><li>اسٹیٹس پڑھیں۔ الفاظ بدل سکتے ہیں، مگر عام طور پر یہ مراحل ہوتے ہیں:<ul><li><b>In process / تصدیق جاری:</b> درخواست ابھی چیک ہو رہی ہے۔</li><li><b>Approved / منظور:</b> لائسنس منظور ہو گیا، پرنٹنگ کا انتظار ہے۔</li><li><b>Printed / پرنٹ:</b> کارڈ پرنٹ ہو گیا، ڈسپیچ ہونا باقی ہے۔</li><li><b>Dispatched / روانہ:</b> کارڈ ڈاک کے حوالے ہو گیا۔ ٹریکنگ آئی ڈی نظر آئے تو کاپی کر لیں۔</li></ul></li></ol>'),
            ("مرحلہ 2: پاکستان پوسٹ پر ڈیلیوری ٹریک کریں", '<ol><li>DLIMS سے ملنے والی ٹریکنگ یا کنسائنمنٹ آئی ڈی محفوظ کریں۔</li><li><a href="https://ep.gov.pk/services/ums_intro.asp" rel="noopener">پاکستان پوسٹ UMS پورٹل</a> کھولیں۔</li><li>Track &amp; Trace میں اپنا نمبر لکھیں۔</li><li>نتیجے میں ڈاک کی روانگی اور مقامی ڈاک خانے تک پہنچنے کی معلومات نظر آتی ہیں۔</li></ol><p class="ur-note">اپنا رجسٹرڈ موبائل نمبر فعال رکھیں۔ ڈاکیا ڈیلیوری سے پہلے کال کر سکتا ہے۔</p>'),
            ("ایک نظر میں: لائسنس ٹریکنگ کے مراحل", '<div class="guide-table-wrap"><table class="guide-table"><thead><tr><th scope="col">ٹریکنگ کا مرحلہ</th><th scope="col">سرکاری پورٹل</th><th scope="col">کیا درکار ہے</th><th scope="col">آپ کیا دیکھ سکتے ہیں</th></tr></thead><tbody><tr><td><strong>1. منظوری اور کارڈ کی پرنٹنگ</strong></td><td><a href="https://dlims.punjab.gov.pk/track" target="_blank" rel="noopener noreferrer">DLIMS پنجاب ٹریکنگ</a></td><td>13 ہندسوں کا شناختی کارڈ نمبر (یا جو تفصیل صفحہ مانگے)</td><td>تصدیق کی صورتحال، پرنٹنگ کا اسٹیٹس اور جہاں دستیاب ہو، ڈاک کی ٹریکنگ آئی ڈی</td></tr><tr><td><strong>2. کارڈ کی گھر پر ڈیلیوری</strong></td><td><a href="https://ep.gov.pk/services/ums_intro.asp" target="_blank" rel="noopener noreferrer">پاکستان پوسٹ EMTTS / UMS</a></td><td>DLIMS سے ملنے والی ٹریکنگ آئی ڈی</td><td>ڈاک کی ترسیل، مقامی ڈاک خانے میں پہنچنے اور ڈیلیوری کا اسٹیٹس</td></tr><tr><td><strong>3. ڈیجیٹل لائسنس</strong></td><td><a href="https://dlims.punjab.gov.pk/elicense" target="_blank" rel="noopener noreferrer">DLIMS ای لائسنس</a></td><td>DLIMS کی مانگی گئی تفصیل</td><td>جہاں دستیاب ہو، اپنے ریکارڈ کے لیے ڈیجیٹل ای لائسنس PDF ڈاؤن لوڈ کریں</td></tr></tbody></table></div>'),
            ("ای لائسنس کیسے ڈاؤن لوڈ کریں؟", '<p>منظوری کے بعد سرکاری <a href="https://dlims.punjab.gov.pk/elicense" rel="noopener">DLIMS ای لائسنس صفحے</a> سے ڈیجیٹل لائسنس دیکھا جا سکتا ہے۔ ڈیجیٹل ریکارڈ اور فزیکل کارڈ کی ڈیلیوری دو الگ مرحلے ہیں۔</p>'),
            ("لائسنس آنے میں دیر کیوں ہوتی ہے؟", "<ul><li>درخواست کی تصدیق ابھی جاری ہو۔</li><li>پرنٹنگ میں رش ہو۔</li><li>پتہ نامکمل یا غلط ہو۔</li><li>موبائل نمبر بند ہونے سے ڈاکیا رابطہ نہ کر سکے۔</li></ul><p>اسٹیٹس کئی دن تک نہ بدلے تو واٹس ایپ پر اپنی درخواست کی تفصیل بھیجیں، ہم رہنمائی کر دیں گے۔</p>"),
            ("تجدید یا نئے لائسنس میں مدد", '<p>اگر ابھی درخواست دینی ہے تو <a href="/ur/services/renewal-of-regular-license/">لائسنس کی تجدید</a> یا <a href="/ur/services/learner-driving-license/">لرنر پرمٹ</a> کا صفحہ دیکھیں۔</p>'),
        ],
        hero=("/assets/track-driving-license-punjab-dastak-90807.webp", "پنجاب ڈرائیونگ لائسنس ٹریکنگ گائیڈ، DLIMS اور پاکستان پوسٹ، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["renew_guide"], R["renew"], R["learner"]), sources=(("https://dlims.punjab.gov.pk/track", "پنجاب DLIMS ٹریکنگ (سرکاری)"), ("https://ep.gov.pk/services/ums_intro.asp", "پاکستان پوسٹ EMTTS / UMS"), ("https://dastak.punjab.gov.pk/", "سرکاری دستک پورٹل"))),
    faqs=[
        ("لائسنس کا اسٹیٹس کیسے چیک کریں؟ (License status check kaise karein)", "سرکاری DLIMS ٹریکنگ صفحے پر اپنا 13 ہندسوں کا شناختی کارڈ نمبر لکھ کر اسٹیٹس دیکھیں۔"),
        ("Dispatched کا کیا مطلب ہے؟", "اس کا مطلب ہے کہ کارڈ ڈاک کے حوالے ہو گیا ہے۔ اب پاکستان پوسٹ پر ٹریکنگ آئی ڈی سے ڈیلیوری دیکھیں۔"),
        ("ٹریکنگ آئی ڈی کہاں ملتی ہے؟", "اسٹیٹس Dispatched ہونے پر DLIMS کے نتیجے میں ٹریکنگ یا کنسائنمنٹ نمبر نظر آتا ہے۔"),
        ("پنجاب میں ڈرائیونگ لائسنس ملنے میں کتنے دن لگتے ہیں؟", "بہت سے درخواست گزاروں کو بائیومیٹرک تصدیق اور فیس جمع ہونے کے بعد عموماً دو سے چار ہفتوں میں اسمارٹ کارڈ مل جاتا ہے، مگر وقت پرنٹنگ کے کام اور ڈاک کی ترسیل کے حساب سے بدل سکتا ہے۔ پرنٹنگ اور ڈسپیچ لائسنسنگ اتھارٹی کے پاس ہے، اس لیے تازہ اسٹیٹس کے لیے DLIMS ٹریکنگ صفحہ دیکھیں۔"),
        ("کیا فزیکل کارڈ آنے تک پنجاب ای لائسنس کارآمد ہے؟", "اگر DLIMS آپ کے ریکارڈ کے لیے ای لائسنس دیتا ہے تو آپ اسے PDF میں ڈاؤن لوڈ کر کے فون میں رکھ سکتے ہیں۔ کسی خاص صورتحال میں یہ قبول ہو گا یا نہیں، یہ ٹریفک حکام طے کرتے ہیں، اس لیے اصل شناختی کارڈ ساتھ رکھیں اور شک ہو تو اپنے لائسنسنگ آفس سے تصدیق کر لیں۔"),
        ("کیا ختم شدہ لائسنس آن لائن یا گھر بیٹھے رینیو ہو سکتا ہے؟", "رجسٹرڈ فیسیلیٹیٹر محمد عثمان (کوڈ 90807) گوجرخان، راولپنڈی اور پورے پنجاب میں لائسنس کی تجدید کے لیے دستاویزات کی جانچ اور درخواست میں مدد کرتے ہیں۔ اپنی کیٹیگری اور اہلیت جاننے کے لیے واٹس ایپ 0345-5583530 پر پیغام بھیجیں۔"),
        ("کیا دستک 90807 سرکاری ٹریکنگ ویب سائٹ ہے؟", "نہیں۔ ہم آزاد فیسیلیٹیٹر ہیں اور صرف رہنمائی کرتے ہیں۔ ٹریکنگ سرکاری DLIMS اور پاکستان پوسٹ کی ویب سائٹس پر ہوتی ہے۔"),
    ]))

PAGES.append(dict(
    path="/guides/punjab-police-character-certificate-online/", kind="guide", main_class="service-detail page-shell", en_title="Punjab Police Character Certificate",
    title="پولیس کریکٹر سرٹیفیکیٹ کیسے بنوائیں؟ مکمل گائیڈ | دستک 90807",
    desc="پنجاب پولیس کریکٹر سرٹیفیکیٹ کب چاہیے، کون سی دستاویزات، فیس، بیرون ملک سے اپلائی کرنے کا طریقہ اور سرٹیفیکیٹ کی تصدیق۔ پورے پنجاب میں مدد، دستک کوڈ 90807۔",
    h1="پنجاب پولیس کریکٹر سرٹیفیکیٹ: مکمل گائیڈ", eyebrow='<p class="eyebrow">پولیس دستاویزات گائیڈ</p>',
    og="/assets/punjab-police-character-certificate-guide-dastak-90807-og.jpg",
    og_alt="پنجاب پولیس کریکٹر سرٹیفیکیٹ گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
    crumbs=[("گائیڈز", "/ur/guides/"), ("کریکٹر سرٹیفیکیٹ گائیڈ", "/ur/guides/punjab-police-character-certificate-online/")],
    body=guide_body(
        "پنجاب پولیس کریکٹر سرٹیفیکیٹ کے لیے اصل شناختی کارڈ، پاسپورٹ اور سفید بیک گراؤنڈ والی لائیو تصویر چاہیے۔ اگر سرٹیفیکیٹ کسی دوسرے ملک کے لیے ہے تو پاسپورٹ پر ویزا ضروری ہے۔ دستک تربیتی مینول کے مطابق سرکاری فیس 1,000 روپے ہے اور سرٹیفیکیٹ تقریباً 3 دن میں کوریئر سے آتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔",
        [
            ("کریکٹر سرٹیفیکیٹ کب چاہیے ہوتا ہے؟", "<p>بیرون ملک سفر، باہر کی کمپنیوں میں نوکری، امیگریشن اور کئی ویزا درخواستوں کے لیے۔ جس ادارے نے سرٹیفیکیٹ مانگا ہے اس سے پوچھ لیں کہ اسے کریکٹر سرٹیفیکیٹ چاہیے یا جنرل پولیس ویریفکیشن، کیونکہ یہ دو الگ خدمات ہیں۔</p>"),
            ("کون سی دستاویزات چاہئیں؟", "<ul><li>اصل شناختی کارڈ (CNIC)</li><li>اصل پاسپورٹ، اور دوسرے ملک کے لیے ہو تو اس پر ویزا</li><li>سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)</li><li>بیرون ملک موجود درخواست گزار کے لیے اتھارٹی لیٹر</li></ul>"),
            ("فیس اور وقت", '<table class="ur-fee"><tbody><tr><th scope="row">سرکاری فیس</th><td>Rs 1,000</td></tr><tr><th scope="row">دستک فیسیلیٹیٹر چارجز</th><td>Rs 950</td></tr><tr><th scope="row">پلیٹ فارم چارجز</th><td>Rs 19</td></tr><tr><th scope="row">وقت</th><td>تقریباً 3 دن، کوریئر سے</td></tr></tbody></table><p class="ur-note">' + FEE_SOURCE + '</p>'),
            ("بیرون ملک سے کیسے اپلائی کریں؟", "<p>درخواست گزار بیرون ملک ہو تو اس کا خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ لیٹر پر متعلقہ ایمبیسی کی مہر ہو، ورنہ دو معزز افراد کی تصدیق ہو جو درخواست گزار کو جانتے ہوں۔ لیٹر میں بیرون ملک قیام کی مدت ضرور لکھیں۔ بھیجنے سے پہلے واٹس ایپ پر چیک کروا لیں۔</p>"),
            ("سرٹیفیکیٹ کی تصدیق کیسے کریں؟", '<p>جاری شدہ سرٹیفیکیٹ سرکاری <a href="https://pkm.punjab.gov.pk/public/app/verification" rel="noopener">پنجاب پولیس ویریفکیشن صفحے</a> پر چیک کیا جا سکتا ہے۔ تفصیل نہ ملے تو جاری کرنے والے دفتر سے رابطہ کریں۔</p>'),
            ("ہم کہاں مدد کرتے ہیں؟", f"<p>پورے پنجاب کے لیے واٹس ایپ پر دستاویزات کی جانچ اور رہنمائی۔ {AREAS} میں گھر پر وزٹ، پہلے سے وقت طے کر کے۔</p>"),
        ],
        hero=("/assets/punjab-police-character-certificate-guide-dastak-90807.webp", "پنجاب پولیس کریکٹر سرٹیفیکیٹ گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["character"], R["gk"], R["contact"]), sources=(("https://pkm.punjab.gov.pk/", "پنجاب پولیس خدمت مرکز (سرکاری)"), ("https://pkm.punjab.gov.pk/public/app/verification", "پولیس سرٹیفیکیٹ کی تصدیق (سرکاری)"), ("https://dastak.punjab.gov.pk/", "سرکاری دستک پورٹل"), ("https://sites.google.com/view/dastakservices/latest-updates-guide/punjab-police-character-certificate-online", "ہماری اصل سروس گائیڈ (انگریزی)"))),
    faqs=[
        ("کیا کریکٹر سرٹیفیکیٹ اور جنرل پولیس ویریفکیشن ایک ہی ہیں؟", "نہیں، دونوں الگ خدمات ہیں۔ جس ادارے کو دستاویز چاہیے اس سے پوچھ لیں۔"),
        ("کیا آپ گوجرخان سے باہر بھی مدد کرتے ہیں؟", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر دستاویزات کی جانچ اور رہنمائی ہوتی ہے۔ گھر پر وزٹ گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
        ("Bahar se character certificate kaise banwayen?", "خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ لیٹر پر ایمبیسی کی مہر یا دو معزز افراد کی تصدیق ہو۔"),
        ("کیا فیسیلیٹیٹر سرٹیفیکیٹ منظور کرتا ہے؟", "نہیں۔ فیسیلیٹیٹر درخواست تیار اور جمع کرواتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔"),
    ]))

PAGES.append(dict(
    path="/guides/vehicle-transfer-token-tax-punjab/", kind="guide", main_class="service-detail page-shell", en_title="Vehicle Transfer and Token Tax in Punjab",
    title="گاڑی کی ملکیت کی منتقلی (ٹرانسفر) اور ٹوکن ٹیکس پنجاب: مکمل گائیڈ | دستک 90807",
    desc="پنجاب میں گاڑی اور موٹر سائیکل کی ملکیت کی منتقلی اور ٹوکن ٹیکس کی مکمل اردو گائیڈ: دستاویزات، بائیومیٹرک، PSID ادائیگی، وقت اور عام سوالات۔ دستک کوڈ 90807۔",
    h1="گاڑی اور موٹر سائیکل کی ملکیت کی منتقلی اور ٹوکن ٹیکس: مکمل گائیڈ", eyebrow='<p class="eyebrow">گاڑی اور ایکسائز گائیڈ</p>',
    og="/assets/og/vehicles.jpg",
    crumbs=[("گائیڈز", "/ur/guides/"), ("ملکیت کی منتقلی اور ٹوکن ٹیکس", "/ur/guides/vehicle-transfer-token-tax-punjab/")],
    body=guide_body(
        "پنجاب میں گاڑی یا موٹر سائیکل اپنے نام کروانے کے لیے گاڑی کا نمبر، خریدار کا اصل شناختی کارڈ اور گاڑی کی اصل فائل اور بُک یا کارڈ چاہیے، اور خریدار اور بیچنے والے دونوں کی بائیومیٹرک لازمی ہے۔ ٹوکن ٹیکس کے لیے صرف گاڑی کا نمبر کافی ہے۔ دونوں کاموں میں سرکاری فیس PSID پر بنتی ہے۔",
        [
            ("ملکیت کی منتقلی کے لیے دستاویزات", "<ul><li>گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر</li><li>خریدار کا اصل شناختی کارڈ</li><li>گاڑی کی اصل فائل اور رجسٹریشن بُک یا اسمارٹ کارڈ</li><li>خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق</li></ul>"),
            ("ملکیت کی منتقلی کا طریقہ، قدم بہ قدم", f"<ol><li><b>کاغذات کی جانچ:</b> کارڈ یا بُک اور شناختی کارڈ کی تصاویر واٹس ایپ {PHONE} پر بھیجیں تاکہ واجب الادا ٹوکن ٹیکس اور تفصیلات چیک ہو جائیں۔</li><li><b>PSID:</b> فیسیلیٹیٹر سرکاری سسٹم میں درخواست جمع کرواتا ہے اور PSID بنتا ہے۔</li><li><b>ادائیگی:</b> PSID کی رقم بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے ادا کریں۔</li><li><b>بائیومیٹرک:</b> خریدار اور بیچنے والا دونوں بائیومیٹرک تصدیق کرواتے ہیں۔</li><li><b>کارڈ:</b> تقریباً 10 دن میں نیا رجسٹریشن کارڈ کوریئر سے آتا ہے۔</li></ol>"),
            ("ٹوکن ٹیکس کیسے جمع کروائیں؟", "<p>گاڑی کا نمبر بھیجیں۔ سرکاری سسٹم سے واجب الادا رقم چیک ہو کر PSID بنتا ہے۔ ادائیگی کے بعد کام عام طور پر موقع پر مکمل ہو جاتا ہے۔ کمرشل گاڑیوں کے لیے 3، 6، 9 ماہ یا 1 سال کی مدت منتخب کی جا سکتی ہے۔</p>"),
            ("فیس کتنی ہے؟", '<table class="ur-fee"><tbody><tr><th scope="row">سرکاری منتقلی فیس / ٹوکن ٹیکس</th><td>گاڑی کی قسم، انجن، ماڈل اور سرکاری پالیسی کے مطابق، PSID پر لکھی ہوتی ہے</td></tr><tr><th scope="row">دستک فیسیلیٹیٹر چارجز</th><td>Rs 950 (ہر سروس)</td></tr><tr><th scope="row">پلیٹ فارم چارجز</th><td>Rs 19</td></tr></tbody></table><p>اندازے کے لیے <a href="/ur/calculators/tools/punjab-car-token-tax-transfer-fee-calculator">کار فیس کیلکولیٹر</a> اور <a href="/ur/calculators/tools/punjab-bike-registration-transfer-fee-calculator">موٹر سائیکل فیس کیلکولیٹر</a> دیکھیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔</p><p class="ur-note">' + FEE_SOURCE + '</p>'),
            ("درخواست رکنے کی عام وجوہات", "<ul><li>گاڑی کا نمبر کاغذات سے نہ ملنا۔</li><li>شناختی کارڈ کی مدت ختم ہونا۔</li><li>بیچنے والے کا بائیومیٹرک کے لیے دستیاب نہ ہونا۔</li><li>اصل فائل یا کارڈ کا نہ ہونا۔</li></ul>"),
        ],
        hero=None,
        related=(R["transfer"], R["token"], R["calc"])),
    faqs=[
        ("کیا بیچنے والے کی بائیومیٹرک کے بغیر منتقلی ہو سکتی ہے؟", "نہیں، عام طور پر خریدار اور بیچنے والے دونوں کی لائیو بائیومیٹرک لازمی ہے۔"),
        ("گھر بیٹھے ٹوکن ٹیکس کیسے جمع کروائیں؟", "واٹس ایپ 0345-5583530 پر گاڑی کا نمبر بھیجیں۔ ہم سرکاری PSID بنا دیتے ہیں جسے آپ موبائل بینکنگ سے ادا کر سکتے ہیں۔"),
        ("Bike transfer fee kitni hai?", "سرکاری فیس PSID پر لکھی ہوتی ہے اور حکومت کے فیصلوں کے مطابق بدل سکتی ہے۔ دستک فیسیلیٹیٹر چارجز 950 روپے ہیں۔ اندازے کے لیے موٹر سائیکل فیس کیلکولیٹر دیکھیں۔"),
        ("نیا کارڈ کب آتا ہے؟", "عام طور پر تقریباً 10 دن میں کوریئر سے۔"),
    ]))

# ================================================================ HUBS AND LOCAL PAGES
PAGES.append(dict(
    path="/services/", kind="hub", en_title="All services",
    title="دستک خدمات (سروسز): لائسنس، پولیس، گاڑی، ڈومیسائل | دستک 90807",
    desc="پنجاب میں دستک کی گھر بیٹھے خدمات: ڈرائیونگ لائسنس، پولیس کریکٹر سرٹیفیکیٹ، گاڑی کی ملکیت کی منتقلی، ٹوکن ٹیکس اور ڈومیسائل۔ رجسٹرڈ فیسیلیٹیٹر کوڈ 90807، واٹس ایپ 0345-5583530۔",
    h1="دستک خدمات: سرکاری خدمات گھر کی دہلیز پر", og="/assets/og/general.jpg",
    crumbs=[("خدمات", "/ur/services/")],
    body=f'''<div class="card quick"><b>مختصر تعارف</b><p>میں محمد عثمان ہوں، مریم کی دستک پروگرام کا رجسٹرڈ فیسیلیٹیٹر (کوڈ {CODE})۔ پورے پنجاب میں واٹس ایپ پر رہنمائی کرتا ہوں اور {AREAS} میں گھر آ کر سرکاری دستاویزات کا کام کرواتا ہوں۔ ہر سروس پر دستک فیسیلیٹیٹر چارجز 950 روپے ہیں، اور سرکاری فیس PSID پر لکھی ہوتی ہے۔</p></div>
<section class="service-module"><h2>ڈرائیونگ لائسنس</h2>{cards((R["renew"], R["learner"], R["track"]))}</section>
<section class="service-module"><h2>پولیس خدمات</h2>{cards((R["character"], ("/ur/services/general-police-verification/", "جنرل پولیس ویریفکیشن", "نوکری اور ویزا کے لیے پس منظر کی تصدیق"), ("/ur/services/tenant-registration/", "کرایہ دار کی رجسٹریشن", "مکان کرائے پر دینے والوں کے لیے"), ("/ur/services/loss-report/", "گمشدگی کی رپورٹ", "کاغذات گم ہونے کی رپورٹ")))}</section>
<section class="service-module"><h2>گاڑی اور ایکسائز</h2>{cards((R["transfer"], R["token"], ("/ur/services/motor-vehicle-registration/", "نئی گاڑی کی رجسٹریشن", "نئی گاڑی یا بائیک رجسٹر کروائیں")))}</section>
<section class="service-module"><h2>ڈومیسائل اور سول سرٹیفیکیٹس</h2>{cards((R["domicile"], ("/ur/services/birth-certificate/", "پیدائش سرٹیفیکیٹ", "یونین کونسل سے پیدائش کا اندراج"), ("/ur/services/marriage-certificate/", "نکاح نامہ سرٹیفیکیٹ", "شادی کا کمپیوٹرائزڈ سرٹیفیکیٹ"), ("/ur/services/e-stamping/", "ای اسٹامپ پیپر", "بیان حلفی اور دیگر اسٹامپ پیپر")))}</section>
<p class="ur-note">جن خدمات کے ساتھ (English) لکھا ہے ان کی تفصیل ابھی انگریزی میں ہے۔ اردو صفحات جلد آ رہے ہیں۔ <a href="/en/services/" lang="en">All services in English</a></p>
{booking_block("دستک سروس")}''',
    faqs=[
        ("دستک سروس کیا ہے؟", "مریم کی دستک حکومتِ پنجاب کا پروگرام ہے جس میں رجسٹرڈ فیسیلیٹیٹر گھر آ کر سرکاری دستاویزات کا کام کرواتا ہے۔ دستک 90807 ایک آزاد رجسٹرڈ فیسیلیٹیٹر کی سروس ہے۔"),
        ("فیسیلیٹیٹر چارجز کتنے ہیں؟", "دستک تربیتی مینول کے مطابق ہر سروس پر فیسیلیٹیٹر چارجز 950 روپے ہیں۔ سرکاری فیس الگ ہے اور PSID پر لکھی ہوتی ہے۔"),
        ("بکنگ کیسے کریں؟", "دستک ایپ میں Doorstep Delivery منتخب کر کے کوڈ 90807 لکھیں، یا واٹس ایپ 0345-5583530 کریں۔"),
    ]))

PAGES.append(dict(
    path="/guides/", kind="hub", en_title="Guides & Updates",
    title="اردو گائیڈز: لائسنس، کریکٹر سرٹیفیکیٹ، گاڑی کی ملکیت کی منتقلی | دستک 90807",
    desc="پنجاب کی سرکاری دستاویزات پر آسان اردو گائیڈز: ڈرائیونگ لائسنس کی تجدید، لائسنس ٹریکنگ، پولیس کریکٹر سرٹیفیکیٹ، گاڑی کی ملکیت کی منتقلی اور ٹوکن ٹیکس۔ دستک کوڈ 90807۔",
    h1="اردو گائیڈز: سرکاری دستاویزات آسان زبان میں", og="/assets/og/general.jpg",
    crumbs=[("گائیڈز", "/ur/guides/")],
    body=f'''<div class="card quick"><b>ان گائیڈز میں کیا ہے؟</b><p>ہر گائیڈ میں دستاویزات کی فہرست، قدم بہ قدم طریقہ، فیس کی معلومات اور عام سوالات آسان اردو میں ہیں۔ فیس کی معلومات صرف سرکاری دستک تربیتی مینول اور سرکاری پورٹل سے لی گئی ہیں۔</p></div>
{cards((R["renew_guide"], R["track"], R["character_guide"], R["vehicle_guide"]))}
<p class="ur-note">مزید گائیڈز انگریزی میں: <a href="/en/guides/" lang="en">Guides &amp; Updates</a></p>''',
    faqs=[]))

PAGES.append(dict(
    path="/calculators/", kind="hub", en_title="Fee Calculators",
    title="فیس کیلکولیٹر پنجاب: لائسنس، کار، موٹر سائیکل | دستک 90807",
    desc="پنجاب ڈرائیونگ لائسنس، کار اور موٹر سائیکل کی ملکیت کی منتقلی اور ٹوکن ٹیکس کی فیس کا اندازہ لگائیں۔ دستک فیسیلیٹیٹر چارجز 950 روپے شامل۔ حتمی رقم PSID پر۔ دستک کوڈ 90807۔",
    h1="فیس کیلکولیٹر: لائسنس، کار اور موٹر سائیکل", og="/assets/og/general.jpg",
    crumbs=[("فیس کیلکولیٹر", "/ur/calculators/")],
    body=f'''<div class="card quick"><b>اہم بات</b><p>یہ کیلکولیٹر صرف <b>اندازہ</b> دیتے ہیں۔ سرکاری فیس حکومت کے فیصلوں کے مطابق بدل سکتی ہے، اور حتمی رقم ہمیشہ سرکاری سسٹم کے PSID پر لکھی ہوتی ہے۔ گاڑی اور موٹر سائیکل کیلکولیٹر میں دستک فیسیلیٹیٹر چارجز 950 روپے شامل ہیں۔ کیلکولیٹرز میں اردو اور انگریزی دونوں زبانیں ہیں۔</p></div>
{cards((("/ur/calculators/tools/punjab-driving-license-fee-calculator", "ڈرائیونگ لائسنس فیس کیلکولیٹر", "تجدید کی فیس، 1 سے 5 سال کی مدت کے مطابق"), ("/ur/calculators/tools/punjab-car-token-tax-transfer-fee-calculator", "کار کی ملکیت کی منتقلی اور ٹوکن ٹیکس کیلکولیٹر", "کار کی ملکیت کی منتقلی کی فیس اور ٹوکن ٹیکس کا اندازہ"), ("/ur/calculators/tools/punjab-bike-registration-transfer-fee-calculator", "موٹر سائیکل رجسٹریشن اور ملکیت کی منتقلی کیلکولیٹر", "بائیک اور ای بائیک کی فیس کا اندازہ")))}
<section class="service-module"><h2>متعلقہ خدمات</h2>{cards((R["renew"], R["transfer"], R["token"]))}</section>''',
    faqs=[
        ("کیا کیلکولیٹر کی فیس حتمی ہے؟", "نہیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔ حتمی رقم سرکاری PSID پر ہوتی ہے۔"),
        ("کیا فیسیلیٹیٹر چارجز شامل ہیں؟", "گاڑی اور موٹر سائیکل کیلکولیٹر میں دستک فیسیلیٹیٹر چارجز 950 روپے شامل ہیں۔"),
    ]))

PAGES.append(dict(
    path="/gujar-khan/", kind="service", en_title="Gujar Khan", areas=("Gujar Khan", "Kallar Syedan", "Kahuta", "Mandra", "Bewal", "Daultala", "Jatli", "Sukho", "Qazian", "Rawalpindi"),
    title="گوجرخان میں دستک سروس: گھر بیٹھے سرکاری دستاویزات | دستک 90807",
    desc="گوجرخان، کلر سیداں، مندرہ، جاتلی، دولتالہ، بیول اور قریبی علاقوں میں ڈومیسائل، ڈرائیونگ لائسنس، پولیس سرٹیفیکیٹ اور گاڑی خدمات گھر پر۔ دستک کوڈ 90807۔",
    h1="گوجرخان میں دستک سروس: گھر بیٹھے سرکاری دستاویزات", og="/assets/og/general.jpg",
    og_alt="گوجرخان میں دستک سروس، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، صندل روڈ، گوجرخان",
    crumbs=[("گوجرخان", "/ur/gujar-khan/")],
    body=f'''<div class="card quick"><b>مختصر جواب</b><p>گوجرخان اور آس پاس کے علاقوں میں مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر محمد عثمان (کوڈ {CODE}) گھر آ کر سرکاری دستاویزات کا کام کرواتے ہیں۔ گوجرخان اور راولپنڈی میں زیادہ تر کام ڈومیسائل کا ہوتا ہے، ساتھ ڈرائیونگ لائسنس، پولیس، گاڑی اور سول دستاویزات بھی۔ آن لائن رابطہ کسی بھی وقت، گھر پر وزٹ پہلے سے وقت طے کر کے۔</p></div>
<div class="sd-actions"><a class="btn g" data-ga-event="service_whatsapp_click" href="{wa_link('گوجرخان میں دستک سروس')}">واٹس ایپ: {PHONE}</a><a class="btn o" href="tel:+923455583530">کال کریں</a><a class="btn o" href="https://www.google.com/maps/search/?api=1&amp;query=Dastak+Online+Document+Facilitation+Sandal+Road+Gujar+Khan" rel="noopener">گوگل میپ پر دیکھیں</a></div>
<section class="service-module"><h2>کن علاقوں میں گھر پر سروس ملتی ہے؟</h2><p>{AREAS}۔ اپنا علاقہ واٹس ایپ پر بتا کر پہلے تصدیق کر لیں۔</p></section>
<section class="service-module"><h2>گوجرخان میں سب سے زیادہ مانگی جانے والی خدمات</h2>{cards((R["domicile"], R["renew"], R["character"], R["transfer"], R["token"], R["learner"]))}</section>
<section class="service-module"><h2>ہمارا پتہ</h2><p>صندل روڈ، وارڈ نمبر 14، گوجرخان، پنجاب <span class="ltr">47850</span>۔ شہری اکثر یہاں بھی تشریف لاتے ہیں، مگر آنے سے پہلے واٹس ایپ پر وقت طے کر لیں۔</p></section>
{booking_block("گوجرخان میں دستک سروس")}''',
    faqs=[
        ("Gujar Khan mein domicile kaise banwayen?", "دستک ایپ میں کوڈ 90807 کے ساتھ بکنگ کریں یا واٹس ایپ 0345-5583530 کریں۔ دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے اور 300 روپے کا بیان حلفی الگ ہے۔"),
        ("کیا آپ کلر سیداں، مندرہ اور جاتلی بھی آتے ہیں؟", "جی ہاں، کلر سیداں، کہوٹہ، مندرہ، بیول، دولتالہ، جاتلی، سکھو اور قاضیاں میں بھی وزٹ پہلے سے وقت طے کر کے ہوتا ہے۔"),
        ("کیا یہ سرکاری دفتر ہے؟", "نہیں۔ یہ ایک آزاد رجسٹرڈ فیسیلیٹیٹر کی سروس ہے، کوئی سرکاری دفتر نہیں۔"),
    ]))

PAGES.append(dict(
    path="/contact/", kind="hub", en_title="Contact",
    title="رابطہ: واٹس ایپ 0345-5583530، گوجرخان | دستک 90807",
    desc="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن سے رابطہ: واٹس ایپ اور کال 0345-5583530، ای میل، پتہ صندل روڈ گوجرخان۔ رجسٹرڈ فیسیلیٹیٹر محمد عثمان، کوڈ 90807۔",
    h1="رابطہ کریں", og="/assets/og/general.jpg",
    crumbs=[("رابطہ", "/ur/contact/")],
    body=f'''<div class="card quick"><b>سب سے تیز رابطہ</b><p>واٹس ایپ پر اپنی سروس اور شہر لکھ کر بھیجیں: {PHONE}۔ آن لائن رابطہ کسی بھی وقت، گھر پر وزٹ پہلے سے وقت طے کر کے۔</p></div>
<div class="sd-actions"><a class="btn g" data-ga-event="contact_whatsapp_click" href="{WA}">واٹس ایپ {PHONE}</a><a class="btn y" data-ga-event="contact_call_click" href="tel:+923455583530">کال کریں</a></div>
<section class="service-module"><h2>رابطے کی تفصیل</h2><table class="ur-fee"><tbody>
<tr><th scope="row">نام</th><td>محمد عثمان، رجسٹرڈ دستک فیسیلیٹیٹر (کوڈ {CODE})</td></tr>
<tr><th scope="row">واٹس ایپ اور کال</th><td><a href="{WA}">{PHONE}</a></td></tr>
<tr><th scope="row">ای میل</th><td><a href="mailto:support@dastak90807.com"><span class="ltr">support@dastak90807.com</span></a><br><a href="mailto:dastak90807@zohamail.com"><span class="ltr">dastak90807@zohamail.com</span></a></td></tr>
<tr><th scope="row">پتہ</th><td>صندل روڈ، وارڈ نمبر 14، گوجرخان، پنجاب <span class="ltr">47850</span></td></tr>
<tr><th scope="row">اوقات</th><td>آن لائن رابطہ کسی بھی وقت۔ گھر پر وزٹ پہلے سے وقت طے کر کے۔</td></tr>
</tbody></table><div class="row"><a class="btn o" href="https://www.google.com/maps/search/?api=1&amp;query=Dastak+Online+Document+Facilitation+Sandal+Road+Gujar+Khan" rel="noopener">گوگل میپ پر لوکیشن</a><a class="btn o" href="https://share.google/nmpsQYND7NTAnZzqI" rel="noopener">گوگل پروفائل اور ریویوز</a></div></section>
<section class="service-module"><h2>دھوکے سے بچیں</h2><ul><li>میں کبھی آپ سے پاس ورڈ یا OTP نہیں مانگتا۔</li><li>فیس ہمیشہ سرکاری سسٹم کے PSID سے ادا ہوتی ہے۔</li><li>کام مکمل ہونے اور ڈیلیوری کے بعد آپ کی دستاویزات ڈیلیٹ کر دی جاتی ہیں۔</li><li id="verify">{VERIFY}</li></ul></section>''',
    faqs=[
        ("آپ سے رابطہ کیسے کریں؟", "واٹس ایپ یا کال 0345-5583530، یا ای میل support@dastak90807.com۔"),
        ("کیا آپ کا دفتر ہے؟", "پتہ صندل روڈ، وارڈ نمبر 14، گوجرخان ہے۔ آنے سے پہلے واٹس ایپ پر وقت طے کر لیں۔"),
    ]))

HP = json.load(open(os.path.join(ROOT, "scripts", "home_parts.json"), encoding="utf-8"))
ARROW = HP["arrow"]


def home_card(icon, tag, title, links, more_href, more_text, wa_topic):
    lis = "".join(f'<li><a href="{h}">{t} ←</a></li>' for h, t in links)
    return (f'<article class="card home-category"><span class="home-popular">{tag}</span><span class="category-icon">{icon}</span>'
            f'<h3>{title}</h3><ul>{lis}</ul><div class="home-category-foot"><a class="btn y home-category-more" href="{more_href}">{more_text} {ARROW}</a>'
            f'<a class="btn g home-category-wa" href="{wa_link(wa_topic)}">واٹس ایپ پر پوچھیں</a></div></article>')


SV, TL = HP["svc"], HP["tools"]
for _t in TL:  # Phase 6: the calculators have Urdu pages
    _t["more"] = _t["more"].replace("/en/calculators/tools/", "/ur/calculators/tools/")
STRIP_TEXT = ["گھر کی دہلیز پر کاغذات کی وصولی اور ڈیلیوری", f"کوڈ {CODE} کی تصدیق سرکاری پورٹل پر کریں", "آزاد فیسیلیٹیشن سروس، سرکاری دفتر نہیں"]
strip_items = "".join(f"<li>{ic}<span>{t}</span></li>" for ic, t in zip(HP["strip"], STRIP_TEXT))
STRIP = ('<aside class="top trust-strip" aria-label="سروس کی خصوصیات"><div class="announcement-window"><div class="announcement-track">'
         f'<ul class="announcement-message">{strip_items}</ul><ul class="announcement-message announcement-copy" aria-hidden="true">{strip_items}</ul>'
         f'<ul class="announcement-message announcement-copy" aria-hidden="true">{strip_items}</ul>'
         f'<ul class="announcement-message announcement-copy" aria-hidden="true">{strip_items}</ul></div></div>'
         '<button class="announcement-toggle" type="button" aria-label="سروس کی خصوصیات روکیں" data-resume-label="سروس کی خصوصیات دوبارہ چلائیں" hidden>Ⅱ</button></aside>')
TRUST = [("رجسٹرڈ فیسیلیٹیٹر", f"کوڈ {CODE}"), ("سرکاری پورٹلز", "پنجاب کے سرکاری سسٹم سے کارروائی"),
         ("اسٹیٹس اپ ڈیٹس", "ٹریکنگ آئی ڈی آپ کو دی جاتی ہے"), ("آزاد سروس", "سرکاری دفتر نہیں")]
trust_html = "".join(f'<div class="home-trust-item"><span>{ic}</span><div><strong>{a}</strong><small>{b}</small></div></div>'
                     for ic, (a, b) in zip(HP["trust"], TRUST))

HERO_ALT = ("گوجرخان، راولپنڈی اور پنجاب میں دستک فیسیلیٹیٹر گھر کی دہلیز پر شہری کو دستاویزات دیتے ہوئے، "
            "دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)")

CARDS_SVC = "".join([
    home_card(SV[0]["icon"], "مقبول", "ڈرائیونگ لائسنس",
              [("/ur/services/learner-driving-license/", "لرنر پرمٹ"), ("/ur/services/renewal-of-regular-license/", "لائسنس کی تجدید"),
               ("/ur/guides/how-to-track-driving-license-in-punjab/", "لائسنس ٹریک کریں")], "/ur/services/", "تمام خدمات", "ڈرائیونگ لائسنس"),
    home_card(SV[1]["icon"], "مقبول", "گاڑی اور ایکسائز",
              [("/ur/services/transfer-of-motor-vehicle/", "گاڑی اور موٹر سائیکل کی ملکیت کی منتقلی"), ("/ur/services/token-tax/", "ٹوکن ٹیکس"),
               ("/ur/guides/vehicle-transfer-token-tax-punjab/", "ملکیت کی منتقلی اور ٹوکن ٹیکس گائیڈ")], "/ur/services/", "تمام خدمات", "گاڑی اور ایکسائز"),
    home_card(SV[2]["icon"], "مقبول", "پولیس خدمات",
              [("/ur/services/character-certificate/", "پولیس کریکٹر سرٹیفیکیٹ"), ("/ur/guides/punjab-police-character-certificate-online/", "کریکٹر سرٹیفیکیٹ گائیڈ"),
               ("/ur/services/tenant-registration/", "کرایہ دار کی رجسٹریشن")], "/ur/services/", "تمام خدمات", "پولیس خدمات"),
    home_card(SV[3]["icon"], "گوجرخان", "سول دستاویزات",
              [("/ur/services/domicile-certificate/", "ڈومیسائل سرٹیفیکیٹ"), ("/ur/services/e-stamping/", "ای اسٹامپ"),
               ("/ur/services/birth-certificate/", "پیدائش سرٹیفیکیٹ")], "/ur/gujar-khan/", "گوجرخان خدمات", "سول دستاویزات"),
    home_card(SV[4]["icon"], "رہنمائی", "جنگلات، وائلڈ لائف اور فشریز",
              [("/ur/services/other-punjab-dastak-services/", "فشریز ای لائسنس رہنمائی"),
               ("/ur/services/other-punjab-dastak-services/", "وائلڈ لائف پرمٹ رہنمائی")], "/ur/services/", "تمام خدمات", "جنگلات، وائلڈ لائف اور فشریز"),
    home_card(SV[5]["icon"], "رہنمائی", "ای بز کاروباری خدمات",
              [("/ur/services/other-punjab-dastak-services/", "فوڈ اتھارٹی لائسنس رہنمائی"),
               ("/ur/services/other-punjab-dastak-services/", "کاروبار کی رجسٹریشن رہنمائی"),
               ("/ur/services/general-inquiry-and-guide/", "گھر پر کاروباری سہولت")], "/ur/services/", "تمام خدمات", "ای بز کاروباری خدمات"),
])
CARDS_TOOLS = "".join([
    home_card(TL[0]["icon"], "مفت", "ڈرائیونگ لائسنس فیس کیلکولیٹر",
              [(TL[0]["more"], "تجدید فیس (1 سے 5 سال)"), (TL[0]["more"], "نیا اور ڈپلیکیٹ لائسنس"), (TL[0]["more"], "انٹرنیشنل ڈرائیونگ پرمٹ")],
              TL[0]["more"], "ابھی حساب کریں", "ڈرائیونگ لائسنس فیس"),
    home_card(TL[1]["icon"], "مفت", "کار ٹوکن ٹیکس اور ملکیت کی منتقلی کیلکولیٹر",
              [(TL[1]["more"], "کار اور جیپ کا ٹوکن ٹیکس"), (TL[1]["more"], "کار کی ملکیت کی منتقلی فیس"), (TL[1]["more"], "فائلر اور نان فائلر ریٹس")],
              TL[1]["more"], "ابھی حساب کریں", "کار فیس"),
    home_card(TL[2]["icon"], "مفت", "موٹر سائیکل رجسٹریشن اور ملکیت کی منتقلی کیلکولیٹر",
              [(TL[2]["more"], "نئی بائیک رجسٹریشن فیس"), (TL[2]["more"], "موٹر سائیکل کی ملکیت کی منتقلی فیس"), (TL[2]["more"], "لائف ٹائم ٹوکن ٹیکس")],
              TL[2]["more"], "ابھی حساب کریں", "موٹر سائیکل فیس"),
])

STEPS = (
    '<li class="home-step"><span class="home-step-num">1</span><h3>شروع کرنے کا طریقہ منتخب کریں</h3>'
    f'<p>دستک ایپ میں <strong>Doorstep Delivery</strong> منتخب کریں، پھر <strong>Self</strong> یا <strong>On Behalf</strong> چنیں اور Facilitator Code کے خانے میں <strong>{CODE}</strong> لکھیں۔ '
    f'یا واٹس ایپ یا کال کریں: {PHONE}۔ میں آپ کو دستاویزات اور فیس کی تفصیل بتاتا ہوں۔</p><span class="home-step-tag">دستک ایپ · واٹس ایپ · فون</span></li>'
    '<li class="home-step"><span class="home-step-num">2</span><h3>درخواست مکمل کریں</h3>'
    '<p>میں دستاویزات کی تیاری میں رہنمائی کرتا ہوں اور آپ کے ساتھ درخواست مکمل کرتا ہوں۔ آپ SMS یا ایپ میں آنے والے کوڈ (OTP) سے تصدیق کرتے ہیں۔ گوجرخان میں یہ کام آپ کے گھر پر ہو سکتا ہے۔</p>'
    '<span class="home-step-tag">آن لائن · گوجرخان میں گھر پر</span></li>'
    '<li class="home-step"><span class="home-step-num">3</span><h3>جمع کروائیں اور ٹریک کریں</h3>'
    '<p>درخواست سرکاری دستک سسٹم کے ذریعے جمع ہوتی ہے اور فیس سرکاری PSID سے ادا ہوتی ہے۔ آپ کو ٹریکنگ آئی ڈی ملتی ہے اور محکمے کے کام مکمل کرنے تک میں آپ کو اپ ڈیٹ دیتا رہتا ہوں۔</p>'
    '<span class="home-step-tag">ٹریکنگ آئی ڈی · اسٹیٹس اپ ڈیٹس</span></li>'
)

MONTHS_UR = {"January":"جنوری","February":"فروری","March":"مارچ","April":"اپریل","May":"مئی","June":"جون","July":"جولائی",
             "August":"اگست","September":"ستمبر","October":"اکتوبر","November":"نومبر","December":"دسمبر"}
_track = HP["review_track"]
for _en, _ur in MONTHS_UR.items():
    _track = re.sub(r'(<time datetime="[^"]+">)(\d+) ' + _en + r' (\d{4})</time>', lambda m, u=_ur: f'{m.group(1)}{m.group(2)} {u} {m.group(3)}</time>', _track)

REVIEWS = (
    '<section class="band rev" id="reviews"><div class="wrap"><div class="home-review-heading"><div>'
    '<p class="eyebrow">ہمارے صارفین کی زبانی</p><h2>شہری کیا کہتے ہیں</h2>'
    '<p class="sub">گوجرخان، راولپنڈی اور پورے پنجاب میں جن شہریوں کی ہم نے مدد کی، ان کے منتخب تبصرے۔</p></div>'
    '<a class="review-badge" href="https://share.google/nmpsQYND7NTAnZzqI" target="_blank" rel="noopener" data-ga-event="home_review_cta_click" '
    'aria-label="78 گوگل ریویوز میں 5 میں سے 4.9 ریٹنگ۔ ہمارا گوگل بزنس پروفائل کھولیں">'
    + HP["review_g"] +
    '<span class="review-score"><b class="ltr">4.9</b><span class="review-stars" aria-hidden="true">★★★★★</span></span>'
    '<span class="review-meta"><b>گوگل ریٹنگ</b><small><span class="ltr">78</span> ریویوز · سب دیکھیں ←</small></span></a></div>'
    '<div class="review-controls-row"><div class="review-controls">'
    '<button type="button" data-review-direction="1" aria-label="پچھلے تبصرے" aria-controls="home-review-track">→</button>'
    '<button type="button" data-review-direction="-1" aria-label="اگلے تبصرے" aria-controls="home-review-track">←</button></div></div>'
    '<div class="home-review-track" id="home-review-track" tabindex="0" role="region" aria-label="صارفین کے تبصرے">' + _track + '</div>'
    '<p class="sub">یہ تبصرے زیادہ تر ہمارے گوگل بزنس پروفائل اور چند فیس بک سفارشات سے لیے گئے ہیں اور صارفین کے اپنے الفاظ میں ہیں، اس لیے ان کا ترجمہ نہیں کیا گیا۔ '
    'کچھ تبصرے اقتباس ہیں۔ 24 نومبر 2026 تک <span class="ltr">78</span> ریویوز سے گوگل ریٹنگ <span class="ltr">4.9</span>۔ ہر شخص کا تجربہ اور کام کا وقت مختلف ہو سکتا ہے۔</p>'
    '<div class="row"><a data-ga-event="home_review_cta_click" class="btn y" href="https://g.page/r/CcbPfWByTNL1ECE/review" target="_blank" rel="noopener">گوگل پر ریویو دیں</a>'
    '<a data-ga-event="home_review_cta_click" class="btn o" href="https://www.facebook.com/Dastak90807/reviews" target="_blank" rel="noopener">فیس بک پر ریویو دیں</a></div></div></section>'
)

AREAS = ["گوجرخان", "کلر سیداں", "کہوٹہ", "راولپنڈی", "مندرہ", "بیول", "دولتالہ", "سکھو", "جاتلی", "قاضیاں", "پورے پنجاب میں آن لائن"]
FACILITATOR = (
    '<section class="band home-fc" id="contact"><div class="wrap"><div class="fc-grid">'
    '<article class="fc-profile" id="facilitator"><div class="fc-head">'
    '<img src="/assets/usman.webp" alt="محمد عثمان، مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر، کوڈ 90807، گوجرخان راولپنڈی" width="112" height="112" loading="lazy">'
    f'<div><span class="chip">فیسیلیٹیٹر کوڈ {CODE}</span><h2>اپنے رجسٹرڈ مریم کی دستک فیسیلیٹیٹر سے ملیں</h2><p class="fc-name">محمد عثمان</p></div></div>'
    f'<p>میں محمد عثمان ہوں، حکومتِ پنجاب کے مریم کی دستک پروگرام کے تحت رجسٹرڈ فیسیلیٹیٹر (کوڈ {CODE})۔ '
    'میں پنجاب کے شہریوں کی سرکاری دستاویزات، ای لائسنس اور ای بز سے متعلق درخواستوں میں مدد کرتا ہوں۔</p>'
    '<p class="fc-label">آپ کے علاقے میں گھر پر وزٹ</p><ul class="area-tags">' + "".join(f"<li>{a}</li>" for a in AREAS) + '</ul>'
    f'<div class="ur-verify-box" id="verify"><h3>فیسیلیٹیٹر کی تصدیق کیسے کریں؟</h3><p>{VERIFY}</p></div>'
    '<a class="fc-more" href="/ur/about/">محمد عثمان کا تعارف اور رجسٹریشن کی تصدیق ←</a></article>'
    '<aside class="fc-contact"><p class="fc-eyebrow">آئیں آپ کے کاغذات مکمل کریں</p><h2>اپنے دستک فیسیلیٹیٹر سے رابطہ کریں</h2>'
    '<p>اپنی سروس اور شہر کا نام بھیجیں۔ میں آپ کو ضروری دستاویزات اور اگلے قدم بتا دوں گا۔</p>'
    f'<a class="btn fc-wa" href="{wa_link("دستک سروس میں رہنمائی")}">واٹس ایپ {PHONE}</a>'
    '<a class="btn fc-call" href="tel:+923455583530">محمد عثمان کو کال کریں</a>'
    '<p class="fc-line"><strong>ای میل:</strong> <a class="ltr" href="mailto:support@dastak90807.com">support@dastak90807.com</a></p>'
    '<p class="fc-line"><strong>دفتر:</strong> صندل روڈ، وارڈ نمبر <span class="ltr">14</span>، گوجرخان، راولپنڈی، پنجاب</p>'
    '<a class="fc-maplink" href="https://www.google.com/maps/place/Dastak+Online+Document+Facilitation/@33.2547796,73.2958553,17z/data=!4m5!3m4!1s0x392005c98ae34345:0xf5d24c72607dcfc6!8m2!3d33.2547796!4d73.2958553" target="_blank" rel="noopener">گوگل بزنس پروفائل پر ہماری لوکیشن کھولیں ↗</a></aside></div>'
    '<div class="fc-map"><iframe class="contact-map" title="گوجرخان میں دستک آن لائن ڈاکومنٹ فیسیلیٹیشن کی لوکیشن" src="https://www.google.com/maps?q=33.2547796,73.2958553&amp;z=17&amp;output=embed" width="800" height="320" loading="lazy" referrerpolicy="strict-origin-when-cross-origin"></iframe></div>'
    '<p class="fc-note">یہ ایک آزاد فیسیلیٹیشن سروس ہے، سرکاری دفتر نہیں۔ بکنگ سے پہلے شرائط اور دستیابی کی تصدیق کر لیں۔</p></div></section>'
)

# Parity with the English home: "More free tools" row and the 3 picture guide cards
_SVG = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{}"/></svg>'
TOOL_LINKS = ('<div class="home-tool-links"><p class="home-tool-links-label">مزید مفت ٹولز</p><div class="home-tool-links-row">'
    + "".join(f'<a class="btn o" href="{h}" data-ga-event="home_tool_launcher_click" data-tool-name="{n}">{_SVG.format(d)} {t}</a>' for h, n, d, t in (
        ("/ur/document-checklist/", "Document Checklist", "M9 11l2 2 4-4M5 4h14v16H5z", "دستاویزات کی چیک لسٹ"),
        ("/ur/citizen-tools/", "Tracking &amp; Official Portals", "M12 3a9 9 0 100 18 9 9 0 000-18zM3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18", "سرکاری پورٹلز"),
        ("/ur/downloads/", "Forms &amp; Downloads", "M12 4v11m0 0l-4-4m4 4l4-4M5 20h14", "فارمز اور ڈاؤن لوڈز")))
    + '</div></div><p class="home-tools-note">یہ صرف اندازہ ہے۔ سرکاری فیس پنجاب کا سرکاری سسٹم بناتا ہے۔ دستک 90807 ایک آزاد فیسیلیٹیشن سروس ہے۔</p>')
_G = [
    ("vehicle", "/assets/punjab-token-tax-guide-dastak-90807-thumb.webp", "پنجاب ٹوکن ٹیکس کی 30 نومبر 2026 کی رپورٹ شدہ آخری تاریخ کا پوسٹر، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی",
     "نئی · گاڑی اور ٹوکن ٹیکس گائیڈ", "/ur/guides/punjab-token-tax-payment-and-penalty/", "پنجاب ٹوکن ٹیکس 2026: آخری تاریخ، جرمانہ اور ادائیگی کا طریقہ", "30 نومبر 2026 کی رپورٹ شدہ آخری تاریخ، جرمانہ اور سرکاری PSID سے ادائیگی۔"),
    ("driving", "/assets/track-driving-license-punjab-dastak-90807-thumb.webp", "پنجاب میں DLIMS اور پاکستان پوسٹ سے ڈرائیونگ لائسنس ٹریک کرنے کی گائیڈ، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی",
     "نئی · ڈرائیونگ لائسنس گائیڈ", "/ur/guides/how-to-track-driving-license-in-punjab/", "پنجاب میں ڈرائیونگ لائسنس ٹریک کرنے کا طریقہ (DLIMS اور پاکستان پوسٹ)", "دو مرحلوں میں ٹریکنگ: شناختی کارڈ سے DLIMS اسٹیٹس، پھر پاکستان پوسٹ سے ڈیلیوری۔"),
    ("driving", "/assets/punjab-driving-license-renewal-guide-dastak-90807-thumb.webp", "گوجرخان اور راولپنڈی میں پنجاب ڈرائیونگ لائسنس کی تجدید کی گائیڈ، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
     "پنجاب ڈرائیونگ لائسنس گائیڈ", "/ur/guides/punjab-driving-license-renewal-online/", "پنجاب ڈرائیونگ لائسنس کی آن لائن تجدید: دستاویزات، فیس اور طریقہ", "لائسنس کی تجدید: دستاویزات، فیس، ٹریکنگ اور پورے پنجاب میں مدد۔"),
]
HOME_GUIDES = ('<section class="wrap guides ur-home-guides" id="guides"><p class="eyebrow">تیاری کیسے کریں</p><h2>مقامی دستاویزات کی گائیڈز</h2>'
    '<p class="sub">گوجرخان، راولپنڈی اور آس پاس کے علاقوں کے لیے عملی معلومات۔</p><div class="guide-grid">'
    + "".join(f'<article class="card guide-card local-guide" data-guide-category="{c}"><div class="guide-illustration has-thumb"><img src="{img}" width="640" height="357" loading="lazy" decoding="async" alt="{alt}"></div>'
              f'<div class="guide-body"><span class="eyebrow">{eb}</span><h3><a data-ga-event="home_guide_click" href="{u}">{t}</a></h3><p>{d}</p>'
              f'<a data-ga-event="home_guide_click" class="btn y" href="{u}">گائیڈ پڑھیں <span aria-hidden="true">↗</span></a></div></article>' for c, img, alt, eb, u, t, d in _G)
    + '</div><p><a data-ga-event="home_guide_click" href="/ur/guides/">تمام گائیڈز دیکھیں</a></p></section>')

HOME_BODY = (
    '<section class="hero"><div class="wrap two"><div>'
    f'<span class="chip">رجسٹرڈ فیسیلیٹیٹر · مریم کی دستک · کوڈ {CODE}</span>'
    '<h1>دستک آن لائن ڈاکومنٹ فیسیلیٹیشن <span>پورے پنجاب میں آن لائن · گوجرخان اور راولپنڈی میں گھر کی دہلیز پر</span></h1>'
    '<p class="hero-tagline">گھر بیٹھے اپلائی کریں، دفتر جانے کی ضرورت نہیں۔</p>'
    f'<p class="lead">پولیس، ڈرائیونگ لائسنس، گاڑی اور ڈومیسائل جیسی سرکاری خدمات کے لیے پنجاب میں کہیں سے بھی گھر بیٹھے اپلائی کریں، رجسٹرڈ فیسیلیٹیٹر محمد عثمان (کوڈ {CODE}) کے ساتھ۔ '
    'گوجرخان اور راولپنڈی میں گھر پر وزٹ۔ <a href="#verify">تصدیق کیسے کریں؟</a></p>'
    f'<div class="row"><a class="btn g" data-ga-event="hero_whatsapp_click" href="{wa_link("دستک سروس میں رہنمائی")}">واٹس ایپ: {PHONE}</a>'
    f'<a class="btn y hero-calc" data-ga-event="hero_calculator_click" href="#fee-calculators">فیس معلوم کریں {ARROW}</a>'
    f'<a class="btn o hero-call" data-ga-event="hero_call_click" href="tel:+923455583530">{HP["call"]}کال کریں {PHONE}</a></div></div>'
    f'<div class="art"><img src="/assets/muhammad-usman-dastak-90807-doorstep-facilitation-gujar-khan-urdu-rtl.webp" width="2400" height="1340" alt="{HERO_ALT}" fetchpriority="high"></div></div></section>'
    + STRIP +
    '<section class="wrap home-services" id="services" aria-labelledby="home-services-title"><p class="eyebrow">پورے پنجاب میں آن لائن · گوجرخان میں گھر کی دہلیز پر</p>'
    '<h2 id="home-services-title">پنجاب میں کہیں سے بھی آن لائن اپلائی کریں</h2><p class="sub">اپنی خدمت منتخب کریں اور دستاویزات اور اگلے قدم دیکھیں۔</p>'
    f'<div class="home-category-grid">{CARDS_SVC}</div></section>'
    '<section class="wrap home-tools" id="citizen-tools"><p class="eyebrow">مفت فیس کیلکولیٹر</p><h2 id="fee-calculators">اپنی فیس کا اندازہ لگائیں</h2>'
    '<p class="sub">ڈرائیونگ لائسنس، کار اور موٹر سائیکل کے مفت فیس کیلکولیٹر، اردو اور انگریزی دونوں میں۔ اندازہ PDF میں ڈاؤن لوڈ کریں۔ حتمی رقم ہمیشہ PSID پر ہوتی ہے۔</p>'
    f'<div class="home-category-grid">{CARDS_TOOLS}</div>' + TOOL_LINKS + '</section>'
    '<section class="band process" id="how-it-works"><div class="wrap"><p class="eyebrow">طریقہ کار</p><h2>3 آسان قدموں میں اپلائی کریں</h2>'
    f'<p class="sub home-steps-sub">پورے پنجاب سے آن لائن۔ گوجرخان میں گھر کی دہلیز پر۔</p><ol class="home-steps">{STEPS}</ol>'
    f'<div class="home-trust-strip">{trust_html}</div>'
    f'<div class="row"><a class="btn g" href="{wa_link("سروس کی بکنگ")}">واٹس ایپ {PHONE}</a><a class="btn y" href="#fee-calculators">فیس معلوم کریں {ARROW}</a></div></div></section>'
    + REVIEWS + '<!--FAQ-->' + FACILITATOR +
    HOME_GUIDES
)

# Home page terminology (phase 1: home only; roll out to inner pages after approval)
HOME_BODY = HOME_BODY.replace("سرٹیفیکیٹ", "سرٹیفیکیٹ").replace("ملکیت کی منتقلی اور ٹوکن ٹیکس گائیڈ", "ملکیت کی منتقلی اور ٹوکن ٹیکس گائیڈ")

PAGES.append(dict(
    path="/", kind="hub", raw=True, main_class="home home-ur", en_title="Home",
    css=["/assets/home-wide.css", "/assets/home-refinement.css?v=20261126a", "/assets/guide-cards.css?v=1"], js=["/assets/home-refinement.js?v=third1"],
    title="دستک 90807 | گھر بیٹھے سرکاری دستاویزات، گوجرخان اور پنجاب",
    desc="ڈرائیونگ لائسنس، پولیس کریکٹر سرٹیفیکیٹ، گاڑی کی منتقلی، ٹوکن ٹیکس اور ڈومیسائل میں گھر بیٹھے مدد۔ مریم کی دستک فیسیلیٹیٹر کوڈ 90807۔ واٹس ایپ 0345-5583530۔",
    h1="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن", og="/assets/dastak-online-document-facilitation-punjab-og.jpg",
    og_alt="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی اور پنجاب میں گھر بیٹھے سرکاری دستاویزات",
    crumbs=[],
    body=HOME_BODY,
    faqs=[
        ("مریم کی دستک کیسے کام کرتی ہے؟", "مریم کی دستک حکومتِ پنجاب کا اقدام ہے جس کے تحت سرکاری خدمات گھر کی دہلیز پر دی جاتی ہیں۔ دستاویزات اور دستیابی کی تصدیق کے لیے رجسٹرڈ فیسیلیٹیٹر محمد عثمان (کوڈ 90807) سے رابطہ کریں۔ درخواستیں پنجاب کے متعلقہ سرکاری نظام کے ذریعے جمع ہوتی ہیں۔"),
        ("فیسیلیٹیٹر کوڈ 90807 کی تصدیق کیسے کریں؟", "دستاویزات دینے سے پہلے سرکاری دستک پورٹل یا ایپ پر کوڈ 90807 چیک کریں، یا مریم کی دستک کی سرکاری ہیلپ لائن 1202 پر کال کر کے محمد عثمان اور کوڈ 90807 کی تصدیق کریں۔ 1202 سرکاری ہیلپ لائن ہے، ہمارا نمبر نہیں۔"),
        ("کیا یہ سرکاری ویب سائٹ ہے؟", "نہیں۔ یہ مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر (کوڈ 90807) کی آزاد سروس ہے، کوئی سرکاری ویب سائٹ یا محکمہ نہیں۔ سرکاری پورٹل dastak.punjab.gov.pk ہے۔"),
        ("آپ کن علاقوں میں خدمات دیتے ہیں؟", "گوجرخان، راولپنڈی اور قریبی علاقوں میں پہلے سے وقت طے کر کے گھر پر وزٹ کیا جاتا ہے۔ پورے پنجاب کے لیے آن لائن رہنمائی دستیاب ہے۔ اپنی سروس اور علاقے کے لیے دستیابی کی تصدیق کر لیں۔"),
        ("کیا آپ ڈرائیونگ لائسنس اور گاڑی کی ملکیت کی منتقلی میں مدد کرتے ہیں؟", "جی ہاں۔ ہم ڈرائیونگ لائسنس کی تجدید، ڈپلیکیٹ لائسنس، گاڑی کی رجسٹریشن اور ملکیت کی منتقلی کے لیے دستاویزات کی تیاری اور درخواست میں رہنمائی کرتے ہیں۔ جہاں لازمی ہو وہاں ٹیسٹ، بائیومیٹرک اور محکمے کا وزٹ ضروری رہتا ہے۔"),
        ("کیا آپ پولیس سرٹیفیکیٹ اور سول دستاویزات میں مدد کرتے ہیں؟", "پولیس کریکٹر سرٹیفیکیٹ، گمشدگی رپورٹ، ڈومیسائل، ای اسٹامپ اور سول رجسٹریشن کے بارے میں پوچھیں۔ شرائط اور کارروائی کا وقت متعلقہ سرکاری محکمے پر منحصر ہے۔"),
        ("کیا آپ ای بز اور فشریز کی درخواستوں میں مدد کرتے ہیں؟", "پنجاب ای بز کاروباری خدمات اور فشریز ای لائسنس کے بارے میں رہنمائی کے لیے رابطہ کریں۔ بکنگ سے پہلے سروس کی شرائط اور دستیابی کی تصدیق کر لیں۔"),
        ("اپلائی کرنے سے پہلے فیس کیسے معلوم کریں؟", "ہمارے پنجاب فیس کیلکولیٹر سے اندازہ لگائیں اور آگے بڑھنے سے پہلے سرکاری فیس اور فیسیلیٹیشن چارجز کی تصدیق کر لیں۔ دستک تربیتی مینول کے مطابق فیسیلیٹیٹر چارجز 950 روپے ہیں۔ حتمی فیس اور اہلیت متعلقہ محکمہ طے کرتا ہے۔"),
    ]))

_RS = re.compile(r"Rs\.? ?[\d,]+")
_ROMAN = re.compile(r"\((?=[A-Za-z])[A-Za-z][A-Za-z ,'\-]*\)")


_NUM = re.compile(r"0345-5583530|\+92-345-5583530|(?<![\d,.A-Za-z@])(?:90807|47850|1202)(?![\d,A-Za-z.]\w)")
_APP = re.compile(r"Doorstep Delivery|Self Service|On Behalf|Facilitator Code|\bSelf\b")


def fix_bidi(doc):
    """Inside <main>: keep numbers, Rs amounts, app labels and Roman-Urdu brackets left-to-right and unbroken."""
    i, j = doc.find("<main"), doc.find("</main>")
    body = doc[i:j]
    skip = []
    k = body.find('<div class="home-review-track"')
    if k != -1:
        skip.append((k, body.find('</div><p class="sub">', k)))
    def text_fix(m):
        if any(a <= m.start() < b for a, b in skip):
            return m.group(0)
        before = body[max(0, m.start() - 40):m.start() + 1]
        t = m.group(0)
        if before.endswith('class="ltr">') or before.endswith('dir="ltr">') or re.search(r'<(strong|b)[^>]*>$', before) and _NUM.fullmatch(t[1:-1] or "x"):
            return t
        t = _RS.sub(lambda x: f'<span class="ltr">{x.group(0)}</span>', t)
        t = _ROMAN.sub(lambda x: f'<bdi dir="ltr">{x.group(0)}</bdi>', t)
        t = _NUM.sub(lambda x: f'<span class="ltr">{x.group(0)}</span>', t)
        t = _APP.sub(lambda x: f'<bdi dir="ltr">{x.group(0)}</bdi>', t)
        return t
    body = re.sub(r">[^<>]+<", text_fix, body)
    return doc[:i] + body + doc[j:]


# Phase 2: driving license and police service pages (body comes from the English page).
PHASE2_SERVICES = []
PAGES.append(dict(
    path="/services/renewal-of-learners-driving-license/", kind="service", en_title="Renewal of Learners Driving License",
    title="لرنر پرمٹ کی تجدید پنجاب: گھر بیٹھے آن لائن | دستک 90807",
    desc="پنجاب میں لرنر ڈرائیونگ پرمٹ کی تجدید گھر بیٹھے کروائیں۔ شناختی کارڈ اور تصویر کافی، ڈیجیٹل دستاویز فوراً تیار۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="لرنر پرمٹ کی تجدید", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("لرنر پرمٹ کی تجدید", "/ur/services/renewal-of-learners-driving-license/")], faqs=[]))
PHASE2_SERVICES.append("/services/renewal-of-learners-driving-license/")
PAGES.append(dict(
    path="/services/duplicate-driving-license/", kind="service", en_title="Duplicate Driving License",
    title="ڈپلیکیٹ ڈرائیونگ لائسنس پنجاب: آن لائن درخواست | دستک 90807",
    desc="گم شدہ یا خراب ڈرائیونگ لائسنس کا ڈپلیکیٹ پنجاب میں گھر بیٹھے بنوائیں۔ دستاویزات کی فہرست، طریقہ اور فیس کا اندازہ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ڈپلیکیٹ ڈرائیونگ لائسنس", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈپلیکیٹ ڈرائیونگ لائسنس", "/ur/services/duplicate-driving-license/")], faqs=[]))
PHASE2_SERVICES.append("/services/duplicate-driving-license/")
PAGES.append(dict(
    path="/services/renewal-international-driving-license/", kind="service", en_title="Renewal International Driving License",
    title="انٹرنیشنل ڈرائیونگ لائسنس کی تجدید پنجاب | دستک 90807",
    desc="پنجاب میں انٹرنیشنل ڈرائیونگ لائسنس کی تجدید گھر بیٹھے کروائیں۔ پاسپورٹ، ویزا اور لائسنس کے ساتھ آن لائن درخواست، کورئیر سے ڈیلیوری۔ کوڈ 90807۔",
    h1="انٹرنیشنل ڈرائیونگ لائسنس کی تجدید", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("انٹرنیشنل ڈرائیونگ لائسنس کی تجدید", "/ur/services/renewal-international-driving-license/")], faqs=[]))
PHASE2_SERVICES.append("/services/renewal-international-driving-license/")
PAGES.append(dict(
    path="/services/duplicate-international-driving-license/", kind="service", en_title="Duplicate International Driving License",
    title="ڈپلیکیٹ انٹرنیشنل ڈرائیونگ لائسنس پنجاب | دستک 90807",
    desc="گم شدہ انٹرنیشنل ڈرائیونگ لائسنس کا ڈپلیکیٹ پنجاب میں گھر بیٹھے بنوائیں۔ مکمل دستاویزات، طریقہ اور بکنگ۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="ڈپلیکیٹ انٹرنیشنل ڈرائیونگ لائسنس", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈپلیکیٹ انٹرنیشنل ڈرائیونگ لائسنس", "/ur/services/duplicate-international-driving-license/")], faqs=[]))
PHASE2_SERVICES.append("/services/duplicate-international-driving-license/")
PAGES.append(dict(
    path="/services/general-police-verification/", kind="service", en_title="General Police Verification",
    title="جنرل پولیس ویریفکیشن پنجاب: آن لائن درخواست | دستک 90807",
    desc="پاکستان میں نوکری اور داخلے کے لیے جنرل پولیس ویریفکیشن گھر بیٹھے کروائیں۔ شناختی کارڈ یا ب فارم کافی۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="جنرل پولیس ویریفکیشن", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("جنرل پولیس ویریفکیشن", "/ur/services/general-police-verification/")], faqs=[]))
PHASE2_SERVICES.append("/services/general-police-verification/")
PAGES.append(dict(
    path="/services/tenant-registration/", kind="service", en_title="Tenant Registration",
    title="کرایہ دار کی رجسٹریشن پنجاب: آن لائن | دستک 90807",
    desc="پنجاب پولیس میں کرایہ دار کی رجسٹریشن گھر بیٹھے کروائیں۔ مالک مکان اور کرایہ دار کے شناختی کارڈ، کرایہ نامہ اور تصاویر۔ دستک کوڈ 90807، گوجرخان۔",
    h1="کرایہ دار کی رجسٹریشن", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("کرایہ دار کی رجسٹریشن", "/ur/services/tenant-registration/")], faqs=[]))
PHASE2_SERVICES.append("/services/tenant-registration/")
PAGES.append(dict(
    path="/services/loss-report/", kind="service", en_title="Loss Report",
    title="گمشدگی کی رپورٹ (لاس رپورٹ) پنجاب: آن لائن | دستک 90807",
    desc="گم شدہ دستاویزات کی پولیس رپورٹ پنجاب میں گھر بیٹھے درج کروائیں، کام موقع پر مکمل۔ دستاویزات کی فہرست اور بکنگ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="گمشدگی کی رپورٹ", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("گمشدگی کی رپورٹ", "/ur/services/loss-report/")], faqs=[]))
PHASE2_SERVICES.append("/services/loss-report/")
PAGES.append(dict(
    path="/services/crime-report/", kind="service", en_title="Crime Report",
    title="جرم کی رپورٹ پنجاب پولیس: آن لائن | دستک 90807",
    desc="پنجاب پولیس میں جرم کی رپورٹ گھر بیٹھے آن لائن درج کروائیں۔ تحریری شکایت کافی، بکنگ دستک ایپ یا واٹس ایپ سے۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="جرم کی رپورٹ", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("جرم کی رپورٹ", "/ur/services/crime-report/")], faqs=[]))
PHASE2_SERVICES.append("/services/crime-report/")
PAGES.append(dict(
    path="/services/copy-of-fir/", kind="service", en_title="Copy of FIR",
    title="ایف آئی آر کی کاپی پنجاب: آن لائن حاصل کریں | دستک 90807",
    desc="پنجاب میں FIR کی کاپی گھر بیٹھے حاصل کریں۔ FIR نمبر، تھانہ اور وجہ بتائیں، باقی کام ہم کرتے ہیں۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="ایف آئی آر کی کاپی", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ایف آئی آر کی کاپی", "/ur/services/copy-of-fir/")], faqs=[]))
PHASE2_SERVICES.append("/services/copy-of-fir/")
PAGES.append(dict(
    path="/services/traffic-challan/", kind="service", en_title="Traffic Challan",
    title="ٹریفک چالان پنجاب: آن لائن چیک اور ادائیگی | دستک 90807",
    desc="پنجاب میں ٹریفک چالان آن لائن چیک، ٹریک اور ادا کریں۔ شناختی کارڈ یا گاڑی کی تفصیل کافی، ادائیگی PSID سے۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ٹریفک چالان", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ٹریفک چالان", "/ur/services/traffic-challan/")], faqs=[]))
PHASE2_SERVICES.append("/services/traffic-challan/")
PAGES.append(dict(
    path="/services/safe-city-challan/", kind="service", en_title="Safe City Challan",
    title="سیف سٹی چالان پنجاب: آن لائن چیک اور ادائیگی | دستک 90807",
    desc="پنجاب سیف سٹی ای چالان آن لائن چیک اور PSID سے ادا کریں، کام موقع پر مکمل۔ گاڑی کا نمبر یا شناختی کارڈ کافی۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="سیف سٹی چالان", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("سیف سٹی چالان", "/ur/services/safe-city-challan/")], faqs=[]))
PHASE2_SERVICES.append("/services/safe-city-challan/")

# Phase 3: vehicle, domicile, e-stamp and civil service pages.
PAGES.append(dict(
    path="/services/motor-vehicle-registration/", kind="service", en_title="Motor Vehicle Registration",
    title="نئی گاڑی کی رجسٹریشن گوجرخان، راولپنڈی | دستک 90807",
    desc="گوجرخان اور راولپنڈی میں نئی گاڑی یا موٹر سائیکل کی رجسٹریشن گھر بیٹھے کروائیں۔ دستاویزات، طریقہ اور فیس کا اندازہ۔ رجسٹریشن کارڈ کورئیر سے۔ دستک کوڈ 90807۔",
    h1="نئی گاڑی کی رجسٹریشن", og="/assets/og/vehicles.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("نئی گاڑی کی رجسٹریشن", "/ur/services/motor-vehicle-registration/")], faqs=[]))
PHASE2_SERVICES.append("/services/motor-vehicle-registration/")
PAGES.append(dict(
    path="/services/duplicate-domicile/", kind="service", en_title="Duplicate Domicile",
    title="ڈپلیکیٹ ڈومیسائل گوجرخان: گھر بیٹھے | دستک 90807",
    desc="گم شدہ ڈومیسائل کا ڈپلیکیٹ گوجرخان میں گھر بیٹھے بنوائیں۔ مکمل دستاویزات کی فہرست، طریقہ اور بکنگ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ڈپلیکیٹ ڈومیسائل", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈپلیکیٹ ڈومیسائل", "/ur/services/duplicate-domicile/")], faqs=[]))
PHASE2_SERVICES.append("/services/duplicate-domicile/")
PAGES.append(dict(
    path="/services/modification-domicile/", kind="service", en_title="Modification Domicile",
    title="ڈومیسائل میں ترمیم گوجرخان | دستک 90807",
    desc="گوجرخان میں ڈومیسائل سرٹیفیکیٹ میں درستگی یا ترمیم گھر بیٹھے کروائیں۔ درخواست اور موجودہ ڈومیسائل کافی۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ڈومیسائل میں ترمیم", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈومیسائل میں ترمیم", "/ur/services/modification-domicile/")], faqs=[]))
PHASE2_SERVICES.append("/services/modification-domicile/")
PAGES.append(dict(
    path="/services/noc-for-domicile-transfer/", kind="service", en_title="NOC for Domicile Transfer",
    title="ڈومیسائل منتقلی کا NOC گوجرخان | دستک 90807",
    desc="گوجرخان میں ڈومیسائل کی دوسرے ضلع منتقلی کا NOC گھر بیٹھے حاصل کریں۔ دستاویزات، طریقہ اور بکنگ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="ڈومیسائل کی منتقلی کا NOC", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈومیسائل کی منتقلی کا NOC", "/ur/services/noc-for-domicile-transfer/")], faqs=[]))
PHASE2_SERVICES.append("/services/noc-for-domicile-transfer/")
PAGES.append(dict(
    path="/services/e-stamping/", kind="service", en_title="E-Stamping",
    title="ای اسٹامپ پیپر پنجاب: آن لائن | دستک 90807",
    desc="پنجاب میں ای اسٹامپ پیپر گھر بیٹھے حاصل کریں، بینک آف پنجاب سے لے کر آپ تک۔ صرف شناختی کارڈ کافی۔ دستک فیسیلیٹیٹر کوڈ 90807، گوجرخان۔",
    h1="ای اسٹامپ پیپر", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ای اسٹامپ پیپر", "/ur/services/e-stamping/")], faqs=[]))
PHASE2_SERVICES.append("/services/e-stamping/")
PAGES.append(dict(
    path="/services/birth-certificate/", kind="service", en_title="Birth Certificate",
    title="پیدائش سرٹیفیکیٹ گوجرخان: گھر بیٹھے | دستک 90807",
    desc="گوجرخان میں بچے کا پیدائش سرٹیفیکیٹ گھر بیٹھے بنوائیں۔ فارم A سمیت تمام دستاویزات کی فہرست اور طریقہ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="پیدائش سرٹیفیکیٹ", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("پیدائش سرٹیفیکیٹ", "/ur/services/birth-certificate/")], faqs=[]))
PHASE2_SERVICES.append("/services/birth-certificate/")
PAGES.append(dict(
    path="/services/death-certificate/", kind="service", en_title="Death Certificate",
    title="وفات سرٹیفیکیٹ گوجرخان: گھر بیٹھے | دستک 90807",
    desc="گوجرخان میں وفات سرٹیفیکیٹ گھر بیٹھے بنوائیں۔ فارم B، گواہ اور تدفین کی پرچی سمیت دستاویزات کی فہرست۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="وفات سرٹیفیکیٹ", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("وفات سرٹیفیکیٹ", "/ur/services/death-certificate/")], faqs=[]))
PHASE2_SERVICES.append("/services/death-certificate/")
PAGES.append(dict(
    path="/services/marriage-certificate/", kind="service", en_title="Marriage Certificate",
    title="میرج سرٹیفیکیٹ گوجرخان: گھر بیٹھے | دستک 90807",
    desc="گوجرخان میں نکاح نامے سے میرج سرٹیفیکیٹ گھر بیٹھے بنوائیں۔ دلہا، دلہن اور والدین کے شناختی کارڈ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="نکاح (میرج) سرٹیفیکیٹ", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("نکاح (میرج) سرٹیفیکیٹ", "/ur/services/marriage-certificate/")], faqs=[]))
PHASE2_SERVICES.append("/services/marriage-certificate/")
PAGES.append(dict(
    path="/services/divorce-certificate/", kind="service", en_title="Divorce Certificate",
    title="طلاق سرٹیفیکیٹ گوجرخان | دستک 90807",
    desc="گوجرخان میں طلاق سرٹیفیکیٹ کے لیے درکار دستاویزات، طریقہ اور بکنگ۔ یونین کونسل نوٹس اور ثالثی کونسل ریکارڈ۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="طلاق سرٹیفیکیٹ", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("طلاق سرٹیفیکیٹ", "/ur/services/divorce-certificate/")], faqs=[]))
PHASE2_SERVICES.append("/services/divorce-certificate/")
PAGES.append(dict(
    path="/services/general-inquiry-and-guide/", kind="service", en_title="General Inquiry and Guide",
    title="مریم کی دستک: رہنمائی اور عام معلومات | دستک 90807",
    desc="مریم کی دستک کیسے کام کرتی ہے، دستک ایپ کیسے استعمال کریں، اور سرکاری دستاویزات گھر بیٹھے کیسے حاصل کریں۔ واٹس ایپ پر سوال پوچھیں۔ کوڈ 90807۔",
    h1="مریم کی دستک: رہنمائی اور عام معلومات", og="/assets/og/general.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("مریم کی دستک: رہنمائی اور عام معلومات", "/ur/services/general-inquiry-and-guide/")], faqs=[]))
PHASE2_SERVICES.append("/services/general-inquiry-and-guide/")
PAGES.append(dict(
    path="/services/other-punjab-dastak-services/", kind="service", en_title="Other Punjab Dastak Services",
    title="پنجاب دستک کی دیگر خدمات | دستک 90807",
    desc="پنجاب کے دیگر محکموں کی دستک خدمات: فشریز، فوڈ اتھارٹی، e-Biz اور مزید۔ سروس کا نام بھیجیں، میں بتاؤں گا کہ مدد ہو سکتی ہے۔ کوڈ 90807۔",
    h1="پنجاب دستک کی دیگر خدمات", og="/assets/og/general.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("پنجاب دستک کی دیگر خدمات", "/ur/services/other-punjab-dastak-services/")], faqs=[]))
PHASE2_SERVICES.append("/services/other-punjab-dastak-services/")

# Phase 4: guides and content pages (body comes from the English page).
PHASE4_PAGES = []
PAGES.append(dict(
    path="/guides/punjab-token-tax-payment-and-penalty/", kind="guide", en_title="Punjab Token Tax 2026",
    title="پنجاب ٹوکن ٹیکس 2026: آخری تاریخ اور جرمانہ | دستک 90807",
    desc="خبروں کے مطابق 30 نومبر 2026 آخری تاریخ، 1 دسمبر سے جرمانہ۔ PSID سے ٹوکن ٹیکس کیسے ادا کریں اور سرکاری رقم کہاں چیک کریں۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="پنجاب ٹوکن ٹیکس 2026: آخری تاریخ، جرمانہ اور ادائیگی", og="/assets/punjab-token-tax-guide-dastak-90807-og.jpg?v=1",
    crumbs=[('رہنمائی', '/ur/guides/'), ('پنجاب ٹوکن ٹیکس 2026: آخری تاریخ، جرمانہ اور ادائیگی', '/ur/guides/punjab-token-tax-payment-and-penalty/')], faqs=[]))
PHASE4_PAGES.append("/guides/punjab-token-tax-payment-and-penalty/")
PAGES.append(dict(
    path="/guides/domicile-stamp-paper-gujar-khan-rawalpindi/", kind="guide", en_title="Domicile & e-Stamp Paper Guide",
    title="ڈومیسائل اور ای اسٹامپ پیپر: گوجرخان، راولپنڈی گائیڈ | دستک 90807",
    desc="گوجرخان اور راولپنڈی میں ڈومیسائل کی درخواست اور ای اسٹامپ پیپر کی مکمل گائیڈ: دستاویزات، طریقہ اور تصدیق۔ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="گوجرخان اور راولپنڈی میں ڈومیسائل اور ای اسٹامپ پیپر", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('رہنمائی', '/ur/guides/'), ('گوجرخان اور راولپنڈی میں ڈومیسائل اور ای اسٹامپ پیپر', '/ur/guides/domicile-stamp-paper-gujar-khan-rawalpindi/')], faqs=[]))
PHASE4_PAGES.append("/guides/domicile-stamp-paper-gujar-khan-rawalpindi/")
PAGES.append(dict(
    path="/rawalpindi/", kind="page", en_title="Rawalpindi",
    title="راولپنڈی: گھر پر سرکاری دستاویزات کی مدد | دستک 90807",
    desc="راولپنڈی میں ڈومیسائل، ڈرائیونگ لائسنس، پولیس، گاڑی اور سول دستاویزات میں مدد۔ دستک ایپ میں کوڈ 90807 کے ساتھ بکنگ یا واٹس ایپ 0345-5583530۔",
    h1="راولپنڈی میں گھر پر دستاویزات کی مدد", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('راولپنڈی میں گھر پر دستاویزات کی مدد', '/ur/rawalpindi/')], faqs=[]))
PHASE4_PAGES.append("/rawalpindi/")
PAGES.append(dict(
    path="/citizen-tools/", kind="page", en_title="Citizen Tools",
    title="پنجاب سرکاری پورٹلز: لائسنس ٹریکنگ، ای چالان، تصدیق | دستک 90807",
    desc="ڈرائیونگ لائسنس ٹریک کریں، گاڑی، پولیس، ڈومیسائل اور ای اسٹامپ کی تصدیق کریں۔ پنجاب کے سرکاری پورٹلز کے لنکس ایک جگہ۔ یہ سرکاری ویب سائٹ نہیں۔",
    h1="پنجاب حکومت کے پورٹلز ایک جگہ", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('پنجاب حکومت کے پورٹلز ایک جگہ', '/ur/citizen-tools/')], faqs=[]))
PHASE4_PAGES.append("/citizen-tools/")
PAGES.append(dict(
    path="/document-checklist/", kind="page", en_title="Document Checklist",
    title="دستاویزات کی چیک لسٹ: پنجاب خدمات | دستک 90807",
    desc="سروس چنیں، موجود دستاویزات پر نشان لگائیں اور فہرست واٹس ایپ پر بھیجیں۔ لائسنس، پولیس، گاڑی، ڈومیسائل اور سول دستاویزات۔ کوڈ 90807۔",
    h1="پنجاب کی خدمات کے لیے دستاویزات کی چیک لسٹ", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('پنجاب کی خدمات کے لیے دستاویزات کی چیک لسٹ', '/ur/document-checklist/')], faqs=[]))
PHASE4_PAGES.append("/document-checklist/")
PAGES.append(dict(
    path="/downloads/", kind="page", en_title="Downloads",
    title="پنجاب درخواست فارمز PDF ڈاؤن لوڈ | دستک 90807",
    desc="گاڑی کی رجسٹریشن، ڈرائیونگ لائسنس میڈیکل، ڈومیسائل، پولیس اور یونین کونسل کے فارمز مفت ڈاؤن لوڈ کریں۔ ہر فارم کا ذریعہ درج۔ کوڈ 90807۔",
    h1="پنجاب کے درخواست فارمز (PDF)", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('پنجاب کے درخواست فارمز (PDF)', '/ur/downloads/')], faqs=[]))
PHASE4_PAGES.append("/downloads/")
PAGES.append(dict(
    path="/how-it-works/", kind="page", en_title="How it works",
    title="طریقہ کار: دستک سروس کیسے کام کرتی ہے | دستک 90807",
    desc="بکنگ سے ڈیلیوری تک: دستک ایپ میں کوڈ 90807، ادائیگی PSID سے، اور دستاویزات کی حفاظت۔ گوجرخان، راولپنڈی اور پنجاب۔",
    h1="طریقہ کار", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('طریقہ کار', '/ur/how-it-works/')], faqs=[]))
PHASE4_PAGES.append("/how-it-works/")
PAGES.append(dict(
    path="/reviews/", kind="page", en_title="Reviews",
    title="کسٹمر ریویوز: دستک آن لائن ڈاکومنٹ فیسیلیٹیشن | دستک 90807",
    desc="Google اور Facebook پر دستک 90807 کے اصل کسٹمر ریویوز پڑھیں یا اپنا ریویو دیں۔ Google ریٹنگ 5 میں سے 4.9۔",
    h1="کسٹمر ریویوز", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[('کسٹمر ریویوز', '/ur/reviews/')], faqs=[]))
PHASE4_PAGES.append("/reviews/")

# Phase 5: about, FAQs and legal pages (body comes from the English page).
PHASE5_PAGES = []
PAGES.append(dict(
    path="/about/", kind="page", en_title="About",
    title="ہمارے بارے میں: محمد عثمان، فیسیلیٹیٹر کوڈ 90807 | دستک 90807",
    desc="محمد عثمان، حکومتِ پنجاب کے مریم کی دستک پروگرام کے رجسٹرڈ فیسیلیٹیٹر (کوڈ 90807)، گوجرخان۔ 700 سے زیادہ خدمات مکمل، Google ریٹنگ 4.9۔ اپنی تصدیق خود کریں۔",
    h1="محمد عثمان، گوجرخان میں آپ کے مریم کی دستک فیسیلیٹیٹر", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[("محمد عثمان، گوجرخان میں آپ کے مریم کی دستک فیسیلیٹیٹر", "/ur/about/")], faqs=[]))
PHASE5_PAGES.append("/about/")
PAGES.append(dict(
    path="/faqs/", kind="page", en_title="FAQs",
    title="عام سوالات: دستک خدمات، فیس اور تصدیق | دستک 90807",
    desc="ڈرائیونگ لائسنس، گاڑی، پولیس، ڈومیسائل اور سول دستاویزات کے بارے میں عام سوالات کے جواب۔ بکنگ، فیس اور فیسیلیٹیٹر کوڈ 90807 کی تصدیق۔",
    h1="عام سوالات", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[("عام سوالات", "/ur/faqs/")], faqs=[]))
PHASE5_PAGES.append("/faqs/")
PAGES.append(dict(
    path="/disclaimer/", kind="page", en_title="Disclaimer",
    title="ڈسکلیمر | دستک 90807",
    desc="دستک 90807 ایک آزاد فیسیلیٹیشن سروس ہے، سرکاری دفتر یا ویب سائٹ نہیں۔ فیس سرکاری سسٹم بناتا ہے۔ منظوری یا وقت کی کوئی ضمانت نہیں۔",
    h1="ڈسکلیمر", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[("ڈسکلیمر", "/ur/disclaimer/")], faqs=[]))
PHASE5_PAGES.append("/disclaimer/")
PAGES.append(dict(
    path="/privacy/", kind="page", en_title="Privacy",
    title="پرائیویسی پالیسی | دستک 90807",
    desc="آپ کی دستاویزات صرف آپ کی درخواست کے لیے استعمال ہوتی ہیں اور کام مکمل ہوتے ہی ڈیلیٹ کر دی جاتی ہیں۔ ہم کبھی پاس ورڈ یا OTP نہیں مانگتے۔",
    h1="پرائیویسی پالیسی", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[("پرائیویسی پالیسی", "/ur/privacy/")], faqs=[]))
PHASE5_PAGES.append("/privacy/")
PAGES.append(dict(
    path="/terms/", kind="page", en_title="Terms",
    title="شرائط | دستک 90807",
    desc="دستک 90807 کی خدمات کی شرائط: فیس اور رقم کی واپسی، کوئی ضمانت نہیں، اور آپ کی ذمہ داری۔ رجسٹرڈ فیسیلیٹیٹر کوڈ 90807۔",
    h1="شرائط", og="/assets/dastak-online-document-facilitation-punjab-og.jpg?v=1",
    crumbs=[("شرائط", "/ur/terms/")], faqs=[]))
PHASE5_PAGES.append("/terms/")


# Hub pages: layout comes from the English page itself (scripts/ur_hub_convert.py).
from ur_hub_convert import convert as _hub_convert  # noqa: E402
for _p in PAGES:
    if _p["path"] in ("/services/", "/guides/", "/calculators/", "/contact/") or _p["path"] in PHASE2_SERVICES or _p["path"] in PHASE4_PAGES or _p["path"] in PHASE5_PAGES:
        _h = _hub_convert(_p["path"].strip("/"))
        _p.update(hub_en=True, raw=True, main_class=_h["main_class"], body=_h["body"], faqs=_h["faqs"],
                  css=_h["css"], js=_h["js"], h1=re.sub(r"<[^>]+>", "", re.search(r"<h1[^>]*>(.*?)</h1>", _h["body"], re.S).group(1)))


def main():
    for p in PAGES:
        out_dir = os.path.join(ROOT, "ur", p["path"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(fix_bidi(page(p)))
    print(f"Built {len(PAGES)} Urdu pages")


if __name__ == "__main__":
    main()
