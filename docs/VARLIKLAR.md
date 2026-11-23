# Tasarım varlıkları

## Gerçek fotoğraflar

Kullanıcının gönderdiği 18 etkinlik fotoğrafı `content/photos.json` listesinde tanımlıdır. Galeri, sanatçı portresi ve hizmet kartları bu kaynaklardan üretilir. Fotoğraflardaki yüzler, kıyafetler, kuklalar ve mekânlar üretken bir modelle yeniden çizilmedi. Kenardaki görüntüleyici okları ve alt sayfalama noktaları kırpıldı; hafif ışık ve keskinlik düzenlemesi uygulandı. Orijinal ölçüdeki WebP kopyaları ayrı klasörde bulunur.

Her galeri kartının görüntüsü aynı 3:4 oranında, 480 × 640 ve 960 × 1280 pikseldir. Büyütme görünümü doğal oranı korur. Hizmet kartları 1200 × 900 pikseldir. Büyük indirme dosyalarının uzun kenarı 3840 pikseldir; bu ölçekleme kaynakta bulunmayan ayrıntının geri kazanıldığı anlamına gelmez.

Göksun etkinlik afişi geçmiş etkinlik görseli olarak kullanılır; fotoğraf açıklamasında “Arşiv afişi” yazar. Afişteki “bugün” ve saat bilgisi güncel etkinlik ilanı olarak sunulmaz.

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

Arayüz ikonları Lucide, sosyal medya işaretleri Simple Icons kaynaklıdır. Küçük inline SVG biçiminde kullanılır; emoji veya harici ikon betiği yoktur. Favicon projeye özel sade kukla sahnesi çizimidir; düzenlenebilir kaynak `assets/icons/favicon.svg` dosyasıdır.
