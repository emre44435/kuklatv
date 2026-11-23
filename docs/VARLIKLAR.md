# Tasarım varlıkları

## Çizgi film sahnesi

Yeni temanın bulut, güneş, balon, flama, yıldız, tepe ve küçük dekoratif kukla çizimleri projeye özel SVG olarak yazıldı. Bunlar `content/cartoon-scene.html` içinde yer alır. Perde üstlüğü `content/stage-valance.svg`, küçük arka plan deseni `assets/img/cartoon-sprinkles.svg` dosyasındadır. Harici bir çizim veya animasyon servisine istek göndermez.

Çizimler dekoratiftir; ekran okuyucu ve tıklama akışına katılmaz. Hareket CSS dönüşümleriyle sağlanır; ziyaretçi kapatabilir. Ekran dışında kalan sahne ve gizli sekmedeki hareketler duraklar. Cihazın azaltılmış hareket tercihi animasyonları kaldırır. Çizimlerin renk ve hareketleri `assets/css/cartoon.css` dosyasında düzenlenebilir.

## Yazı tipleri

Başlıklardaki Fredoka, kullanıcının paylaştığı afişin dolgun ve eğlenceli harflerine yakın bir seçimdir. Gövde metinlerinde okunabilirliği korumak için Nunito Sans kullanılır. Dosyalar yereldir, Türkçe karakterleri içerir ve `font-display: swap` ile yüklenir. Lisans metinleri bu klasördedir.

## İkonlar

Arayüz ikonları Lucide, sosyal medya işaretleri Simple Icons kaynaklıdır. Uygulama ikonları rastgele emoji veya uydurma sosyal medya simgesi değildir. Siteye küçük inline SVG’ler olarak eklenir; bir ikon kütüphanesi betiği indirilmez.

Favicon projeye özel, basit bir sahne ve gülen kukla çizimidir. `assets/icons/favicon.svg` düzenlenebilir vektör kaynaktır.

## Video kapakları

Kapak dosyaları, kullanıcının belirttiği kanalın gerçek dört Shorts videosunun `frame0.jpg` görsellerinin yerel WebP sürümleridir. Görüntüler başka bir videoya bağlanmaz. Site başlıkları, okunabilir koyu katman, marka etiketi ve oynat düğmesi CSS ile eklenir; video dosyası kopyalanmaz veya kendi sunucusunda barındırılmaz.

| Kimlik | Kanalda doğrulanan başlık |
| --- | --- |
| B8wlJ1Jrzro | Paylaşmak |
| g4sx3WoJEy4 | Ben Zoyo 2. Bölüm: Parktaki Çocuklar |
| g3krZ8XySIY | Ben Zoyo 1. Bölüm: Büyük Z Gezegeni |
| YAKxwfMalA4 | Yalan |

## Üretilen tanıtım görselleri

Üç görsel yerleşik görsel üretimiyle oluşturuldu, ardından site performansı için farklı boyutlarda WebP olarak dışa aktarıldı. Bunlar gerçek bir etkinliğin fotoğrafı veya gerçek Zoyo’nun görünüşüne ilişkin belge değildir. Kullanıcı daha sonra gerçek fotoğrafları sağlayacaktır. Görsellerde uydurma bir Ali Cengiz portresi yoktur.

Son istem seti:

1. **Kukla portresi:** Dikey 4:5; bal sarısı keçe kumaşlı, neşeli, turuncu burunlu özgün bir kukla; turkuaz kadife yelek ve küçük mercan papyon; el sallama; turkuaz tiyatro perdesi ve sıcak sahne ışığı. Dokulu profesyonel kukla fotoğrafçılığı; insan, yazı, logo ve filigran yok. Mevcut gerçek bir karakterin temsili olarak kullanılmayan geçici tanıtım karakteri.
2. **Okul sahnesi:** Yatay 3:2; okulun çok amaçlı salonunda mercan perdeli, turkuaz fonlu, sıcak ampullü küçük kukla sahnesi; ahşap zemin, ölçülü renkli flamalar ve önde boş sandalyeler. Dokulu, özenle hazırlanmış sahne illüstrasyonu; insan, çocuk, yazı ve logo yok.
3. **Açık hava sahnesi:** Yatay 3:2; yapraklı bir parkta altın saat ışığında turkuaz perdeli, mercan cepheli küçük kukla sahnesi; sıcak ampuller, ölçülü flamalar ve doğal ağaç dokusu. İnsan, yazı, logo ve filigran yok. Gerçek etkinlik belgesi yerine tanıtım illüstrasyonu.

Projedeki son dosyalar `assets/img/puppet-hero-1120.webp`, `assets/img/puppet-hero-640.webp`, `assets/img/stage.webp`, `assets/img/festival.webp` ve okul sahnesinden hazırlanan `assets/img/social-cover.webp` dosyalarıdır.
