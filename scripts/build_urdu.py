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

SAME_AS = ["https://facebook.com/Dastak90807", "https://instagram.com/dastak90807",
           "https://www.tiktok.com/@dastak90807", "https://x.com/dastak90807",
           "https://www.linkedin.com/in/dastak90807", "https://www.youtube.com/@Dastak90807",
           "https://www.snapchat.com/add/dastak90807", "https://www.pinterest.com/dastak90807",
           "https://share.google/nmpsQYND7NTAnZzqI"]

DISCLAIMER = ("دستک آن لائن ڈاکومنٹ فیسیلیٹیشن محمد عثمان چلاتے ہیں، جو حکومتِ پنجاب کے مریم کی دستک پروگرام کے تحت "
              f"رجسٹرڈ فیسیلیٹیٹر ہیں (فیسیلیٹیٹر کوڈ {CODE})۔ یہ ویب سائٹ ایک آزاد فیسیلیٹیشن سروس ہے، کوئی سرکاری ویب سائٹ یا محکمہ نہیں۔ "
              "فیس سرکاری سسٹم خود بناتا ہے اور حتمی رقم آپ کے PSID پر لکھی ہوتی ہے۔ تفصیلات ہمیشہ سرکاری دستک پورٹل یا ایپ سے تصدیق کریں۔")

