# Ali Abi ve Zoyo · Ali Cengiz

Okul, belediye ve çocuk etkinlikleri için hazırlanmış Türkçe kukla gösterisi sitesi. HTML, CSS ve JavaScript ile çalışır. Ziyaretçiler için kurulum, üyelik veya uygulama indirme gerekmez.

## Hızlı başlangıç

1. ZIP dosyasını çıkartın. `index.html` ile tasarımı açabilirsiniz. Gerçek video pencerelerini denemek için siteyi HTTP üzerinden açın; dosyaya çift tıklayarak açıldığında videolar YouTube bağlantısıyla çalışır.
2. Dosyaları GitHub deponuzun **köküne** yükleyin. `index.html` bir alt klasörde kalmasın. `.github/workflows/pages.yml` dosyası da depoda bulunmalı.
3. GitHub deposunda **Settings → Pages → Build and deployment → Source → GitHub Actions** seçin.
4. **Actions → Publish Ali Abi and Zoyo → Run workflow** ile yayını başlatın. Sonraki `main` veya `master` değişikliklerinde yayın otomatik güncellenir.
5. İşlem tamamlandığında Pages alanındaki adresi açın. Kanonik adresler, paylaşım görseli adresi, robots.txt ve sitemap gerçek GitHub yayın adresiyle otomatik hazırlanır. Depo adı içeren GitHub proje adresleri de desteklenir.

Bu paket teslim edilirken bir GitHub hesabına yüklenmedi ve canlıya alınmadı. Yayın akışı dosyaları hazırdır; gerçek GitHub hesabınızdaki çalıştırma bu adımdan sonra yapılır.

## Telefon ve WhatsApp

Telefon verilmediği için iletişim bağlantıları mevcut Instagram hesabına yönlenir. Hayali telefon veya e-posta yoktur.

`content/site.json` içindeki `phone` ve `whatsapp` alanlarına ülke koduyla gerçek numarayı yazın. Boş bırakılan kanal gösterilmez. GitHub değişikliği kaydedildiğinde sayfalar yeniden oluşturulur. GitHub dışında düzenliyorsanız `python3 scripts/build.py` komutunu çalıştırın.

Etkinlik aracı bir **mesaj taslağı** hazırlar. Bilgileri kaydetmez veya kendiliğinden göndermez. Ziyaretçi mesajı kopyalar ve Instagram’da gönderir. WhatsApp numarası eklendiğinde hazırlanan metin WhatsApp bağlantısına da aktarılır.

## Alan adını daha sonra bağlama

GitHub Pages → Custom domain alanına alan adınızı ekleyin, GitHub’ın gösterdiği DNS kayıtlarını alan adı sağlayıcınızda tanımlayın ve HTTPS’yi açın. Ardından yayın akışını yeniden çalıştırın. `configure-pages` gerçek adresi bildirdiği için SEO adresleri de güncellenir.

GitHub’da otomatik URL kullanmak için `content/site.json` içindeki `site_url` alanını boş bırakın. GitHub dışındaki bir yayında adresi bu alana yazabilir veya `python3 scripts/build.py --url https://gercek-alan-adiniz` kullanabilirsiniz.

**Alan adı bilinmeyen ZIP sürümünde** yanlış örnek adres yayınlamamak için canonical ve mutlak Open Graph adresleri eklenmez; sitemap.xml URL içermeyen başlangıç dosyasıdır. GitHub Actions yayını bunları gerçek adresle doldurur. Sadece dosya yükleyerek başka bir sunucuda yayınlayacaksanız önce gerçek URL ile derleyin.

GitHub proje adresinde robots.txt depo alt klasöründe kalabilir. Search Console’da proje URL’sini URL öneki mülkü olarak ekleyip sitemap adresini doğrudan gönderin. Özel alan adında dosya alan adı kökünden sunulur.

## Gerçek fotoğrafları ekleme

Görseller geçici tanıtım illüstrasyonlarıdır. Kukla portresi, gerçek Zoyo’nun fotoğrafı değildir; sitede bu görseller “Tanıtım illüstrasyonu” olarak belirtilir. Ali Cengiz’e ait uydurma bir portre, müşteri yorumu veya referans kullanılmadı.

