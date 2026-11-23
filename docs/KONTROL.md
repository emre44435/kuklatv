# Teslim öncesi kontrol

23 Kasım 2026 güncellemesi: yeni banner, 18 gerçek fotoğraf, altı özgün sosyal kapak ve mobil kaydırma düzeni.

| Kontrol | Sonuç |
| --- | --- |
| 15 HTML sayfası, tek H1, özgün başlık ve açıklama | Geçti |
| Yerel bağlantılar, görsel ve yazı tipi dosyaları | Geçti |
| Sayfalardaki JSON verileri ve JavaScript söz dizimi | Geçti |
| 81 benzersiz il | Geçti |
| 4 YouTube Shorts ve 2 Instagram hesap kartı | Doğru HTTPS hedefleri; yeni sekme ve noopener |
| Site içi video oynatıcısı | Yok; HTML veya JavaScript iframe oluşturmuyor |
| Altı farklı WebP kapak | Her biri 960 × 1280 px; farklı sahne, renk ve poz |
| 18 gerçek fotoğrafın kart sürümleri | Her biri 480 × 640 ve 960 × 1280 px |
| Büyük WebP dosyaları | Banner, 18 fotoğraf, 6 kapak; toplam 25 dosya, uzun kenar 3840 px |
| Kaynak ölçüsünde WebP yedekleri | Banner ve 18 fotoğraf; 19 dosya |
| Masaüstünde kart hizaları | Tarayıcıda tüm galeri görüntüleri yaklaşık 377 × 503 CSS px; sosyal kapaklar yaklaşık 381 × 508 CSS px |
| 320, 390 ve 768 px çerçevelerde ana sayfa | Yatay sayfa taşması yok; aynı gerçek HTML kaynaklarıyla kontrol edildi |
| 390 px çerçevede mobil sosyal kapaklar | Altı eşit yaklaşık 285 × 380 CSS px kart; yatay kaydırma ve klavyeyle ilerleme çalışıyor |
| 320 px çerçevede mobil sosyal kapaklar | Yaklaşık 233 × 311 CSS px; sayfa taşması yok, kapak şeridi bağımsız kayıyor |
| Mobil kapak yazıları ve eylem | Başlık 26,4 px; platform eylemi en az 44 px yüksekliğinde |
| Mobil menü | Açma ve sayfa seçimi çalışıyor; seçim sonrası kapanıyor |
| Galeri filtreleri | “Okullar” seçimi 3 fotoğraf gösteriyor; sayaç güncelleniyor |
| Fotoğraf büyütme | Doğal oran ve fotoğrafın tamamı korunuyor; WebP indirme yolu doğru |
| Galeride önceki/sonraki ve klavye | Geçti; filtrelenmiş liste içinde dolaşıyor |
| Fotoğraf penceresini kapatma | Escape ve düğme çalışıyor; odak açan karta dönüyor |
| Mobil fotoğraf penceresi | Ekrana sığıyor; kapatma ve gezinme düğmeleri 44 × 44 px |
| Arka plan hareketini durdurma | aria-pressed ve duraklatma durumu güncelleniyor |
| Gerçek URL üretimi | Ayrı test kopyasında kök alan adı ve depo alt yolu geçti; her birinde 14 sitemap URL’si |
| Alan adı belirtilmeyen teslim | Örnek alan adı yok; başlangıç sitemap’i boş, GitHub yayını gerçek adresle dolduruyor |

Masaüstü ve dar genişlik kontrolleri tarayıcıda yapıldı; gerçek telefon donanımı üzerinde cihaz testi yapılmadı. Kaydırma çubuğu nedeniyle 320 / 390 / 768 px çerçevelerin içerik genişliği 305 / 375 / 753 px olabilir. Taşma karşılaştırmasında belgenin gerçek içerik genişliği kullanıldı.

Gerçek fotoğrafların yüzleri üretken düzenlemeyle yeniden çizilmedi. Büyük dosyalar kaynaklardan ölçeklenmiş dışa aktarımlardır; kayıp ayrıntı geri kazanımı iddiası yoktur. Resimli kapaklar tanıtım tasarımıdır; gerçek video karesi gibi sunulmaz. Instagram kartları belirli bir Reel yerine verilen hesaba gider.

Önceki sürümde doğrulanan şehir araması, şehirden iletişime seçim taşıma, mesaj taslağı hazırlama ve SSS işlevleri korunur. Otomatik mesaj gönderme veya veri kaydetme yoktur.

GitHub hesabı ve depo verilmediği için dosya yükleme, gerçek Actions çalıştırması, DNS, Search Console ve canlı yayın testi yapılmadı. Lighthouse veya gerçek kullanıcı performans puanı ölçülmedi.
