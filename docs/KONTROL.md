# Tamamlanan kontroller

Bu rapor çift yönlü React galerisi bulunan 25 fotoğraflı teslim sürümünü belirtir.

## Sayfa ve fotoğraf kontrolü

15 sayfa; 320, 360, 390, 430, 768, 1024 ve 1440 px genişliklerde Chromium tarayıcısında denetlendi. **105 kontrol, 0 hata.** Yatay sayfa taşması, kesilen başlıklar, mobil menü, Instagram hedefleri ve sabit bağlantının dokunma boyutu kontrol edildi. Galerinin kendi içindeki yatay fotoğraf akışı sayfa taşmasından ayrı denetlendi.

25 fotoğraf yedi genişlikte açıldı: **175 büyük görünüm kontrolü, 0 hata.** Doğal oranlı gösterim ve indirme bağlantısının bulunmaması doğrulandı. Galeri filtrelerinin üst bölümlerdeki dört fotoğrafı gizlemediği de denetlendi.

## İki sıralı galeri kontrolü

**11 kontrol, 0 hata:** yedi ekran genişliği, iki hızlandırılmış döngü ve JavaScript kapalı iki görünüm.

- Üst sıranın sola, alt sıranın sağa hareket ettiği ölçüldü.
- İki sıranın sol kenarları, genişlikleri ve aralarındaki boşluk denetlendi.
- Hızlandırılmış 390 px denemesinde sıralar 10 ve 12; 1440 px denemesinde 8 ve 9 döngü tamamladı.
- Döngüler sonunda ana sayfada 25 fotoğraf ve 25 farklı fotoğraf kimliği kaldı. Görsel kopyası oluşturulmadı.
- Fareyle bekletme, büyük fotoğraf penceresi açılınca akışın durması, filtreleme ve büyütme sınandı.
- JavaScript kapalı 390 ve 1440 px görünümlerinde fotoğraflar yatay kaydırmayla erişilebilir kaldı.

Animasyon ölçümleri, tarayıcının animasyon başlangıcına hazır olduğunu bildirmesinden sonra alındı. Azaltılmış hareket için CSS ve JavaScript davranışı kaynakta denetlendi; ayrı bir işletim sistemi ayarı testi yapılmadı.

Doğrudan fotoğraf bağlantıları 390 ve 1440 px genişlikte iki sıradan örneklerle sınandı: **4 kontrol, 0 hata.** Hedef fotoğrafın sıra içinde görünmesi ve doğru büyütme penceresinin açılması doğrulandı.

## Dosyalar ve derleme

`npm run build:slider`, `npm run typecheck`, `python3 scripts/check.py` ve JavaScript sözdizimi kontrolleri başarılı. React bileşeni, TypeScript kaynakları, Tailwind giriş dosyası, shadcn yapılandırması, kilit dosyası ve hazır tarayıcı çıktıları teslim paketindedir.

Galeri React ile önceden HTML olarak üretilir; tarayıcıda aynı HTML’e bağlanır. Hazır tarayıcı kodu yalnızca ana sayfada yüklenir. Tema sıfırlaması eklenmez; Tailwind sınıfları kendi önekini kullanır. GitHub iş akışına galeri derlemesi eklenmiştir.

73 WebP sürümü 25 ayrı kaynaktan gelir. Kaynak ve kaynak piksel özetleriyle tekrar kontrolü yapılır. Önceki fotoğraf dosyaları, ana banner ve çizgi film dekoru korunmuştur. Yeni kareler kaynak çözünürlüğü üzerine büyütülmemiştir.

## Kapsam

Kontroller yerel tarayıcı ve kaynakları kapsar. Dış sosyal platformlardaki oturum durumu sınanmadı. Canlı GitHub yayınına dosya gönderilmedi.
