# Tasarım varlıkları

## Gerçek etkinlik fotoğrafları

Galeri 20 ayrı fotoğraf içerir. Son gönderilen sekiz dosyalık arşivdeki farklı kareler eklendi. Yakın okul sahnesi fotoğrafının ayrıca gönderilen kopyasıyla tek bir galeri kaydı oluşturuldu. Önceki kaynaklardan aynı fotoğraf olan `01`, `04`, `05` ve `18` kayıtları daha yüksek çözünürlüklü yeni orijinalleriyle yenilendi. Dört yeni kayıt `19`, `20`, `21`, `22` kimliklerindedir. Ana sayfada bu sekiz güncel kare gösterilir.

`14-ali-cengiz-imza` ve `09-mavi-perdeli-sahne` fotoğrafları, varyantları ve eski imza portresi çıkarıldı. Yeni kaynakların çoğu doğrudan gerçek fotoğraflardan WebP olarak üretilir. `19` kimlikli yakın okul sahnesine kontrollü fotoğraf restorasyonu uygulandı; bu işlem kayıp ince ayrıntıların birebir geri kazanımı olarak sunulmaz. Önceki `08` ve `12` düzenlenmiş kareleri galeride bulunur. Orijinal WebP yedekleri ve düzenlenmiş kaynaklar ayrı klasörlerdedir.

Bütün kartlar 3:4 oranında 480 × 640 ve 960 × 1280 pikseldir. Büyütme görünümü doğal fotoğraf oranını korur. Hizmet kartları 1200 × 900, tanışma görseli 1200 × 1500 pikseldir. Gerçek fotoğraflara hareketli dönme, sallanma veya zoom uygulanmaz. 3840 px büyük dosyalar ölçeklenmiş dışa aktarımlardır.

Göksun etkinlik afişi geçmiş etkinlik görselidir; güncel saat/tarih ilanı olarak sunulmaz.

## Banner ve sosyal kapaklar

Banner, kullanıcının verdiği çizimli Ali Abi ve turuncu Zoyo görselinden hazırlanmıştır. Bu bir tanıtım çizimidir. Sosyal medya kapakları aynı karakter referansıyla özgün olarak üretilmiştir. Referanstaki siyah çerçeveli gözlük, belirgin kıvrık bıyık, pembe gömlek, koyu askılar; Zoyo’nun turuncu tüyleri, uzun kulakları, mavi burnu ve iki ön dişi korunur. Pozlar ve çevre kapaklara göre değişir.

| Kapak | Sahne ve renk | Bağlantı |
| --- | --- | --- |
| `youtube-01.webp` | Hediye paylaşma, turkuaz ve altın | Paylaşmak · B8wlJ1Jrzro |
| `youtube-02.webp` | Parkta bank, yeşil ve gökyüzü mavisi | Parktaki Çocuklar · g4sx3WoJEy4 |
| `youtube-03.webp` | Hayalî gezegen, gece mavisi ve altın yıldızlar | Büyük Z Gezegeni · g3krZ8XySIY |
| `youtube-04.webp` | Şaşkın sohbet, mercan ve sıcak turuncu | Yalan · YAKxwfMalA4 |
| `instagram-01.webp` | Neşeli sahne, pembe ve mint | @kuklamuklatv Instagram hesabı |
| `instagram-02.webp` | Masal kitabı ve şato, lila ve açık mavi | @kuklamuklatv Instagram hesabı |

Kapak çizimleri gerçek videolardan alınmış kareler değildir; tanıtım tasarımıdır. Başlık, platform rozeti, marka ve bağlantı eylemi kodla eklenir. Her görsel 960 × 1280 piksel WebP’dir; büyük dışa aktarımlar `gorseller-uhd/kapak-*.webp` içindedir. Video dosyaları pakete kopyalanmaz; platformların hesabına veya YouTube videosuna dış bağlantı verilir. Sitede oynatıcı yoktur.

## Dekoratif sahne

Bulut, güneş, balon, flama, yıldız, tepe ve küçük kukla çizimleri projeye özel SVG olarak yazıldı. `content/cartoon-scene.html`, `content/stage-valance.svg` ve `assets/img/cartoon-sprinkles.svg` içinde yer alır. Ekran okuyucu ve tıklama akışına katılmayan dekorlardır. CSS hareketleri kapatılabilir; harici animasyon kütüphanesi kullanılmaz.

## Yazı tipleri ve ikonlar

Fredoka başlık fontu, kullanıcının paylaştığı afişin dolgun ve eğlenceli harflerine yakın seçilmiştir. Nunito Sans gövde metninde kullanılır. Yazı tipleri yereldir, Türkçe karakterleri içerir ve `font-display: swap` ile yüklenir. Lisans metinleri bu klasördedir.

Arayüz ikonları Lucide, sosyal medya işaretleri Simple Icons kaynaklıdır. Küçük inline SVG biçiminde kullanılır; emoji veya harici ikon betiği yoktur. Favicon ve cihaz simgesi yeni logonun ikili karakter simgesinden hazırlanmıştır; PNG dosyaları ve PNG içeren SVG kapsayıcı `assets/icons/` içindedir.


## Yeni logo ve arka plan kuklası

Yeni yatay logo, kullanıcının sağladığı Ali Abi–Zoyo karakter çizimi referansıyla hazırlanmıştır. Koyu turkuaz ana yazı, mercan TV vurgusu ve iki karakterin birlikte yer aldığı açık halka simgesi kullanılır. Logo bir raster görseldir; vektör kaynak olduğu iddia edilmez. Şeffaf yüksek çözünürlüklü PNG ve WebP sürümleri pakettedir. Seçilen son istemler `docs/GORSEL-ISTEMLERI.json` dosyasındadır.

Arka plandaki ek ipli kukla, mevcut SVG sahne diline uygun kodla çizilmiştir. Yalnızca dekoratiftir; pointer olaylarını yakalamaz. Hafif CSS dönüşümleriyle sallanır; ekran dışında, gizli sekmede veya hareket durdurulunca duraklar. Cihazın azaltılmış hareket tercihine uyar.


## WhatsApp ve Instagram iletişim düğmeleri

Instagram işareti projedeki Simple Icons kaynağından, WhatsApp işareti Bootstrap Icons projesinin gerçek `whatsapp.svg` dosyasından alınmıştır. Resmî kaynak: https://github.com/twbs/icons/blob/main/icons/whatsapp.svg . MIT lisans metni `docs/BOOTSTRAP-ICONS-LICENSE.txt` içindedir. Marka işaretleri değiştirilmeden inline SVG kullanılır; konuşma balonu biçimi, renk ve hareket CSS çerçevesidir.

81 il görseli, mevcut vektör sahne diline uygun SVG ile kodlanmıştır. Buradaki Ali Abi–Zoyo görseli onaylanan tanıtım çizimidir; rota ve konum işaretleri dekoratiftir, gerçek bir turne takvimi veya güzergâh iddiası taşımaz.
