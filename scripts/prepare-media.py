#!/usr/bin/env python3
"""Technical WebP exports from supplied photos, without generative face redraw."""
import concurrent.futures
import json
import subprocess
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
UPLOAD=ROOT.parent/'upload'
PHOTOS=json.loads((ROOT/'content/photos.json').read_text())
WEB=ROOT/'assets/img/photos'
MASTER=ROOT/'gorseller-uhd'
ORIGINAL=ROOT/'gorseller-orijinal'
for p in (WEB,MASTER,ORIGINAL):p.mkdir(parents=True,exist_ok=True)

def run(src,dest,*args):
    subprocess.run(['convert',str(src),'-auto-orient',*args,'-strip','-define','webp:method=5','-quality','91',str(dest)],check=True,capture_output=True)

def geometry(width,height,aspect,focal):
    if width/height>aspect:ch=height;cw=round(ch*aspect)
    else:cw=width;ch=round(cw/aspect)
    x=max(0,min(width-cw,round(width*focal[0]-cw/2)))
    y=max(0,min(height-ch,round(height*focal[1]-ch/2)))
    return f'{cw}x{ch}+{x}+{y}'

def photo(item):
    src=UPLOAD/item['source'];stem=item['file']
    w,h=Image.open(src).size
    # Remove the screenshot viewer's side controls and pagination through edge cropping.
    # This does not reconstruct a face or change facial geometry.
    left=36;right=36;bottom=28
    clean=WEB/(stem+'-source.webp')
    run(src,clean,'-crop',f'{w-left-right}x{h-bottom}+{left}+0','+repage','-gamma','1.025','-unsharp','0x0.45+0.3+0.02')
    cw,ch=Image.open(clean).size
    for width,height in ((480,640),(960,1280)):
        run(clean,WEB/f'{stem}-{width}.webp','-crop',geometry(cw,ch,3/4,item['focal']),'+repage','-filter','Lanczos','-resize',f'{width}x{height}!')
    run(clean,WEB/(stem+'-large.webp'),'-filter','Lanczos','-resize','1920x1920')
    run(clean,MASTER/(stem+'.webp'),'-filter','Lanczos','-resize','3840x3840')
    run(src,ORIGINAL/(stem+'.webp'))
    clean.unlink()
    print(f'photo {item["id"]} WebP ready',flush=True)

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
    list(pool.map(photo,PHOTOS))

hero=UPLOAD/'6e97f5ad-548f-4eea-9b0a-5dd8d018f2ae.png'
for width,height in ((640,800),(1280,1600)):
    run(hero,ROOT/f'assets/img/ali-abi-zoyo-hero-{width}.webp','-filter','Lanczos','-resize',f'{width}x{height}!')
run(hero,MASTER/'00-ali-abi-zoyo-banner.webp','-filter','Lanczos','-resize','3840x3840')
run(hero,ORIGINAL/'00-ali-abi-zoyo-banner.webp')

features=[('stage.webp','18',(.55,.44)),('festival.webp','12',(.52,.42)),('special.webp','09',(.49,.40))]
byid={p['id']:p for p in PHOTOS}
for out,key,focal in features:
    src=WEB/(byid[key]['file']+'-large.webp');w,h=Image.open(src).size
    run(src,ROOT/'assets/img'/out,'-crop',geometry(w,h,4/3,focal),'+repage','-filter','Lanczos','-resize','1200x900!')
src=WEB/(byid['14']['file']+'-large.webp');w,h=Image.open(src).size
run(src,ROOT/'assets/img/ali-cengiz-portre.webp','-crop',geometry(w,h,4/5,(.45,.45)),'+repage','-filter','Lanczos','-resize','1200x1500!')
w,h=Image.open(hero).size
run(hero,ROOT/'assets/img/social-cover.webp','-crop',geometry(w,h,1200/630,(.52,.43)),'+repage','-filter','Lanczos','-resize','1200x630!')
print('hero, feature images and UHD exports ready',flush=True)
