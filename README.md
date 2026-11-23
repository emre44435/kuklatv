# Ali Abi ve Zoyo · kuklamukla TV

Ali Cengiz’in okul, belediye ve çocuk etkinlikleri için hazırlanmış Türkçe kukla gösterisi sitesi. HTML, CSS ve JavaScript ile çalışır. Masaüstünde hizalı kartlar, mobilde okunaklı içerik ve kaydırılabilen sosyal medya kapakları kullanılır.

## GitHub Pages ile yayın

1. ZIP’i çıkartın. İçindeki proje dosyalarını GitHub deponuzun **köküne** yükleyin; `index.html` alt klasörde kalmasın. `.github/workflows/pages.yml` dosyasını da ekleyin.
2. GitHub’da **Settings → Pages → Build and deployment → Source → GitHub Actions** seçin.
3. **Actions → Publish Ali Abi and Zoyo → Run workflow** ile yayını başlatın. `main` veya `master` dalındaki sonraki değişiklikler otomatik yayınlanır.
4. Pages alanında gösterilen adresi açın. Canonical, paylaşım adresleri, robots.txt ve sitemap gerçek yayın adresiyle hazırlanır; GitHub proje alt yolları desteklenir.

Bu teslim GitHub hesabınıza yüklenmedi; yayın dosyaları pakette hazırdır. Tasarımı yerel olarak `index.html` dosyasını açarak da inceleyebilirsiniz. Sosyal medya kartları doğrudan harici platforma gider.

## Alan adını daha sonra bağlama

GitHub Pages’te Custom domain alanına seçtiğiniz alan adını ekleyin, GitHub’ın gösterdiği DNS kayıtlarını sağlayıcınızda tanımlayın ve HTTPS’yi açın. Yayın akışını yeniden çalıştırın.

`content/site.json` içindeki `site_url` boş olduğunda GitHub yayın adresini otomatik bildirir. GitHub dışındaki sunucular için bu alana gerçek HTTPS adresini yazıp derleyin. Adres belirtilmeyen ZIP’te örnek bir alan adı bulunmaz; sitemap başlangıç dosyası boştur. Gerçek adresle derlendiğinde 14 indekslenebilir sayfanın URL’si oluşur.

## Yeni fotoğraflar ve eşit ölçüler

Ana sayfada son gönderilen kaynaklardan seçilen **sekiz gerçek etkinlik fotoğrafı** kullanılır. Yeni arşivdeki bütün farklı kareler eklendi; aynı yakın sahne fotoğrafının iki kopyası tek kare olarak kullanıldı. Eski imza fotoğrafı hem tanışma alanından hem galeriden çıkarıldı. İstenmeyen mavi perdeli kare de kullanılmaz. Sanatçıyı tanıtan görsel, Ali Cengiz’in Zoyo ile gösteri yaptığı sahne fotoğrafıdır.

| Dosya veya klasör | İçerik |
| --- | --- |
| `assets/img/photos/` | 20 fotoğrafın eşit 480 × 640 ve 960 × 1280 kartları; ayrıca büyük, doğal oranlı sürümler |
| `assets/img/ali-cengiz-sahnede.webp` | Zoyo ile sahnedeki Ali Cengiz; 1200 × 1500 |
| `assets/img/stage.webp`, `festival.webp`, `special.webp` | Üç yeni hizmet görseli; her biri 1200 × 900 |
| `gorseller-orijinal/` | Banner ve 20 fotoğrafın kaynak ölçüsünde WebP yedekleri |
| `gorseller-duzenlenmis/` | Netlik, ışık veya fon düzenlemesi uygulanmış üç seçili kaynak |
| `gorseller-uhd/` | Banner, 20 fotoğraf ve altı sosyal kapağın 3840 px uzun kenarlı dışa aktarımları |

Yeni fotoğraflarda yüksek çözünürlüklü özgün dosyalar kullanıldı. Yakın okul sahnesi fotoğrafına kontrollü restorasyon uygulandı; diğer yeni karelerde gerçek yüzler ve mekân geometrisi korunarak orijinal kaynaklardan WebP üretildi. Gerçek fotoğraf kartlarında sallanma, dönüş veya yakınlaşma animasyonu yoktur. Sadece arka plan dekoru hareketlidir.

3840 px dışa aktarım, kayıp ayrıntının geri kazanıldığı anlamına gelmez. Kartlar küçük WebP sürümlerini geç yükler; büyük dosya ancak büyütme veya indirme istendiğinde açılır. Fotoğraf penceresi doğal oranı korur ve klavye/dokunma gezinmesini destekler.

Fotoğraf listesi `content/photos.json`, teknik boyut üretimi `scripts/prepare-media.py` içindedir. Normal GitHub yayını hazır görselleri kullanır; Pillow veya ImageMagick kurulumu gerektirmez. Fotoğraf üretme betiği ayrıca bu araçları ister. `source_crop: false` yeni orijinal dosyalarda gereksiz ekran görüntüsü kırpmasını engeller.

## Logo ve mobil üst bölüm

Yeni logo, gönderilen Ali Abi ve Zoyo ikilisiyle hazırlanmıştır. Şeffaf PNG ve simge dosyaları `logo/`, web sürümleri `assets/img/kuklamukla-tv-logo*.webp` içindedir. Üst ve alt bölüm aynı logoyu kullanır. Favicon ve cihaz simgesi de yeni markayla eşleşir.

