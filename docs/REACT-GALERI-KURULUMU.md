# React galeri bileşeni

Ana sayfadaki galeri iki hizalı sıradan oluşur. Üst sıra sola, alt sıra sağa otomatik akar. Fotoğraflar çoğaltılmaz; mevcut kartların sırası döngü sonunda değiştirilir. 25 gerçek fotoğraf ana sayfada birer kez bulunur: dört fotoğraf üst bölümlerde, 21 fotoğraf iki galeri sırasında.

## Dosya düzeni

| Amaç | Yol |
| --- | --- |
| React / TypeScript bileşeni | `components/ui/image-auto-slider.tsx` |
| Demo | `components/ui/demo.tsx` |
| Bileşen stilleri | `components/ui/image-auto-slider.css` |
| Tailwind giriş dosyası | `styles/globals.css` |
| Mevcut site stilleri | `assets/css/style.css` ve diğer tema dosyaları |
| Derlenmiş galeri stilleri | `assets/css/image-auto-slider.css` |
| React başlangıcı | `frontend/image-auto-slider.tsx` |
| Hazır tarayıcı kodu | `assets/js/image-auto-slider.js` |
| shadcn yapılandırması | `components.json` |
| TypeScript / import adresleri | `tsconfig.json` |

`components/ui` yeniden kullanılabilir arayüz bileşenlerini tek yerde toplar. `components.json` içindeki `aliases.ui` aynı klasörü gösterir; `@/components/ui/...` importları ve CLI ile eklenen bileşenlerin adresleri tutarlı kalır. `@/*` projenin köküne bağlanır.

Mevcut proje statik HTML sayfaları üzerinde çalışır. React yalnızca galeri alanına bağlanır. İlk galeri HTML’i de hazır olarak üretilir; bu sayede fotoğraflar başlangıçta görünür ve JavaScript kapalıyken yatay kaydırmayla ulaşılabilir. ZIP’te derlenmiş dosyalar bulunduğu için siteyi açmak için Node kurulumu gerekmez.

## Geliştirme kurulumu

Node.js 22 veya uyumlu daha yeni bir sürüm ve Python 3 ile proje klasöründe:

```bash
npm ci
npm run build
```

Bu komut galeri JavaScript ve CSS’ini derler, TypeScript kontrolünü çalıştırır, HTML sayfalarını üretir, bağlantıları denetler ve `_site/` yayın klasörünü hazırlar. GitHub iş akışı aynı galeri derlemesini otomatik yapar.

Yalnızca bileşeni değiştirdikten sonra:

```bash
npm run build:slider
npm run typecheck
python3 scripts/build.py
python3 scripts/check.py
```

Bağımlılıkları kilit dosyası bulunmayan başka bir projede elle eklemek için:

```bash
npm install react react-dom lucide-react clsx tailwind-merge class-variance-authority
npm install -D typescript @types/react @types/react-dom @types/node esbuild tailwindcss @tailwindcss/cli
```

Yeni bir shadcn / Vite projesi başlatmak için boş bir çalışma klasöründe:

```bash
npx shadcn@latest init --template vite --name kuklamukla-react
```

Teslim edilen projede TypeScript, Tailwind, import adresleri ve `components.json` hazırdır. Tailwind sınıfları `sg:` öneki kullanır. Tema dosyalarını korumak için genel Preflight sıfırlaması eklenmemiştir.

## Props ve davranış

`images`, `id`, `src`, `srcSet`, `full`, `width`, `height`, `title`, `alt`, `category` ve `order` alanları bulunan fotoğraf listesidir. `pixelsPerSecond` hızı belirler; varsayılan değer 24’tür. `className` ek kapsayıcı sınıflarını kabul eder. Demo dosyası gerçek yerel galeri verisini kullanır.

Bileşen yerel React state ve ref’lerini kullanır; ek context provider veya genel state yöneticisi gerekmez. Lucide fotoğraf büyütme ikonunu sağlar. Görseller `content/photos.json`, öncelikli yerleşimler `content/site.json` içinden üretilir.

İmleç, klavye odağı veya fotoğraf penceresi açıkken akış durur. Görünüm dışındayken ve sekme gizliyken de bekler. Cihazın azaltılmış hareket tercihi etkinse otomatik hareket durur ve fotoğraflar yatay kaydırmayla erişilebilir kalır. Gerçek fotoğraflara yakınlaştırma veya şekil değiştirme efekti uygulanmaz.

## Resmî kaynaklar

- https://ui.shadcn.com/docs/installation/manual
- https://ui.shadcn.com/docs/components-json
- https://ui.shadcn.com/docs/cli
- https://tailwindcss.com/docs/preflight
- https://react.dev/reference/react-dom/client/hydrateRoot
