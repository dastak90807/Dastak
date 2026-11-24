#!/usr/bin/env python3
"""Rebuild guide cards from assets/guides.json.
Usage: python3 scripts/build_guides.py          # rewrite home (latest 3) + guides listing
       python3 scripts/build_guides.py --check  # also verify sitemap, llms.txt, search index, files
"""
import html, json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://www.dastak90807.com'
def rd(p): return open(os.path.join(ROOT, p), encoding='utf-8').read()
data = json.load(open(os.path.join(ROOT, 'assets/guides.json'), encoding='utf-8'))
guides = sorted(data['guides'], key=lambda g: g['date'], reverse=True)  # stable: ties keep list order
e = lambda s: html.escape(s, quote=True)
def card(g, home):
    href = ('guides/%s/index.html' if home else '%s/index.html') % g['slug']
    ga = 'home_guide_click' if home else 'guide_read'
    if g.get('thumb'):
        media = '<div class="guide-illustration has-thumb"><img src="/assets/%s" width="%d" height="%d" loading="lazy" decoding="async" alt="%s"></div>' % (g['thumb'], g['thumb_w'], g['thumb_h'], e(g['thumb_alt']))
    else:
        media = '<div class="guide-illustration">%s</div>' % data['icons'][g['category']]
    return ('<article class="card guide-card local-guide" data-guide-category="%s">%s<div class="guide-body"><span class="eyebrow">%s</span>'
            '<h3><a data-ga-event="%s" href="%s">%s</a></h3><p>%s</p><a data-ga-event="%s" class="btn y" href="%s">Read guide <span aria-hidden="true">↗</span></a></div></article>'
            % (g['category'], media, e(g['eyebrow']), ga, href, e(g['title']), e(g['summary']), ga, href))
import datetime
CAT = {'driving':'Driving License','vehicle':'Vehicle & Excise','police':'Police','civil':'Domicile & Civil'}
REL = {'driving':[('Service page','/en/services/renewal-of-regular-license/'),('Fee calculator','/en/calculators/tools/punjab-driving-license-fee-calculator')],
       'vehicle':[('Token Tax service','/en/services/token-tax/'),('Fee calculator','/en/calculators/tools/punjab-car-token-tax-transfer-fee-calculator')],
       'police':[('Service page','/en/services/character-certificate/')],
       'civil':[('Service page','/en/services/domicile-certificate/')]}
def fdate(d): 
    x = datetime.date.fromisoformat(d); return '%d %s %d' % (x.day, x.strftime('%b'), x.year)
def card2(g, feat=False):
    href = '/en/guides/%s/' % g['slug']
    rel = ''.join('<a href="%s">%s</a>' % (h, e(t)) for t, h in REL.get(g['category'], []))
    img = '<img src="/assets/%s" width="%d" height="%d" loading="%s" decoding="async" alt="%s">' % (g['thumb'], g['thumb_w'], g['thumb_h'], 'eager' if feat else 'lazy', e(g['thumb_alt']))
    txt = 'data-gp-cat="%s" data-gp-text="%s"' % (g['category'], e((g['title'] + ' ' + g['summary'] + ' ' + CAT[g['category']]).lower()))
    if feat:
        return ('<article class="gp-feat" %s><a class="gp-feat-img" href="%s" tabindex="-1" aria-hidden="true">%s</a><div class="gp-feat-b"><span class="gp-tag">Featured &middot; Published %s</span>'
                '<h2><a data-ga-event="guide_read" href="%s">%s</a></h2><p>%s</p><div class="row"><a data-ga-event="guide_read" class="btn y" href="%s">Read Guide <svg class="btn-arrow" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg></a>%s</div></div></article>'
                % (txt, href, img, fdate(g['date']), href, e(g['title']), e(g['summary']), href,
                   ''.join('<a class="btn o" href="%s">Calculate Fees</a>' % h for t, h in REL.get(g['category'], []) if 'calculator' in h)))
    return ('<article class="gp-card" %s><a class="gp-img" href="%s" tabindex="-1" aria-hidden="true">%s</a><div class="gp-b"><span class="gp-t">%s</span>'
            '<h3><a data-ga-event="guide_read" href="%s">%s</a></h3><p>%s</p><div class="gp-meta"><span>Published %s</span><a data-ga-event="guide_read" class="gp-read" href="%s">Read Guide <span aria-hidden="true">&#8599;</span></a></div>'
            '<div class="gp-rel">%s</div></div></article>' % (txt, href, img, CAT[g['category']].upper(), href, e(g['title']), e(g['summary']), fdate(g['date']), href, rel))
