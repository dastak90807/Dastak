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
def rebuild(path, items, home):
    s = rd(path); a, b = '<!--guides:start-->', '<!--guides:end-->'
    i, j = s.index(a) + len(a), s.index(b)
    new = s[:i] + ''.join(card(g, home) for g in items) + s[j:]
    if new != s: open(os.path.join(ROOT, path), 'w', encoding='utf-8').write(new)
    return new
def main():
    rebuild('en/index.html', guides[:3], True)
    rebuild('en/guides/index.html', guides, False)
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
