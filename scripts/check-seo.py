#!/usr/bin/env python3
"""Check the publication URLs, structured data and portable local assets."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse
import json
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
config=json.loads((ROOT/'content/site.json').read_text())
base=config['site_url'].rstrip('/')
assert urlparse(base).scheme=='https' and urlparse(base).netloc, 'Publication address missing'
assert (ROOT/'CNAME').read_text().strip()==urlparse(base).netloc
class Document(HTMLParser):
    def __init__(self):
        super().__init__();self.tags=[]
    def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))

files=sorted(ROOT.glob('*.html'))
indexed=[]
for file in files:
    source=file.read_text();doc=Document();doc.feed(source)
    expected=base+'/' + ('' if file.name=='index.html' else file.name)
    canon=[a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='canonical']
    assert canon==[expected], (file.name,'canonical',canon)
    meta={a.get('property') or a.get('name'):a.get('content') for t,a in doc.tags if t=='meta'}
    assert meta['og:url']==expected
    assert meta['og:image']==base+'/assets/img/social-cover.webp'
    assert meta['twitter:image']==meta['og:image']
    assert meta['og:title']==meta['twitter:title']
    assert meta['description']==meta['og:description']==meta['twitter:description']
    if file.name=='404.html':assert 'noindex' in meta['robots']
    else:
        assert 'noindex' not in meta['robots'];indexed.append(expected)
    graph=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',source,re.S).group(1))['@graph']
    page=next(n for n in graph if n['@type']=='WebPage')
    assert page['url']==expected
    assert any(n['@type']=='Person' and n['name']=='Ali Cengiz' for n in graph)
    if file.name not in ('index.html','404.html'):
        trail=next(n for n in graph if n['@type']=='BreadcrumbList')
        assert trail['itemListElement'][0]['item']==base+'/'
        assert trail['itemListElement'][-1]['item']==expected
    for tag,a in doc.tags:
        if tag in ('img','script') and a.get('src'):assert not urlparse(a['src']).scheme,(file.name,'external asset')
        if tag=='link' and a.get('rel') in ('stylesheet','preload'):assert not urlparse(a['href']).scheme
        if tag=='a' and a.get('href'):assert urlparse(a['href']).netloc!=urlparse(base).netloc,(file.name,'nonportable local link')
    assert 'localhost' not in source and '127.0.0.1' not in source and '__SITE_BASE__' not in source
locs=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
assert sorted(locs)==sorted(indexed)
assert 'Sitemap: '+base+'/sitemap.xml' in (ROOT/'robots.txt').read_text()
source=(ROOT/'index.html').read_text()
show=json.loads((ROOT/'content/home-show.json').read_text())
assert 'Sahnede Ali Cengiz,<br>' not in source
assert all(text in source for text in [show['title'],show['subtitle'],show['intro'],show['purpose'],*show['participation'],*show['values'],*show['audiences']])
assert 'show-story.css' in source
print(f'PASS · {len(files)} canonical URLs · {len(locs)} indexed sitemap URLs · 13 breadcrumbs · complete show text · portable local assets')
