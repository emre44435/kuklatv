# Teslim öncesi kontrol

Çizgi film teması güncellemesinde masaüstü ve 320 / 390 / 768 CSS piksel genişlikler yeniden incelendi. Ana sayfada yatay taşma ve bozuk görsel görülmedi. Animasyonun çalışan → duraklatılmış → çalışan geçişi, düğme etiketi ve `aria-pressed` durumu tarayıcıda doğrulandı. Sahne ekran dışına çıktığında hareketlerin duraklatılması kontrol edildi. Yeni temada gerçek YouTube oynatıcısının açılması ve kapatılınca kaldırılması da doğrulandı. Azaltılmış hareket tercihi CSS düzeyinde desteklenir.

23 Kasım 2026 tarihinde uygulanan kontroller:

| Kontrol | Sonuç |
| --- | --- |
| 14 HTML dosyası, tek H1, özgün başlık ve açıklama | Geçti |
| Yerel bağlantılar, görsel ve yazı tipi dosyaları | Geçti |
| Sayfa içi JSON verileri | Geçti |
| JavaScript söz dizimi | Geçti |
| 81 benzersiz il ve 4 geçerli video kimliği | Geçti |
| Alan adı olmadan önizleme | Geçti; örnek alan adı yayınlanmıyor |
| Gerçek URL tanımlama mantığı, kök alan adı ve depo alt yolu | Ayrı test kopyalarında geçti; her birinde 13 sitemap URL’si ve doğru canonical adresleri |
| Masaüstü ana sayfa, video alanı ve hizmet sayfası | Tarayıcıda görsel kontrol yapıldı |
| 320, 390 ve 768 CSS piksel genişlik | Tarayıcıda aynı kaynağı kullanan çerçevelerde kontrol edildi; yatay taşma yok |
| Mobil menü ve Escape ile kapatma | Geçti |
| Türkçe karakterli şehir araması | “MERSİN” araması yalnızca Mersin’i gösterdi |
| Şehirden iletişim sayfasına geçiş | Mersin otomatik seçildi |
| Mesaj taslağı hazırlama ve kopyalama | Geçti; otomatik mesaj gönderilmedi |
| YouTube tıklamadan önce | Sayfada YouTube iframe’i yok |
| Video penceresi açma | Gerçek Paylaşmak videosunun YouTube oynatıcısı yüklendi |
| Video penceresini kapatma | Iframe kaldırıldı, odak oynat bağlantısına döndü |
| Sık sorulan soru açma | Cevap görünür oldu |

GitHub hesabı ve depo verilmediği için GitHub’a dosya yükleme, gerçek Actions çalıştırması, DNS, Search Console doğrulaması ve canlı yayın testi yapılmadı. Yayın akışı, mevcut resmi GitHub Pages belgelerine göre hazırlandı. Alan adı seçildiğinde yayın adresiyle sitemap ve canonical üretimi devreye girer.

Lighthouse puanı, gerçek kullanıcı Core Web Vitals verisi, trafik veya Google sıralaması ölçülmedi. Bunlar için canlı yayın ve yeterli kullanım verisi gerekir.
