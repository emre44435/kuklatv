# kuklagosterisi.com yayın rehberi

Alan adı `kuklagosterisi.com` olarak hazırlanmıştır. ASCII Latin harflerinden oluşur; Türkçe karakter veya Punycode dönüşümü içermez. Site adresi `https://kuklagosterisi.com/` olarak kullanılır.

## GitHub Pages

1. `Kuklamukla_TV` klasörünün içeriğini mevcut deponun köküne aktarın; `.github/workflows/pages.yml` dosyası da yerinde olmalıdır.
2. **Settings → Pages** bölümünde yayın kaynağını **GitHub Actions** seçin. **Custom domain** alanına `kuklagosterisi.com` yazıp kaydedin.
3. Alan adınızın DNS yönetiminde kök alanın `A` kayıtlarını aşağıdaki adreslere yönlendirin:

| Tür | Ad | Değer |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |

`www` için `CNAME` hedefi, yayın yaptığınız GitHub hesabının `kullanıcıadı.github.io` adresidir; depo adı eklenmez. Kullanıcı adı bu pakette varsayılmamıştır. DNS doğrulaması ve sertifika hazır olduğunda Pages ayarlarında **Enforce HTTPS** seçeneğini açın.

Actions ile yayında domaini Pages ayarlarına girmek gerekir; arşivdeki `CNAME` dosyası tek başına bu ayarı yapmaz. İş akışı SEO adresini `content/site.json` dosyasından alır ve sadece herkese açık yayın dosyalarını yükler.

## cPanel veya statik hosting

Alan adını hosting hesabındaki doğru belge köküne bağlayın. Yalnızca aşağıdaki hazır yayın dosyalarını bu köke yüklemek yeterlidir:

- Kök dizindeki HTML dosyaları
- `assets/` klasörü
- `robots.txt`, `sitemap.xml`, `site.webmanifest` ve `.nojekyll`

Kaynak klasörlerini, belgeleri, `node_modules` klasörünü ve geliştirme dosyalarını web köküne yüklemek gerekmez. Hosting panelinde SSL sertifikasını etkinleştirip HTTP ve `www` adreslerini `https://kuklagosterisi.com/` adresine yönlendirin. DNS hedefi hosting sağlayıcınızın verdiği sunucu adresidir; yukarıdaki GitHub IP’leri cPanel için kullanılmaz.

Yayın dosyalarını ayrı klasörde hazırlamak isterseniz:

```bash
python3 scripts/export.py
```

Sonuç `_site/` klasörüdür. Hazır paketi yayınlamak için Node kurmak gerekmez. React veya içerik kaynaklarını yeniden derlemek için `npm ci` ve `npm run build` kullanılır.

## SEO ve son kontrol

Canonical, Open Graph, Twitter ve yapılandırılmış veri adresleri aynı HTTPS alanını kullanır. Site haritası 14 dizine eklenebilir sayfayı içerir; 404 sayfasında `noindex` bulunur. Metin HTML içinde hazırdır. Görseller responsive WebP biçimindedir; yazı tipleri yereldir ve ekran altındaki fotoğraflar gecikmeli yüklenir.

Yayından sonra ana sayfanın ve iç sayfaların HTTPS ile açıldığını kontrol edin. Google Search Console’da alan adını doğrulayın ve `https://kuklagosterisi.com/sitemap.xml` adresini gönderin. URL Denetleme aracından ana sayfanın canlı testini çalıştırın. Kaynak kontrolleri `npm run check` komutuyla tekrarlanabilir.

## Resmî kaynaklar

- https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
- https://developers.google.com/search/docs/fundamentals/seo-starter-guide?hl=tr
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=tr
