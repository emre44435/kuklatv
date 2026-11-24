# Son sürüm kontrolleri

Bu rapor, fareyle ve dokunarak kaydırılabilen çift yönlü galeri içeren V5 teslim sürümünü belirtir.

## Otomatik ve elle kaydırma

Chromium tarayıcısında **20 kontrol, 0 hata**:

- 320, 360, 390, 430, 768, 1024 ve 1440 px genişliklerde otomatik yön, iki sıranın hizası ve yatay sayfa taşması denetlendi.
- 390 px mobil görünümde her iki sırada sağa ve sola TouchEvent hareketleriyle kaydırma sınandı: dört ayrı yön denemesi.
- 1440 px masaüstü görünümde her iki sırada sağa ve sola fare hareketleriyle kaydırma sınandı: dört ayrı yön denemesi.
- Basılı tutarken akışın durduğu, sürükleme sırasında fotoğraf penceresinin açılmadığı ve bırakıldıktan bir saniye sonra otomatik akışın kendi yönünde devam ettiği ölçüldü.
- Fotoğraf penceresi açıkken hareketin durması, indirme bağlantısının bulunmaması, kategori filtreleri ve dikey dokunma hareketinin engellenmemesi denetlendi.
- 390 ve 1440 px görünümlerinde hızlandırılmış döngü boyunca boşluk oluşmadığı ve 25 fotoğrafın tekil kaldığı kontrol edildi.
- JavaScript kapalı 390 ve 1440 px görünümlerinde fotoğraflar yatay kaydırmayla erişilebilir kaldı.

Normal hareket hızı 24’ten 26 piksel/saniyeye çıkarıldı; yaklaşık %8 artış. 400 ms ölçüm aralığında iki sıra ters yönlerde yaklaşık 10,4 piksel hareket etti. Üzerinde yalnızca imlecin bulunması hareketi durdurmaz; basılı tutma, klavye odağı veya fotoğraf penceresi akışı durdurur.

Dokunma kontrolü Chromium içinde TouchEvent ile yapıldı; fiziksel iPhone/Android cihaz testi yapılmadı. Azaltılmış hareket tercihi otomatik akışı durdurur; bu koşulun kaynak uygulaması denetlendi.

Doğrudan fotoğraf bağlantıları 390 ve 1440 px genişliklerde, her iki sıradan örneklerle tekrar denetlendi: **4 kontrol, 0 hata.** Hedef fotoğrafın doğru yerde görünmesi ve büyük penceresinin açılması doğrulandı.

## İçerik ve derleme

`npm run build` ve `npm run check` başarılı. 15 HTML sayfası, 25 tekil fotoğraf yerleşimi, 73 responsive WebP ve 81 il denetimi geçti. React/TypeScript kaynakları, Tailwind stilleri, shadcn yapılandırması, bağımlılık kilit dosyası ve hazır tarayıcı dosyaları pakettedir.

Fotoğraf dosyalarının 73’ü, mevcut banner ve tema kaynakları bir önceki sürümle dosya özetleri üzerinden karşılaştırıldı; değişmedikleri doğrulandı. Fotoğraf kopyaları oluşturulmaz. Galeri döngüsü mevcut kartların konumlandırılmasıyla sağlanır.

Hazır HTML ve yerel JavaScript/CSS sayesinde ZIP çıkarıldıktan sonra `index.html` doğrudan açılabilir. Geliştirme için `docs/REACT-GALERI-KURULUMU.md` izlenir. Canlı GitHub yayınına dosya gönderilmedi.
