# Tamamlanan kontroller

Bu rapor teslim edilen sürüm üzerinde çalıştırılan kontrolleri belirtir.

## Sayfa ve ekran matrisi

Yerel Chromium tarayıcısında 15 sayfa, aşağıdaki yedi görünüm genişliğinin her birinde denetlendi. Toplam **105 kontrol, 0 hata**.

| Genişlik | Denetlenen sayfa | Sonuç |
| --- | --- | --- |
| 320 px | 15 | Başarılı |
| 360 px | 15 | Başarılı |
| 390 px | 15 | Başarılı |
| 430 px | 15 | Başarılı |
| 768 px | 15 | Başarılı |
| 1024 px | 15 | Başarılı |
| 1440 px | 15 | Başarılı |

Matris; yatay sayfa taşması, içeriklerin görünüm dışına çıkması, kesilen başlıklar, mobil menü açılıp kapanması, menü üzerindeki sabit kontroller, hareket durdurma düğmesi, fotoğrafın doğal oranlı görünümü, gerçek fotoğraflarda hareket uygulanmaması, Instagram hedefleri ve sabit Instagram düğmesinin en az 44 × 44 px olması için çalıştırıldı.

Fotoğraf penceresi matris boyunca toplam 126 kez açıldı. Ayrıca gerçek tıklamalarla mobil menü, fotoğrafın sonraki karesine geçiş, Escape ile kapatma, galeri kategori filtresi, filtrelenmiş fotoğraflar arasında gezinme, Mersin ve Türkçe İstanbul aramaları ile sonuç bulunamayan şehir durumu doğrulandı. Mobil banner ve iletişim bölümü görsel olarak incelendi.

## Kaynak ve dosya doğrulaması

`python3 scripts/check.py` başarılı:

- 15 HTML sayfası, her sayfada tek ana başlık ve farklı sayfa açıklamaları.
- 18 ayrı kaynak fotoğraf ve her biri için yalnızca bir sayfa/içerik konumu.
- 52 WebP ekran sürümü; kaynak boyutunun üzerine büyütme yok.
- Yerel sayfa bağlantıları, bölüm bağlantıları, görseller, srcset hedefleri ve stil dosyalarındaki varlıklar mevcut.
- Instagram bağlantılarının tamamı belirtilen hesaba, güvenli yeni sekmede yönleniyor.
- Altı özgün video kapağı ilgili dış platform bağlantılarıyla korunuyor.
- 81 benzersiz il mevcut.
- Sayfa meta verileri ve yapılandırılmış veriler geçerli.

`node --check assets/js/main.js` başarılı. Yerel site kaynaklı tarayıcı hata veya uyarı kaydı gözlenmedi.

Gerçek bir dış alan adı eklenmeden, yerel HTTPS adresi ve alt dizinli adres yapısı ile sayfa üretimi ayrıca sınandı. Bu üretimde canonical bağlantıları ve 14 sayfalık sitemap doğrulandı. Teslim dosyaları daha sonra göreli yerel adreslerle yeniden üretildi. GitHub yayını mevcut iş akışındaki gerçek yayın adresini kullanır.

Bütün sayfalar, kaynak içerikler, JavaScript, stiller ve teslim belgeleri içerik açısından tarandı. İletişim çağrıları Instagram hesabı çevresinde birleştirildi. Artık kullanılmayan eski görsel arşivleri teslim dosyalarına eklenmedi.

## Doğrulamanın sınırı

Bu rapor yerel tarayıcı ve kaynak kontrollerini kapsar. Dış sosyal platformların oturum veya erişilebilirlik durumu test edilmedi; bağlantıların hedefleri doğrulandı. Canlı GitHub yayınına dosya gönderimi yapılmadı.
