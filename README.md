# kuklamukla TV · Ali Abi ve Zoyo

Ali Cengiz’in Zoyo’yu seslendirip oynattığı canlı kukla gösterilerini tanıtan, mevcut renkli ve animasyonlu görsel kimliği koruyan statik web sitesi.

İletişim adresi: https://www.instagram.com/kuklamuklatv/

## Kullanım

`index.html` dosyasını tarayıcıda açabilirsiniz. Sunucu tarafı uygulama veya veritabanı gerekmez. Bütün HTML sayfaları, yazı tipleri, logo, dekoratif çizimler ve görseller bu arşivde bulunur.

GitHub’da mevcut projenin kökündeki dosyaları bu sürümdekilerle değiştirin. Güncellerken daha önceki gerçek fotoğraf klasörlerini ve artık kaynaklarda yer almayan eski dosyaları da kaldırın. Arşivdeki `.github/workflows/pages.yml` yayın düzeni korunmuştur. GitHub Pages kaynağı **GitHub Actions** olmalıdır. Ana dala gönderimden sonra mevcut iş akışı gerçek yayın adresiyle sayfaları üretir, bağlantıları denetler ve yalnızca yayın dosyalarını aktarır.

## İki sıralı otomatik galeri

Üst sıra sola, alt sıra sağa otomatik akar. Kareler çoğaltılmadan döngüye alınır. React, TypeScript, Tailwind ve shadcn bileşen düzeni projeye eklenmiştir. Kurulum, varsayılan klasörler, bileşen props’ları ve demo bilgileri `docs/REACT-GALERI-KURULUMU.md` dosyasındadır. ZIP hazır JavaScript ve CSS içerir; `index.html` doğrudan açılabilir.

## İçerikleri güncelleme

- `content/site.json`: marka, Instagram hesabı ve dış platformlarda açılan video bağlantıları.
- `content/pages.json`: gösteri sayfaları, açıklamalar ve sık sorulan sorular.
- `content/photos.json`: 25 özgün fotoğrafın tekil sayfa konumları, boyutları ve ekran sürümleri.
- `content/cartoon-scene.html`, `content/tour-scene.html`: dekoratif sahne ve otomatik perdeli 81 il sahnesi.

İçerik dosyaları değişince:

```bash
npm ci
npm run build
```

`SITE_URL` ortam değişkeni gerçek yayın adresini belirler. GitHub iş akışı bunu otomatik sağlar. Adres bilinmiyorsa yerel bağlantılar göreli kalır; alan adı uydurulmaz. İsteğe bağlı `python3 scripts/build.py --url GERÇEK_HTTPS_YAYIN_ADRESİNİZ` komutuyla kendi yayın adresinizi kullanabilirsiniz.

Yalnızca yayın dosyalarını dışa aktarmak için `python3 scripts/export.py` çalıştırın. Sonuç `_site/` dizinine yazılır. Kaynaklar ve bu belgeler dışa aktarıma eklenmez.

## Referanstaki açılış bannerı

Ana sayfanın ilk ekranında ve 81 il sayfasında referanstaki hizalı, mor/altın sahne tasarımı kullanılır. Çizgili çember ve konum işaretleri kaldırılmıştır. Görsel, bilgi satırı ve metin sütunu ortak ölçülere oturur. Mobilde önce iki satırlı başlık ve tam genişlikte Instagram bağlantısı, ardından sahne gelir. Eski çizgi film dekoru, renkli bayraklar ve kukla arka planı bannerın devamındaki tanıtım bölümünde korunur. Galeri dar ekranlarda taşmadan tek veya iki sütuna uyarlanır. Perde yaklaşık 2,3 saniyede açılır ve açık kalır; arka plan ışıkları görünür biçimde otomatik hareket eder. Ali Abi ve Zoyo’nun çizimi sabittir. Stil kaynakları `assets/css/tour.css` ve `assets/css/harmony.css`, davranış kaynağı `assets/js/main.js` dosyasıdır; bir kurulum veya harici animasyon servisi gerekmez.

## Fotoğraflar

25 görselin tamamı `assets/img/photos/` altında optimize edilmiş WebP olarak bulunur. 25 fotoğrafın tamamı ana sayfada birer kez gösterilir: üç gösteri kartı, bir tanıtım fotoğrafı ve 21 karelik galeri. Diğer sayfalardaki bağlantılar bu fotoğrafların ana sayfadaki konumlarına gider. Düşük ve yüksek ekran çözünürlükleri aynı fotoğrafın responsive sürümleridir. Büyük görünüm kendi kartından açılır ve fotoğrafı doğal oranıyla gösterir. Görüntüleyicide indirme bağlantısı bulunmaz. Son eklenen yedi fotoğrafta yüksek kaliteli WebP sürümleri kullanılır; önceki 18 fotoğraf dosyası korunur.

Karelere yalnızca ölçülü, tüm görüntüye uygulanan ışık ve renk ayarları, gerekli yerlerde doğal kadraj ve iki sınıf fotoğrafına hafif doğrultma uygulanmıştır. Görseller kaynak çözünürlüklerinin üstüne büyütülmemiştir.

Fotoğrafları yeniden hazırlamak gerekirse orijinal 25 JPEG’i ayrı bir klasörde tutup Pillow kurulu bir Python ortamında çalıştırın:

```bash
python3 scripts/photos.py --source-dir ORIJINAL_GORSELLERIN_KLASORU
python3 scripts/build.py
python3 scripts/check.py
```

Normal yayın ve sayfa üretiminde Pillow gerekmez; hazır WebP dosyaları kullanılır. Görsel eşleştirmeleri `docs/FOTOGRAF-KULLANIMI.md` ve `docs/FOTOGRAF-KULLANIMI.csv` içindedir. Ölçülebilen kontroller `docs/KONTROL.md` dosyasında açıklanır.

## Etkileşimler

Mobil menü, fotoğraf büyütme, galeri kategorileri ve il arama yerel JavaScript ile çalışır. Galerinin iki sıralı akışı React bileşenidir. 81 il sahnesinin perdesi görsel ekrana geldiğinde bir kez otomatik açılır. Aç/kapa veya tekrar oynat düğmesi yoktur. Sisteminizin azaltılmış hareket tercihi gözetilir. JavaScript kapalıysa perde açık kalır; içerik kaybolmaz. Fotoğraflar doğal oranlarını korur. Hareket, iki galeri sırasında ve dekoratif öğelerde kullanılır.

Video kapakları ilgili YouTube videosunu veya Instagram hesabını güvenli yeni sekmede açar. Ana iletişim çağrıları Instagram hesabına yönlenir.

## Lisanslar

Font ve ikon lisansları `docs/` içinde korunmuştur. Kullanıcı tarafından sağlanan logo, karakter çizimleri ve etkinlik görselleri mevcut görsel kimliğin parçalarıdır.
