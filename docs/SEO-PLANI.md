# Ali Cengiz · Arama niyeti ve SEO planı

Hazırlık tarihi: 23 Kasım 2026. Amaç: okul, belediye ve çocuk etkinliği düzenleyen kişilerin doğru hizmet sayfasına ulaşması ve etkinlik için iletişime geçmesi.

Araştırma, herkese açık arama sonuçları, paylaşılan sosyal hesaplar ve Google’ın teknik belgeleriyle yapıldı. Ücretli anahtar kelime planlayıcısına bağlı kesin hacim, rekabet veya TBM ölçümü yapılmadı. Aşağıdaki öncelikler arama niyetine göre hazırlanmış editoryal değerlendirmedir; ölçülmüş aylık arama sayısı değildir.

## Arama niyeti eşlemesi

| Öncelik | Arama grubu ve örnek sorgular | Niyet | Hedef sayfa |
| --- | --- | --- | --- |
| Yüksek | Ali Cengiz kukla sanatçısı, Ali Abi Zoyo, Zoyo kukla gösterisi, Kukla Mukla TV | Sanatçıyı bulma ve tanıma | `index.html`, ayrıntılı biyografi `ali-cengiz.html` |
| Yüksek | kukla gösterisi, kukla gösterisi organizasyonu, kukla sanatçısı, canlı kukla gösterisi | Gösteri sağlayıcı bulma | `kukla-gosterisi.html` |
| Yüksek | okullarda kukla gösterisi, okula gelen kukla tiyatrosu, okul kukla gösterisi organizasyonu | Okul için sanatçı daveti | `okullarda-kukla-gosterisi.html` |
| Yüksek | anaokulu kukla gösterisi, ilkokul kukla gösterisi, okul öncesi kukla gösterisi | Yaş grubuna uygun etkinlik | `okullarda-kukla-gosterisi.html` |
| Yüksek | belediye kukla gösterisi, belediye çocuk etkinliği, çocuk şenliği kukla gösterisi, kültür merkezi kukla gösterisi | Kurumsal etkinlik planlama | `belediye-kukla-gosterisi.html` |
| Orta | çocuklar için kukla tiyatrosu, çocuk kukla gösterisi, çocuk tiyatrosu kukla | Gösteri türünü ve uygunluğu araştırma | `cocuk-tiyatrosu.html` |
| Mevsimsel yüksek | 23 Nisan kukla gösterisi, 23 Nisan okul etkinliği kukla, 23 Nisan belediye gösterisi | Belirli gün için program bulma | `23-nisan-kukla-gosterisi.html` |
| Yüksek | kukla gösterisi fiyatları, okul kukla gösterisi ücreti, kukla gösterisi kaç dakika, kukla tiyatrosu organizasyonu nasıl yapılır | Bütçe ve hazırlık bilgisi | `kukla-gosterisi-planlama.html` |
| Orta | İstanbul kukla gösterisi, Ankara kukla gösterisi, İzmir kukla gösterisi, Mersin kukla gösterisi ve diğer iller | Şehre gelebilen sanatçı bulma | `hizmet-bolgeleri.html` ve ilgili hizmet sayfası |
| Orta | Zoyo izle, Kukla Mukla TV Shorts, Ali Abi Zoyo video | İçerik izleme | `videolar.html` |
| Yüksek | Ali Cengiz iletişim, kukla gösterisi teklif, Zoyo gösteri davet | İletişime geçme | `iletisim.html` |

Başlık ve metinler ilgili sorguyu doğal bir dille yanıtlar. Ana sayfa marka ve genel teklifi tanıtır; okul, belediye ve özel gün ayrıntıları kendi sayfalarında yer alır. Aynı kelime grubunu hedefleyen çok sayıda benzer sayfa üretilmedi.

Kukla yapımı, kukla satın alma, kukla oyuncak, kukla şablonu, yetişkin kukla kabare gibi sorgular farklı niyetler taşır. Sunulduğu doğrulanmayan Karagöz, ipli kukla, atölye, sihirbaz veya maskot hizmetleri eklenmedi. Çocuk gelişimi veya eğitimde sonuç garantisi verilmedi.

## 81 il stratejisi

81 ilin tamamı erişilebilir HTML listesinde yer alır. Filtre yalnızca görünümü daraltır; içerik arama motoru için JavaScript’e bağlı değildir. İl seçimi iletişim aracına o şehri taşır. Her ilde şube bulunduğu ileri sürülmez.

Tek paragrafın il adını değiştirerek 81 kez kopyalanması yerine, tek hizmet bölgeleri sayfası ve özgün hizmet sayfaları kullanıldı. Gerçek bir ilde gösteri yapıldığında kurum izniyle etkinlik fotoğrafları, tarih, mekân ve o buluşmaya ait özgün anlatımla ayrı bir etkinlik yazısı eklenebilir. Gelecekteki il içerikleri böyle gerçek malzemeyle güçlendirilmelidir.