def listing_html(gs):
    more = ('<article class="gp-card gp-more" data-gp-cat="more" data-gp-text="more guides coming learner license duplicate license tenant registration"><div class="gp-more-in"><b>More guides coming</b><p>Learner license, duplicate license, tenant registration. Tell me which guide you need.</p>'
            '<a class="btn g" data-ga-event="whatsapp_lead" href="https://wa.me/923455583530">Ask on WhatsApp</a></div></article>')
    return card2(gs[0], True) + '<h2 class="gp-h" id="gp-all">All guides</h2><p class="gp-sub">%d guides. Each links to its service page or calculator.</p><div class="gp-grid">' % len(gs) + ''.join(card2(g) for g in gs[1:]) + more + '</div>'
FAQ = json.load(open(os.path.join(ROOT, 'assets/guides-faq.json'), encoding='utf-8'))
def ld_html(gs):
    items = [{'@type':'ListItem','position':i+1,'url':SITE+'/en/guides/%s/' % g['slug'],'name':g['title']} for i, g in enumerate(gs)]
    graph = [
     {'@type':'CollectionPage','@id':SITE+'/en/guides/#page','url':SITE+'/en/guides/','name':'Punjab Driving License, Police & Vehicle Guides (Pakistan)','inLanguage':'en-PK',
      'description':'Step-by-step guides for Punjab driving license, police character certificate, domicile, token tax and vehicle transfer in Pakistan.',
      'isPartOf':{'@type':'WebSite','name':'Dastak Online Document Facilitation','url':SITE+'/'},
      'about':{'@type':'Organization','name':'Dastak Online Document Facilitation (Registered Facilitator Code 90807)','url':SITE+'/'},
      'mainEntity':{'@type':'ItemList','itemListElement':items}},
     {'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':SITE+'/en/'},{'@type':'ListItem','position':2,'name':'Guides','item':SITE+'/en/guides/'}]},
     {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q['q'],'acceptedAnswer':{'@type':'Answer','text':q['a']}} for q in FAQ]}]
    return '<script type="application/ld+json">' + json.dumps({'@context':'https://schema.org','@graph':graph}, ensure_ascii=False) + '</script>'
def swap(s, a, b, new):
    i, j = s.index(a) + len(a), s.index(b); return s[:i] + new + s[j:]
def rebuild_listing(path, gs):
    s = rd(path)
    s = swap(s, '<!--feat:start-->', '<!--feat:end-->', listing_html(gs))
    s = swap(s, '<!--ld:start-->', '<!--ld:end-->', ld_html(gs))
    s = swap(s, '<!--gfaq:start-->', '<!--gfaq:end-->', ''.join('<details><summary>%s</summary><p>%s</p></details>' % (e(q['q']), e(q['a'])) for q in FAQ))
    open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(s)
def rebuild(path, items, home):
    s = rd(path); a, b = '<!--guides:start-->', '<!--guides:end-->'
    i, j = s.index(a) + len(a), s.index(b)
    new = s[:i] + ''.join(card(g, home) for g in items) + s[j:]
    if new != s: open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(new)
    return new
def main():
    rebuild('en/index.html', guides[:3], True)
    rebuild_listing('en/guides/index.html', guides)
    print('rebuilt: home = latest 3, listing = %d guides' % len(guides))
    if '--check' not in sys.argv: return
    sm, ll = rd('sitemap.xml'), rd('llms.txt')
    si = {x['url'] for x in json.loads(rd('assets/search-index.json'))}
    bad = []
    for g in guides:
        u = '/en/guides/%s/' % g['slug']
        if not os.path.exists(os.path.join(ROOT, 'en/guides/%s/index.html' % g['slug'])): bad.append('missing page ' + u)
        if SITE + u not in sm: bad.append('sitemap.xml missing ' + u)
        if SITE + u not in ll: bad.append('llms.txt missing ' + u)
        if u not in si: bad.append('search-index.json missing ' + u)
        if g.get('thumb') and not os.path.exists(os.path.join(ROOT, 'assets', g['thumb'])): bad.append('missing thumb ' + g['thumb'])
    print('\n'.join(bad) if bad else 'check OK: all guides in sitemap, llms.txt, search index; files exist')
    sys.exit(1 if bad else 0)
main()
