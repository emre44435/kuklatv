#!/usr/bin/env python3
"""Optional, conservative photo preparation from the supplied JPEG originals.

Only run when replacing photographic assets. Normal site builds use the
already prepared WebP files and need no imaging dependency.
"""
import argparse
import json
import math
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--source-dir', required=True, type=Path)
parser.add_argument('--ids', nargs='*', help='Prepare only the selected photo IDs; existing files stay untouched')
args = parser.parse_args()
manifest = ROOT/'content/photos.json'
photos = json.loads(manifest.read_text())
out = ROOT/'assets/img/photos'
out.mkdir(exist_ok=True)

for photo in photos:
    if args.ids and photo['id'] not in args.ids:
        continue
    with Image.open(args.source_dir/photo['source']) as original:
        im = ImageOps.exif_transpose(original).convert('RGB')
        photo['source_width'], photo['source_height'] = im.size
    adjustments = photo['adjustments']
    if adjustments['crop']:
        im = im.crop(tuple(adjustments['crop']))
    angle = adjustments.get('rotation', 0)
    if angle:
        w,h = im.size
        radians = math.radians(abs(angle))
        cosine,sine = math.cos(radians),math.sin(radians)
        scale = min(w/(w*cosine+h*sine),h/(w*sine+h*cosine))
        im = im.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        cw,ch = int(w*scale)-2,int(h*scale)-2
        left,top = (im.width-cw)//2,(im.height-ch)//2
        im = im.crop((left,top,left+cw,top+ch))
    # Global channel gains preserve all captured detail, expressions and shapes.
    gains = adjustments['white_balance']
    im = Image.merge('RGB', tuple(channel.point([min(255,round(v*gain)) for v in range(256)])
                                 for channel,gain in zip(im.split(),gains)))
    im = ImageEnhance.Brightness(im).enhance(adjustments['brightness'])
    im = ImageEnhance.Contrast(im).enhance(adjustments['contrast'])
    im = ImageEnhance.Color(im).enhance(adjustments['color'])
    # No reconstruction, face filters, skin smoothing, or artificial sharpening.
    im.thumbnail((1600,1600), Image.Resampling.LANCZOS)
    photo['width'],photo['height'] = im.size
    renditions=[]
    for width in sorted({min(480,im.width),min(960,im.width),im.width}):
        height=round(im.height*width/im.width)
        rendition=im if width==im.width else im.resize((width,height),Image.Resampling.LANCZOS)
        filename=f"{photo['file']}-{width}.webp"
        quality = photo.get('quality', {})
        rendition.save(out/filename, 'WEBP', quality=quality.get('full',87) if width==im.width else quality.get('responsive',84), method=6)
        renditions.append({'file':filename,'width':width,'height':height})
    photo['renditions']=renditions
    photo['full']=renditions[-1]['file']
    print(f"{photo['id']}: {photo['source_width']}x{photo['source_height']} -> {im.width}x{im.height}")

manifest.write_text(json.dumps(photos,ensure_ascii=False,indent=2)+'\n')
print(f'{len(photos)} photos; {sum(len(p["renditions"]) for p in photos)} responsive WebP files.')