## Uygulanan teknik yapı

- Metinler, başlıklar ve sayfa bağlantıları hazır HTML içinde. Sayfayı anlamak için JavaScript çalıştırmak gerekmez.
- Her sayfada tek H1, özgün title ve meta açıklama; mantıklı H2 bölümleri ve açıklayıcı iç bağlantılar.
- Gerçek yayın adresiyle kendine işaret eden canonical; ana sayfada `/` biçimi. `/index.html` sitemap’e ayrı bir kopya olarak eklenmez.
- GitHub proje alt yolu dahil otomatik URL üretimi. Özel alan adına geçildiğinde yayın yeniden çalıştırılır.
- Sitemap yalnızca indekslenebilir 13 sayfayı içerir. 404 sayfası noindex’tir ve sitemap’te bulunmaz. Değiştirilmemiş sayfalara her derlemede sahte `lastmod` yazılmaz.
- Gerçek URL bilindiğinde Person, WebSite, WebPage ve hizmet sayfalarında Service verisi. Türkiye ülke hizmet alanıdır; uydurma adres veya puan eklenmez.
- Sayfalardaki görünen sorularla eşleşen FAQPage verisi. Bu, Google’da zengin sonuç gösterileceği anlamına gelmez; uygunluk ve gösterim Google’a bağlıdır.
- Videolar gerçek YouTube bağlantılarıyla ItemList içinde tanımlanır. Bilinmeyen yükleme tarihi, süre veya izlenme sayısı uydurularak VideoObject eklenmez.
- Görsel alt metinleri, boyutlar, sosyal paylaşım görseli, favicon ve manifest.
- WebP görseller, yerel fontlar, küçük bağımsız JavaScript, geç yüklenen alt bölüm görselleri ve tıklamayla yüklenen YouTube oynatıcısı.

Google `meta keywords` etiketini sıralama için kullanmadığından anahtar kelime listesini bu etikete doldurmak yerine sayfa içeriği ve niyet eşlemesi kullanıldı.

## Gerçek yayın sonrası

1. Alan adı / GitHub adresiyle yayını tamamlayın; HTTPS ve sayfaların açıldığını kontrol edin.
2. Gerçek URL ile Search Console mülkünü doğrulayın. Oluşan `sitemap.xml` adresini gönderin.
3. Ana sayfa ve okul/belediye hizmetlerini URL Denetimi’nde kontrol edin. İndeksleme talebi tarama veya sıralama garantisi değildir.
4. Gerçek Ali Cengiz ve Zoyo fotoğraflarını ekleyin. Görünür illüstrasyon etiketleri ve alt metinler de güncellensin.
5. Instagram, YouTube ve Facebook profil açıklamalarına yayınlanan site adresini hesap sahibi eklesin. Şu anda hesaplarda değişiklik yapılmadı.
6. İlk gösteriler için kurum izniyle gerçek etkinlik içerikleri ekleyin. Çocukların tanınabildiği fotoğraflar yalnızca uygun yayın izniyle kullanılsın.
7. Search Console’da gösterim alan gerçek sorguları inceleyin; “gösteri”, “okul”, “belediye”, “23 Nisan” ve şehir gruplarını ayrı değerlendirin. Başlık ve içerikleri gelen veriye göre iyileştirin.
8. İletişim tıklamalarını ölçmek istenirse analiz hesabı ayrıca bağlanmalı. Paket, hesap bilgisi olmadan sahte Analytics kimliği veya izleme kodu içermez.

SEO altyapısı ve hedefli içerik hazırdır. Arama görünürlüğü yayın, tarama, gerçek referanslar ve zaman içinde toplanan verilerle gelişir; belirli sıra veya trafik miktarı vaat edilmez.

## Kaynaklar

- [Google SEO başlangıç kılavuzu](https://developers.google.com/search/docs/fundamentals/seo-starter-guide)
- [Google yararlı ve güvenilir içerik rehberi](https://developers.google.com/search/docs/fundamentals/creating-helpful-content)
- [Sitemap oluşturma](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [Google’ın desteklediği meta etiketleri](https://developers.google.com/search/docs/crawling-indexing/special-tags)
- [FAQ yapılandırılmış veri](https://developers.google.com/search/docs/appearance/structured-data/faqpage)
- [YouTube oynatıcı parametreleri](https://developers.google.com/youtube/player_parameters)
- [YouTube oynatıcı ve hata tanımları](https://developers.google.com/youtube/iframe_api_reference)
- [GitHub Pages özel yayın akışları](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [Kukla Mukla TV YouTube Shorts](https://www.youtube.com/@KuklamuklaTV/shorts)
- [Instagram](https://www.instagram.com/kuklamuklatv/) · [Facebook](https://www.facebook.com/kuklamuklatv/)