Mobil ana başlık iki dengeli satırdır. Birincil iletişim düğmesi ile ayrı yuvarlak video bağlantısı kullanılır. Bannerda aynı onaylanan ikili korunur; üstündeki kalın perde, etiket ve ek çerçeve katmanları kaldırılmıştır. Arka planın renkli ve hareketli sahnesi korunur.

## YouTube ve Instagram

**Sitede video oynatılmaz.** Dört YouTube kartı ilgili gerçek Shorts videosunu, iki Instagram kartı verilen `@kuklamuklatv` hesabını yeni sekmede açar. Instagram kartları belirli bir Reel’in varlığını iddia etmez; hesaptaki paylaşımlara yönlendirir.

Altı kapak, gönderilen çizimli Ali Abi ve Zoyo referansıyla farklı pozlarda, sahnelerde ve renklerde hazırlandı. Turkuaz sahne, yeşil park, gece mavisi gezegen, mercan sahne, pembe–mint ve lila–mavi masal dünyası kullanılır. Yazılar ve platform işaretleri HTML/CSS katmanındadır. Mobilde büyük kapaklar yatay kaydırılarak gezilir.

Sayfa açılışında YouTube veya Instagram oynatıcısı, API betiği ve uzak kapak isteği yoktur. Her kapak yerel WebP dosyasıdır. Sosyal içerikler otomatik çekilmez; API anahtarı gerekmez.

Yeni kartlar için `content/site.json` dosyasındaki `videos` listesine `id`, `platform`, `url`, `cover`, `title` ve `label` ekleyin. Kapağı `assets/img/covers/` içine koyun. `platform` değeri YouTube veya Instagram olabilir. YouTube’da gerçek Shorts kimliğini; Instagram’da gerçek hesap ya da paylaşım bağlantısını kullanın. Desteklenen bağlantı denetimini `scripts/check.py` içinde de güncelleyin.

## İletişim ve kayan düğmeler

Telefon ve WhatsApp: **+90 538 248 72 08**. Sağ alttaki WhatsApp düğmesi `905382487208` numarasını, Instagram düğmesi `@kuklamuklatv` hesabını açar. Gerçek marka ikonları, temaya uygun renkli konuşma balonu çerçevelerinde kullanılır. Mobilde düğmeler yan yana, masaüstünde alt alta durur. Hafif hareketler durdurma düğmesine ve azaltılmış hareket tercihine uyar.

Bilgiler `content/site.json` içindeki `phone`, `whatsapp` ve sosyal hesap alanlarından yönetilir. Etkinlik aracı yalnızca mesaj taslağı hazırlar; verileri kaydetmez ve mesajı kendiliğinden göndermez. Ziyaretçi, hazırlanan metni WhatsApp’ta inceleyip kendisi gönderir.

## Tema ve mobil kullanım

Perdeler, bulutlar, güneş, flamalar, balonlar ve dekoratif kukla çizimleri hafif SVG ve CSS ile hareket eder. “Hareketi durdur” düğmesi ve cihazın azaltılmış hareket tercihi desteklenir. Ekran dışındaki veya gizli sekmedeki hareketler duraklatılır.

Renkli ve hareketli arka tema `assets/css/cartoon.css`, galeri ve sosyal kartlar `assets/css/media.css`, sadeleştirilmiş başlık, banner, logo ve kart düzenleri `assets/css/refined.css` içindedir. Bayrak, bulut, balon ve kukla animasyonları korunur; köşeye eklenen küçük ipli kukla yavaşça sallanır. Yerel Fredoka başlık ve Nunito Sans gövde yazı tipleri Türkçe karakterleri içerir. Gerçek Lucide ve Simple Icons ikonları kullanılır. Marka tüm metinlerde **kuklamukla TV** biçimindedir.

## Düzenleme ve doğrulama

```bash
python3 scripts/build.py
python3 scripts/check.py
node --check assets/js/main.js
python3 scripts/export.py
```

Komutları proje klasöründe çalıştırın. Derleme ve kontrol betikleri Python standart kütüphanesiyle çalışır. `prepare-media.py` ayrıca ImageMagick ve Pillow ister; normal yayın için çalıştırılmaz. Tarayıcıda JavaScript kullanıldığından `.java` yerine `.js` bulunur.

`_site/`, ziyaretçiye sunulacak HTML ve varlıkları içerir. Kaynak JSON, belgeler ve orijinal görsel yedekleri bu çıktıya eklenmez; indirilebilir `gorseller-uhd/` eklenir.

Paket 15 HTML sayfası, 81 il listesi, özgün hizmet içerikleri, fotoğraf galerisi, sosyal video kartları, iletişim, SSS, gizlilik ve 404 sayfasını içerir. SEO eşlemesi `docs/SEO-PLANI.md`, görsel ve lisans bilgileri `docs/VARLIKLAR.md`, doğrulama sonuçları `docs/KONTROL.md` içindedir.

81 il bölümündeki gezici kukla sahnesi `content/tour-scene.html` içindedir. Hareketli rota, küçük konum işaretleri ve perde detayları kullanılır; karakter görüntüsü sabittir. Yeni alanın ve kayan iletişim düğmelerinin stilleri `assets/css/engagement.css` dosyasındadır.
