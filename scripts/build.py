#!/usr/bin/env python3
"""Dependency-free static renderer. Rebuild after editing content/*.json."""
import argparse
import html
import json
import os
import re
from pathlib import Path
from urllib.parse import urlparse, quote
from xml.sax.saxutils import escape as xml_escape

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--url', default=None, help='Final https URL, including GitHub repository path if needed')
args = parser.parse_args()
config = json.loads((ROOT / 'content/site.json').read_text())
pages = json.loads((ROOT / 'content/pages.json').read_text())
provinces = json.loads((ROOT / 'content/provinces.json').read_text())
photos = json.loads((ROOT / 'content/photos.json').read_text())
icons = json.loads((ROOT / 'content/icons.json').read_text())
scene_markup = (ROOT / 'content/cartoon-scene.html').read_text()
valance_markup = (ROOT / 'content/stage-valance.svg').read_text()
site_url = (args.url if args.url is not None else os.environ.get('SITE_URL') or config['site_url']).strip().rstrip('/')
if site_url:
    parsed = urlparse(site_url)
    if parsed.scheme != 'https' or not parsed.netloc or parsed.query or parsed.fragment or parsed.username:
        raise SystemExit('Yayın adresi https:// ile başlamalı; sorgu veya # içermemeli.')
    if parsed.hostname in ('example.com', 'example.invalid', 'localhost'):
        raise SystemExit('Örnek alan adı yerine gerçek yayın adresini kullanın.')
for key in ('phone', 'whatsapp'):
    if config.get(key) and not re.fullmatch(r'\+?[1-9][0-9 ()-]{8,20}', config[key]):
        raise SystemExit(f'{key}: ülke koduyla geçerli numara girin.')

def esc(value):
    return html.escape(str(value), quote=True)

def link(path=''):
    return f'{site_url}/{path}' if site_url else f'./{path or "index.html"}'

def icon(name, cls=''):
    spec = icons[name]
    attrs = 'fill="currentColor"' if spec.get('brand') else 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    nodes = ''.join('<' + tag + ' ' + ' '.join(f'{k}="{esc(v)}"' for k,v in props.items()) + ' />' for tag,props in spec['nodes'])
    return f'<svg class="icon {esc(cls)}" width="24" height="24" viewBox="{esc(spec.get("viewBox","0 0 24 24"))}" {attrs} aria-hidden="true" focusable="false">{nodes}</svg>'

def button(text, path='iletisim.html', style='primary', name='CalendarDays'):
    return f'<a class="button button--{style}" href="{esc(link(path))}">{icon(name)}<span>{esc(text)}</span></a>'

def socials():
    return ''.join(f'<a href="{esc(config[key])}" target="_blank" rel="noopener noreferrer" aria-label="kuklamukla TV {title} hesabı (yeni sekme)">{icon(title)}</a>' for key,title in [('instagram','Instagram'),('youtube','Youtube'),('facebook','Facebook')])

def floating_contacts():
    number=re.sub(r'\D','',config.get('whatsapp',''))
    if not number:return ''
    message=quote('Merhaba, Ali Abi ve Zoyo kukla gösterisi için bilgi almak istiyorum.')
    return f'<aside class="floating-socials" aria-label="Hızlı iletişim"><a class="quick-contact quick-instagram" href="{esc(config["instagram"])}" target="_blank" rel="noopener noreferrer" aria-label="Instagram hesabımızı açın (yeni sekme)"><span class="quick-tip">Instagram</span>{icon("Instagram")}</a><a class="quick-contact quick-whatsapp" href="https://wa.me/{number}?text={message}" target="_blank" rel="noopener noreferrer" aria-label="WhatsApp’tan gösteri için yazın: +90 538 248 72 08 (yeni sekme)"><span class="quick-tip">Gösteri için WhatsApp’tan yazın</span>{icon("WhatsApp")}</a></aside>'

def logo():
    return f'<a class="brand brand--image" href="{link()}" aria-label="kuklamukla TV · Ali Abi ve Zoyo, ana sayfa"><img src="{link("assets/img/kuklamukla-tv-logo.webp")}" alt="kuklamukla TV · Ali Abi &amp; Zoyo" width="960" height="320" decoding="async"></a>'

service_titles = {p['slug']:p['eyebrow'].capitalize() for p in pages}
service_titles.update({'iletisim':'İletişim','hizmet-bolgeleri':'81 ilde gösteri'})

def header(active=''):
    return f'''<a class="skip-link" href="#icerik">İçeriğe geç</a>
    <div class="topline"><div class="container"><span>{icon('MapPin')} Türkiye’nin 81 ilinde kukla gösterisi</span><a href="{link('iletisim.html')}">Okullar ve kurumlar için bilgi alın</a></div></div>
    <header class="site-header"><div class="container header-inner">{logo()}
      <button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Menüyü aç">{icon('Menu')}<span>Menü</span></button>
      <nav id="main-nav" class="main-nav" aria-label="Ana menü">
        <a href="{link('ali-cengiz.html')}" {'aria-current="page"' if active=='ali-cengiz' else ''}>Ali Abi &amp; Zoyo</a>
        <details class="nav-dropdown"><summary>Gösteriler {icon('ChevronDown')}</summary><div class="nav-dropdown-content">
          <a href="{link('kukla-gosterisi.html')}">{icon('Theater')}Kukla gösterisi</a>
          <a href="{link('okullarda-kukla-gosterisi.html')}">{icon('School')}Okullar için</a>
          <a href="{link('belediye-kukla-gosterisi.html')}">{icon('Landmark')}Belediyeler için</a>
          <a href="{link('23-nisan-kukla-gosterisi.html')}">{icon('PartyPopper')}23 Nisan &amp; özel günler</a>
          <a href="{link('cocuk-tiyatrosu.html')}">{icon('Ticket')}Çocuklar için kukla tiyatrosu</a>
        </div></details>
        <a href="{link('videolar.html')}" {'aria-current="page"' if active=='videolar' else ''}>Videolar</a><a href="{link('fotograflar.html')}" {'aria-current="page"' if active=='fotograflar' else ''}>Fotoğraflar</a>
        <a href="{link('hizmet-bolgeleri.html')}" {'aria-current="page"' if active=='hizmet-bolgeleri' else ''}>81 ilde gösteri</a>
        {button('Gösteri planlayalım',style='small')}
      </nav></div></header>'''

