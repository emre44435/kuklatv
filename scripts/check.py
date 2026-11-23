#!/usr/bin/env python3
"""Checks real publish risks: missing assets, links, metadata and sitemap URLs."""
import json
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]
errors = []
titles, descriptions = set(), set()

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[]
        self.ids=set()
        self.h1=0
        self.in_title=False
        self.title=''
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        if tag=='h1':self.h1+=1
        if tag=='title':self.in_title=True
        if 'id' in attrs:
            if attrs['id'] in self.ids:errors.append('Duplicate id '+attrs['id'])
            self.ids.add(attrs['id'])
    def handle_data(self,data):
        if self.in_title:self.title+=data
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False

files=sorted(ROOT.glob('*.html'))
parsed={p.name:Page() for p in files}
for p in files:parsed[p.name].feed(p.read_text(encoding='utf-8'))
for p in files:
    data=p.read_text(encoding='utf-8');doc=parsed[p.name]
    if doc.h1!=1:errors.append(f'{p.name}: expected one h1, got {doc.h1}')
    if not doc.title.strip() or doc.title in titles:errors.append(f'{p.name}: empty or duplicate title')
    titles.add(doc.title)
    metas={a.get('name'):a.get('content') for t,a in doc.tags if t=='meta'}
    desc=metas.get('description')
    if not desc or desc in descriptions:errors.append(f'{p.name}: empty or duplicate description')
    descriptions.add(desc)
    if not any(t=='html' and a.get('lang')=='tr' for t,a in doc.tags):errors.append(f'{p.name}: Turkish lang missing')
    canonicals=[a['href'] for t,a in doc.tags if t=='link' and a.get('rel')=='canonical']
    base=urlparse(canonicals[0]) if canonicals else None
    base_prefix=base.path.rsplit('/',1)[0]+'/' if base and base.path.endswith('.html') else base.path if base else ''
    for tag,a in doc.tags:
        if tag=='img' and not all(k in a for k in ('alt','width','height')):errors.append(f'{p.name}: image lacks alt or dimensions')
        if tag=='iframe':errors.append(f'{p.name}: embedded video is not allowed')
        if tag=='a' and a.get('target')=='_blank' and 'noopener' not in a.get('rel',''):errors.append(f'{p.name}: insecure blank target')
        for key in ('href','src'):
            ref=a.get(key)
            if not ref or ref.startswith(('tel:','mailto:','data:')):continue
            u=urlparse(ref)
            if u.scheme and (not base or u.netloc!=base.netloc):continue
            path=unquote(u.path)
            if u.scheme and base:
                if not path.startswith(base_prefix):errors.append(f'{p.name}: bad project base path: {ref}');continue
                path=path[len(base_prefix):]
            path=path.lstrip('./')
            target=ROOT/(path or p.name)
            if not target.exists():errors.append(f'{p.name}: missing {ref}')
            if u.fragment and target.suffix=='.html' and target.name in parsed:
                if u.fragment not in parsed[target.name].ids:errors.append(f'{p.name}: broken anchor {ref}')
    for text in re.findall(r'<script type="application/(?:ld\+json|json)"[^>]*>(.*?)</script>',data,re.S):
        try:json.loads(text)
        except json.JSONDecodeError:errors.append(f'{p.name}: invalid JSON')
    if re.search(r'(lorem ipsum|example\.com|\b(?:TODO|undefined|NaN)\b)',data,re.I):errors.append(f'{p.name}: placeholder content')

tree=ET.parse(ROOT/'sitemap.xml')
locs=[x.text for x in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if locs:
    if len(locs)!=len(files)-1:errors.append('Sitemap page count mismatch')
    if any(not v.startswith('https://') or v.endswith('404.html') for v in locs):errors.append('Sitemap contains invalid URLs')
    if len(locs)!=len(set(locs)):errors.append('Duplicate sitemap URLs')
provinces=json.loads((ROOT/'content/provinces.json').read_text())
if len(provinces)!=81 or len(set(provinces))!=81:errors.append('Province list must have 81 unique entries')
videos=json.loads((ROOT/'content/site.json').read_text())['videos']
for v in videos:
    platform=v.get('platform')
    u=urlparse(v.get('url',''))
    if platform=='YouTube':
        if not re.fullmatch('[A-Za-z0-9_-]{11}',v['id']):errors.append('Invalid YouTube video ID')
        if u.netloc!='www.youtube.com' or u.path!='/shorts/'+v['id']:errors.append('Incorrect YouTube destination')
    elif platform=='Instagram':
        if u.netloc!='www.instagram.com' or u.path!='/kuklamuklatv/':errors.append('Incorrect Instagram account destination')
    else:errors.append('Unknown social video platform')
    if u.scheme!='https':errors.append('Social destination must use HTTPS')
    if not (ROOT/'assets/img/covers'/v['cover']).exists():errors.append('Missing local video cover')
if len({v['cover'] for v in videos})!=len(videos):errors.append('Social covers must be unique')
for name in ('index.html','videolar.html'):
    links=[a for t,a in parsed[name].tags if t=='a' and 'social-video' in a.get('class','').split()]
    if len(links)!=len(videos):errors.append(name+': missing social video cards')
    if any(a.get('target')!='_blank' or a.get('href') not in {v['url'] for v in videos} for a in links):errors.append(name+': social cards must open the supplied accounts or videos externally')
photos=json.loads((ROOT/'content/photos.json').read_text())
if not photos or len({p['id'] for p in photos})!=len(photos):errors.append('Photo entries must be nonempty and unique')
for photo in photos:
    for suffix in ('-480.webp','-960.webp','-large.webp'):
        if not (ROOT/'assets/img/photos'/(photo['file']+suffix)).exists():errors.append('Missing photo rendition: '+photo['file']+suffix)
    if not (ROOT/'gorseller-uhd'/(photo['file']+'.webp')).exists():errors.append('Missing large WebP download')
if re.search(r'createElement\([\'"]iframe|youtube(?:-nocookie)?\.com/embed', (ROOT/'assets/js/main.js').read_text()):errors.append('On-site video player code remains')
for css in (ROOT/'assets/css').glob('*.css'):
    for ref in re.findall(r'url\([\'"]?([^\)\'\"]+)',css.read_text()):
        if not ref.startswith('data:') and not (css.parent/ref).exists():errors.append('Missing CSS asset: '+ref)
if errors:
    print('\n'.join(errors),file=sys.stderr);raise SystemExit(1)
print(f'PASS · {len(files)} HTML pages · {len(provinces)} provinces · {len(videos)} external social cards · {len(photos)} photos · {len(locs)} sitemap URLs')
