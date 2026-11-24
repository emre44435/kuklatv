#!/usr/bin/env python3
"""Validate site pages, responsive assets, destinations and photo ownership."""
import json
import hashlib
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse,unquote

ROOT=Path(__file__).resolve().parents[1]
errors=[]
config=json.loads((ROOT/'content/site.json').read_text())
IG='https://www.instagram.com/kuklamuklatv/'
photos=json.loads((ROOT/'content/photos.json').read_text())
by_id={p['id']:p for p in photos}
expected_photo_count=int(config.get('photo_count',len(photos)))
uses=Counter()

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags=[];self.ids=set();self.title='';self.in_title=False
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs);self.tags.append((tag,attrs))
        if tag=='title':self.in_title=True
        if 'id' in attrs:
            if attrs['id'] in self.ids:errors.append('Duplicate ID: '+attrs['id'])
            self.ids.add(attrs['id'])
    def handle_endtag(self,tag):
        if tag=='title':self.in_title=False
    def handle_data(self,data):
        if self.in_title:self.title+=data

files=sorted(ROOT.glob('*.html'))
docs={p.name:Page() for p in files}
for p in files:docs[p.name].feed(p.read_text())

def local_target(ref,name):
    u=urlparse(ref)
    if u.scheme or u.netloc:
        site=urlparse(config.get('site_url') or '')
        # Actual build URL is present in the canonical tag even when supplied by the CI environment.
        canonical=next((a['href'] for t,a in docs[name].tags if t=='link' and a.get('rel')=='canonical'),None)
        if not canonical:return None,u
        site=urlparse(canonical)
        if u.netloc!=site.netloc:return None,u
        prefix=site.path.rsplit('/',1)[0]+'/' if site.path.endswith('.html') else site.path
        if not u.path.startswith(prefix):
            errors.append(name+': local URL escapes the publication path: '+ref)
            return None,u
        path=u.path[len(prefix):]
    else:
        path=u.path
    return ROOT/(unquote(path).removeprefix('./') or name),u

titles=set();descriptions=set()
for file in files:
    name=file.name;doc=docs[name];data=file.read_text()
    if sum(t=='h1' for t,a in doc.tags)!=1:errors.append(name+': expected one H1')
    if not doc.title.strip() or doc.title in titles:errors.append(name+': empty or duplicate title')
    titles.add(doc.title)
    desc=next((a.get('content') for t,a in doc.tags if t=='meta' and a.get('name')=='description'),None)
    if not desc or desc in descriptions:errors.append(name+': empty or duplicate description')
    descriptions.add(desc)
    if not any(t=='html' and a.get('lang')=='tr' for t,a in doc.tags):errors.append(name+': language missing')
    if any(t=='a' and ('download' in a or a.get('id')=='photo-download') for t,a in doc.tags):errors.append(name+': unexpected download control')
    for tag,a in doc.tags:
        if tag in ('form','textarea','select','iframe','video'):errors.append(name+': unexpected interactive content: '+tag)
        if tag=='input' and not (name=='hizmet-bolgeleri.html' and a.get('type')=='search'):errors.append(name+': unexpected input')
        if tag=='img' and not all(k in a for k in ('alt','width','height')):errors.append(name+': image dimensions or alternative text missing')
        if tag=='a':
            ref=a.get('href','');u=urlparse(ref)
            if u.scheme not in ('','http','https'):errors.append(name+': unsupported link protocol')
            if u.netloc and u.netloc not in ('www.instagram.com','www.youtube.com','policies.google.com',urlparse(next((x['href'] for t,x in doc.tags if t=='link' and x.get('rel')=='canonical'),'')).netloc):errors.append(name+': unexpected external destination')
            if u.netloc=='www.instagram.com' and (ref!=IG or a.get('target')!='_blank' or not {'noopener','noreferrer'}.issubset(set(a.get('rel','').split()))):errors.append(name+': invalid Instagram link')
            if a.get('target')=='_blank' and not {'noopener','noreferrer'}.issubset(set(a.get('rel','').split())):errors.append(name+': unsafe external link')
            if 'data-photo' in a:
                pid=a['data-photo'];uses[pid]+=1
                if pid not in by_id or by_id[pid]['page']!=name:errors.append(name+': incorrect photo ownership: '+pid)
        for key in ('href','src','data-full'):
            ref=a.get(key)
            if not ref or ref.startswith('data:'):continue
            target,u=local_target(ref,name)
            if target is None:continue
            if not target.exists():errors.append(name+': missing local target: '+ref)
            if u.fragment and target.suffix=='.html' and target.name in docs and u.fragment not in docs[target.name].ids:errors.append(name+': broken anchor: '+ref)
        if 'srcset' in a:
            for src in a['srcset'].split(','):
                parts=src.strip().split()
                if len(parts)!=2 or not re.fullmatch(r'\d+w',parts[1]):errors.append(name+': invalid srcset');continue
                target,_=local_target(parts[0],name)
                if target and not target.exists():errors.append(name+': missing responsive image: '+parts[0])
        if tag=='img' and 'real-photo' in a.get('class','').split():
            if not a.get('srcset') or not a.get('sizes') or a.get('loading')!='lazy':errors.append(name+': incomplete responsive photography')
    for script in re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>',data,re.S):
        try:json.loads(script)
        except json.JSONDecodeError:errors.append(name+': invalid structured data')