def footer():
    return f'''<footer class="site-footer"><div class="container footer-grid"><div>{logo()}<p>Bir kukla, bir ses, birlikte atılan kahkahalar.<br>Ali Abi ve Zoyo’yla sahnede buluşalım.</p><div class="socials">{socials()}</div></div>
      <div><h2>Gösteriler</h2><a href="{link('kukla-gosterisi.html')}">Kukla gösterisi</a><a href="{link('okullarda-kukla-gosterisi.html')}">Okullar için gösteri</a><a href="{link('belediye-kukla-gosterisi.html')}">Belediye etkinlikleri</a><a href="{link('cocuk-tiyatrosu.html')}">Çocuklar için kukla tiyatrosu</a><a href="{link('23-nisan-kukla-gosterisi.html')}">23 Nisan etkinlikleri</a></div>
      <div><h2>Tanışalım</h2><a href="{link('ali-cengiz.html')}">Ali Cengiz &amp; Zoyo</a><a href="{link('videolar.html')}">Gösteri videoları</a><a href="{link('fotograflar.html')}">Fotoğraflar</a><a href="{link('hizmet-bolgeleri.html')}">Hizmet bölgeleri</a><a href="{link('sik-sorulan-sorular.html')}">Sık sorulan sorular</a><a href="{link('kukla-gosterisi-planlama.html')}">Etkinlik rehberi</a></div>
      <div><h2>Birlikte planlayalım</h2><p>Kurumunuzu, şehrinizi ve düşündüğünüz tarihi paylaşın.</p><a class="footer-contact" href="{link('iletisim.html')}">{icon('MessageCircle')} İletişime geçin</a><a href="{esc(config['instagram'])}" target="_blank" rel="noopener noreferrer">@kuklamuklatv</a></div></div>
      <div class="container footer-bottom"><span>© <span data-year>2026</span> Ali Cengiz · kuklamukla TV</span><span><a href="{link('gizlilik.html')}">Gizlilik &amp; çerezler</a><span>Çocuklar için, sevgiyle.</span>{icon('Heart')}</span></div></footer>'''

common_faqs = [
    ['Hangi şehirlerde kukla gösterisi yapıyorsunuz?', 'Ali Cengiz, Ali Abi ve Zoyo kukla gösterisiyle Türkiye’nin 81 iline gelebiliyor. Tarih, ulaşım ve etkinlik koşulları birlikte netleştiriliyor.'],
    ['Okulumuza kukla gösterisi için nasıl davet edebiliriz?', 'Okulun adını, il ve ilçesini, düşündüğünüz tarihi, öğrenci sayısını ve yaş grubunu paylaşın. Programın uygunluğunu ve gösteri ayrıntılarını birlikte konuşalım.'],
    ['Belediyeler ve çocuk şenlikleri için gösteri yapılıyor mu?', 'Evet. Belediyelerin kültür programları, kültür merkezleri ve çocuk şenlikleri için kukla gösterisi planlanabiliyor. Mekân ve teknik ihtiyaçlar önceden görüşülüyor.'],
    ['Gösteri süresi ve ücretini nasıl öğrenebilirim?', 'Süre ve teklif; yaş grubu, şehir, tarih, seans sayısı ve teknik hazırlığa göre görüşülüyor. Etkinlik bilgilerinizi göndererek ayrıntılı bilgi alabilirsiniz.'],
    ['Zoyo’yu kim seslendirip oynatıyor?', 'Zoyo’yu kukla sanatçısı Ali Cengiz seslendiriyor ve oynatıyor. Çocuklar onu sahnede Ali Abi olarak tanıyor.'],
    ['Videoları nereden izleyebilirim?', 'Videolar bölümündeki kapaklar YouTube videolarını veya Instagram hesabını açar. İzlemeye ilgili platformda devam edebilirsiniz.']
]

def faq_html(faqs):
    return '<div class="faq-list">' + ''.join(f'<details><summary>{esc(q)}{icon("ChevronDown")}</summary><div><p>{esc(a)}</p></div></details>' for q,a in faqs) + '</div>'

