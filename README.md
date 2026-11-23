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

## Fotoğraflar ve eşit ölçüler

Bannerda kullanıcının sağladığı Ali Abi ve Zoyo çizimi kullanılır. Galeride gönderilen **18 gerçek etkinlik fotoğrafı** bulunur. Gerçek fotoğraflarda yüzler yeniden çizilmedi; hafif ışık ve keskinlik düzenlemesi ile kenarlardaki ekran görüntüsü kontrollerinin kırpılması uygulandı.

| Dosya veya klasör | İçerik ve ölçü |
| --- | --- |
| `assets/img/ali-abi-zoyo-hero-640.webp` ve `-1280.webp` | 640 × 800 ve 1280 × 1600 banner |
| `assets/img/photos/` | Her fotoğraf için 480 × 640, 960 × 1280 kart ve doğal oranlı büyük görüntü |
| `assets/img/stage.webp`, `festival.webp`, `special.webp` | Gerçek fotoğraflardan 1200 × 900 hizmet görselleri |
| `assets/img/ali-cengiz-portre.webp` | Gerçek Ali Cengiz fotoğrafı; 1200 × 1500 |
| `assets/img/covers/` | Altı farklı resimli sosyal medya kapağı; her biri 960 × 1280 |
| `gorseller-uhd/` | Banner, 18 fotoğraf ve altı kapağın uzun kenarı 3840 px olan WebP dışa aktarımları |
| `gorseller-orijinal/` | Gönderilen banner ve 18 fotoğrafın kaynak ölçüsünde WebP kopyaları |

3840 px dosyalar yüksek çözünürlüklü dışa aktarımlardır; düşük çözünürlüklü kaynaklarda bulunmayan gerçek ayrıntıyı geri getirdiği iddia edilmez. Site ilk açılışta büyük indirme dosyalarını yüklemez. Galeri kartları küçük WebP sürümlerini kullanır; fotoğrafa dokununca büyük sürüm açılır. Önceki/sonraki düğmeleri, klavye ve yatay dokunma hareketi desteklenir. “WebP indir” bağlantısı büyük dosyayı indirir. Eski etkinlik afişi **arşiv afişi** olarak etiketlenir.

Yeni fotoğraflar `content/photos.json` içinden yönetilir. `source` alanı fotoğraf hazırlama sırasında kullanılan kaynak dosya adıdır. `scripts/prepare-media.py`, kaynak yüklemeler mevcutsa ImageMagick ve Pillow ile tüm boyutları yeniden üretir; GitHub yayını bu işleme ihtiyaç duymaz. Yeni dosyalarda kart ölçülerini aynı tutun. Hazır HTML yerine kaynak şablonları düzenleyin.

## YouTube ve Instagram

**Sitede video oynatılmaz.** Dört YouTube kartı ilgili gerçek Shorts videosunu, iki Instagram kartı verilen `@kuklamuklatv` hesabını yeni sekmede açar. Instagram kartları belirli bir Reel’in varlığını iddia etmez; hesaptaki paylaşımlara yönlendirir.

Altı kapak, gönderilen çizimli Ali Abi ve Zoyo referansıyla farklı pozlarda, sahnelerde ve renklerde hazırlandı. Turkuaz sahne, yeşil park, gece mavisi gezegen, mercan sahne, pembe–mint ve lila–mavi masal dünyası kullanılır. Yazılar ve platform işaretleri HTML/CSS katmanındadır. Mobilde büyük kapaklar yatay kaydırılarak gezilir.

Sayfa açılışında YouTube veya Instagram oynatıcısı, API betiği ve uzak kapak isteği yoktur. Her kapak yerel WebP dosyasıdır. Sosyal içerikler otomatik çekilmez; API anahtarı gerekmez.

Yeni kartlar için `content/site.json` dosyasındaki `videos` listesine `id`, `platform`, `url`, `cover`, `title` ve `label` ekleyin. Kapağı `assets/img/covers/` içine koyun. `platform` değeri YouTube veya Instagram olabilir. YouTube’da gerçek Shorts kimliğini; Instagram’da gerçek hesap ya da paylaşım bağlantısını kullanın. Desteklenen bağlantı denetimini `scripts/check.py` içinde de güncelleyin.

## İletişim

Telefon verilmediği için iletişim mevcut Instagram hesabına yönlenir. `content/site.json` içindeki `phone` ve `whatsapp` alanlarına ülke koduyla gerçek numara eklendiğinde ilgili kanallar görünür.

Etkinlik aracı yalnızca **mesaj taslağı** hazırlar. Bilgileri kaydetmez ve mesaj göndermez. Ziyaretçi metni kopyalayıp Instagram’dan iletir; WhatsApp numarası eklendiğinde bağlantı da oluşur.

## Tema ve mobil kullanım

Perdeler, bulutlar, güneş, flamalar, balonlar ve dekoratif kukla çizimleri hafif SVG ve CSS ile hareket eder. “Hareketi durdur” düğmesi ve cihazın azaltılmış hareket tercihi desteklenir. Ekran dışındaki veya gizli sekmedeki hareketler duraklatılır.

Tema `assets/css/cartoon.css`, galeri ve sosyal kart düzenleri `assets/css/media.css` içindedir. Yerel Fredoka başlık ve Nunito Sans gövde yazı tipleri Türkçe karakterleri içerir. Gerçek Lucide ve Simple Icons ikonları kullanılır. Marka tüm metinlerde **kuklamukla TV** biçimindedir.

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