FEE_SOURCE = ("فیس کی معلومات کا ذریعہ: سرکاری دستک تربیتی مینول (ورژن 5، اپڈیٹ 26 جون 2025) اور سرکاری دستک پورٹل۔ "
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
    en_note = f'<p class="ur-en-link" lang="en" dir="ltr">Read in English: <a href="/en{path}" hreflang="en">{esc(p.get("en_title", "English version"))}</a></p>'

    return f'''<!doctype html><html lang="ur" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><link rel="canonical" href="{ur_url}"><link rel="alternate" hreflang="ur" href="{ur_url}"><link rel="alternate" hreflang="en" href="{en_url}"><link rel="alternate" hreflang="x-default" href="{en_url}"><meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="{"article" if p.get("kind") == "guide" else "website"}"><meta property="og:site_name" content="Dastak 90807"><meta property="og:locale" content="ur_PK"><meta property="og:locale:alternate" content="en_PK"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{ur_url}"><meta property="og:image" content="{og_img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{esc(og_alt)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(desc)}"><meta name="twitter:image" content="{og_img}"><meta name="twitter:image:alt" content="{esc(og_alt)}"><meta name="theme-color" content="#0A3F35"><link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="{SITE}/assets/apple-touch-icon.png"><link rel="manifest" href="/site.webmanifest"><link rel="preload" href="/assets/fonts/noto-sans-arabic-arabic-400-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/assets/style.css"><link rel="stylesheet" href="/assets/site-update.css?v=20261122-ui"><link rel="stylesheet" href="/assets/site-polish.css?v=6"><link rel="stylesheet" href="/assets/services-design.css?v=1"><link rel="stylesheet" href="/assets/page-design.css?v=20261125a"><link rel="stylesheet" href="/assets/service-detail-v2.css?v=20261125a">{"".join(f'<link rel="stylesheet" href="{c}">' for c in p.get("css", []))}<link rel="stylesheet" href="/assets/urdu-rtl.css?v=8"><script type="application/ld+json">{ld}</script></head><body id="top"><a class="skip" href="#main">مواد پر جائیں</a>
<aside class="top" aria-label="سرکاری پورٹل اور رجسٹریشن"><p class="ur-top">مریم کی دستک (حکومتِ پنجاب کا اقدام) کے <b>رجسٹرڈ فیسیلیٹیٹر</b> · <b class="gold">کوڈ {CODE}</b> · سرکاری پورٹل: <a href="https://dastak.punjab.gov.pk" rel="noopener" class="ltr">dastak.punjab.gov.pk</a></p></aside>
<script src="/assets/shared-header.js?v=7"></script><noscript><nav aria-label="مرکزی مینیو"><a href="/ur/">ہوم</a> <a href="/ur/services/">خدمات</a> <a href="/ur/calculators/">فیس کیلکولیٹر</a> <a href="/ur/guides/">گائیڈز</a> <a href="/ur/contact/">رابطہ</a> <a href="/en{path}" lang="en">English</a></nav></noscript>
{(f'<main id="main" class="{main_class}">{p["body"]}<section class="wrap home-faqs">{faq_block}{en_note}<p class="disc">{DISCLAIMER}</p></section></main>') if p.get("raw") else f'''<main id="main" class="{main_class}"><section class="wrap"><header class="service-intro"><p class="crumb">{crumb_html}</p>{p.get("eyebrow", "")}<h1>{p["h1"]}</h1><p class="meta">{p.get("meta", f"آخری اپڈیٹ: {UPDATED_UR} · تحریر: محمد عثمان، فیسیلیٹیٹر کوڈ {CODE}")}</p></header>
{p["body"]}
{faq_block}
{en_note}
<p class="disc">{DISCLAIMER}</p></section></main>'''}
{FOOTER}
<aside aria-label="فوری رابطہ"><a class="wafloat btn g" href="{WA}">واٹس ایپ</a><div class="bar"><a class="btn g" href="{WA}">واٹس ایپ</a><a class="btn y" href="tel:+923455583530">کال کریں</a></div></aside>
<script src="/assets/app.js" defer></script><a class="back-to-top" href="#top" aria-label="اوپر جائیں" title="اوپر جائیں">↑</a><script src="/assets/site-update.js?v=20261122-ui" defer></script><script src="/assets/site-polish.js?v=4" defer></script></body></html>
'''


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
<section class="service-module fee-module"><h2>{esc(name)} کی فیس کتنی ہے؟</h2>{fee_table(fees)}<p class="ur-note">{FEE_SOURCE}</p></section>
<section class="service-module steps-module"><h2>{esc(name)} کا طریقہ، قدم بہ قدم</h2><ol>{steps_html}</ol></section>
{extra}
{booking_block(name)}
{rel}'''


def guide_body(quick, sections, hero=None, related=()):
    toc = "".join(f'<li><a href="#s{i+1}">{h}</a></li>' for i, (h, _) in enumerate(sections))
    secs = "".join(f'<section class="service-module" id="s{i+1}"><h2>{h}</h2>{b}</section>' for i, (h, b) in enumerate(sections))
    hero_html = (f'<figure class="guide-hero"><img src="{hero[0]}" width="1600" height="893" alt="{esc(hero[1])}" fetchpriority="high"></figure>' if hero else "")
    rel = ("<section class=\"service-module related-module\"><h2>یہ بھی پڑھیں</h2>" + cards(related) + "</section>") if related else ""
    return f'''{hero_html}<div class="card quick answer-summary"><b>مختصر جواب</b><p>{quick}</p></div>
<nav class="guide-contents card" aria-label="اس صفحے میں"><strong>اس گائیڈ میں</strong><ul>{toc}</ul></nav>
{secs}
<div class="card book"><h2>مدد چاہیے؟</h2><p>پورے پنجاب میں واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ۔ {AREAS} میں گھر پر وزٹ پہلے سے وقت طے کر کے۔</p><div class="row"><a class="btn y" data-ga-event="guide_whatsapp_click" href="{WA}">واٹس ایپ {PHONE}</a><a class="btn g" href="tel:+923455583530">کال کریں</a><a class="btn o" href="/ur/calculators/">فیس کیلکولیٹر</a></div></div>
{rel}'''


# ---------------------------------------------------------------- related link sets
R = {
    "renew": ("/ur/services/renewal-of-regular-license/", "ڈرائیونگ لائسنس رینیول", "پنجاب میں لائسنس کی تجدید، دستاویزات اور فیس"),
    "learner": ("/ur/services/learner-driving-license/", "لرنر ڈرائیونگ لائسنس", "لرنر پرمٹ کیسے بنوائیں، فیس 500 روپے فی کیٹیگری"),
    "track": ("/ur/guides/how-to-track-driving-license-in-punjab/", "لائسنس ٹریک کرنے کا طریقہ", "DLIMS اور پاکستان پوسٹ سے اسٹیٹس دیکھیں"),
    "renew_guide": ("/ur/guides/punjab-driving-license-renewal-online/", "لائسنس رینیول آن لائن گائیڈ", "مکمل طریقہ، تیاری اور عام غلطیاں"),
    "character": ("/ur/services/character-certificate/", "پولیس کریکٹر سرٹیفکیٹ", "بیرون ملک سفر اور نوکری کے لیے"),
    "character_guide": ("/ur/guides/punjab-police-character-certificate-online/", "کریکٹر سرٹیفکیٹ گائیڈ", "دستاویزات، طریقہ اور تصدیق"),
    "transfer": ("/ur/services/transfer-of-motor-vehicle/", "گاڑی / موٹر سائیکل ٹرانسفر", "ملکیت اپنے نام کروانے کا طریقہ"),
    "token": ("/ur/services/token-tax/", "ٹوکن ٹیکس", "گھر بیٹھے سالانہ ٹوکن ٹیکس جمع کروائیں"),
    "vehicle_guide": ("/ur/guides/vehicle-transfer-token-tax-punjab/", "ٹرانسفر اور ٹوکن ٹیکس گائیڈ", "بائیومیٹرک، PSID اور عام سوالات"),
    "domicile": ("/ur/services/domicile-certificate/", "ڈومیسائل سرٹیفکیٹ", "فیس 1,200 روپے، گوجرخان اور راولپنڈی"),
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
RENEW_FEE_TABLE = ('<div class="ur-table-wrap"><table class="ur-fee ur-fee-grid"><caption>سرکاری رینیول فیس (1 سال)، سرکاری دستک پورٹل کے مطابق</caption>'
    '<thead><tr><th scope="col">کیٹیگری</th><th scope="col">رینیول فیس</th><th scope="col">جرمانہ 1 سے 3 ماہ</th><th scope="col">جرمانہ 3 ماہ سے 1 سال</th><th scope="col">جرمانہ 1 سال سے زیادہ</th><th scope="col">کل (کورئیر Rs 480 سمیت، جرمانے کے بغیر)</th></tr></thead><tbody>'
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
    title="ڈرائیونگ لائسنس رینیول پنجاب: دستاویزات اور فیس | دستک 90807",
    desc="پنجاب میں ڈرائیونگ لائسنس رینیول کا طریقہ، دستاویزات، فیس اور وقت۔ 1 سے 5 سال کے لیے تجدید۔ رجسٹرڈ دستک فیسیلیٹیٹر کوڈ 90807، واٹس ایپ 0345-5583530۔",
    h1="ڈرائیونگ لائسنس رینیول (پنجاب)", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈرائیونگ لائسنس رینیول", "/ur/services/renewal-of-regular-license/")],
    body=service_body(
        "ڈرائیونگ لائسنس رینیول",
        "پنجاب میں ریگولر ڈرائیونگ لائسنس کی تجدید (رینیول) دستک سروس کے ذریعے گھر بیٹھے ہو جاتی ہے۔ آپ کو اصل شناختی کارڈ، پرانا لائسنس اور سفید بیک گراؤنڈ والی تازہ تصویر چاہیے۔ لائسنس 1، 2، 3، 4 یا 5 سال کے لیے بن سکتا ہے اور تقریباً 10 دن میں کورئیر سے گھر پہنچ جاتا ہے۔ سرکاری فیس کیٹیگری اور مدت کے حساب سے بنتی ہے اور PSID پر لکھی ہوتی ہے۔",
        [("محکمہ", "ٹریفک پولیس پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 10 دن"), ("ڈیلیوری", "کورئیر کے ذریعے گھر پر")],
        ["اصل شناختی کارڈ (CNIC)", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)", "پرانا ڈرائیونگ لائسنس (اصل)",
         "میڈیکل سرٹیفکیٹ، صرف اگر عمر 50 سال سے زیادہ ہو", "ایف آئی آر یا گمشدگی رپورٹ کی کاپی، اگر اصل لائسنس گم ہو گیا ہو"],
        ["واٹس ایپ پر اپنا شناختی کارڈ اور پرانا لائسنس بھیجیں تاکہ کیٹیگری اور اہلیت چیک ہو جائے۔",
         "طے کریں کہ لائسنس کتنے سال (1 سے 5) کے لیے بنوانا ہے۔ فیس کا اندازہ <a href=\"/ur/calculators/\">فیس کیلکولیٹر</a> سے لگائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا ہمیں کال کریں۔",
         "فیسیلیٹیٹر آپ کی لائیو تصویر لے کر درخواست جمع کرواتا ہے اور PSID بنتا ہے۔",
         "PSID کی ادائیگی بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے کریں۔",
         "تقریباً 10 دن میں نیا لائسنس کورئیر سے آپ کے پتے پر آ جاتا ہے۔ اسٹیٹس <a href=\"/ur/guides/how-to-track-driving-license-in-punjab/\">یہاں سے ٹریک کریں</a>۔"],
        [("سرکاری فیس", "لائسنس کی کیٹیگری اور مدت (1 سے 5 سال) کے مطابق مختلف"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"),
         ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"), ("ادائیگی", "PSID کے ذریعے"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>سرکاری رینیول فیس کی تفصیل (پورٹل کے مطابق)</h2>' + RENEW_FEE_TABLE + '</section>',
        related=(R["renew_guide"], R["track"], R["learner"], R["calc"])),
    faqs=[
        ("لائسنس رینیو کیسے کریں؟ (License renew kaise karein)", "دستک ایپ میں Doorstep Delivery منتخب کر کے کوڈ 90807 لکھیں، یا واٹس ایپ 0345-5583530 پر رابطہ کریں۔ فیسیلیٹیٹر گھر آ کر تصویر لیتا ہے، درخواست جمع کرواتا ہے اور لائسنس کورئیر سے آپ کو مل جاتا ہے۔"),
        ("ڈرائیونگ لائسنس رینیول فیس کتنی ہے؟", "سرکاری فیس لائسنس کی کیٹیگری اور مدت کے حساب سے بنتی ہے۔ اس کے ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں (تربیتی مینول کے مطابق)۔ حتمی رقم PSID پر لکھی ہوتی ہے۔"),
        ("لائسنس کتنے سال کے لیے رینیو ہو سکتا ہے؟", "تربیتی مینول کے مطابق 1، 2، 3، 4 یا 5 سال کے لیے۔"),
        ("50 سال سے زیادہ عمر میں کیا چاہیے؟", "50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفکیٹ بھی ضروری ہے۔"),
        ("لائسنس گم ہو گیا ہو تو کیا کریں؟", "گمشدگی کی ایف آئی آر یا لاسٹ رپورٹ کی کاپی ساتھ لگائیں۔ ہم لاسٹ رپورٹ بنوانے میں بھی مدد کرتے ہیں۔"),
        ("Kya Gujar Khan se bahar bhi madad milti hai?", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ ہوتی ہے۔ گھر پر وزٹ گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/learner-driving-license/", kind="service", en_title="Learner Driving License",
    title="لرنر ڈرائیونگ لائسنس کیسے بنوائیں؟ فیس اور دستاویزات | دستک 90807",
    desc="پنجاب میں لرنر ڈرائیونگ لائسنس (لرنر پرمٹ) بنوانے کا طریقہ: صرف شناختی کارڈ اور تصویر، سرکاری فیس 500 روپے فی کیٹیگری، 180 دن کارآمد۔ دستک کوڈ 90807۔",
    h1="لرنر ڈرائیونگ لائسنس (لرنر پرمٹ)", og="/assets/og/driving-license.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("لرنر ڈرائیونگ لائسنس", "/ur/services/learner-driving-license/")],
    body=service_body(
        "لرنر ڈرائیونگ لائسنس",
        "گاڑی یا موٹر سائیکل چلانا سیکھنے والے ہر شخص کے لیے لرنر پرمٹ ضروری ہے۔ پنجاب میں یہ دستک سروس کے ذریعے گھر بیٹھے بن جاتا ہے: صرف اصل شناختی کارڈ اور سفید بیک گراؤنڈ والی لائیو تصویر چاہیے۔ سرکاری فیس 500 روپے فی کیٹیگری ہے، پرمٹ کی PDF موقع پر مل جاتی ہے اور یہ 180 دن کارآمد رہتا ہے۔",
        [("محکمہ", "ٹریفک پولیس پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "زیادہ سے زیادہ 2 دن"), ("ملتا کیسے ہے", "PDF موقع پر")],
        ["اصل شناختی کارڈ (CNIC)", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)", "میڈیکل سرٹیفکیٹ، صرف اگر عمر 50 سال سے زیادہ ہو"],
        ["طے کریں کہ کون سی کیٹیگری چاہیے، مثلاً موٹر سائیکل، کار یا دونوں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا واٹس ایپ کریں۔",
         "فیسیلیٹیٹر آپ کی لائیو تصویر لے کر درخواست جمع کرواتا ہے۔",
         "PSID پر لکھی فیس ادا کریں۔",
         "لرنر پرمٹ کی PDF موقع پر مل جاتی ہے۔ اسے سنبھال کر رکھیں اور 180 دن کے اندر پکا لائسنس بنوانے کی تیاری کریں۔"],
        [("سرکاری فیس", "Rs 500 فی کیٹیگری"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"), ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"),
         ("کارآمد مدت", "180 دن"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>اہم شرائط</h2><ul><li>کمرشل لائسنس کے لیے عمر 21 سال سے زیادہ ہونی چاہیے۔</li><li>لرنر پرمٹ 180 دن کے لیے کارآمد ہوتا ہے۔ مدت ختم ہو جائے تو لرنر لائسنس رینیو بھی دستک کے ذریعے ہو جاتا ہے۔</li><li>شناختی کارڈ کارآمد ہو اور اس کی تفصیلات درخواست سے میل کھاتی ہوں۔</li></ul></section>',
        related=(R["renew"], R["renew_guide"], R["calc"], R["track"])),
    faqs=[
        ("لرنر لائسنس کیسے بنوائیں؟ (Learner license kaise banaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھ کر بکنگ کریں یا واٹس ایپ 0345-5583530 کریں۔ صرف شناختی کارڈ اور لائیو تصویر چاہیے۔"),
        ("لرنر لائسنس کی فیس کتنی ہے؟", "تربیتی مینول کے مطابق سرکاری فیس 500 روپے فی کیٹیگری ہے، ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے۔ حتمی رقم PSID پر ہوتی ہے۔"),
        ("لرنر پرمٹ کتنے دن چلتا ہے؟", "180 دن۔"),
        ("لرنر لائسنس کتنی دیر میں ملتا ہے؟", "عام طور پر موقع پر ہی PDF مل جاتی ہے، زیادہ سے زیادہ 2 دن۔"),
        ("کیا ٹیسٹ دینا پڑتا ہے؟", "لرنر پرمٹ کے لیے ٹیسٹ نہیں ہوتا۔ پکے لائسنس کے لیے ٹریفک پولیس کے طریقہ کار کے مطابق ٹیسٹ ہوتا ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/character-certificate/", kind="service", en_title="Police Character Certificate",
    title="پولیس کریکٹر سرٹیفکیٹ پنجاب: فیس اور دستاویزات | دستک 90807",
    desc="پنجاب پولیس کریکٹر سرٹیفکیٹ بیرون ملک سفر، نوکری اور امیگریشن کے لیے۔ دستاویزات، سرکاری فیس 1,000 روپے، 3 دن میں کورئیر۔ رجسٹرڈ دستک فیسیلیٹیٹر کوڈ 90807۔",
    h1="پولیس کریکٹر سرٹیفکیٹ (پنجاب پولیس)", og="/assets/og/police.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("پولیس کریکٹر سرٹیفکیٹ", "/ur/services/character-certificate/")],
    body=service_body(
        "پولیس کریکٹر سرٹیفکیٹ",
        "پولیس کریکٹر سرٹیفکیٹ بیرون ملک سفر، باہر نوکری اور امیگریشن کے لیے ضروری ہوتا ہے۔ دستک سروس کے ذریعے پنجاب پولیس کا کریکٹر سرٹیفکیٹ گھر بیٹھے اپلائی ہو جاتا ہے۔ اصل شناختی کارڈ، پاسپورٹ اور لائیو تصویر چاہیے۔ سرکاری فیس 1,000 روپے ہے اور سرٹیفکیٹ تقریباً 3 دن میں کورئیر سے آتا ہے۔",
        [("محکمہ", "پنجاب پولیس"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 3 دن"), ("ڈیلیوری", "کورئیر کے ذریعے")],
        ["اصل شناختی کارڈ (CNIC)", "اصل پاسپورٹ", "سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)",
         "اتھارٹی لیٹر، اگر درخواست گزار بیرون ملک ہو۔ اس پر متعلقہ ایمبیسی کی مہر ہو، ورنہ دو معزز افراد کی تصدیق ہو جو درخواست گزار کو جانتے ہوں۔ لیٹر میں بیرون ملک قیام کی مدت بھی لکھی ہو۔"],
        ["پہلے معلوم کریں کہ آپ کو کریکٹر سرٹیفکیٹ چاہیے یا جنرل پولیس ویری فکیشن۔ دونوں الگ خدمات ہیں۔",
         "اگر سرٹیفکیٹ کسی دوسرے ملک کے لیے ہے تو پاسپورٹ پر اس ملک کا ویزا لگا ہونا چاہیے، ورنہ درخواست آگے نہیں بڑھتی۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا واٹس ایپ کریں۔",
         "فیسیلیٹیٹر آپ کی دستاویزات چیک کر کے لائیو تصویر لیتا ہے اور درخواست جمع کرواتا ہے۔",
         "PSID پر لکھی رقم ادا کریں۔",
         "پنجاب پولیس کی منظوری کے بعد سرٹیفکیٹ تقریباً 3 دن میں کورئیر سے آ جاتا ہے۔"],
        [("سرکاری فیس", "Rs 1,000"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"), ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"),
         ("ادائیگی", "PSID کے ذریعے"), ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>بیرون ملک موجود افراد کے لیے</h2><p>اگر درخواست گزار بیرون ملک ہے تو اس کا کوئی خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ اتھارٹی لیٹر پر ایمبیسی کی مہر ہو یا دو معزز افراد کی تصدیق۔ لیٹر بھیجنے سے پہلے واٹس ایپ پر چیک کروا لیں تاکہ درخواست مسترد نہ ہو۔</p></section>',
        related=(R["character_guide"], R["gk"], R["contact"])),
    faqs=[
        ("کریکٹر سرٹیفکیٹ کیسے بنوائیں؟ (Character certificate kaise banwaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ شناختی کارڈ، پاسپورٹ اور لائیو تصویر چاہیے۔"),
        ("پولیس کریکٹر سرٹیفکیٹ کی فیس کتنی ہے؟", "تربیتی مینول کے مطابق سرکاری فیس 1,000 روپے، دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے۔ حتمی رقم PSID پر ہوتی ہے۔"),
        ("کریکٹر سرٹیفکیٹ کتنے دن میں ملتا ہے؟", "عام طور پر تقریباً 3 دن، پنجاب پولیس کی منظوری کے بعد کورئیر سے۔"),
        ("کیا ویزا ضروری ہے؟", "اگر سرٹیفکیٹ کسی دوسرے ملک کے لیے چاہیے تو پاسپورٹ پر ویزا لگا ہونا ضروری ہے۔"),
        ("کریکٹر سرٹیفکیٹ اور جنرل پولیس ویری فکیشن میں کیا فرق ہے؟", "یہ دو الگ خدمات ہیں۔ جس ادارے کو دستاویز چاہیے اس سے پوچھ لیں کہ اسے کون سی سروس چاہیے۔"),
        ("کیا فیسیلیٹیٹر سرٹیفکیٹ منظور کرتا ہے؟", "نہیں۔ فیسیلیٹیٹر صرف درخواست تیار اور جمع کرواتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔"),
    ]))

PAGES.append(dict(
    path="/services/transfer-of-motor-vehicle/", kind="service", en_title="Transfer of Motor Vehicle",
    title="گاڑی اور موٹر سائیکل ٹرانسفر پنجاب: طریقہ اور فیس | دستک 90807",
    desc="پنجاب میں گاڑی یا موٹر سائیکل اپنے نام ٹرانسفر کروانے کا طریقہ: دستاویزات، خریدار اور بیچنے والے کی بائیومیٹرک، PSID فیس اور 10 دن میں کورئیر۔ دستک کوڈ 90807۔",
    h1="گاڑی اور موٹر سائیکل کی ملکیت ٹرانسفر", og="/assets/og/vehicles.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("گاڑی ٹرانسفر", "/ur/services/transfer-of-motor-vehicle/")],
    body=service_body(
        "گاڑی ٹرانسفر",
        "پنجاب میں رجسٹرڈ گاڑی یا موٹر سائیکل کی ملکیت نئے مالک کے نام کروانے کے لیے گاڑی کا نمبر، خریدار کا اصل شناختی کارڈ اور گاڑی کی اصل فائل اور بُک یا کارڈ چاہیے۔ خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق لازمی ہے۔ سرکاری فیس گاڑی کی قسم کے مطابق PSID پر بنتی ہے، اور نیا رجسٹریشن کارڈ تقریباً 10 دن میں کورئیر سے آتا ہے۔",
        [("محکمہ", "ایکسائز، ٹیکسیشن اینڈ نارکوٹکس کنٹرول، پنجاب"), ("علاقہ", "پورا پنجاب (گھر پر وزٹ: گوجرخان اور راولپنڈی)"), ("وقت", "تقریباً 10 دن"), ("ڈیلیوری", "کورئیر کے ذریعے کارڈ")],
        ["گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر", "خریدار کا اصل شناختی کارڈ (CNIC)", "گاڑی کی اصل فائل اور رجسٹریشن بُک یا اسمارٹ کارڈ",
         "خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق"],
        ["گاڑی کا نمبر اور کارڈ یا بُک کی تصویر واٹس ایپ پر بھیجیں تاکہ واجب الادا ٹوکن ٹیکس اور دیگر تفصیلات چیک ہو جائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا کال کریں۔",
         "فیسیلیٹیٹر درخواست جمع کرواتا ہے اور سرکاری PSID بنتا ہے۔",
         "PSID پر لکھی سرکاری فیس بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے ادا کریں۔",
         "خریدار اور بیچنے والا دونوں بائیومیٹرک تصدیق مکمل کریں۔",
         "تقریباً 10 دن میں نیا رجسٹریشن کارڈ کورئیر سے آ جاتا ہے۔"],
        [("سرکاری فیس", "گاڑی کی قسم اور انجن (سی سی) کے مطابق، PSID پر لکھی ہوتی ہے"), ("دستک فیسیلیٹیٹر چارجز", "Rs 950"),
         ("پلیٹ فارم چارجز", "Rs 19 (تربیتی مینول کے مطابق)"), ("فیس کا اندازہ", '<a href="/ur/calculators/">کار اور موٹر سائیکل فیس کیلکولیٹر</a> (صرف اندازہ)'),
         ("حتمی رقم", "آپ کے PSID پر لکھی ہوتی ہے")],
        extra='<section class="service-module"><h2>درخواست مسترد ہونے سے کیسے بچیں؟</h2><ul><li>گاڑی کا نمبر رجسٹریشن کے کاغذات سے بالکل ملتا ہو۔</li><li>خریدار کا شناختی کارڈ کارآمد اور واضح ہو۔</li><li>خریدار اور بیچنے والا دونوں بائیومیٹرک کے لیے دستیاب ہوں۔</li><li>پچھلا ٹوکن ٹیکس پہلے سے چیک کر لیں۔</li></ul></section>',
        related=(R["vehicle_guide"], R["token"], R["calc"])),
    faqs=[
        ("گاڑی ٹرانسفر کیسے کروائیں؟ (Gari transfer kaise karwayen)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ گاڑی کا نمبر، خریدار کا شناختی کارڈ اور فائل اور بُک یا کارڈ تیار رکھیں۔"),
        ("گاڑی ٹرانسفر فیس پنجاب کتنی ہے؟", "سرکاری فیس گاڑی کی قسم کے مطابق مختلف ہوتی ہے اور PSID پر لکھی ہوتی ہے۔ اس کے ساتھ دستک فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں۔ اندازے کے لیے فیس کیلکولیٹر دیکھیں۔"),
        ("موٹر سائیکل ٹرانسفر کیسے ہوتی ہے؟ (Bike transfer kaise karein)", "طریقہ گاڑی جیسا ہی ہے: بائیک کا نمبر، خریدار کا شناختی کارڈ، اصل فائل اور کارڈ، اور دونوں فریقوں کی بائیومیٹرک۔"),
        ("کیا بیچنے والے کی بائیومیٹرک ضروری ہے؟", "جی ہاں، خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق لازمی ہے۔"),
        ("نیا کارڈ کتنے دن میں آتا ہے؟", "عام طور پر تقریباً 10 دن میں کورئیر سے۔ ڈیلیوری کا وقت مختلف ہو سکتا ہے۔"),
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
        ("گاڑی ٹرانسفر سے پہلے ٹوکن ٹیکس ضروری ہے؟", "ٹرانسفر سے پہلے واجب الادا ٹوکن ٹیکس چیک کر لیں۔ ہم دونوں کام ساتھ کروا دیتے ہیں۔"),
    ]))

PAGES.append(dict(
    path="/services/domicile-certificate/", kind="service", en_title="Domicile Certificate", areas=("Gujar Khan", "Rawalpindi"),
    title="ڈومیسائل کیسے بنوائیں؟ فیس 1,200 روپے، گوجرخان | دستک 90807",
    desc="گوجرخان اور راولپنڈی میں ڈومیسائل سرٹیفکیٹ: دستاویزات کی مکمل فہرست، فیس 1,200 روپے بذریعہ PSID، 300 روپے کا بیان حلفی الگ۔ گھر پر سہولت، دستک کوڈ 90807۔",
    h1="ڈومیسائل سرٹیفکیٹ، گوجرخان اور راولپنڈی", og="/assets/og/civil.jpg",
    crumbs=[("خدمات", "/ur/services/"), ("ڈومیسائل سرٹیفکیٹ", "/ur/services/domicile-certificate/")],
    body=service_body(
        "ڈومیسائل سرٹیفکیٹ",
        "ڈومیسائل یہ ثابت کرتا ہے کہ آپ کس ضلع کے رہائشی ہیں۔ یہ سرکاری نوکری، تعلیمی کوٹے اور کئی دفتری کاموں میں چاہیے ہوتا ہے۔ دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے جو PSID سے ادا ہوتی ہے۔ 300 روپے کا بیان حلفی (ای اسٹامپ) الگ سے چاہیے۔ دستاویزات تحصیل (اسسٹنٹ کمشنر) دفتر میں جمع ہوتی ہیں اور تیار ڈومیسائل فیسیلیٹیٹر آپ تک پہنچاتا ہے۔",
        [("محکمہ", "بورڈ آف ریونیو، پنجاب"), ("علاقہ", "گوجرخان، راولپنڈی اور قریبی علاقے"), ("وقت", "15 دن تک"), ("ملتا کیسے ہے", "اسسٹنٹ کمشنر دفتر سے لے کر گھر پر")],
        ["درخواست فارم P-1 (تصدیق شدہ)", "درخواست گزار کی تازہ تصویر (تصدیق شدہ)", "درخواست گزار کا شناختی کارڈ یا ب فارم (اصل، کاپی اور تصدیق)",
         "والد، والدہ یا شوہر کا شناختی کارڈ (اصل، کاپی اور تصدیق)", "300 روپے کا بیان حلفی (ای اسٹامپ)", "تازہ ترین تعلیمی سرٹیفکیٹ (تصدیق شدہ)",
         "یوٹیلیٹی بل (اصل، کاپی اور تصدیق)"],
        ["واٹس ایپ پر اپنی دستاویزات کی تصاویر بھیجیں تاکہ کمی پہلے ہی پوری ہو جائے۔",
         "یقینی بنائیں کہ آپ کا موجودہ اور مستقل پتہ ایک ہی ضلع کا ہو۔",
         "300 روپے کا بیان حلفی (ای اسٹامپ) تیار کریں، یا یہ بھی دستک کے ذریعے بنوائیں۔",
         "دستک ایپ میں بکنگ کریں (Doorstep Delivery، کوڈ 90807) یا کال کریں۔",
         "PSID پر لکھی 1,200 روپے کی رقم ادا کریں۔",
         "فیسیلیٹیٹر دستاویزات اسسٹنٹ کمشنر (تحصیل) دفتر میں جمع کرواتا ہے اور منظوری کے بعد ڈومیسائل آپ تک پہنچاتا ہے۔"],
        [("ڈومیسائل (دستک سروس)", "<b>کل Rs 1,200</b>، PSID کے ذریعے"), ("بیان حلفی (ای اسٹامپ)", "Rs 300 کا ای اسٹامپ الگ سے درکار ہے"),
         ("ای اسٹامپ دستک کے ذریعے", "کل Rs 1,250 (Rs 300 ای اسٹامپ + Rs 950 فیسیلیٹیٹر چارجز)"), ("وقت", "15 دن تک، محکمے کی منظوری پر منحصر")],
        extra='<section class="service-module"><h2>ڈومیسائل کی دیگر خدمات</h2><p>ہم ڈومیسائل سے متعلق یہ کام بھی کرواتے ہیں (تفصیل انگریزی صفحات پر):</p><ul><li><a href="/en/services/duplicate-domicile/" lang="en">Duplicate Domicile</a>: ڈومیسائل گم یا خراب ہو جائے تو ڈپلیکیٹ</li><li><a href="/en/services/modification-domicile/" lang="en">Modification of Domicile</a>: ڈومیسائل میں درستگی</li><li><a href="/en/services/noc-for-domicile-transfer/" lang="en">NOC for Domicile Transfer</a>: ڈومیسائل دوسرے ضلع منتقل کرنے کا این او سی</li></ul></section>',
        related=(R["gk"], R["contact"])),
    faqs=[
        ("ڈومیسائل کیسے بنوائیں؟ (Domicile kaise banaye)", "دستک ایپ میں Doorstep Delivery کے ساتھ کوڈ 90807 لکھیں یا واٹس ایپ 0345-5583530 کریں۔ اوپر دی گئی دستاویزات تیار رکھیں۔ فیسیلیٹیٹر انہیں تحصیل دفتر میں جمع کرواتا ہے۔"),
        ("ڈومیسائل کی فیس کتنی ہے؟", "دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے جو PSID سے ادا ہوتی ہے۔ 300 روپے کا بیان حلفی (ای اسٹامپ) الگ سے چاہیے۔"),
        ("کیا ای اسٹامپ بھی آپ بنوا دیتے ہیں؟", "جی ہاں۔ دستک کے ذریعے 300 روپے کا ای اسٹامپ بنوانے کی کل رقم 1,250 روپے ہے۔"),
        ("ڈومیسائل کتنے دن میں بنتا ہے؟", "15 دن تک، محکمے کی منظوری پر منحصر۔"),
        ("کیا دوسرے ضلع کا پتہ چل سکتا ہے؟", "نہیں۔ موجودہ اور مستقل پتہ ایک ہی ضلع کا ہونا چاہیے۔ ضلع بدلنا ہو تو ڈومیسائل ٹرانسفر کا این او سی لیں۔"),
        ("Domicile kahan jama hota hai?", "دستاویزات متعلقہ تحصیل یعنی اسسٹنٹ کمشنر دفتر میں جمع ہوتی ہیں۔ یہ کام فیسیلیٹیٹر خود کرتا ہے۔"),
    ]))

# ================================================================ GUIDES
PAGES.append(dict(
    path="/guides/punjab-driving-license-renewal-online/", kind="guide", main_class="service-detail page-shell", en_title="Punjab Driving License Renewal Online",
    title="ڈرائیونگ لائسنس رینیول آن لائن پنجاب: مکمل طریقہ | دستک 90807",
    desc="پنجاب میں ڈرائیونگ لائسنس آن لائن رینیو کرنے کا مکمل طریقہ: تیاری، دستاویزات، فیس، PSID، ٹریکنگ اور عام غلطیاں۔ پورے پنجاب میں واٹس ایپ رہنمائی، دستک کوڈ 90807۔",
    h1="پنجاب میں ڈرائیونگ لائسنس آن لائن رینیول کا مکمل طریقہ", eyebrow='<p class="eyebrow">ڈرائیونگ لائسنس گائیڈ</p>',
    og="/assets/punjab-driving-license-renewal-guide-dastak-90807-og.jpg",
    og_alt="پنجاب ڈرائیونگ لائسنس رینیول گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
    crumbs=[("گائیڈز", "/ur/guides/"), ("لائسنس رینیول گائیڈ", "/ur/guides/punjab-driving-license-renewal-online/")],
    body=guide_body(
        "پنجاب میں ڈرائیونگ لائسنس رینیو کروانے کے لیے اصل شناختی کارڈ، پرانا لائسنس اور سفید بیک گراؤنڈ والی تازہ تصویر چاہیے (50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفکیٹ بھی)۔ دستک سروس کے ذریعے درخواست جمع ہوتی ہے، PSID پر سرکاری فیس ادا ہوتی ہے اور نیا لائسنس تقریباً 10 دن میں کورئیر سے گھر آ جاتا ہے۔ لائسنس 1 سے 5 سال کے لیے بن سکتا ہے۔",
        [
            ("رینیول سے پہلے کیا تیاری کریں؟", "<ul><li>اصل شناختی کارڈ، جس کی مدت ختم نہ ہوئی ہو۔</li><li>پرانا ڈرائیونگ لائسنس، چاہے اس کی مدت ختم ہو چکی ہو۔</li><li>سفید بیک گراؤنڈ والی لائیو تصویر، جو فیسیلیٹیٹر موقع پر لیتا ہے۔</li><li>50 سال سے زیادہ عمر ہو تو میڈیکل سرٹیفکیٹ۔</li><li>لائسنس گم ہو گیا ہو تو ایف آئی آر یا لاسٹ رپورٹ کی کاپی۔</li><li>ایک فعال موبائل نمبر، کیونکہ ڈیلیوری والا رابطہ کر سکتا ہے۔</li></ul>"),
            ("آن لائن رینیول کیسے ہوتا ہے؟", f"<ol><li>دستک ایپ میں Doorstep Delivery منتخب کریں اور کوڈ {CODE} لکھیں، یا واٹس ایپ {PHONE} کریں۔</li><li>فیسیلیٹیٹر آپ کی کیٹیگری اور اہلیت چیک کرتا ہے۔</li><li>آپ لائسنس کی مدت (1 سے 5 سال) منتخب کرتے ہیں۔</li><li>لائیو تصویر اور دستاویزات کے ساتھ درخواست جمع ہوتی ہے اور PSID بنتا ہے۔</li><li>آپ PSID کی ادائیگی موبائل بینکنگ، جاز کیش یا ایزی پیسہ سے کرتے ہیں۔</li><li>تقریباً 10 دن میں لائسنس کورئیر سے آپ کے پتے پر پہنچ جاتا ہے۔</li></ol><p>کچھ کیٹیگریز یا بہت پرانے ختم شدہ لائسنس کے لیے لائسنسنگ سینٹر جانا پڑ سکتا ہے۔ بکنگ سے پہلے واٹس ایپ پر اپنی صورتحال چیک کروا لیں۔</p>"),
            ("رینیول پر کتنا خرچ آتا ہے؟", RENEW_FEE_TABLE + '<p>سرکاری فیس لائسنس کی کیٹیگری، مدت اور مدت ختم ہونے کی تاریخ کے حساب سے بنتی ہے، اور حتمی رقم PSID پر لکھی ہوتی ہے۔ دستک تربیتی مینول کے مطابق فیسیلیٹیٹر چارجز 950 روپے اور پلیٹ فارم چارجز 19 روپے ہیں۔ اندازے کے لیے ہمارا <a href="/en/calculators/tools/punjab-driving-license-fee-calculator">ڈرائیونگ لائسنس فیس کیلکولیٹر</a> استعمال کریں۔</p>'),
            ("لائسنس کا اسٹیٹس کیسے دیکھیں؟", '<p>درخواست کے بعد DLIMS پر شناختی کارڈ نمبر سے پرنٹنگ اور ڈسپیچ کا اسٹیٹس دیکھیں، پھر پاکستان پوسٹ پر ٹریکنگ آئی ڈی سے ڈیلیوری ٹریک کریں۔ مکمل طریقہ: <a href="/ur/guides/how-to-track-driving-license-in-punjab/">ڈرائیونگ لائسنس ٹریک کرنے کا طریقہ</a>۔</p>'),
            ("عام غلطیاں جن سے درخواست رکتی ہے", "<ul><li>شناختی کارڈ کی مدت ختم ہونا۔</li><li>تصویر کا بیک گراؤنڈ سفید نہ ہونا۔</li><li>50 سال سے زیادہ عمر میں میڈیکل سرٹیفکیٹ نہ لگانا۔</li><li>گمشدہ لائسنس کی ایف آئی آر کے بغیر درخواست دینا۔</li><li>غلط یا بند موبائل نمبر دینا۔</li></ul>"),
            ("مدد کہاں سے ملے گی؟", f"<p><b>پورے پنجاب میں:</b> واٹس ایپ {PHONE} پر رہنمائی اور دستاویزات کی جانچ۔</p><p><b>گوجرخان اور راولپنڈی:</b> {AREAS} میں گھر پر وزٹ، پہلے سے وقت طے کر کے۔</p><p>دستک 90807 ایک آزاد رجسٹرڈ فیسیلیٹیٹر ہے، سرکاری دفتر نہیں۔ منظوری اور ڈیلیوری لائسنسنگ اتھارٹی کے اختیار میں ہے۔</p>"),
        ],
        hero=("/assets/punjab-driving-license-renewal-guide-dastak-90807.webp", "پنجاب ڈرائیونگ لائسنس رینیول گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["renew"], R["track"], R["learner"])),
    faqs=[
        ("کیا میں گوجرخان سے باہر رہ کر بھی لائسنس رینیو کروا سکتا ہوں؟", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ ہوتی ہے۔ گھر پر وزٹ صرف گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
        ("کیا کیلکولیٹر کی فیس حتمی ہوتی ہے؟", "نہیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔ حتمی رقم سرکاری سسٹم کے PSID پر ہوتی ہے۔"),
        ("Expired license renew ho sakta hai?", "جی ہاں، عام طور پر ختم شدہ لائسنس بھی رینیو ہو جاتا ہے، مگر بہت پرانے لائسنس یا کچھ کیٹیگریز کے لیے سینٹر جانا پڑ سکتا ہے۔ پہلے واٹس ایپ پر چیک کروا لیں۔"),
        ("رینیو شدہ لائسنس کتنے دن میں ملتا ہے؟", "تربیتی مینول کے مطابق تقریباً 10 دن، کورئیر سے۔"),
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
            ("ای لائسنس کیسے ڈاؤن لوڈ کریں؟", '<p>منظوری کے بعد سرکاری <a href="https://dlims.punjab.gov.pk/elicense" rel="noopener">DLIMS ای لائسنس صفحے</a> سے ڈیجیٹل لائسنس دیکھا جا سکتا ہے۔ ڈیجیٹل ریکارڈ اور فزیکل کارڈ کی ڈیلیوری دو الگ مرحلے ہیں۔</p>'),
            ("لائسنس آنے میں دیر کیوں ہوتی ہے؟", "<ul><li>درخواست کی تصدیق ابھی جاری ہو۔</li><li>پرنٹنگ میں رش ہو۔</li><li>پتہ نامکمل یا غلط ہو۔</li><li>موبائل نمبر بند ہونے سے ڈاکیا رابطہ نہ کر سکے۔</li></ul><p>اسٹیٹس کئی دن تک نہ بدلے تو واٹس ایپ پر اپنی درخواست کی تفصیل بھیجیں، ہم رہنمائی کر دیں گے۔</p>"),
            ("رینیول یا نئے لائسنس میں مدد", '<p>اگر ابھی درخواست دینی ہے تو <a href="/ur/services/renewal-of-regular-license/">لائسنس رینیول</a> یا <a href="/ur/services/learner-driving-license/">لرنر لائسنس</a> کا صفحہ دیکھیں۔</p>'),
        ],
        hero=("/assets/track-driving-license-punjab-dastak-90807.webp", "پنجاب ڈرائیونگ لائسنس ٹریکنگ گائیڈ، DLIMS اور پاکستان پوسٹ، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["renew_guide"], R["renew"], R["learner"])),
    faqs=[
        ("لائسنس کا اسٹیٹس کیسے چیک کریں؟ (License status check kaise karein)", "سرکاری DLIMS ٹریکنگ صفحے پر اپنا 13 ہندسوں کا شناختی کارڈ نمبر لکھ کر اسٹیٹس دیکھیں۔"),
        ("Dispatched کا کیا مطلب ہے؟", "اس کا مطلب ہے کہ کارڈ ڈاک کے حوالے ہو گیا ہے۔ اب پاکستان پوسٹ پر ٹریکنگ آئی ڈی سے ڈیلیوری دیکھیں۔"),
        ("ٹریکنگ آئی ڈی کہاں ملتی ہے؟", "اسٹیٹس Dispatched ہونے پر DLIMS کے نتیجے میں ٹریکنگ یا کنسائنمنٹ نمبر نظر آتا ہے۔"),
        ("کیا دستک 90807 سرکاری ٹریکنگ ویب سائٹ ہے؟", "نہیں۔ ہم آزاد فیسیلیٹیٹر ہیں اور صرف رہنمائی کرتے ہیں۔ ٹریکنگ سرکاری DLIMS اور پاکستان پوسٹ کی ویب سائٹس پر ہوتی ہے۔"),
    ]))

PAGES.append(dict(
    path="/guides/punjab-police-character-certificate-online/", kind="guide", main_class="service-detail page-shell", en_title="Punjab Police Character Certificate",
    title="پولیس کریکٹر سرٹیفکیٹ کیسے بنوائیں؟ مکمل گائیڈ | دستک 90807",
    desc="پنجاب پولیس کریکٹر سرٹیفکیٹ کب چاہیے، کون سی دستاویزات، فیس، بیرون ملک سے اپلائی کرنے کا طریقہ اور سرٹیفکیٹ کی تصدیق۔ پورے پنجاب میں مدد، دستک کوڈ 90807۔",
    h1="پنجاب پولیس کریکٹر سرٹیفکیٹ: مکمل گائیڈ", eyebrow='<p class="eyebrow">پولیس دستاویزات گائیڈ</p>',
    og="/assets/punjab-police-character-certificate-guide-dastak-90807-og.jpg",
    og_alt="پنجاب پولیس کریکٹر سرٹیفکیٹ گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)",
    crumbs=[("گائیڈز", "/ur/guides/"), ("کریکٹر سرٹیفکیٹ گائیڈ", "/ur/guides/punjab-police-character-certificate-online/")],
    body=guide_body(
        "پنجاب پولیس کریکٹر سرٹیفکیٹ کے لیے اصل شناختی کارڈ، پاسپورٹ اور سفید بیک گراؤنڈ والی لائیو تصویر چاہیے۔ اگر سرٹیفکیٹ کسی دوسرے ملک کے لیے ہے تو پاسپورٹ پر ویزا ضروری ہے۔ دستک تربیتی مینول کے مطابق سرکاری فیس 1,000 روپے ہے اور سرٹیفکیٹ تقریباً 3 دن میں کورئیر سے آتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔",
        [
            ("کریکٹر سرٹیفکیٹ کب چاہیے ہوتا ہے؟", "<p>بیرون ملک سفر، باہر کی کمپنیوں میں نوکری، امیگریشن اور کئی ویزا درخواستوں کے لیے۔ جس ادارے نے سرٹیفکیٹ مانگا ہے اس سے پوچھ لیں کہ اسے کریکٹر سرٹیفکیٹ چاہیے یا جنرل پولیس ویری فکیشن، کیونکہ یہ دو الگ خدمات ہیں۔</p>"),
            ("کون سی دستاویزات چاہئیں؟", "<ul><li>اصل شناختی کارڈ (CNIC)</li><li>اصل پاسپورٹ، اور دوسرے ملک کے لیے ہو تو اس پر ویزا</li><li>سفید بیک گراؤنڈ کے ساتھ لائیو تصویر (کندھوں تک)</li><li>بیرون ملک موجود درخواست گزار کے لیے اتھارٹی لیٹر</li></ul>"),
            ("فیس اور وقت", '<table class="ur-fee"><tbody><tr><th scope="row">سرکاری فیس</th><td>Rs 1,000</td></tr><tr><th scope="row">دستک فیسیلیٹیٹر چارجز</th><td>Rs 950</td></tr><tr><th scope="row">پلیٹ فارم چارجز</th><td>Rs 19</td></tr><tr><th scope="row">وقت</th><td>تقریباً 3 دن، کورئیر سے</td></tr></tbody></table><p class="ur-note">' + FEE_SOURCE + '</p>'),
            ("بیرون ملک سے کیسے اپلائی کریں؟", "<p>درخواست گزار بیرون ملک ہو تو اس کا خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ لیٹر پر متعلقہ ایمبیسی کی مہر ہو، ورنہ دو معزز افراد کی تصدیق ہو جو درخواست گزار کو جانتے ہوں۔ لیٹر میں بیرون ملک قیام کی مدت ضرور لکھیں۔ بھیجنے سے پہلے واٹس ایپ پر چیک کروا لیں۔</p>"),
            ("سرٹیفکیٹ کی تصدیق کیسے کریں؟", '<p>جاری شدہ سرٹیفکیٹ سرکاری <a href="https://pkm.punjab.gov.pk/public/app/verification" rel="noopener">پنجاب پولیس ویری فکیشن صفحے</a> پر چیک کیا جا سکتا ہے۔ تفصیل نہ ملے تو جاری کرنے والے دفتر سے رابطہ کریں۔</p>'),
            ("ہم کہاں مدد کرتے ہیں؟", f"<p>پورے پنجاب کے لیے واٹس ایپ پر دستاویزات کی جانچ اور رہنمائی۔ {AREAS} میں گھر پر وزٹ، پہلے سے وقت طے کر کے۔</p>"),
        ],
        hero=("/assets/punjab-police-character-certificate-guide-dastak-90807.webp", "پنجاب پولیس کریکٹر سرٹیفکیٹ گائیڈ، گوجرخان اور راولپنڈی، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)"),
        related=(R["character"], R["gk"], R["contact"])),
    faqs=[
        ("کیا کریکٹر سرٹیفکیٹ اور جنرل پولیس ویری فکیشن ایک ہی ہیں؟", "نہیں، دونوں الگ خدمات ہیں۔ جس ادارے کو دستاویز چاہیے اس سے پوچھ لیں۔"),
        ("کیا آپ گوجرخان سے باہر بھی مدد کرتے ہیں؟", "جی ہاں۔ پورے پنجاب کے لیے واٹس ایپ پر دستاویزات کی جانچ اور رہنمائی ہوتی ہے۔ گھر پر وزٹ گوجرخان، راولپنڈی اور قریبی علاقوں میں ہوتا ہے۔"),
        ("Bahar se character certificate kaise banwayen?", "خونی رشتہ دار اتھارٹی لیٹر کے ساتھ درخواست جمع کروا سکتا ہے۔ لیٹر پر ایمبیسی کی مہر یا دو معزز افراد کی تصدیق ہو۔"),
        ("کیا فیسیلیٹیٹر سرٹیفکیٹ منظور کرتا ہے؟", "نہیں۔ فیسیلیٹیٹر درخواست تیار اور جمع کرواتا ہے۔ تصدیق اور منظوری پنجاب پولیس کرتی ہے۔"),
    ]))

PAGES.append(dict(
    path="/guides/vehicle-transfer-token-tax-punjab/", kind="guide", main_class="service-detail page-shell", en_title="Vehicle Transfer and Token Tax in Punjab",
    title="گاڑی ٹرانسفر اور ٹوکن ٹیکس پنجاب: مکمل گائیڈ | دستک 90807",
    desc="پنجاب میں گاڑی اور موٹر سائیکل کی ملکیت ٹرانسفر اور ٹوکن ٹیکس کی مکمل اردو گائیڈ: دستاویزات، بائیومیٹرک، PSID ادائیگی، وقت اور عام سوالات۔ دستک کوڈ 90807۔",
    h1="گاڑی اور موٹر سائیکل ٹرانسفر اور ٹوکن ٹیکس: مکمل گائیڈ", eyebrow='<p class="eyebrow">گاڑی اور ایکسائز گائیڈ</p>',
    og="/assets/og/vehicles.jpg",
    crumbs=[("گائیڈز", "/ur/guides/"), ("ٹرانسفر اور ٹوکن ٹیکس", "/ur/guides/vehicle-transfer-token-tax-punjab/")],
    body=guide_body(
        "پنجاب میں گاڑی یا موٹر سائیکل اپنے نام کروانے کے لیے گاڑی کا نمبر، خریدار کا اصل شناختی کارڈ اور گاڑی کی اصل فائل اور بُک یا کارڈ چاہیے، اور خریدار اور بیچنے والے دونوں کی بائیومیٹرک لازمی ہے۔ ٹوکن ٹیکس کے لیے صرف گاڑی کا نمبر کافی ہے۔ دونوں کاموں میں سرکاری فیس PSID پر بنتی ہے۔",
        [
            ("ٹرانسفر کے لیے دستاویزات", "<ul><li>گاڑی یا موٹر سائیکل کا رجسٹریشن نمبر</li><li>خریدار کا اصل شناختی کارڈ</li><li>گاڑی کی اصل فائل اور رجسٹریشن بُک یا اسمارٹ کارڈ</li><li>خریدار اور بیچنے والے دونوں کی بائیومیٹرک تصدیق</li></ul>"),
            ("ٹرانسفر کا طریقہ، قدم بہ قدم", f"<ol><li><b>کاغذات کی جانچ:</b> کارڈ یا بُک اور شناختی کارڈ کی تصاویر واٹس ایپ {PHONE} پر بھیجیں تاکہ واجب الادا ٹوکن ٹیکس اور تفصیلات چیک ہو جائیں۔</li><li><b>PSID:</b> فیسیلیٹیٹر سرکاری سسٹم میں درخواست جمع کرواتا ہے اور PSID بنتا ہے۔</li><li><b>ادائیگی:</b> PSID کی رقم بینکنگ ایپ، جاز کیش یا ایزی پیسہ سے ادا کریں۔</li><li><b>بائیومیٹرک:</b> خریدار اور بیچنے والا دونوں بائیومیٹرک تصدیق کرواتے ہیں۔</li><li><b>کارڈ:</b> تقریباً 10 دن میں نیا رجسٹریشن کارڈ کورئیر سے آتا ہے۔</li></ol>"),
            ("ٹوکن ٹیکس کیسے جمع کروائیں؟", "<p>گاڑی کا نمبر بھیجیں۔ سرکاری سسٹم سے واجب الادا رقم چیک ہو کر PSID بنتا ہے۔ ادائیگی کے بعد کام عام طور پر موقع پر مکمل ہو جاتا ہے۔ کمرشل گاڑیوں کے لیے 3، 6، 9 ماہ یا 1 سال کی مدت منتخب کی جا سکتی ہے۔</p>"),
            ("فیس کتنی ہے؟", '<table class="ur-fee"><tbody><tr><th scope="row">سرکاری ٹرانسفر فیس / ٹوکن ٹیکس</th><td>گاڑی کی قسم، انجن، ماڈل اور سرکاری پالیسی کے مطابق، PSID پر لکھی ہوتی ہے</td></tr><tr><th scope="row">دستک فیسیلیٹیٹر چارجز</th><td>Rs 950 (ہر سروس)</td></tr><tr><th scope="row">پلیٹ فارم چارجز</th><td>Rs 19</td></tr></tbody></table><p>اندازے کے لیے <a href="/en/calculators/tools/punjab-car-token-tax-transfer-fee-calculator">کار فیس کیلکولیٹر</a> اور <a href="/en/calculators/tools/punjab-bike-registration-transfer-fee-calculator">موٹر سائیکل فیس کیلکولیٹر</a> دیکھیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔</p><p class="ur-note">' + FEE_SOURCE + '</p>'),
            ("درخواست رکنے کی عام وجوہات", "<ul><li>گاڑی کا نمبر کاغذات سے نہ ملنا۔</li><li>شناختی کارڈ کی مدت ختم ہونا۔</li><li>بیچنے والے کا بائیومیٹرک کے لیے دستیاب نہ ہونا۔</li><li>اصل فائل یا کارڈ کا نہ ہونا۔</li></ul>"),
        ],
        hero=None,
        related=(R["transfer"], R["token"], R["calc"])),
    faqs=[
        ("کیا بیچنے والے کی بائیومیٹرک کے بغیر ٹرانسفر ہو سکتی ہے؟", "نہیں، عام طور پر خریدار اور بیچنے والے دونوں کی لائیو بائیومیٹرک لازمی ہے۔"),
        ("گھر بیٹھے ٹوکن ٹیکس کیسے جمع کروائیں؟", "واٹس ایپ 0345-5583530 پر گاڑی کا نمبر بھیجیں۔ ہم سرکاری PSID بنا دیتے ہیں جسے آپ موبائل بینکنگ سے ادا کر سکتے ہیں۔"),
        ("Bike transfer fee kitni hai?", "سرکاری فیس PSID پر لکھی ہوتی ہے اور حکومت کے فیصلوں کے مطابق بدل سکتی ہے۔ دستک فیسیلیٹیٹر چارجز 950 روپے ہیں۔ اندازے کے لیے موٹر سائیکل فیس کیلکولیٹر دیکھیں۔"),
        ("نیا کارڈ کب آتا ہے؟", "عام طور پر تقریباً 10 دن میں کورئیر سے۔"),
    ]))

# ================================================================ HUBS AND LOCAL PAGES
PAGES.append(dict(
    path="/services/", kind="hub", en_title="All services",
    title="دستک خدمات (سروسز): لائسنس، پولیس، گاڑی، ڈومیسائل | دستک 90807",
    desc="پنجاب میں دستک کی گھر بیٹھے خدمات: ڈرائیونگ لائسنس، پولیس کریکٹر سرٹیفکیٹ، گاڑی ٹرانسفر، ٹوکن ٹیکس اور ڈومیسائل۔ رجسٹرڈ فیسیلیٹیٹر کوڈ 90807، واٹس ایپ 0345-5583530۔",
    h1="دستک خدمات: سرکاری خدمات گھر کی دہلیز پر", og="/assets/og/general.jpg",
    crumbs=[("خدمات", "/ur/services/")],
    body=f'''<div class="card quick"><b>مختصر تعارف</b><p>میں محمد عثمان ہوں، مریم کی دستک پروگرام کا رجسٹرڈ فیسیلیٹیٹر (کوڈ {CODE})۔ پورے پنجاب میں واٹس ایپ پر رہنمائی کرتا ہوں اور {AREAS} میں گھر آ کر سرکاری دستاویزات کا کام کرواتا ہوں۔ ہر سروس پر دستک فیسیلیٹیٹر چارجز 950 روپے ہیں، اور سرکاری فیس PSID پر لکھی ہوتی ہے۔</p></div>
<section class="service-module"><h2>ڈرائیونگ لائسنس</h2>{cards((R["renew"], R["learner"], R["track"]))}</section>
<section class="service-module"><h2>پولیس خدمات</h2>{cards((R["character"], ("/en/services/general-police-verification/", "جنرل پولیس ویری فکیشن (English)", "نوکری اور ویزا کے لیے پس منظر کی تصدیق"), ("/en/services/tenant-registration/", "کرایہ دار رجسٹریشن (English)", "مکان کرائے پر دینے والوں کے لیے"), ("/en/services/loss-report/", "گمشدگی رپورٹ (English)", "کاغذات گم ہونے کی رپورٹ")))}</section>
<section class="service-module"><h2>گاڑی اور ایکسائز</h2>{cards((R["transfer"], R["token"], ("/en/services/motor-vehicle-registration/", "نئی گاڑی کی رجسٹریشن (English)", "نئی گاڑی یا بائیک رجسٹر کروائیں")))}</section>
<section class="service-module"><h2>ڈومیسائل اور سول سرٹیفکیٹس</h2>{cards((R["domicile"], ("/en/services/birth-certificate/", "پیدائش سرٹیفکیٹ (English)", "یونین کونسل سے پیدائش کا اندراج"), ("/en/services/marriage-certificate/", "نکاح نامہ سرٹیفکیٹ (English)", "شادی کا کمپیوٹرائزڈ سرٹیفکیٹ"), ("/en/services/e-stamping/", "ای اسٹامپ پیپر (English)", "بیان حلفی اور دیگر اسٹامپ پیپر")))}</section>
<p class="ur-note">جن خدمات کے ساتھ (English) لکھا ہے ان کی تفصیل ابھی انگریزی میں ہے۔ اردو صفحات جلد آ رہے ہیں۔ <a href="/en/services/" lang="en">All services in English</a></p>
{booking_block("دستک سروس")}''',
    faqs=[
        ("دستک سروس کیا ہے؟", "مریم کی دستک حکومتِ پنجاب کا پروگرام ہے جس میں رجسٹرڈ فیسیلیٹیٹر گھر آ کر سرکاری دستاویزات کا کام کرواتا ہے۔ دستک 90807 ایک آزاد رجسٹرڈ فیسیلیٹیٹر کی سروس ہے۔"),
        ("فیسیلیٹیٹر چارجز کتنے ہیں؟", "دستک تربیتی مینول کے مطابق ہر سروس پر فیسیلیٹیٹر چارجز 950 روپے ہیں۔ سرکاری فیس الگ ہے اور PSID پر لکھی ہوتی ہے۔"),
        ("بکنگ کیسے کریں؟", "دستک ایپ میں Doorstep Delivery منتخب کر کے کوڈ 90807 لکھیں، یا واٹس ایپ 0345-5583530 کریں۔"),
    ]))

PAGES.append(dict(
    path="/guides/", kind="hub", en_title="Guides & Updates",
    title="اردو گائیڈز: لائسنس، کریکٹر سرٹیفکیٹ، گاڑی ٹرانسفر | دستک 90807",
    desc="پنجاب کی سرکاری دستاویزات پر آسان اردو گائیڈز: ڈرائیونگ لائسنس رینیول، لائسنس ٹریکنگ، پولیس کریکٹر سرٹیفکیٹ، گاڑی ٹرانسفر اور ٹوکن ٹیکس۔ دستک کوڈ 90807۔",
    h1="اردو گائیڈز: سرکاری دستاویزات آسان زبان میں", og="/assets/og/general.jpg",
    crumbs=[("گائیڈز", "/ur/guides/")],
    body=f'''<div class="card quick"><b>ان گائیڈز میں کیا ہے؟</b><p>ہر گائیڈ میں دستاویزات کی فہرست، قدم بہ قدم طریقہ، فیس کی معلومات اور عام سوالات آسان اردو میں ہیں۔ فیس کی معلومات صرف سرکاری دستک تربیتی مینول اور سرکاری پورٹل سے لی گئی ہیں۔</p></div>
{cards((R["renew_guide"], R["track"], R["character_guide"], R["vehicle_guide"]))}
<p class="ur-note">مزید گائیڈز انگریزی میں: <a href="/en/guides/" lang="en">Guides &amp; Updates</a></p>''',
    faqs=[]))

PAGES.append(dict(
    path="/calculators/", kind="hub", en_title="Fee Calculators",
    title="فیس کیلکولیٹر پنجاب: لائسنس، کار، موٹر سائیکل | دستک 90807",
    desc="پنجاب ڈرائیونگ لائسنس، کار اور موٹر سائیکل ٹرانسفر اور ٹوکن ٹیکس کی فیس کا اندازہ لگائیں۔ دستک فیسیلیٹیٹر چارجز 950 روپے شامل۔ حتمی رقم PSID پر۔ دستک کوڈ 90807۔",
    h1="فیس کیلکولیٹر: لائسنس، کار اور موٹر سائیکل", og="/assets/og/general.jpg",
    crumbs=[("فیس کیلکولیٹر", "/ur/calculators/")],
    body=f'''<div class="card quick"><b>اہم بات</b><p>یہ کیلکولیٹر صرف <b>اندازہ</b> دیتے ہیں۔ سرکاری فیس حکومت کے فیصلوں کے مطابق بدل سکتی ہے، اور حتمی رقم ہمیشہ سرکاری سسٹم کے PSID پر لکھی ہوتی ہے۔ گاڑی اور موٹر سائیکل کیلکولیٹر میں دستک فیسیلیٹیٹر چارجز 950 روپے شامل ہیں۔ کیلکولیٹرز میں اردو اور انگریزی دونوں زبانیں ہیں۔</p></div>
{cards((("/en/calculators/tools/punjab-driving-license-fee-calculator", "ڈرائیونگ لائسنس فیس کیلکولیٹر", "رینیول کی فیس، 1 سے 5 سال کی مدت کے مطابق"), ("/en/calculators/tools/punjab-car-token-tax-transfer-fee-calculator", "کار ٹرانسفر اور ٹوکن ٹیکس کیلکولیٹر", "کار کی ٹرانسفر فیس اور ٹوکن ٹیکس کا اندازہ"), ("/en/calculators/tools/punjab-bike-registration-transfer-fee-calculator", "موٹر سائیکل رجسٹریشن اور ٹرانسفر کیلکولیٹر", "بائیک اور ای بائیک کی فیس کا اندازہ")))}
<section class="service-module"><h2>متعلقہ خدمات</h2>{cards((R["renew"], R["transfer"], R["token"]))}</section>''',
    faqs=[
        ("کیا کیلکولیٹر کی فیس حتمی ہے؟", "نہیں۔ کیلکولیٹر صرف اندازہ دیتا ہے۔ حتمی رقم سرکاری PSID پر ہوتی ہے۔"),
        ("کیا فیسیلیٹیٹر چارجز شامل ہیں؟", "گاڑی اور موٹر سائیکل کیلکولیٹر میں دستک فیسیلیٹیٹر چارجز 950 روپے شامل ہیں۔"),
    ]))

PAGES.append(dict(
    path="/gujar-khan/", kind="service", en_title="Gujar Khan", areas=("Gujar Khan", "Kallar Syedan", "Kahuta", "Mandra", "Bewal", "Daultala", "Jatli", "Sukho", "Qazian", "Rawalpindi"),
    title="گوجرخان میں دستک سروس: گھر بیٹھے سرکاری دستاویزات | دستک 90807",
    desc="گوجرخان، کلر سیداں، مندرہ، جاتلی، دولتالہ، بیول اور قریبی علاقوں میں ڈومیسائل، ڈرائیونگ لائسنس، پولیس سرٹیفکیٹ اور گاڑی خدمات گھر پر۔ دستک کوڈ 90807۔",
    h1="گوجرخان میں دستک سروس: گھر بیٹھے سرکاری دستاویزات", og="/assets/og/general.jpg",
    og_alt="گوجرخان میں دستک سروس، دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، سینڈل روڈ، گوجرخان",
    crumbs=[("گوجرخان", "/ur/gujar-khan/")],
    body=f'''<div class="card quick"><b>مختصر جواب</b><p>گوجرخان اور آس پاس کے علاقوں میں مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر محمد عثمان (کوڈ {CODE}) گھر آ کر سرکاری دستاویزات کا کام کرواتے ہیں۔ گوجرخان اور راولپنڈی میں زیادہ تر کام ڈومیسائل کا ہوتا ہے، ساتھ ڈرائیونگ لائسنس، پولیس، گاڑی اور سول دستاویزات بھی۔ آن لائن رابطہ کسی بھی وقت، گھر پر وزٹ پہلے سے وقت طے کر کے۔</p></div>
<div class="sd-actions"><a class="btn g" data-ga-event="service_whatsapp_click" href="{wa_link('گوجرخان میں دستک سروس')}">واٹس ایپ: {PHONE}</a><a class="btn o" href="tel:+923455583530">کال کریں</a><a class="btn o" href="https://www.google.com/maps/search/?api=1&amp;query=Dastak+Online+Document+Facilitation+Sandal+Road+Gujar+Khan" rel="noopener">گوگل میپ پر دیکھیں</a></div>
<section class="service-module"><h2>کن علاقوں میں گھر پر سروس ملتی ہے؟</h2><p>{AREAS}۔ اپنا علاقہ واٹس ایپ پر بتا کر پہلے تصدیق کر لیں۔</p></section>
<section class="service-module"><h2>گوجرخان میں سب سے زیادہ مانگی جانے والی خدمات</h2>{cards((R["domicile"], R["renew"], R["character"], R["transfer"], R["token"], R["learner"]))}</section>
<section class="service-module"><h2>ہمارا پتہ</h2><p>سینڈل روڈ، وارڈ نمبر 14، گوجرخان، پنجاب <span class="ltr">47850</span>۔ شہری اکثر یہاں بھی تشریف لاتے ہیں، مگر آنے سے پہلے واٹس ایپ پر وقت طے کر لیں۔</p></section>
{booking_block("گوجرخان میں دستک سروس")}''',
    faqs=[
        ("Gujar Khan mein domicile kaise banwayen?", "دستک ایپ میں کوڈ 90807 کے ساتھ بکنگ کریں یا واٹس ایپ 0345-5583530 کریں۔ دستک کے ذریعے ڈومیسائل کی کل فیس 1,200 روپے ہے اور 300 روپے کا بیان حلفی الگ ہے۔"),
        ("کیا آپ کلر سیداں، مندرہ اور جاتلی بھی آتے ہیں؟", "جی ہاں، کلر سیداں، کہوٹہ، مندرہ، بیول، دولتالہ، جاتلی، سکھو اور قاضیاں میں بھی وزٹ پہلے سے وقت طے کر کے ہوتا ہے۔"),
        ("کیا یہ سرکاری دفتر ہے؟", "نہیں۔ یہ ایک آزاد رجسٹرڈ فیسیلیٹیٹر کی سروس ہے، کوئی سرکاری دفتر نہیں۔"),
    ]))

PAGES.append(dict(
    path="/contact/", kind="hub", en_title="Contact",
    title="رابطہ: واٹس ایپ 0345-5583530، گوجرخان | دستک 90807",
    desc="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن سے رابطہ: واٹس ایپ اور کال 0345-5583530، ای میل، پتہ سینڈل روڈ گوجرخان۔ رجسٹرڈ فیسیلیٹیٹر محمد عثمان، کوڈ 90807۔",
    h1="رابطہ کریں", og="/assets/og/general.jpg",
    crumbs=[("رابطہ", "/ur/contact/")],
    body=f'''<div class="card quick"><b>سب سے تیز رابطہ</b><p>واٹس ایپ پر اپنی سروس اور شہر لکھ کر بھیجیں: {PHONE}۔ آن لائن رابطہ کسی بھی وقت، گھر پر وزٹ پہلے سے وقت طے کر کے۔</p></div>
<div class="sd-actions"><a class="btn g" data-ga-event="contact_whatsapp_click" href="{WA}">واٹس ایپ {PHONE}</a><a class="btn y" data-ga-event="contact_call_click" href="tel:+923455583530">کال کریں</a></div>
<section class="service-module"><h2>رابطے کی تفصیل</h2><table class="ur-fee"><tbody>
<tr><th scope="row">نام</th><td>محمد عثمان، رجسٹرڈ دستک فیسیلیٹیٹر (کوڈ {CODE})</td></tr>
<tr><th scope="row">واٹس ایپ اور کال</th><td><a href="{WA}">{PHONE}</a></td></tr>
<tr><th scope="row">ای میل</th><td><a href="mailto:support@dastak90807.com"><span class="ltr">support@dastak90807.com</span></a><br><a href="mailto:dastak90807@zohamail.com"><span class="ltr">dastak90807@zohamail.com</span></a></td></tr>
<tr><th scope="row">پتہ</th><td>سینڈل روڈ، وارڈ نمبر 14، گوجرخان، پنجاب <span class="ltr">47850</span></td></tr>
<tr><th scope="row">اوقات</th><td>آن لائن رابطہ کسی بھی وقت۔ گھر پر وزٹ پہلے سے وقت طے کر کے۔</td></tr>
</tbody></table><div class="row"><a class="btn o" href="https://www.google.com/maps/search/?api=1&amp;query=Dastak+Online+Document+Facilitation+Sandal+Road+Gujar+Khan" rel="noopener">گوگل میپ پر لوکیشن</a><a class="btn o" href="https://share.google/nmpsQYND7NTAnZzqI" rel="noopener">گوگل پروفائل اور ریویوز</a></div></section>
<section class="service-module"><h2>دھوکے سے بچیں</h2><ul><li>میں کبھی آپ سے پاس ورڈ یا OTP نہیں مانگتا۔</li><li>فیس ہمیشہ سرکاری سسٹم کے PSID سے ادا ہوتی ہے۔</li><li>کام مکمل ہونے اور ڈیلیوری کے بعد آپ کی دستاویزات ڈیلیٹ کر دی جاتی ہیں۔</li><li id="verify">{VERIFY}</li></ul></section>''',
    faqs=[
        ("آپ سے رابطہ کیسے کریں؟", "واٹس ایپ یا کال 0345-5583530، یا ای میل support@dastak90807.com۔"),
        ("کیا آپ کا دفتر ہے؟", "پتہ سینڈل روڈ، وارڈ نمبر 14، گوجرخان ہے۔ آنے سے پہلے واٹس ایپ پر وقت طے کر لیں۔"),
    ]))

HP = json.load(open(os.path.join(ROOT, "scripts", "home_parts.json"), encoding="utf-8"))
ARROW = HP["arrow"]


def home_card(icon, tag, title, links, more_href, more_text, wa_topic):
    lis = "".join(f'<li><a href="{h}">{t} ←</a></li>' for h, t in links)
    return (f'<article class="card home-category"><span class="home-popular">{tag}</span><span class="category-icon">{icon}</span>'
            f'<h3>{title}</h3><ul>{lis}</ul><div class="home-category-foot"><a class="btn y home-category-more" href="{more_href}">{more_text} {ARROW}</a>'
            f'<a class="btn g home-category-wa" href="{wa_link(wa_topic)}">واٹس ایپ پر پوچھیں</a></div></article>')


SV, TL = HP["svc"], HP["tools"]
STRIP_TEXT = ["گھر کی دہلیز پر کاغذات کی وصولی اور ڈیلیوری", f"کوڈ {CODE} کی تصدیق سرکاری پورٹل پر کریں", "آزاد فیسیلیٹیشن سروس، سرکاری دفتر نہیں"]
strip_items = "".join(f"<li>{ic}<span>{t}</span></li>" for ic, t in zip(HP["strip"], STRIP_TEXT))
STRIP = ('<aside class="top trust-strip" aria-label="سروس کی خصوصیات"><div class="announcement-window"><div class="announcement-track">'
         f'<ul class="announcement-message">{strip_items}</ul><ul class="announcement-message announcement-copy" aria-hidden="true">{strip_items}</ul>'
         f'<ul class="announcement-message announcement-copy" aria-hidden="true">{strip_items}</ul></div></div></aside>')
TRUST = [("رجسٹرڈ فیسیلیٹیٹر", f"کوڈ {CODE}"), ("سرکاری پورٹلز", "پنجاب کے سرکاری سسٹم سے کارروائی"),
         ("اسٹیٹس اپڈیٹس", "ٹریکنگ آئی ڈی آپ کو دی جاتی ہے"), ("آزاد سروس", "سرکاری دفتر نہیں")]
trust_html = "".join(f'<div class="home-trust-item"><span>{ic}</span><div><strong>{a}</strong><small>{b}</small></div></div>'
                     for ic, (a, b) in zip(HP["trust"], TRUST))

HERO_ALT = ("گوجرخان، راولپنڈی اور پنجاب میں دستک فیسیلیٹیٹر گھر کی دہلیز پر شہری کو دستاویزات دیتے ہوئے، "
            "دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)")

CARDS_SVC = "".join([
    home_card(SV[0]["icon"], "مقبول", "ڈرائیونگ لائسنس",
              [("/ur/services/learner-driving-license/", "لرنر ڈرائیونگ لائسنس"), ("/ur/services/renewal-of-regular-license/", "لائسنس رینیول"),
               ("/ur/guides/how-to-track-driving-license-in-punjab/", "لائسنس ٹریک کریں")], "/ur/services/", "تمام خدمات", "ڈرائیونگ لائسنس"),
    home_card(SV[1]["icon"], "مقبول", "گاڑی اور ایکسائز",
              [("/ur/services/transfer-of-motor-vehicle/", "گاڑی اور موٹر سائیکل ٹرانسفر"), ("/ur/services/token-tax/", "ٹوکن ٹیکس"),
               ("/ur/guides/vehicle-transfer-token-tax-punjab/", "ٹرانسفر اور ٹوکن ٹیکس گائیڈ")], "/ur/services/", "تمام خدمات", "گاڑی اور ایکسائز"),
    home_card(SV[2]["icon"], "مقبول", "پولیس خدمات",
              [("/ur/services/character-certificate/", "پولیس کریکٹر سرٹیفکیٹ"), ("/ur/guides/punjab-police-character-certificate-online/", "کریکٹر سرٹیفکیٹ گائیڈ"),
               ("/en/services/tenant-registration/", "کرایہ دار رجسٹریشن (English)")], "/ur/services/", "تمام خدمات", "پولیس خدمات"),
    home_card(SV[3]["icon"], "گوجرخان", "سول دستاویزات",
              [("/ur/services/domicile-certificate/", "ڈومیسائل سرٹیفکیٹ"), ("/en/services/e-stamping/", "ای اسٹامپ (English)"),
               ("/en/services/birth-certificate/", "پیدائش سرٹیفکیٹ (English)")], "/ur/gujar-khan/", "گوجرخان خدمات", "سول دستاویزات"),
    home_card(SV[4]["icon"], "رہنمائی", "جنگلات، وائلڈ لائف اور فشریز",
              [("/en/services/other-punjab-dastak-services/", "فشریز ای لائسنس رہنمائی (English)"),
               ("/en/services/other-punjab-dastak-services/", "وائلڈ لائف پرمٹ رہنمائی (English)")], "/ur/services/", "تمام خدمات", "جنگلات، وائلڈ لائف اور فشریز"),
    home_card(SV[5]["icon"], "رہنمائی", "ای بز کاروباری خدمات",
              [("/en/services/other-punjab-dastak-services/", "فوڈ اتھارٹی لائسنس رہنمائی (English)"),
               ("/en/services/other-punjab-dastak-services/", "کاروبار کی رجسٹریشن رہنمائی (English)"),
               ("/en/services/general-inquiry-and-guide/", "گھر پر کاروباری سہولت (English)")], "/ur/services/", "تمام خدمات", "ای بز کاروباری خدمات"),
])
CARDS_TOOLS = "".join([
    home_card(TL[0]["icon"], "مفت", "ڈرائیونگ لائسنس فیس کیلکولیٹر",
              [(TL[0]["more"], "رینیول فیس (1 سے 5 سال)"), (TL[0]["more"], "نیا اور ڈپلیکیٹ لائسنس"), (TL[0]["more"], "انٹرنیشنل ڈرائیونگ پرمٹ")],
              TL[0]["more"], "ابھی حساب کریں", "ڈرائیونگ لائسنس فیس"),
    home_card(TL[1]["icon"], "مفت", "کار ٹوکن ٹیکس اور ٹرانسفر کیلکولیٹر",
              [(TL[1]["more"], "کار اور جیپ کا ٹوکن ٹیکس"), (TL[1]["more"], "کار ٹرانسفر فیس"), (TL[1]["more"], "فائلر اور نان فائلر ریٹس")],
              TL[1]["more"], "ابھی حساب کریں", "کار فیس"),
    home_card(TL[2]["icon"], "مفت", "موٹر سائیکل رجسٹریشن اور ٹرانسفر کیلکولیٹر",
              [(TL[2]["more"], "نئی بائیک رجسٹریشن فیس"), (TL[2]["more"], "موٹر سائیکل ٹرانسفر فیس"), (TL[2]["more"], "لائف ٹائم ٹوکن ٹیکس")],
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
    '<p>درخواست سرکاری دستک سسٹم کے ذریعے جمع ہوتی ہے اور فیس سرکاری PSID سے ادا ہوتی ہے۔ آپ کو ٹریکنگ آئی ڈی ملتی ہے اور محکمے کے کام مکمل کرنے تک میں آپ کو اپڈیٹ دیتا رہتا ہوں۔</p>'
    '<span class="home-step-tag">ٹریکنگ آئی ڈی · اسٹیٹس اپڈیٹس</span></li>'
)

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
    f'<div class="art"><img src="/assets/muhammad-usman-dastak-90807-doorstep-document-facilitation-punjab.webp" width="2400" height="1340" alt="{HERO_ALT}" fetchpriority="high"></div></div></section>'
    + STRIP +
    '<section class="wrap home-services" id="services" aria-labelledby="home-services-title"><p class="eyebrow">پورے پنجاب میں آن لائن · گوجرخان میں گھر کی دہلیز پر</p>'
    '<h2 id="home-services-title">پنجاب میں کہیں سے بھی آن لائن اپلائی کریں</h2><p class="sub">اپنی خدمت منتخب کریں اور دستاویزات اور اگلے قدم دیکھیں۔</p>'
    f'<div class="home-category-grid">{CARDS_SVC}</div></section>'
    '<section class="wrap home-tools" id="citizen-tools"><p class="eyebrow">مفت فیس کیلکولیٹر</p><h2 id="fee-calculators">اپنی فیس کا اندازہ لگائیں</h2>'
    '<p class="sub">ڈرائیونگ لائسنس، کار اور موٹر سائیکل کے مفت فیس کیلکولیٹر، اردو اور انگریزی دونوں میں۔ اندازہ PDF میں ڈاؤن لوڈ کریں۔ حتمی رقم ہمیشہ PSID پر ہوتی ہے۔</p>'
    f'<div class="home-category-grid">{CARDS_TOOLS}</div></section>'
    '<section class="band process" id="how-it-works"><div class="wrap"><p class="eyebrow">طریقہ کار</p><h2>3 آسان قدموں میں اپلائی کریں</h2>'
    f'<p class="sub home-steps-sub">پورے پنجاب سے آن لائن۔ گوجرخان میں گھر کی دہلیز پر۔</p><ol class="home-steps">{STEPS}</ol>'
    f'<div class="home-trust-strip">{trust_html}</div>'
    f'<div class="row"><a class="btn g" href="{wa_link("سروس کی بکنگ")}">واٹس ایپ {PHONE}</a><a class="btn y" href="#fee-calculators">فیس معلوم کریں {ARROW}</a></div></div></section>'
    f'<section class="wrap"><div class="card ur-verify-box" id="verify"><h2>فیسیلیٹیٹر کی تصدیق کیسے کریں؟</h2><p>{VERIFY}</p></div></section>'
    '<section class="wrap ur-home-guides"><h2>مفید اردو گائیڈز</h2>' + cards((R["renew_guide"], R["track"], R["character_guide"], R["vehicle_guide"])) + '</section>'
)

PAGES.append(dict(
    path="/", kind="hub", raw=True, main_class="home home-ur", en_title="Home",
    css=["/assets/home-wide.css", "/assets/home-refinement.css?v=20261125a", "/assets/guide-cards.css?v=1"],
    title="دستک 90807 | گھر بیٹھے سرکاری دستاویزات، گوجرخان اور پنجاب",
    desc="ڈرائیونگ لائسنس، پولیس کریکٹر سرٹیفکیٹ، گاڑی ٹرانسفر، ٹوکن ٹیکس اور ڈومیسائل میں گھر بیٹھے مدد۔ مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر، کوڈ 90807۔ واٹس ایپ 0345-5583530۔",
    h1="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن", og="/assets/dastak-online-document-facilitation-punjab-og.jpg",
    og_alt="دستک آن لائن ڈاکومنٹ فیسیلیٹیشن (رجسٹرڈ فیسیلیٹیٹر کوڈ 90807)، گوجرخان، راولپنڈی اور پنجاب میں گھر بیٹھے سرکاری دستاویزات",
    crumbs=[],
    body=HOME_BODY,
    faqs=[
        ("کیا یہ سرکاری ویب سائٹ ہے؟", "نہیں۔ یہ مریم کی دستک کے رجسٹرڈ فیسیلیٹیٹر (کوڈ 90807) کی آزاد سروس ہے، کوئی سرکاری ویب سائٹ یا محکمہ نہیں۔ سرکاری پورٹل dastak.punjab.gov.pk ہے۔"),
        ("گھر بیٹھے سرکاری کاغذات کیسے بنوائیں؟ (Ghar baithe documents kaise banwayen)", "واٹس ایپ 0345-5583530 پر رابطہ کریں یا دستک ایپ میں Doorstep Delivery منتخب کر کے کوڈ 90807 لکھیں۔"),
        ("فیس کتنی ہے؟", "سرکاری فیس ہر سروس کی الگ ہے اور PSID پر لکھی ہوتی ہے۔ دستک تربیتی مینول کے مطابق فیسیلیٹیٹر چارجز 950 روپے ہیں۔"),
        ("کیا آپ پورے پنجاب میں کام کرتے ہیں؟", "جی ہاں، پورے پنجاب کے لیے واٹس ایپ پر رہنمائی اور دستاویزات کی جانچ۔ گھر پر وزٹ گوجرخان، راولپنڈی اور قریبی علاقوں میں۔"),
    ]))

def main():
    for p in PAGES:
        out_dir = os.path.join(ROOT, "ur", p["path"].strip("/"))
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(page(p))
    print(f"Built {len(PAGES)} Urdu pages")


if __name__ == "__main__":
    main()