def faq_schema(faqs):
    return {'@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in faqs]}

def video_cards():
    items=[]
    for v in config['videos']:
        platform=v['platform']
        platform_icon='Youtube' if platform=='YouTube' else 'Instagram'
        action='YouTube’da izle' if platform=='YouTube' else 'Instagram’da aç'
        items.append(f'''<article class="video-card"><a class="video-launch social-video" href="{esc(v['url'])}" target="_blank" rel="noopener noreferrer" aria-label="{esc(v['title'])} · {esc(action)} (yeni sekme)">
          <img src="{link('assets/img/covers/'+v['cover'])}" alt="Ali Abi ve Zoyo karakterleriyle {esc(v['title'])} tanıtım kapağı" width="960" height="1280" loading="lazy" decoding="async">
          <span class="video-badge platform-{platform.lower()}">{icon(platform_icon)} {esc(platform)}</span>
          <span class="video-brand">kuklamukla TV</span><span class="video-info"><span>{esc(v['label'])}</span><strong>{esc(v['title'])}</strong><span class="media-action">{icon('Play')}{esc(action)}</span></span></a></article>''')
    return '<p class="media-rail-note">Kapakları kaydırın, neşeye katılın.</p><div class="video-grid">'+''.join(items)+'</div>'

def gallery_cards(items):
    output=[]
    for p in items:
        stem=p['file']
        category='Arşiv afişi' if p['category']=='Arşiv' else p['category']
        output.append(f'''<figure class="photo-card" data-category="{esc(p['category'])}"><a class="photo-launch" href="{link('assets/img/photos/'+stem+'-large.webp')}" data-photo="{p['id']}" data-title="{esc(p['title'])}" data-alt="{esc(p['alt'])}" data-full="{link('gorseller-uhd/'+stem+'.webp')}" aria-label="{esc(p['title'])} fotoğrafını büyüt">
          <img src="{link('assets/img/photos/'+stem+'-480.webp')}" srcset="{link('assets/img/photos/'+stem+'-480.webp')} 480w, {link('assets/img/photos/'+stem+'-960.webp')} 960w" sizes="(max-width:600px) 46vw, (max-width:1000px) 44vw, 30vw" alt="{esc(p['alt'])}" width="960" height="1280" loading="lazy" decoding="async"><span class="photo-zoom">{icon('Search')}<span>Büyüt</span></span></a><figcaption><span>{esc(category)}</span><strong>{esc(p['title'])}</strong></figcaption></figure>''')
    return '<div class="photo-grid" id="photo-grid">'+''.join(output)+'</div>'

def gallery_section():
    featured=[p for key in ['19','01','20','21','22','04','18','05'] for p in photos if p['id']==key]
    return f'''<section class="section photo-section"><div class="container"><div class="section-heading"><div><span class="eyebrow">GÖSTERİLERDEN KARELER</span><h2>Gerçek buluşmalar,<br>güzel hatıralar.</h2></div><div><p>Ali Abi, Zoyo ve çocuklarla bir arada.</p><a class="text-link" href="{link('fotograflar.html')}">Tüm fotoğrafları görün</a></div></div>{gallery_cards(featured)}</div></section>'''

def photo_dialog():
    return f'''<dialog class="photo-dialog" id="photo-dialog" aria-labelledby="photo-title"><div class="photo-dialog-inner"><div class="photo-dialog-top"><h2 id="photo-title">Gösterilerden bir kare</h2><button class="icon-button" data-close-photo type="button" aria-label="Fotoğrafı kapat">{icon('X')}</button></div><div class="photo-viewer-media"><img id="photo-full" alt="" width="1440" height="1920"></div><div class="photo-dialog-bottom"><div class="photo-navigation"><button class="icon-button" data-prev-photo type="button" aria-label="Önceki fotoğraf">{icon('ChevronLeft')}</button><span id="photo-position" aria-live="polite"></span><button class="icon-button" data-next-photo type="button" aria-label="Sonraki fotoğraf">{icon('ChevronRight')}</button></div><a id="photo-download" href="{link('fotograflar.html')}" download>WebP indir</a></div></div></dialog>'''


def cta():
    return f'''<section class="section cta-section"><div class="container cta-panel"><div class="cta-doodle" aria-hidden="true">{icon('Sparkles')}</div><div><span class="eyebrow">SIRADAKİ BULUŞMA SİZİNLE OLSUN</span><h2>Zoyo sizin şehrinize de gelsin.</h2><p>Okulunuz veya kurumunuz için kukla gösterisi planlayalım.</p></div>{button('Tarih ve bilgi alalım',style='light')}</div></section>'''

def page_intro(eyebrow,title,intro):
    breadcrumb=eyebrow if eyebrow=='kuklamukla TV' else eyebrow.capitalize()
    return f'<section class="page-intro">{scene_markup}<div class="container"><nav class="breadcrumbs" aria-label="Sayfa yolu"><a href="{link()}">Ana sayfa</a>{icon("ChevronRight")}<span>{esc(breadcrumb)}</span></nav><span class="eyebrow">{esc(eyebrow)}</span><h1>{title}</h1><p>{esc(intro)}</p></div></section>'

def layout(filename, title, description, body, active='', extra_schema=None, noindex=False):
    canonical = link('' if filename=='index.html' else filename) if site_url else ''
    image = link('assets/img/social-cover.webp') if site_url else ''
    ld = {'@context':'https://schema.org','@graph':[]}
    if site_url:
        ld['@graph'] = [
            {'@type':'Person','@id':site_url+'/#ali-cengiz','name':'Ali Cengiz','alternateName':'Ali Abi','jobTitle':'Kukla sanatçısı','url':link('ali-cengiz.html'),'sameAs':[config['instagram'],config['youtube'],config['facebook']]},
            {'@type':'WebSite','@id':site_url+'/#website','name':'Ali Abi ve Zoyo | kuklamukla TV','url':link(),'inLanguage':'tr-TR','publisher':{'@id':site_url+'/#ali-cengiz'}},
            {'@type':'WebPage','@id':canonical+'#webpage','url':canonical,'name':title,'description':description,'inLanguage':'tr-TR','isPartOf':{'@id':site_url+'/#website'}},
        ]
    if extra_schema:
        ld['@graph'] += extra_schema
    ld_text = json.dumps(ld, ensure_ascii=False).replace('<','\\u003c')
    client = {k:config[k] for k in ['phone','whatsapp','instagram']}
    client_text = json.dumps(client,ensure_ascii=False).replace('<','\\u003c')
    canonical_tag = f'<link rel="canonical" href="{esc(canonical)}"><meta property="og:url" content="{esc(canonical)}">' if canonical else ''
    social_image = f'<meta property="og:image" content="{esc(image)}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Ali Abi ve Zoyo kukla gösterisi tanıtım illüstrasyonu"><meta name="twitter:card" content="summary_large_image">' if image else '<meta name="twitter:card" content="summary">'
    output = f'''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{esc(title)}</title>
<meta name="description" content="{esc(description)}"><meta name="robots" content="{'noindex, follow' if noindex else 'index, follow, max-image-preview:large'}"><meta name="theme-color" content="#665697"><meta name="referrer" content="strict-origin-when-cross-origin">
{canonical_tag}<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR"><meta property="og:site_name" content="Ali Abi ve Zoyo"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}">{social_image}
<link rel="icon" href="{link('assets/icons/favicon.svg')}" type="image/svg+xml"><link rel="icon" href="{link('assets/icons/favicon.png')}" type="image/png"><link rel="apple-touch-icon" href="{link('assets/icons/apple-touch-icon.png')}"><link rel="manifest" href="{link('site.webmanifest')}">
<link rel="preload" href="{link('assets/fonts/fredoka-600.ttf')}" as="font" type="font/ttf" crossorigin><link rel="preload" href="{link('assets/fonts/nunito-sans-400.ttf')}" as="font" type="font/ttf" crossorigin>
<link rel="stylesheet" href="{link('assets/css/style.css')}"><link rel="stylesheet" href="{link('assets/css/cartoon.css')}"><link rel="stylesheet" href="{link('assets/css/media.css')}"><link rel="stylesheet" href="{link('assets/css/refined.css')}"><link rel="stylesheet" href="{link('assets/css/engagement.css')}"><script src="{link('assets/js/main.js')}" defer></script>
<script type="application/ld+json">{ld_text}</script><script type="application/json" id="site-config">{client_text}</script>
</head><body class="cartoon-theme">{header(active)}<main id="icerik">{body}</main>{footer()}{floating_contacts()}<button class="motion-toggle" id="motion-toggle" type="button" aria-pressed="false" aria-label="Arka plan hareketini durdur">{icon('Sun')}<span data-motion-label>Hareketi durdur</span></button>{photo_dialog()}<div id="live-status" class="sr-only" role="status" aria-live="polite"></div></body></html>'''
    (ROOT / filename).write_text(output,encoding='utf-8')

home = f'''
<section class="hero">{scene_markup}<div class="container hero-grid"><div class="hero-copy"><span class="eyebrow"><span class="eyebrow-line"></span> ALİ CENGİZ · KUKLA SANATÇISI</span><h1><span class="hero-title-first">Ali Abi ve <span class="zoyo-word">Zoyo</span></span> <span class="hero-title-second">ile kukla gösterisi.</span></h1><p>Okullarda, belediye etkinliklerinde ve çocuk şenliklerinde, Türkiye’nin <strong>81 ilinde</strong> çocuklarla buluşuyoruz.</p><div class="hero-actions">{button('Gösteri planlayalım')}{button('Zoyo’yu izleyin','videolar.html','outline','Play')}</div><div class="hero-footnote">{icon('Heart')} Çocuklar için, sevgiyle.</div></div>
<div class="hero-art"><div class="hero-photo"><img src="{link('assets/img/ali-abi-zoyo-hero-1280.webp')}" srcset="{link('assets/img/ali-abi-zoyo-hero-640.webp')} 640w, {link('assets/img/ali-abi-zoyo-hero-1280.webp')} 1280w" sizes="(max-width:600px) 90vw, (max-width:820px) 460px, 45vw" alt="Ali Abi ve turuncu kuklası Zoyo’nun çizimli tanıtım görseli" width="1280" height="1600" fetchpriority="high" decoding="async"></div></div></div></section>
<div class="audience-strip"><div class="container"><span>{icon('School')}Okul etkinlikleri</span><span>{icon('Landmark')}Belediye programları</span><span>{icon('Theater')}Çocuk şenlikleri</span><span>{icon('MapPin')}Türkiye’nin 81 ili</span></div></div>
<section class="section" id="gosteriler"><div class="container"><div class="section-heading"><div><span class="eyebrow">BİRLİKTE BULUŞALIM</span><h2>Her buluşmada bir kahkaha.</h2></div><p>Etkinliğinize uygun bir kukla gösterisi için<br>ayrıntıları birlikte planlayalım.</p></div><div class="program-grid">
<article class="program-card program-card--school"><div class="program-image"><img src="{link('assets/img/stage.webp')}" alt="Ali Cengiz okul salonunda kukla gösterisi yapıyor" width="1200" height="900" loading="lazy" decoding="async"><span>{icon('School')}</span></div><div class="program-copy"><h3>Okullar için</h3><p>Anaokulu ve ilkokul etkinliklerinde Ali Abi ve Zoyo çocuklarla buluşsun.</p><a href="{link('okullarda-kukla-gosterisi.html')}">Okul gösterisini inceleyin</a></div></article>
<article class="program-card program-card--city"><div class="program-image"><img src="{link('assets/img/festival.webp')}" alt="Ali Cengiz çocuklarla sahne etkinliğinde buluşuyor" width="1200" height="900" loading="lazy" decoding="async"><span>{icon('Landmark')}</span></div><div class="program-copy"><h3>Belediyeler için</h3><p>Kültür merkezlerinde ve çocuk şenliklerinde şehrin çocuklarıyla bir araya gelelim.</p><a href="{link('belediye-kukla-gosterisi.html')}">Belediye gösterisini inceleyin</a></div></article>
<article class="program-card program-card--special"><div class="program-image"><img src="{link('assets/img/special.webp')}" alt="Ali Cengiz ve Zoyo okul sahnesinde kukla gösterisi yapıyor" width="1200" height="900" loading="lazy" decoding="async"><span>{icon('PartyPopper')}</span></div><div class="program-copy"><h3>23 Nisan &amp; özel günler</h3><p>Çocukların bayramına, okul şenliğine ve özel etkinliğinize neşe katalım.</p><a href="{link('23-nisan-kukla-gosterisi.html')}">Özel günleri inceleyin</a></div></article>
</div></div></section>
<section class="section about-section"><div class="container about-grid"><div class="about-visual"><img src="{link('assets/img/ali-cengiz-sahnede.webp')}" alt="Kukla sanatçısı Ali Cengiz sahnede Zoyo’yu seslendirip oynatırken" width="1200" height="1500" loading="lazy" decoding="async"><div class="about-note">Bir kukla.<br>Bir ses.<br><span>Bir sürü gülümseme.</span></div></div><div class="about-copy"><span class="eyebrow">SAHNEDE İKİ DOST</span><h2>Sahnede Ali Cengiz,<br>yanında Zoyo.</h2><p>Ali Cengiz, Zoyo’yu seslendiren ve oynatan bir kukla sanatçısı. Sahnedeki adıyla Ali Abi, çocuklarla canlı gösterilerde buluşuyor.</p><p>Okulunuz veya belediye etkinliğiniz için şehir ve tarih bilgisiyle gösteri planlayabiliriz. Ali Abi ve Zoyo, Türkiye’nin 81 ilinde çocuklarla buluşabiliyor.</p><a class="text-link" href="{link('ali-cengiz.html')}">Ali Abi ve Zoyo’yu tanıyın</a></div></div></section>
{gallery_section()}<section class="section videos-section" id="videolar"><div class="container"><div class="section-heading"><div><span class="eyebrow">kuklamukla TV</span><h2>Biraz Zoyo, bolca neşe.</h2></div><a class="text-link text-link--light" href="{esc(config['youtube'])}" target="_blank" rel="noopener noreferrer">{icon('Youtube')} YouTube kanalımız</a></div><p class="section-lead">YouTube ve Instagram’da neşeli anlar. İzlemek için bir kapak seçin.</p>{video_cards()}<p class="video-privacy">Kapaklar sizi YouTube veya Instagram’a götürür.</p></div></section>
<section class="section nationwide" id="turkiye-geneli"><div class="container nationwide-grid">{(ROOT/'content/tour-scene.html').read_text().replace('TOUR_IMAGE',link('assets/img/ali-abi-zoyo-hero-640.webp'))}<div><span class="eyebrow">ŞEHRİNİZ NERESİ OLURSA OLSUN</span><h2>Kukla gösterisi<br>şehrinize geliyor.</h2><p>İstanbul’dan Mersin’e, İzmir’den Erzurum’a… Ali Abi ve Zoyo, Türkiye’nin 81 ilinde çocuklarla buluşabiliyor.</p><p>Şehrinizi ve düşündüğünüz tarihi paylaşın. Ulaşımı, mekânı ve gösteri planını birlikte konuşalım.</p>{button('Şehriniz için bilgi alın','hizmet-bolgeleri.html','outline','MapPin')}</div></div></section>
<section class="section faq-section"><div class="container faq-grid"><div><span class="eyebrow">AKLINIZDAKİLER</span><h2>Birkaç küçük<br>soru, açık cevaplar.</h2><p>Etkinlik planlamadan önce bilmek isteyecekleriniz.</p><a class="text-link" href="{link('sik-sorulan-sorular.html')}">Tüm soruları görün</a></div>{faq_html(common_faqs[:4])}</div></section>{cta()}'''
layout('index.html','Ali Cengiz | Ali Abi ve Zoyo Kukla Gösterisi · 81 İl',config['description'],home,extra_schema=[faq_schema(common_faqs[:4])])

for page in pages:
    related = ''.join(f'<a href="{link(s+".html")}">{esc(service_titles[s])}</a>' for s in page['related'])
    body = page_intro(page['eyebrow'],esc(page['title']),page['intro'])
    body += f'<section class="section detail-section"><div class="container detail-grid"><article class="prose">'
    body += ''.join(f'<section><h2>{esc(s["title"])}</h2><p>{esc(s["text"])}</p></section>' for s in page['sections'])
    body += f'''<section><h2>Sık sorulanlar</h2>{faq_html(page['faqs'])}</section><section><h2>İlgili sayfalar</h2><div class="related-links">{related}</div></section></article><aside class="detail-aside"><figure><img src="{link('assets/img/'+page['image'])}" alt="{esc(page['image_alt'])}" width="1200" height="900" decoding="async"></figure><div class="aside-card">{icon(page['icon'])}<h2>Birlikte planlayalım.</h2><p>Kurum, şehir ve tarih bilgisiyle başlayalım.</p>{button('Gösteri için bilgi alın')}<span>{icon('MapPin')} Türkiye’nin 81 ilinde</span></div></aside></div></section>{cta()}'''
    schema = [faq_schema(page['faqs'])]
    if site_url:
        schema.append({'@type':'Service','name':page['seo_title'].split('|')[0].strip(),'description':page['description'],'serviceType':'Kukla gösterisi','areaServed':{'@type':'Country','name':'Türkiye'},'provider':{'@id':site_url+'/#ali-cengiz'},'url':link(page['slug']+'.html')})
    layout(page['slug']+'.html',page['seo_title'],page['description'],body,page['slug'],schema)

about = page_intro('ALİ CENGİZ & ZOYO','Ali Abi’yle tanışın.','Zoyo’nun sesi ve sahnedeki yol arkadaşı: kukla sanatçısı Ali Cengiz.')
about += f'''<section class="section"><div class="container about-grid"><div class="about-visual"><img src="{link('assets/img/ali-cengiz-sahnede.webp')}" alt="Kukla sanatçısı Ali Cengiz sahnede Zoyo’yu seslendirip oynatırken" width="1200" height="1500" decoding="async"></div><div class="prose"><span class="eyebrow">SAHNENİN ARKASINDAKİ İSİM</span><h2>Ali Cengiz, çocukların Ali Abisi.</h2><p>Ali Cengiz bir kukla sanatçısı. Kuklası Zoyo’yu seslendiriyor ve oynatıyor. Sahnedeki adıyla Ali Abi, Zoyo ile birlikte çocuklara kukla gösterisi sunuyor.</p><p>Okullar, belediyeler ve çocuklara yönelik etkinlikler için Türkiye’nin 81 ilinde gösteri yapabiliyor. Her buluşma için şehir, tarih, yaş grubu ve mekân ayrıntıları önceden konuşuluyor.</p><h2>Zoyo’nun dünyası ekranda da devam ediyor.</h2><p>kuklamukla TV YouTube kanalında Zoyo’nun kısa videolarını izleyebilir, Instagram ve Facebook hesaplarından paylaşımları takip edebilirsiniz.</p><div class="about-links">{button('Kısa videoları izleyin','videolar.html','outline','Play')}{button('Gösteri planlayalım')}</div></div></div></section>{cta()}'''
layout('ali-cengiz.html','Ali Cengiz Kimdir? | Kukla Sanatçısı Ali Abi ve Zoyo','Zoyo’yu seslendiren ve oynatan kukla sanatçısı Ali Cengiz ile tanışın. Ali Abi ve Zoyo, Türkiye genelinde çocuklarla kukla gösterilerinde buluşuyor.',about,'ali-cengiz')

videos = page_intro('kuklamukla TV','Zoyo’yu izlemeye ne dersiniz?','YouTube ve Instagram paylaşımlarından neşeli anlar. Bir kapak seçin; ilgili platformda izlemeye devam edin.')
videos += f'<section class="section videos-section videos-page"><div class="container">{video_cards()}<p class="video-privacy">Kapaklar YouTube veya Instagram’ı yeni sekmede açar. <a href="{esc(config["youtube"])}" target="_blank" rel="noopener noreferrer">Kanalı YouTube’da açın.</a></p></div></section>{cta()}'
video_schema = {'@type':'ItemList','name':'kuklamukla TV YouTube ve Instagram paylaşımları','itemListElement':[{'@type':'ListItem','position':i+1,'name':v.get('full_title',v['title']),'url':v['url']} for i,v in enumerate(config['videos'])]}
layout('videolar.html','Zoyo Videoları | YouTube ve Instagram | kuklamukla TV','Ali Abi ve Zoyo’nun kuklamukla TV YouTube videolarını ve Instagram paylaşımlarını keşfedin. İzlemek için ilgili platforma geçin.',videos,'videolar',[video_schema])

gallery = page_intro('FOTOĞRAFLAR','Ali Abi ve Zoyo’yla güzel hatıralar.','Gösterilerden, okul etkinliklerinden ve çocuklarla buluşmalardan seçtiğimiz kareler. Fotoğraflara dokunarak büyütebilirsiniz.')
gallery += '<section class="section photo-section gallery-page"><div class="container"><div class="gallery-filters js-only" role="group" aria-label="Fotoğraf kategorileri">'
for category in ['Tümü','Okullar','Sahne','Buluşmalar','Arşiv']:
    gallery += f'<button class="gallery-filter" type="button" data-photo-filter="{esc(category)}" aria-pressed="{str(category=="Tümü").lower()}">{esc(category)}</button>'
gallery += f'</div><p id="photo-count" class="photo-count" role="status">{len(photos)} fotoğraf</p>'+gallery_cards(photos)+'</div></section>'+cta()
gallery_schema = [{'@type':'ImageGallery','name':'Ali Cengiz ve Zoyo fotoğrafları','image':[link('assets/img/photos/'+p['file']+'-large.webp') for p in photos]}] if site_url else []
layout('fotograflar.html','Ali Cengiz ve Zoyo Fotoğrafları | kuklamukla TV','Ali Cengiz ve Zoyo’nun okul, sahne ve çocuk etkinliklerinden gerçek fotoğrafları. Etkinlik karelerini galeride inceleyin.',gallery,'fotograflar',gallery_schema)

regions = page_intro('TÜRKİYE’NİN 81 İLİNDE','Bir sonraki durak sizin şehriniz.','Kukla gösterisi için Türkiye’nin her iline gelebiliyoruz. Şehrinizi ve etkinlik tarihinizi paylaşın, ayrıntıları birlikte planlayalım.')
regions += f'''<section class="section"><div class="container"><div class="region-intro"><div>{icon('MapPin')}<h2>Okulunuzda, kültür merkezinde, şenlikte.</h2><p>Listede yer alan iller hizmet verilebilen bölgelerdir. Her ilde şubemiz bulunmuyor. Tarih, ulaşım, mekân ve teknik koşullar görüşmede birlikte netleştirilir.</p></div>{button('Şehriniz için gösteri planlayın')}</div><div class="province-search js-only"><label for="province-search">Şehrinizi bulun</label><div>{icon('Search')}<input id="province-search" type="search" placeholder="Örneğin Mersin" autocomplete="off" aria-controls="province-list"></div></div><p class="province-count" id="province-count" role="status">81 ilde gösteri planlanabilir.</p><ul id="province-list" class="province-list">'''
regions += ''.join(f'<li><a href="{link("iletisim.html")}?il={esc(p)}">{icon("MapPin")}{esc(p)}</a></li>' for p in provinces)
regions += f'</ul><p id="province-empty" hidden>Bu adla bir il bulunamadı. İl adını kontrol edin veya doğrudan iletişime geçin.</p><div class="region-note"><h2>Şehir dışı gösteri nasıl planlanır?</h2><p>İl ve ilçe, tarih, kurum adı ve beklenen katılımı iletin. Ulaşım ve varsa konaklama, gösteri kapsamıyla birlikte görüşülür. Birden fazla seans veya farklı mekân talebiniz varsa ilk görüşmede paylaşabilirsiniz.</p></div></div></section>{cta()}'
layout('hizmet-bolgeleri.html','81 İlde Kukla Gösterisi | Türkiye Geneli Ali Abi ve Zoyo','İstanbul, Ankara, İzmir, Mersin ve Türkiye’nin 81 ilinde Ali Abi ve Zoyo ile kukla gösterisi. Okul ve belediye etkinliğiniz için şehir ve tarih bilgisi paylaşın.',regions,'hizmet-bolgeleri')

faq_body = page_intro('SIK SORULAN SORULAR','Gösteriden önce merak ettikleriniz.','Kukla gösterisi, etkinlik planı ve iletişim hakkında kısa cevaplar.')
faq_body += f'<section class="section"><div class="container narrow">{faq_html(common_faqs)}<div class="read-guide">{icon("BookOpen")}<p>Salon, seans ve fiyat teklifine hazırlık için <a href="{link("kukla-gosterisi-planlama.html")}">etkinlik rehberini okuyabilirsiniz.</a></p></div></div></section>{cta()}'
layout('sik-sorulan-sorular.html','Kukla Gösterisi Hakkında Sık Sorulan Sorular | Ali Cengiz','Ali Abi ve Zoyo kukla gösterisi hangi illerde yapılır, süre ve teklif nasıl alınır, okula nasıl davet edilir? Sık sorulan soruların cevapları.',faq_body,extra_schema=[faq_schema(common_faqs)])

wa = re.sub(r'\D','',config.get('whatsapp',''))
phone = re.sub(r'[^+\d]','',config.get('phone',''))
contact_methods = f'<a class="contact-method" href="{esc(config["instagram"])}" target="_blank" rel="noopener noreferrer"><span>{icon("Instagram")}</span><div><strong>Instagram’dan yazın</strong><span>@kuklamuklatv</span></div>{icon("MessageCircle")}</a>'
if wa:
    contact_methods = f'<a class="contact-method" href="https://wa.me/{wa}" target="_blank" rel="noopener noreferrer"><span>{icon("MessageCircle")}</span><div><strong>WhatsApp’tan yazın</strong><span>{esc(config["whatsapp"])}</span></div>{icon("MessageCircle")}</a>' + contact_methods
if phone:
    contact_methods += f'<a class="contact-method" href="tel:{esc(phone)}"><span>{icon("Phone")}</span><div><strong>Telefonla arayın</strong><span>{esc(config["phone"])}</span></div>{icon("Phone")}</a>'
contact = page_intro('GÖSTERİ İÇİN İLETİŞİM','Birlikte güzel bir gün planlayalım.','Okulunuz veya kurumunuz için kukla gösterisi düşünüyorsanız şehrinizi ve tarihinizi paylaşın. Ali Abi ve Zoyo’yla buluşalım.')
contact += f'''<section class="section"><div class="container contact-grid"><div><span class="eyebrow">DOĞRUDAN KONUŞALIM</span><h2>Merhaba demekle başlayalım.</h2><p class="contact-lead">Etkinlik ayrıntılarını doğrudan görüşebiliriz. Gösteri için tarih uygunluğu ve teklif, görüşmede netleşir.</p>{contact_methods}<div class="contact-note">{icon('MapPin')}<p><strong>Türkiye’nin 81 ilinde</strong><br>Okullar, belediyeler ve çocuk etkinlikleri için.</p></div><a class="text-link" href="{link('kukla-gosterisi-planlama.html')}">{icon('BookOpen')} Etkinlik rehberini okuyun</a></div>
<div class="message-maker js-only"><span class="eyebrow">İLK MESAJINIZI HAZIRLAYIN</span><h2>Etkinliğinizden bahsedin.</h2><p>Bilgileri doldurun, mesajınızı kopyalayıp bize gönderin.</p><form id="event-form" action="#mesaj" method="get"><div class="form-grid"><div class="field full"><label for="institution">Kurum / okul adı <span>(isteğe bağlı)</span></label><input id="institution" name="kurum" maxlength="120" placeholder="Kurumunuzun adı" autocomplete="organization"></div><div class="field"><label for="city">Şehir <span aria-hidden="true">*</span></label><select id="city" name="il" required><option value="">İl seçin</option>'''
contact += ''.join(f'<option>{esc(p)}</option>' for p in sorted(provinces, key=lambda name: tuple('abcçdefgğhıijklmnoöprsştuüvyz'.find(c) for c in name.replace('İ','i').lower().replace('â','a'))))
contact += f'''</select></div><div class="field"><label for="event-date">Tarih <span>(isteğe bağlı)</span></label><input id="event-date" name="tarih" type="date"></div><div class="field full"><label for="event-type">Etkinlik türü</label><select id="event-type" name="etkinlik"><option>Okul etkinliği</option><option>Belediye etkinliği</option><option>Çocuk şenliği</option><option>23 Nisan / özel gün</option><option>Diğer etkinlik</option></select></div><div class="field"><label for="age">Çocukların yaş aralığı</label><input id="age" name="yas" maxlength="60" placeholder="Örneğin 5–8 yaş"></div><div class="field"><label for="guests">Tahmini kişi sayısı</label><input id="guests" name="kisi" type="number" min="1" max="100000" inputmode="numeric" placeholder="Örneğin 150"></div><div class="field full"><label for="event-note">Eklemek istedikleriniz</label><textarea id="event-note" name="not" rows="3" maxlength="1000" placeholder="İlçe, mekân veya sormak istedikleriniz..."></textarea></div></div><button type="submit" class="button button--primary">{icon('ClipboardList')} Mesajımı hazırla</button><p class="form-privacy">Bu bilgiler sitede saklanmaz. Mesajı siz gönderirsiniz.</p></form><div id="message-result" class="message-result" hidden><h3>Mesajınız hazır.</h3><textarea id="message-text" rows="9" readonly aria-label="Hazırlanan etkinlik mesajı"></textarea><div class="result-actions"><button class="button button--primary" id="copy-message" type="button">{icon('Copy')} Mesajı kopyala</button><a class="button button--outline" id="send-message" href="{esc(config['instagram'])}" target="_blank" rel="noopener noreferrer">{icon('Instagram')} Instagram’ı aç</a></div><p id="copy-status" role="status">Mesajı kopyalayıp açılan görüşmeye yapıştırabilirsiniz.</p></div></div><noscript><p>Mesaj hazırlama aracı için JavaScript gereklidir. Yukarıdaki Instagram bağlantısından doğrudan iletişime geçebilirsiniz.</p></noscript></div></section>'''
layout('iletisim.html','Kukla Gösterisi İletişim ve Teklif | Ali Cengiz ve Zoyo','Okul, belediye ve çocuk şenliği için Ali Abi ve Zoyo kukla gösterisi planlayın. Şehir, tarih ve etkinlik bilgisiyle iletişime geçin.',contact,'iletisim')

privacy = page_intro('GİZLİLİK & ÇEREZLER','Bilgileriniz hakkında.','Bu sitenin nasıl çalıştığını ve dış bağlantıları burada açıklıyoruz.')
privacy += f'''<section class="section"><article class="container narrow prose"><section><h2>İletişim aracı</h2><p>Etkinlik bilgisi aracı, yazdıklarınızdan tarayıcınız içinde bir mesaj taslağı oluşturur. Bu site bilgileri bir sunucuya göndermez, kaydetmez ve otomatik mesaj göndermez. Taslağı kopyalayıp seçtiğiniz iletişim kanalında paylaşmanız gerekir.</p></section><section><h2>Sosyal medya bağlantıları</h2><p>Video kartları bu sitede oynatıcı açmaz. Kapak görselleri yerel dosyalardır. Bir karta tıkladığınızda YouTube veya Instagram yeni sekmede açılır. İlgili platformu ziyaret ettiğinizde o platformun gizlilik politikası ve teknolojileri geçerlidir.</p><p><a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google gizlilik politikası</a></p></section><section><h2>Çerezler ve ölçüm</h2><p>Bu sürüm, kendiliğinden reklam, analiz veya takip çerezi kurmaz. Yazı tipleri ve görseller site dosyalarından yüklenir. Gösterim ve erişim kayıtları, kullanılan yayın hizmetinin kendi politikalarına göre işlenebilir.</p></section><section><h2>Dış bağlantılar ve iletişim</h2><p>Instagram, Facebook, YouTube ve varsa WhatsApp bağlantıları sizi ilgili platforma yönlendirir. Bu platformlarda paylaştığınız bilgiler, o platformun koşullarına tabidir. Gösteriyle ilgili sorularınız için <a href="{esc(config['instagram'])}" target="_blank" rel="noopener noreferrer">kuklamukla TV Instagram hesabından</a> iletişime geçebilirsiniz.</p></section></article></section>'''
layout('gizlilik.html','Gizlilik ve Çerez Bilgileri | Ali Abi ve Zoyo','İletişim taslağı, YouTube videoları ve dış bağlantılarda gizlilik hakkında bilgi.',privacy)

not_found = page_intro('SAYFA BULUNAMADI','Bu sahne henüz kurulmamış.','Aradığınız sayfa taşınmış veya bağlantı yanlış yazılmış olabilir.')
not_found += f'<section class="section"><div class="container">{button("Ana sayfaya dönün","","primary","Theater")}</div></section>'
layout('404.html','Sayfa Bulunamadı | Ali Abi ve Zoyo','Aradığınız sayfa bulunamadı. Ali Abi ve Zoyo ana sayfasına dönebilirsiniz.',not_found,noindex=True)

filenames = ['index.html'] + [p['slug']+'.html' for p in pages] + ['ali-cengiz.html','videolar.html','hizmet-bolgeleri.html','sik-sorulan-sorular.html','iletisim.html','fotograflar.html','gizlilik.html']
if site_url:
    entries = ''.join(f'<url><loc>{xml_escape(link("" if name=="index.html" else name))}</loc></url>\n' for name in filenames)
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{entries}</urlset>\n'
    robots = f'User-agent: *\nAllow: /\n\nSitemap: {link("sitemap.xml")}\n'
else:
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><!-- GitHub yayını sırasında gerçek URL ile otomatik oluşturulur. --></urlset>\n'
    robots = 'User-agent: *\nAllow: /\n'
(ROOT/'sitemap.xml').write_text(sitemap)
(ROOT/'robots.txt').write_text(robots)
(ROOT/'site.webmanifest').write_text(json.dumps({'name':'Ali Abi ve Zoyo · Kukla Gösterisi','short_name':'Ali Abi & Zoyo','lang':'tr','start_url':'./','display':'browser','background_color':'#e4f6ff','theme_color':'#665697','icons':[{'src':'assets/icons/apple-touch-icon.png','sizes':'180x180','type':'image/png'}]},ensure_ascii=False,indent=2))
(ROOT/'.nojekyll').touch()
print(f'{len(filenames)+1} HTML sayfası oluşturuldu. Yayın adresi: {site_url or "GitHub yayınında otomatik belirlenecek"}')
