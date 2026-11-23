#!/usr/bin/env python3
"""Dependency-free static renderer. Rebuild after editing content/*.json."""
import argparse
import html
import json
import os
from pathlib import Path
from urllib.parse import urlparse
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--url', default=None, help='Actual HTTPS publication URL, including any repository path')
args = parser.parse_args()

def read_json(path):
    return json.loads((ROOT/path).read_text(encoding='utf-8'))

config = read_json('content/site.json')
pages = read_json('content/pages.json')
provinces = read_json('content/provinces.json')
photos = read_json('content/photos.json')
icons = read_json('content/icons.json')
scene_markup = (ROOT/'content/cartoon-scene.html').read_text()
site_url = (args.url if args.url is not None else os.environ.get('SITE_URL') or config['site_url']).strip().rstrip('/')
if site_url:
    parsed = urlparse(site_url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
        raise SystemExit('Yayın adresi geçerli bir HTTPS adresi olmalı.')

IG = config['instagram']
IG_DESCRIPTION = 'Ayrıntılı bilgi için Instagram hesabımızdan bize mesaj atın.'
photo_by_id = {p['id']:p for p in photos}
photo_uses = {}
rendered = []


def esc(value):
    return html.escape(str(value), quote=True)


def link(path=''):
    return f'{site_url}/{path}' if site_url else f'./{path or "index.html"}'


def icon(name, cls=''):
    spec = icons[name]
    attrs = 'fill="currentColor"' if spec.get('brand') else 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    nodes = ''.join('<'+tag+' '+' '.join(f'{k}="{esc(v)}"' for k,v in props.items())+' />' for tag,props in spec['nodes'])
    return f'<svg class="icon {esc(cls)}" width="24" height="24" viewBox="{esc(spec.get("viewBox","0 0 24 24"))}" {attrs} aria-hidden="true" focusable="false">{nodes}</svg>'


def instagram(text='Instagram’dan mesaj atın', style='primary'):
    return f'<a class="button button--{style}" href="{esc(IG)}" target="_blank" rel="noopener noreferrer">{icon("Instagram")}<span>{esc(text)}</span><span class="sr-only"> (yeni sekme)</span></a>'


def button(text, path=None, style='primary', name='Instagram'):
    if path is None:
        return instagram(text, style)
    return f'<a class="button button--{style}" href="{esc(link(path))}">{icon(name)}<span>{esc(text)}</span></a>'


def socials():
    return ''.join(f'<a href="{esc(config[key])}" target="_blank" rel="noopener noreferrer" aria-label="kuklamukla TV {title} hesabı (yeni sekme)">{icon(title)}</a>' for key,title in [('instagram','Instagram'),('youtube','Youtube')])


def floating_contacts():
    return f'<aside class="floating-socials" aria-label="Instagram’dan bize ulaşın"><a class="quick-contact quick-instagram" href="{esc(IG)}" target="_blank" rel="noopener noreferrer" aria-label="Instagram’dan mesaj atın: kuklamukla TV (yeni sekme)"><span class="quick-tip">Instagram’dan mesaj atın</span>{icon("Instagram")}</a></aside>'


def logo():
    return f'<a class="brand brand--image" href="{link()}" aria-label="kuklamukla TV · Ali Abi ve Zoyo, ana sayfa"><img src="{link("assets/img/kuklamukla-tv-logo-480.webp")}" alt="kuklamukla TV · Ali Abi ve Zoyo" width="960" height="320" decoding="async"></a>'


def header(active=''):
    return f'''<a class="skip-link" href="#icerik">İçeriğe geç</a>
    <div class="topline"><div class="container"><span>{icon('MapPin')} Türkiye’nin 81 ilinde kukla gösterisi</span><a href="{esc(IG)}" target="_blank" rel="noopener noreferrer">Instagram’da bize ulaşın</a></div></div>
    <header class="site-header"><div class="container header-inner">{logo()}
    <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Menüyü aç">{icon('Menu')}<span>Menü</span></button>
    <nav id="main-nav" class="main-nav" aria-label="Ana menü">
    <a href="{link('ali-cengiz.html')}" {'aria-current="page"' if active=='ali-cengiz' else ''}>Ali Abi &amp; Zoyo</a>
    <details class="nav-dropdown"><summary>Gösteriler {icon('ChevronDown')}</summary><div class="nav-dropdown-content">
    <a href="{link('kukla-gosterisi.html')}">{icon('Theater')}Kukla gösterisi</a>
    <a href="{link('okullarda-kukla-gosterisi.html')}">{icon('School')}Okullar için</a>
    <a href="{link('belediye-kukla-gosterisi.html')}">{icon('Landmark')}Belediyeler için</a>
    <a href="{link('23-nisan-kukla-gosterisi.html')}">{icon('PartyPopper')}23 Nisan &amp; özel günler</a>
    <a href="{link('cocuk-tiyatrosu.html')}">{icon('Ticket')}Çocuklar için kukla tiyatrosu</a></div></details>
    <a href="{link('videolar.html')}" {'aria-current="page"' if active=='videolar' else ''}>Videolar</a>
    <a href="{link('index.html#fotograflar')}" {'aria-current="page"' if active=='fotograflar' else ''}>Fotoğraflar</a>
    <a href="{link('hizmet-bolgeleri.html')}" {'aria-current="page"' if active=='hizmet-bolgeleri' else ''}>81 ilde gösteri</a>
    {instagram('Instagram’dan mesaj atın','small')}</nav></div></header>'''


def footer():
    return f'''<footer class="site-footer"><div class="container footer-grid"><div>{logo()}<p>Bir kukla, bir ses, birlikte atılan kahkahalar.<br> Ali Abi ve Zoyo’yla sahnede buluşalım.</p><div class="socials">{socials()}</div></div>
    <div><h2>Gösteriler</h2><a href="{link('kukla-gosterisi.html')}">Kukla gösterisi</a><a href="{link('okullarda-kukla-gosterisi.html')}">Okullar için gösteri</a><a href="{link('belediye-kukla-gosterisi.html')}">Belediye etkinlikleri</a><a href="{link('cocuk-tiyatrosu.html')}">Çocuklar için kukla tiyatrosu</a><a href="{link('23-nisan-kukla-gosterisi.html')}">23 Nisan etkinlikleri</a></div>
    <div><h2>Tanışalım</h2><a href="{link('ali-cengiz.html')}">Ali Cengiz &amp; Zoyo</a><a href="{link('videolar.html')}">Gösteri videoları</a><a href="{link('index.html#fotograflar')}">Fotoğraflar</a><a href="{link('hizmet-bolgeleri.html')}">81 ilde gösteri</a><a href="{link('sik-sorulan-sorular.html')}">Sık sorulan sorular</a><a href="{link('kukla-gosterisi-planlama.html')}">Etkinlik rehberi</a></div>
    <div><h2>Instagram’da buluşalım</h2><p>{IG_DESCRIPTION}</p><a class="footer-contact" href="{esc(IG)}" target="_blank" rel="noopener noreferrer">{icon('Instagram')} Instagram’dan mesaj atın</a><a href="{link('iletisim.html')}">İletişim</a></div></div>
    <div class="container footer-bottom"><span>© <span data-year>2026</span> Ali Cengiz · kuklamukla TV</span><span><a href="{link('gizlilik.html')}">Gizlilik &amp; çerezler</a><span>Çocuklar için, sevgiyle.</span>{icon('Heart')}</span></div></footer>'''


common_faqs = [
    ['Zoyo’yu kim seslendirip oynatıyor?', 'Zoyo’yu kukla sanatçısı Ali Cengiz seslendiriyor ve oynatıyor. Çocuklar onu sahnede Ali Abi olarak tanıyor.'],
    ['Hangi şehirlerde kukla gösterisi yapılabiliyor?', 'Ali Abi ve Zoyo, Türkiye’nin 81 ilinde çocuklarla buluşabiliyor. Gösteriler hakkında ayrıntılı bilgi için Instagram hesabımızdan bize mesaj atın.'],
    ['Okullarda ve çocuk şenliklerinde gösteri yapılıyor mu?', 'Evet. Anaokulları, ilkokullar, belediye etkinlikleri, kültür merkezleri ve çocuk şenlikleri için kukla gösterisi yapılabiliyor.'],
    ['Gösteriler hakkında nasıl bilgi alabilirim?', IG_DESCRIPTION],
    ['Gösterinin süresi nasıl belirleniyor?', 'Gösteri süresi çocukların yaş grubu ve etkinlik akışına göre birlikte değerlendirilir. Gösteri hakkında ayrıntılı bilgi için Instagram hesabımızdan bize mesaj atın.'],
    ['Videoları nereden izleyebilirim?', 'Videolar bölümündeki kapaklar ilgili YouTube videosunu veya Instagram hesabımızı yeni sekmede açar. İzlemeye ilgili platformda devam edebilirsiniz.']
]


def faq_html(faqs):
    return '<div class="faq-list">'+''.join(f'<details><summary>{esc(q)}{icon("ChevronDown")}</summary><div><p>{esc(a)}</p></div></details>' for q,a in faqs)+'</div>'


def faq_schema(faqs):
    return {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}


def photo_media(photo_id, page, sizes='(max-width:600px) calc(100vw - 40px), (max-width:1120px) 44vw, 360px'):
    p = photo_by_id[photo_id]
    if p['page'] != page or photo_id in photo_uses:
        raise SystemExit(f'Fotoğrafın tekil konumu doğrulanamadı: {photo_id}')
    photo_uses[photo_id] = page
    prefix = 'assets/img/photos/'
    variants = p['renditions']
    default = next((r for r in variants if r['width']>=min(960,p['width'])),variants[-1])
    srcset = ', '.join(f'{link(prefix+r["file"])} {r["width"]}w' for r in variants)
    return f'''<a class="photo-launch" href="{link(prefix+p['full'])}" data-photo="{p['id']}" data-title="{esc(p['title'])}" data-alt="{esc(p['alt'])}" data-width="{p['width']}" data-height="{p['height']}" aria-label="{esc(p['title'])} fotoğrafını büyüt">
    <img class="real-photo" src="{link(prefix+default['file'])}" srcset="{srcset}" sizes="{esc(sizes)}" alt="{esc(p['alt'])}" width="{p['width']}" height="{p['height']}" loading="lazy" decoding="async"><span class="photo-zoom">{icon('Search')}<span>Büyüt</span></span></a>'''


def photo_figure(photo_id, page, cls='', sizes='(max-width:600px) calc(100vw - 40px), (max-width:1120px) 44vw, 360px'):
    p=photo_by_id[photo_id]
    return f'<figure class="photo-card {esc(cls)}" id="foto-{esc(photo_id)}" data-photo-item data-category="{esc(p["category"])}">{photo_media(photo_id,page,sizes)}<figcaption><span>{esc(p["category"])}</span><strong>{esc(p["title"])}</strong></figcaption></figure>'


def photo_dialog():
    return f'''<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-title"><div class="photo-dialog-inner"><div class="photo-dialog-top"><h2 id="photo-title">Gösterilerden bir kare</h2><button class="icon-button" data-close-photo type="button" aria-label="Fotoğrafı kapat">{icon('X')}</button></div><div class="photo-viewer-media"><img id="photo-full" alt="" width="1600" height="1200"></div><div class="photo-dialog-bottom"><div class="photo-navigation"><button class="icon-button" data-prev-photo type="button" aria-label="Önceki fotoğraf">{icon('ChevronLeft')}</button><span id="photo-position" aria-live="polite"></span><button class="icon-button" data-next-photo type="button" aria-label="Sonraki fotoğraf">{icon('ChevronRight')}</button></div><a id="photo-download" href="{link('index.html#fotograflar')}" download>WebP indir</a></div></div></dialog>'''


def video_cards():
    items=[]
    for v in config['videos']:
        platform=v['platform']
        brand='Youtube' if platform=='YouTube' else 'Instagram'
        action='YouTube’da izle' if platform=='YouTube' else 'Instagram’da aç'
        items.append(f'''<article class="video-card"><a class="video-launch social-video" href="{esc(v['url'])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(v['title'])} · {action} (yeni sekme)"><img src="{link('assets/img/covers/'+v['cover'])}" alt="Ali Abi ve Zoyo karakterleriyle {esc(v['title'])} tanıtım kapağı" width="960" height="1280" loading="lazy" decoding="async"><span class="video-badge platform-{platform.lower()}">{icon(brand)} {platform}</span><span class="video-brand">kuklamukla TV</span><span class="video-info"><span>{esc(v['label'])}</span><strong>{esc(v['title'])}</strong><span class="media-action">{icon('Play')}{action}</span></span></a></article>''')
    return '<p class="media-rail-note">Kapakları kaydırın, neşeye katılın.</p><div class="video-grid">'+''.join(items)+'</div>'


def cta():
    return f'''<section class="section cta-section"><div class="container cta-panel"><div class="cta-doodle" aria-hidden="true">{icon('Sparkles')}</div><div><span class="eyebrow">BİR MERHABAYLA BAŞLAYALIM</span><h2>Instagram’da buluşalım.</h2><p>{IG_DESCRIPTION}</p></div>{instagram(style='light')}</div></section>'''


def tour_visual(hero=False):
    return ((ROOT/'content/tour-scene.html').read_text()
            .replace('TOUR_IMAGE_SMALL', link('assets/img/ali-abi-zoyo-hero-640.webp'))
            .replace('TOUR_IMAGE_LARGE', link('assets/img/ali-abi-zoyo-hero-1280.webp'))
            .replace('loading="lazy"', 'fetchpriority="high"' if hero else 'loading="lazy"'))


def tour_banner(regions_page=False, hero=False):
    title = 'Şehirler farklı,<span>neşemiz ortak.</span>' if regions_page else 'Sıradaki durak,<span>sizin şehriniz.</span>'
    heading = 'h1' if hero else 'h2'
    variant = ' tour-banner--hero' if hero else ''
    return f'''<section class="tour-banner{variant}" id="turkiye-geneli" data-auto-stage aria-labelledby="tour-title">
    <div class="tour-light tour-light--one" aria-hidden="true"></div><div class="tour-light tour-light--two" aria-hidden="true"></div>
    <div class="container tour-grid">{tour_visual(hero=hero)}
    <div class="tour-copy"><span class="tour-eyebrow">ALİ ABİ &amp; ZOYO · TÜRKİYE GENELİNDE</span>
    <{heading} id="tour-title">{title}</{heading}><p class="tour-description">{IG_DESCRIPTION}</p>
    <div class="tour-actions"><a class="tour-instagram" href="{esc(IG)}" target="_blank" rel="noopener noreferrer">{icon("Instagram")}<span>Instagram’dan mesaj atın</span><span class="sr-only"> (yeni sekme)</span></a></div>
    <p class="tour-note">Çocuklar için, sevgiyle.</p><div class="tour-audiences"><span>Okullarda</span><span>Belediye etkinliklerinde</span><span>Çocuk şenliklerinde</span></div></div></div>
    <svg class="tour-wave" viewBox="0 0 1440 100" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path d="M0 66C250 0 382 110 640 62S1050 10 1250 59 1390 62 1440 37V100H0Z"/></svg></section>'''


def page_intro(eyebrow,title,intro):
    return f'<section class="page-intro">{scene_markup}<div class="container"><nav class="breadcrumbs" aria-label="Sayfa yolu"><a href="{link()}">Ana sayfa</a>{icon("ChevronRight")}<span>{esc(eyebrow.capitalize())}</span></nav><span class="eyebrow">{esc(eyebrow)}</span><h1>{title}</h1><p>{esc(intro)}</p></div></section>'


def layout(filename,title,description,body,active='',extra_schema=None,noindex=False):
    canonical=link('' if filename=='index.html' else filename) if site_url else ''
    image=link('assets/img/social-cover.webp') if site_url else ''
    ld={'@context':'https://schema.org','@graph':[]}
    if site_url:
        ld['@graph']=[
            {'@type':'Person','@id':site_url+'/#ali-cengiz','name':'Ali Cengiz','alternateName':'Ali Abi','jobTitle':'Kukla sanatçısı','url':link('ali-cengiz.html'),'sameAs':[IG,config['youtube']]},
            {'@type':'WebSite','@id':site_url+'/#website','name':'kuklamukla TV · Ali Abi ve Zoyo','url':link(),'inLanguage':'tr-TR','publisher':{'@id':site_url+'/#ali-cengiz'}},
            {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'inLanguage':'tr-TR','isPartOf':{'@id':site_url+'/#website'}}]
    if extra_schema:
        ld['@graph']+=extra_schema
    canonical_tag=f'<link rel="canonical" href="{esc(canonical)}"><meta property="og:url" content="{esc(canonical)}">' if canonical else ''
    social_image=f'<meta property="og:image" content="{esc(image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Ali Abi ve Zoyo kukla gösterisi tanıtım illüstrasyonu"><meta name="twitter:card" content="summary_large_image">' if image else '<meta name="twitter:card" content="summary">'
    styles=''.join(f'<link rel="stylesheet" href="{link("assets/css/"+name+".css")}">' for name in ['style','cartoon','media','refined','engagement','revision','tour','harmony'])
    ld_text=json.dumps(ld,ensure_ascii=False).replace('<','\\u003c')
    output=f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"><meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}"><meta name="theme-color" content="#665697"><meta name="referrer" content="strict-origin-when-cross-origin">
{canonical_tag}<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:site_name" content="kuklamukla TV"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">{social_image}
<link rel="icon" href="{link('assets/icons/favicon.svg')}" type="image/svg+xml"><link rel="icon" href="{link('assets/icons/favicon.png')}" type="image/png"><link rel="apple-touch-icon" href="{link('assets/icons/apple-touch-icon.png')}"><link rel="manifest" href="{link('site.webmanifest')}">
<link rel="preload" href="{link('assets/fonts/fredoka-600.ttf')}" as="font" type="font/ttf" crossorigin><link rel="preload" href="{link('assets/fonts/nunito-sans-400.ttf')}" as="font" type="font/ttf" crossorigin>
{styles}<script src="{link('assets/js/main.js')}" defer></script><script type="application/ld+json">{ld_text}</script></head>
<body class="cartoon-theme">{header(active)}<main id="icerik">{body}</main>{footer()}{floating_contacts()}{photo_dialog()}<div id="live-status" class="sr-only" role="status" aria-live="polite"></div></body></html>'''
    (ROOT/filename).write_text(output,encoding='utf-8')
    rendered.append(filename)


# Home: each photograph belongs only to this one content position.
programs=[('04','school','School','Okullar için','Anaokulu ve ilkokul etkinliklerinde Ali Abi ve Zoyo çocuklarla buluşsun.','okullarda-kukla-gosterisi.html','Okul gösterisini inceleyin'),('07','city','Landmark','Belediyeler için','Kültür merkezlerinde ve çocuk şenliklerinde şehrin çocuklarıyla bir araya gelelim.','belediye-kukla-gosterisi.html','Belediye gösterisini inceleyin'),('10','special','PartyPopper','23 Nisan & özel günler','Çocukların bayramına, okul şenliğine ve özel etkinliğinize neşe katalım.','23-nisan-kukla-gosterisi.html','Özel günleri inceleyin')]
program_cards=''.join(f'<article class="program-card program-card--{kind}" id="foto-{pid}" data-photo-item><div class="program-image">{photo_media(pid,"index.html","(max-width:760px) calc(100vw - 40px), 30vw")}<span>{icon(symbol)}</span></div><div class="program-copy"><h3>{esc(title)}</h3><p>{esc(text)}</p><a href="{link(path)}">{esc(action)}</a></div></article>' for pid,kind,symbol,title,text,path,action in programs)
home_gallery_photos=[p for p in photos if p['id'] not in {'04','07','10','12'}]
home_gallery_cards=''.join(photo_figure(p['id'],'index.html',sizes='(max-width:359px) calc(100vw - 40px), (max-width:600px) calc((100vw - 54px) / 2), (max-width:900px) 44vw, 360px') for p in home_gallery_photos)
home_gallery=f'''<section class="section photo-section home-photo-gallery" id="fotograflar" data-photo-gallery><div class="container"><div class="section-heading"><div><span class="eyebrow">BİRLİKTE YAŞANAN ANLAR</span><h2>Sahneden gerçek hatıralar.</h2></div><p>Okullarda, salonlarda, şenliklerde…<br>Birlikte güldüğümüz buluşmalardan.</p></div><div class="gallery-filters js-only" role="group" aria-label="Fotoğraf kategorileri"><button class="gallery-filter" type="button" data-photo-filter="Tümü" aria-pressed="true">Tümü</button><button class="gallery-filter" type="button" data-photo-filter="Sahne" aria-pressed="false">Sahne</button><button class="gallery-filter" type="button" data-photo-filter="Buluşmalar" aria-pressed="false">Buluşmalar</button></div><p class="photo-count" id="photo-count" role="status">{len(home_gallery_photos)} fotoğraf</p><div class="photo-grid">{home_gallery_cards}</div></div></section>'''
home=f'''
{tour_banner(hero=True)}
<section class="home-intro">{scene_markup}<div class="container home-intro-grid"><div><span class="eyebrow">ALİ CENGİZ · KUKLA SANATÇISI</span><h2>Bir kukla, bir ses.<br>Birlikte atılan kahkahalar.</h2></div><div class="home-intro-copy"><p>Ali Abi ve Zoyo; okullarda, belediye etkinliklerinde ve çocuk şenliklerinde çocuklarla buluşuyor.</p><a class="text-link" href="{link('videolar.html')}">{icon('Play')} Zoyo’yu izleyin</a></div></div></section>
<div class="audience-strip"><div class="container"><span>{icon('School')}Okul etkinlikleri</span><span>{icon('Landmark')}Belediye programları</span><span>{icon('Theater')}Çocuk şenlikleri</span><span>{icon('MapPin')}Türkiye’nin 81 ili</span></div></div>
<section class="section" id="gosteriler"><div class="container"><div class="section-heading"><div><span class="eyebrow">BİRLİKTE BULUŞALIM</span><h2>Her buluşmada bir kahkaha.</h2></div><p>Okulda, kültür merkezinde, şenlikte…<br> Ali Abi ve Zoyo’yla gösteri zamanı.</p></div><div class="program-grid">{program_cards}</div></div></section>
<section class="section about-section"><div class="container about-grid">{photo_figure('12','index.html','feature-photo')}<div class="about-copy"><span class="eyebrow">SAHNEDE İKİ DOST</span><h2>Sahnede Ali Cengiz,<br> yanında Zoyo.</h2><p>Ali Cengiz, Zoyo’yu seslendiren ve oynatan bir kukla sanatçısı. Sahnedeki adıyla Ali Abi, çocuklarla canlı gösterilerde buluşuyor.</p><p>Turuncu tüyleri, mavi burnu ve merakıyla Zoyo; Ali Abi’nin sesi ve elleriyle sahnede canlanıyor.</p><a class="text-link" href="{link('ali-cengiz.html')}">Ali Abi ve Zoyo’yu tanıyın</a><a class="text-link" href="{link('index.html#fotograflar')}">Gösterilerden fotoğraflar</a></div></div></section>
{home_gallery}
<section class="section videos-section" id="videolar"><div class="container"><div class="section-heading"><div><span class="eyebrow">kuklamukla TV</span><h2>Biraz Zoyo, bolca neşe.</h2></div><a class="text-link text-link--light" href="{link('videolar.html')}">Gösteri videolarını keşfedin</a></div><p class="section-lead">YouTube ve Instagram’da neşeli anlar. İzlemek için bir kapak seçin.</p>{video_cards()}<p class="video-privacy">Kapaklar sizi YouTube veya Instagram’a götürür.</p></div></section>
<section class="section faq-section"><div class="container faq-grid"><div><span class="eyebrow">AKLINIZDAKİLER</span><h2>Birkaç küçük<br> soru, açık cevaplar.</h2><p>Gösteriler hakkında merak ettikleriniz.</p><a class="text-link" href="{link('sik-sorulan-sorular.html')}">Tüm soruları görün</a></div>{faq_html(common_faqs[:4])}</div></section>{cta()}'''
layout('index.html','Ali Cengiz | Ali Abi ve Zoyo Kukla Gösterisi · kuklamukla TV',config['description'],home,extra_schema=[faq_schema(common_faqs[:4])])

service_titles={p['slug']:p['eyebrow'].capitalize() for p in pages}
service_titles.update({'hizmet-bolgeleri':'81 ilde gösteri','iletisim':'İletişim'})
for page in pages:
    name=page['slug']+'.html'
    related=''.join(f'<a href="{link(s+".html")}">{esc(service_titles[s])}</a>' for s in page['related'])
    body=page_intro(page['eyebrow'],esc(page['title']),page['intro'])
    body+=f'<section class="section detail-section"><div class="container detail-grid"><article class="prose">'
    body+=''.join(f'<section><h2>{esc(s["title"])}</h2><p>{esc(s["text"])}</p></section>' for s in page['sections'])
    body+=f'<section><h2>Sık sorulanlar</h2>{faq_html(page["faqs"])}</section><section><h2>İlgili sayfalar</h2><div class="related-links">{related}</div></section></article><aside class="detail-aside">'
    body+=''.join(photo_figure(pid,name,'detail-photo','(max-width:760px) calc(100vw - 40px), 360px') for pid in page['photos'])
    body+=f'<div class="aside-card">{icon(page["icon"])}<h2>Instagram’da buluşalım.</h2><p>{IG_DESCRIPTION}</p>{instagram()}<span>{icon("MapPin")} Türkiye’nin 81 ilinde</span></div></aside></div></section>{cta()}'
    schema=[faq_schema(page['faqs'])]
    if site_url:
        schema.append({'@type':'Service','name':page['seo_title'].split('|')[0].strip(),'description':page['description'],'serviceType':'Kukla gösterisi','areaServed':{'@type':'Country','name':'Türkiye'},'provider':{'@id':site_url+'/#ali-cengiz'},'url':link(name)})
    layout(name,page['seo_title'],page['description'],body,page['slug'],schema)

about=page_intro('ALİ CENGİZ & ZOYO','Ali Abi’yle tanışın.','Zoyo’nun sesi ve sahnedeki yol arkadaşı: kukla sanatçısı Ali Cengiz.')
about+=f'''<section class="section"><div class="container about-grid"><aside class="artist-note">{icon('Theater')}<span class="eyebrow">ALİ ABİ &amp; ZOYO</span><strong>Bir sahne,<br>iki yol arkadaşı.</strong><a class="text-link" href="{link('index.html#foto-06')}">Ali Abi ve Zoyo’nun fotoğrafını görün</a></aside><div class="prose"><span class="eyebrow">SAHNENİN ARKASINDAKİ İSİM</span><h2>Ali Cengiz, çocukların Ali Abisi.</h2><p>Ali Cengiz bir kukla sanatçısı. Kuklası Zoyo’yu seslendiriyor ve oynatıyor. Sahnedeki adıyla Ali Abi, Zoyo ile birlikte çocuklara canlı kukla gösterisi sunuyor.</p><p>Okullar, belediyeler ve çocuklara yönelik etkinlikler için Türkiye’nin 81 ilinde çocuklarla buluşabiliyor.</p><p>{IG_DESCRIPTION}</p>{instagram()}</div></div></section>
<section class="section artist-story"><div class="container about-grid"><div class="about-copy"><span class="eyebrow">BİRLİKTE GÜLÜNEN ANLAR</span><h2>Zoyo’nun dünyası,<br> çocukların merakı.</h2><p>Gösterinin merkezinde canlı bir buluşma var. Zoyo’nun sesini duyan, hareketlerini izleyen çocuklar Ali Abi’yle aynı hikâyenin içinde yer alıyor.</p><p>kuklamukla TV’de bu dünyayı ekran başında da keşfedebilirsiniz.</p>{button('Zoyo’nun videoları','videolar.html','outline','Play')}</div><aside class="artist-note artist-note--light">{icon('School')}<span class="eyebrow">ÇOCUKLARLA BİRLİKTE</span><strong>Her buluşmada<br>yeni bir kahkaha.</strong><a class="text-link" href="{link('index.html#foto-18')}">Sınıftaki buluşmayı görün</a></aside></div></section>{cta()}'''
layout('ali-cengiz.html','Ali Cengiz Kimdir? | Kukla Sanatçısı Ali Abi ve Zoyo','Zoyo’yu seslendiren ve oynatan kukla sanatçısı Ali Cengiz ile tanışın. Ali Abi ve Zoyo, Türkiye genelinde çocuklarla kukla gösterilerinde buluşuyor.',about,'ali-cengiz')

videos=page_intro('kuklamukla TV','Zoyo’yu izlemeye ne dersiniz?','YouTube ve Instagram paylaşımlarından neşeli anlar. Bir kapak seçin; ilgili platformda izlemeye devam edin.')
videos+=f'<section class="section videos-section videos-page"><div class="container">{video_cards()}<p class="video-privacy">Kapaklar ilgili YouTube videosunu veya Instagram hesabımızı yeni sekmede açar.</p></div></section>{cta()}'
video_schema={'@type':'ItemList','name':'kuklamukla TV YouTube ve Instagram paylaşımları','itemListElement':[{'@type':'ListItem','position':i+1,'name':v.get('full_title',v['title']),'url':v['url']} for i,v in enumerate(config['videos'])]}
layout('videolar.html','Zoyo Videoları | YouTube ve Instagram | kuklamukla TV','Ali Abi ve Zoyo’nun kuklamukla TV YouTube videolarını ve Instagram paylaşımlarını keşfedin. İzlemek için ilgili platforma geçin.',videos,'videolar',[video_schema])

gallery=page_intro('FOTOĞRAFLAR','Birlikte yaşanan gerçek anlar.','Ali Abi ve Zoyo’nun okul, salon ve çocuk şenliği buluşmalarından 18 gerçek fotoğrafı ana sayfada keşfedin.')
gallery+=f'<section class="section"><div class="container"><div class="gallery-directory-intro"><h2>Sahneden hatıralar.</h2><p>Bir kare seçerek fotoğrafın bulunduğu bölüme geçebilirsiniz.</p>{button("Fotoğraf galerisini açın","index.html#fotograflar","primary","Search")}</div><div class="photo-directory">'
gallery+=''.join(f'<a class="photo-directory-card" href="{link("index.html#foto-"+p["id"])}">{icon("Search")}<span><small>{esc(p["category"])}</small><strong>{esc(p["title"])}</strong></span></a>' for p in photos)
gallery+='</div></div></section>'+cta()
layout('fotograflar.html','Ali Cengiz ve Zoyo Fotoğrafları | kuklamukla TV','Ali Cengiz ve Zoyo’nun sahne ve çocuk etkinliklerinden 18 gerçek fotoğrafını ana sayfada inceleyin.',gallery,'fotograflar')

regions=page_intro('TÜRKİYE’NİN 81 İLİNDE','Bir sonraki durak sizin şehriniz.','Ali Abi ve Zoyo, kukla gösterisi için Türkiye’nin her ilinde çocuklarla buluşabiliyor.')
regions+=tour_banner(regions_page=True)
regions+='<section class="section"><div class="container"><div class="region-intro"><div><h2>Türkiye’nin 81 ilinde.</h2><p>Listeden şehrinizi bulup Instagram hesabımıza ulaşabilirsiniz.</p></div></div><div class="province-search js-only"><label for="province-search">Şehrinizi bulun</label><div>'+icon('Search')+'<input id="province-search" type="search" placeholder="Örneğin Mersin" autocomplete="off" aria-controls="province-list"></div></div><p class="province-count" id="province-count" role="status">81 ilde gösteri yapılabiliyor.</p><ul id="province-list" class="province-list">'
regions+=''.join(f'<li><a href="{esc(IG)}" target="_blank" rel="noopener noreferrer" aria-label="{esc(p)} için Instagram’da bize ulaşın (yeni sekme)">{icon("MapPin")}{esc(p)}</a></li>' for p in provinces)
regions+=f'</ul><p id="province-empty" hidden>Bu adla bir il bulunamadı. İl adını kontrol edin.</p><div class="region-note"><h2>Gösteriler hakkında bize yazın.</h2><p>{IG_DESCRIPTION}</p>{instagram("Instagram hesabımız","outline")}</div></div></section>{cta()}'
layout('hizmet-bolgeleri.html','81 İlde Kukla Gösterisi | Türkiye Geneli Ali Abi ve Zoyo','İstanbul, Ankara, İzmir, Mersin ve Türkiye’nin 81 ilinde Ali Abi ve Zoyo ile kukla gösterisi. Ayrıntılı bilgi için Instagram hesabımızdan bize mesaj atın.',regions,'hizmet-bolgeleri')

faq_body=page_intro('SIK SORULAN SORULAR','Gösteriden önce merak ettikleriniz.','Ali Abi ve Zoyo, kukla gösterileri ve çocuklarla buluşmalar hakkında kısa cevaplar.')
faq_body+=f'<section class="section"><div class="container narrow">{faq_html(common_faqs)}<div class="read-guide">{icon("ClipboardList")}<p>Salon ve sahne hazırlığı hakkında <a href="{link("kukla-gosterisi-planlama.html")}">etkinlik rehberini okuyabilirsiniz.</a></p></div></div></section>{cta()}'
layout('sik-sorulan-sorular.html','Kukla Gösterisi Hakkında Sık Sorulan Sorular | Ali Cengiz','Zoyo’yu kim seslendiriyor, gösteriler nerelerde yapılıyor, videolar nereden izleniyor? Ali Abi ve Zoyo hakkında merak edilenler.',faq_body,extra_schema=[faq_schema(common_faqs)])

contact=page_intro('INSTAGRAM’DA BULUŞALIM','Bir merhabayla başlayalım.','Ali Abi ve Zoyo’nun gösterileri hakkında bize Instagram hesabımızdan ulaşabilirsiniz.')
contact+=f'''<section class="section contact-section"><div class="container instagram-panel"><div class="instagram-emblem" aria-hidden="true">{icon('Instagram')}</div><span class="eyebrow">kuklamukla TV</span><h2>Neşeli buluşmalar<br> bir mesaj uzağınızda.</h2><p>{IG_DESCRIPTION}</p>{instagram()}<span class="instagram-handle">@kuklamuklatv</span><span class="contact-location">{icon('MapPin')} Türkiye’nin 81 ilinde kukla gösterisi</span></div></section>'''
layout('iletisim.html','Instagram’dan Bize Ulaşın | Ali Abi ve Zoyo · kuklamukla TV','Ali Abi ve Zoyo kukla gösterileri hakkında ayrıntılı bilgi için kuklamukla TV Instagram hesabımızdan bize mesaj atın.',contact,'iletisim')

privacy=page_intro('GİZLİLİK & ÇEREZLER','Bilgileriniz hakkında.','Bu sitenin nasıl çalıştığını ve dış bağlantıları burada açıklıyoruz.')
privacy+=f'''<section class="section"><article class="container narrow prose"><section><h2>Instagram üzerinden iletişim</h2><p>Gösteriler hakkında iletişim kurmak için Instagram hesabımızı ziyaret edebilirsiniz. Instagram’da paylaştığınız bilgiler ilgili platformun koşullarına tabidir.</p></section><section><h2>Video ve sosyal medya bağlantıları</h2><p>Video kapakları bu siteye ait yerel dosyalardır. Bir kapağa tıkladığınızda YouTube veya Instagram yeni sekmede açılır. İlgili platformu ziyaret ettiğinizde o platformun gizlilik politikası geçerlidir.</p><p><a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google gizlilik politikası</a></p></section><section><h2>Çerezler ve hareket tercihi</h2><p>Bu site kendiliğinden reklam, analiz veya takip çerezi kurmaz. Yazı tipleri ve görseller site dosyalarından yüklenir. Dekoratif hareketler otomatik çalışır ve cihazınızın azaltılmış hareket tercihine uyar. Bu tercih site tarafından kaydedilmez. Yayın hizmetinin erişim kayıtları kendi politikalarına göre işlenebilir.</p></section><section><h2>Gösteriler hakkında</h2><p>{IG_DESCRIPTION}</p>{instagram('Instagram hesabımız','outline')}</section></article></section>'''
layout('gizlilik.html','Gizlilik ve Çerez Bilgileri | Ali Abi ve Zoyo','Instagram ve YouTube dış bağlantıları, yerel görseller, çerezler ve hareket tercihi hakkında bilgi.',privacy)

not_found=page_intro('SAYFA BULUNAMADI','Bu sahne henüz kurulmamış.','Aradığınız sayfa taşınmış veya bağlantı yanlış yazılmış olabilir.')
not_found+=f'<section class="section"><div class="container">{button("Ana sayfaya dönün","","primary","Theater")}</div></section>'
layout('404.html','Sayfa Bulunamadı | Ali Abi ve Zoyo','Aradığınız sayfa bulunamadı. Ali Abi ve Zoyo ana sayfasına dönebilirsiniz.',not_found,noindex=True)

if set(photo_uses) != set(photo_by_id) or len(photo_by_id) != 18:
    raise SystemExit('18 fotoğrafın tamamı tam birer içerik konumunda bulunmalı.')

filenames=[name for name in rendered if name!='404.html']
if site_url:
    entries=''.join(f'<url><loc>{xml_escape(link("" if name=="index.html" else name))}</loc></url>\n' for name in filenames)
    sitemap=f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    robots=f'User-agent: *\nAllow: /\n\nSitemap: {link("sitemap.xml")}\n'
else:
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><!-- GitHub yayını sırasında gerçek URL ile otomatik oluşturulur. --></urlset>\n'
    robots='User-agent: *\nAllow: /\n'
(ROOT/'sitemap.xml').write_text(sitemap)
(ROOT/'robots.txt').write_text(robots)
(ROOT/'site.webmanifest').write_text(json.dumps({'name':'kuklamukla TV · Ali Abi ve Zoyo','short_name':'kuklamukla TV','lang':'tr','start_url':'./','display':'browser','background_color':'#e4f6ff','theme_color':'#665697','icons':[{'src':'assets/icons/apple-touch-icon.png','sizes':'180x180','type':'image/png'}]},ensure_ascii=False,indent=2))
(ROOT/'.nojekyll').touch()
print(f'{len(rendered)} HTML sayfası; 18 tekil fotoğraf. Yayın adresi: {site_url or "GitHub yayınında otomatik belirlenecek"}')
