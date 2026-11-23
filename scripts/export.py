#!/usr/bin/env python3
"""Export public site only. Keep sources and documentation out of deployment."""
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
out=ROOT/'_site'
if out.exists():shutil.rmtree(out)
out.mkdir()
for p in list(ROOT.glob('*.html'))+[ROOT/'robots.txt',ROOT/'sitemap.xml',ROOT/'site.webmanifest',ROOT/'.nojekyll']:
    shutil.copy2(p,out/p.name)
shutil.copytree(ROOT/'assets',out/'assets')
if (ROOT/'gorseller-uhd').exists():shutil.copytree(ROOT/'gorseller-uhd',out/'gorseller-uhd')
if (ROOT/'CNAME').exists():shutil.copy2(ROOT/'CNAME',out/'CNAME')
print('Public site exported to _site/')