# The public touring scene must keep its automatic, decorative behavior.
for name in ('index.html','hizmet-bolgeleri.html'):
    doc=docs[name]
    if sum('data-auto-stage' in a for t,a in doc.tags)!=1:errors.append(name+': expected one automatic theatre')
    if any(a.get('id')=='motion-toggle' for t,a in doc.tags):errors.append(name+': unexpected manual animation control')
    if not any(t=='img' and 'data-stage-image' in a and a.get('srcset') for t,a in doc.tags):errors.append(name+': responsive theatre image missing')
    if any({'tour-route','tour-pin'} & set(a.get('class','').split()) for t,a in doc.tags):errors.append(name+': obsolete route decoration')

slider_rows=[a.get('data-direction') for t,a in docs['index.html'].tags if t=='div' and 'auto-slider-row' in a.get('class','').split()]
if slider_rows!=['left','right']:errors.append('Expected two opposing photo rows')
if not (ROOT/'components/ui/image-auto-slider.tsx').is_file():errors.append('React slider source missing')
if not (ROOT/'styles/globals.css').is_file():errors.append('Tailwind stylesheet source missing')

if any(p['page']!='index.html' for p in photos):errors.append('All real photographs must be on the home page')
if sum(t=='img' and 'real-photo' in a.get('class','').split() for t,a in docs['index.html'].tags)!=expected_photo_count:errors.append('Home page must display every real photograph exactly once')

if len(photos)!=expected_photo_count or len(by_id)!=expected_photo_count or len({p['source'] for p in photos})!=expected_photo_count:errors.append('Photographic source count mismatch')
if len({p.get('source_pixel_sha256') for p in photos})!=expected_photo_count:errors.append('Duplicate decoded photographic sources')
full_hashes=[hashlib.sha256((ROOT/'assets/img/photos'/p['full']).read_bytes()).hexdigest() for p in photos]
if len(set(full_hashes))!=expected_photo_count:errors.append('Duplicate full-size photographs')
if set(uses)!=set(by_id) or any(n!=1 for n in uses.values()):errors.append('Every photograph must appear in exactly one content position')
expected_files=set()
for p in photos:
    if p['width']>p['source_width'] or p['height']>p['source_height']:errors.append('An image was enlarged beyond its source')
    if len(p['renditions'])<2:errors.append('Responsive variants missing')
    for rendition in p['renditions']:
        expected_files.add(rendition['file'])
        if not (ROOT/'assets/img/photos'/rendition['file']).is_file():errors.append('Photographic asset missing: '+rendition['file'])
actual_files={p.name for p in (ROOT/'assets/img/photos').glob('*')}
if actual_files!=expected_files:errors.append('Unexpected or missing photographic assets')

provinces=json.loads((ROOT/'content/provinces.json').read_text())
if len(provinces)!=81 or len(set(provinces))!=81:errors.append('Expected 81 unique provinces')
for name in ['index.html','videolar.html']:
    links=[a for t,a in docs[name].tags if t=='a' and 'social-video' in a.get('class','').split()]
    if len(links)!=len(config['videos']):errors.append(name+': social cover count mismatch')
    if any(a.get('href') not in {v['url'] for v in config['videos']} or a.get('target')!='_blank' for a in links):errors.append(name+': invalid social video destination')
for css in (ROOT/'assets/css').glob('*.css'):
    for ref in re.findall(r'url\([\'\"]?([^\)\'\"]+)',css.read_text()):
        if not ref.startswith('data:') and not (css.parent/ref).exists():errors.append('Missing CSS asset: '+ref)
locs=[n.text for n in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if locs and (len(locs)!=len(files)-1 or len(locs)!=len(set(locs)) or any(not x.startswith('https://') or x.endswith('404.html') for x in locs)):errors.append('Invalid sitemap')
if errors:
    print('\n'.join(errors),file=sys.stderr)
    raise SystemExit(1)
print(f'PASS · {len(files)} pages · {expected_photo_count} unique photo placements · {len(actual_files)} responsive WebP files · 81 provinces · external Instagram and YouTube destinations')