| Dosya | Kullanım | Önerilen oran |
| --- | --- | --- |
| `assets/img/puppet-hero-1120.webp` | Ana görsel | 4:5, yaklaşık 1120 × 1400 |
| `assets/img/puppet-hero-640.webp` | Mobil ana görsel ve tanışma sayfası | Aynı fotoğrafın 640 px genişlikte sürümü |
| `assets/img/stage.webp` | Okul ve sahne görseli | 3:2, 900 × 600 |
| `assets/img/festival.webp` | Belediye ve şenlik görseli | 3:2, 900 × 600 |
| `assets/img/social-cover.webp` | Sosyal paylaşım görseli | 1200 × 630 |

Fotoğrafları aynı dosya adlarıyla değiştirin. Gerçek fotoğraf geldiğinde ilgili `alt` metinlerini ve illüstrasyon etiketlerini `scripts/build.py` içindeki şablonlarda güncelleyin, sonra yeniden derleyin. Sadece oluşturulmuş HTML’yi değiştirirseniz sonraki otomatik derleme o değişikliği ezer.

## Videolar

Kanalda erişilebilen dört gerçek Shorts kullanıldı. Başlık ve bağlantılar 23 Kasım 2026 tarihinde kontrol edildi. Her videonun yerel WebP kapağı, siteye uyumlu başlık alanı ve oynat düğmesi vardır. İlk sayfa açılışında YouTube oynatıcısı, API betiği veya uzak kapak isteği yoktur. Oynatıcı tıklayınca açılır; pencere kapanınca kaldırılır.

Yeni video için `content/site.json` içindeki `videos` listesine gerçek 11 karakterli YouTube kimliği, başlık ve etiket ekleyin. Yerel kapağı `assets/img/short-VIDEO_ID.webp` adıyla kaydedin. Tekrar derleyin. Liste, kanala sonradan eklenen videoları kendiliğinden çekmez; API anahtarı gerektirmez.

Yerleştirmeye kapatılan veya platform tarafından sınırlandırılan videolar için pencerede “YouTube’da aç” bağlantısı bulunur. Kanalın yerleştirme izinleri sitenin kontrolünde değildir.

## Düzenleme ve kontrol

```bash
python3 scripts/build.py
python3 scripts/check.py
node --check assets/js/main.js
```

Yerel önizleme için:

```bash
python3 -m http.server 8000
```

Ardından `http://localhost:8000` adresini açın. Bu komutlar proje klasöründe çalıştırılır. Python derleyicisinin dış paket bağımlılığı yoktur. `.java` yerine tarayıcıların çalıştırdığı `.js` dosyası kullanılır.

Yalnızca ziyaretçiye sunulacak dosyaları ayırmak için `python3 scripts/export.py` çalıştırın. `_site/` çıktısı hazır HTML ve varlıkları içerir; kaynak içerikler ve belgeler bu çıktıya eklenmez.

## Paket

- 14 HTML sayfası: ana sayfa, 6 özgün hizmet/rehber sayfası, tanışma, videolar, 81 il, SSS, iletişim, gizlilik ve 404.
- Yerel yazı tipleri: Fredoka ve Nunito Sans. Harici font bağlantısı yoktur.
- Gerçek Lucide arayüz ve Simple Icons sosyal medya ikonları.
- Mobil menü, klavyeyle kullanılabilen video penceresi, SSS alanı, Türkçe karakter destekli il arama ve mesaj hazırlama.
- Azaltılmış hareket tercihi, görünür klavye odağı, anlamsal HTML ve ekran okuyucu etiketleri.
- Site haritası, robots.txt, yapılandırılmış veri, paylaşım etiketleri ve GitHub Pages yayın akışı.

SEO arama niyeti eşlemesi ve yayın sonrası adımlar `docs/SEO-PLANI.md` dosyasındadır. Tasarım varlıkları ve lisansları `docs/VARLIKLAR.md` dosyasında açıklanır.
