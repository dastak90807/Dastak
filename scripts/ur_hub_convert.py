"""Build an Urdu hub page body from the live English page markup.

The English page (en/<slug>/index.html) is the single source of layout.
Every visible text node and text attribute is replaced from
scripts/ur_hubs/<slug>.json. Any English text without a translation stops
the build, so a new English section can never leak onto the Urdu page.
"""
import html
import json
import os
import posixpath
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

URDU_PATHS = {
    "/", "/services/", "/guides/", "/calculators/", "/contact/", "/gujar-khan/",
    "/services/renewal-of-regular-license/", "/services/learner-driving-license/",
    "/services/character-certificate/", "/services/transfer-of-motor-vehicle/",
    "/services/token-tax/", "/services/domicile-certificate/",
    "/guides/punjab-driving-license-renewal-online/", "/guides/how-to-track-driving-license-in-punjab/",
    "/guides/punjab-police-character-certificate-online/", "/guides/vehicle-transfer-token-tax-punjab/",
    # Phase 2: driving license and police service pages
    "/services/renewal-of-learners-driving-license/", "/services/duplicate-driving-license/",
    "/services/renewal-international-driving-license/", "/services/duplicate-international-driving-license/",
    "/services/general-police-verification/", "/services/tenant-registration/", "/services/loss-report/",
    "/services/crime-report/", "/services/copy-of-fir/", "/services/traffic-challan/", "/services/safe-city-challan/",
    # Phase 3: vehicle, domicile, e-stamp and civil service pages
    "/services/motor-vehicle-registration/", "/services/duplicate-domicile/", "/services/modification-domicile/",
    "/services/noc-for-domicile-transfer/", "/services/e-stamping/", "/services/birth-certificate/",
    "/services/death-certificate/", "/services/marriage-certificate/", "/services/divorce-certificate/",
    "/services/general-inquiry-and-guide/", "/services/other-punjab-dastak-services/",
}

# Text that is the same in both languages (brands, emails, domains, numbers).
KEEP = re.compile(r"^(?:[\d\s\-+().,:/·&;]*|[\w.+-]+@[\w.-]+|(?:www\.)?[\w-]+(?:\.[\w-]+)+|Facebook|Instagram|TikTok|X|LinkedIn|YouTube|Snapchat|Pinterest|&middot;|·)$")
ATTRS = ("aria-label", "alt", "title", "placeholder", "label")


def norm(t):
    return " ".join(t.split())


def convert(slug):
    src = open(os.path.join(ROOT, "en", slug, "index.html"), encoding="utf-8").read()
    m = re.search(r'<main id="main" class="([^"]*)">(.*)</main>', src, re.S)
    main_class, body = m.group(1), m.group(2)
    tr_file = os.path.join(ROOT, "scripts", "ur_hubs", slug + ".json")
    if not os.path.exists(tr_file) and slug.startswith("services/"):
        tr_file = os.path.join(ROOT, "scripts", "ur_hubs", "service-detail.json")  # shared by service pages
    tr = json.load(open(tr_file, encoding="utf-8"))
    missing = []

    def look(t):
        n = norm(t)
        if not n or not re.search(r"[A-Za-z]", n) or KEEP.match(n):
            return None
        for k in (n, html.unescape(n), html.unescape(n).replace("&", "&amp;")):
            if k in tr:
                return tr[k]
        missing.append(n)
        return None

    # Protect SVG, script and style blocks from translation.
    keep = []

    def stash(x):
        keep.append(x.group(0))
        return f"\x00{len(keep) - 1}\x00"

    body = re.sub(r"<(svg|script|style)\b.*?</\1>", stash, body, flags=re.S)

    def piece(t):
        if t.startswith("\x00"):
            return t
        u = look(t)
        if u is None:
            return t
        lead = " " if t[:1].isspace() else ""
        trail = " " if t[-1:].isspace() else ""
        return f"{lead}{u}{trail}"

    def text(x):
        return ">" + "".join(piece(t) for t in re.split(r"(\x00\d+\x00)", x.group(1))) + "<"

    body = re.sub(r">([^<>]+)<", text, body)
    body = body.replace("→", "←").replace("↗", "↖").replace("&#8599;", "&#8598;").replace("&#8594;", "&#8592;").replace("&rarr;", "&larr;")  # arrows point left in RTL

    def attr(x):
        name, val = x.group(1), x.group(2)
        u = look(val)
        return f'{name}="{u}"' if u is not None else x.group(0)

    body = re.sub(r'\b(%s)="([^"]*)"' % "|".join(ATTRS), attr, body)

    # Internal links: Urdu page where one exists, otherwise English marked hreflang.
    def link(x):
        path, rest = x.group(1), x.group(2)
        bare = re.sub(r"[#?].*$", "", path)
        if bare in URDU_PATHS:
            return f'href="/ur{path}"{rest}'
        return f'href="/en{path}" hreflang="en"{rest}'

    # Relative links (../x/index.html) are resolved against the English page first.
    def rel(x):
        href = x.group(1)
        if re.match(r"(?:[a-z]+:|/|#)", href):
            return x.group(0)
        frag = re.search(r"[#?].*$", href)
        frag = frag.group(0) if frag else ""
        full = posixpath.normpath(posixpath.join("/en/" + slug + "/", href[:len(href) - len(frag)]))
        full = re.sub(r"/index\.html$", "", full).rstrip("/") + "/"
        return f'href="{full}{frag}"'

    body = re.sub(r'href="([^"]*)"', rel, body)
    body = re.sub(r'href="/en(/[^"]*)"([^>]*)', link, body)
    body = body.replace('src="../../', 'src="/')
    body = re.sub(r"\x00(\d+)\x00", lambda x: keep[int(x.group(1))], body)

    if missing:
        raise SystemExit(f"[ur_hub_convert] {slug}: {len(missing)} English strings need Urdu in "
                         f"{os.path.relpath(tr_file, ROOT)}:\n  " + "\n  ".join(dict.fromkeys(missing)))

    faqs = [(re.sub("<[^>]+>", "", q), re.sub("<[^>]+>", "", a))
            for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", body, re.S)]
    css = re.findall(r'<link rel="stylesheet" href="(/assets/(?:guide-cards|guides-page|tools-pages|service-info-pages|contact-page|services-page)[^"]*)"', src)
    js = re.findall(r'<script src="(/assets/(?:guides-page|services-page)[^"]*)"', src)
    return dict(main_class=main_class + " ur-hub", body=body, faqs=faqs, css=css, js=js)
