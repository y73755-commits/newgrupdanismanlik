# New Grup Danışmanlık — web sitesi

İstanbul temizlik ve kurumsal hizmetler sitesi. Statik HTML; GitHub Pages ile yayınlanır.

## Bilgileri güncelleme
Tüm içerik **`data/site.json`** dosyasındadır. GitHub'da dosyayı açın → kalem simgesi → düzenleyin → *Commit changes*.
Birkaç dakika içinde site otomatik yeniden oluşturulur (Actions → "Siteyi oluştur").

| Ne değişecek | site.json alanı |
|---|---|
| Ev temizliği fiyatları | `ev_fiyatlari` |
| Ofis fiyat aralığı | `ofis_fiyati` |
| Hizmet bölgeleri | `bolgeler` |
| Telefon / WhatsApp / yetkili | `iletisim` |
| Kurumsal hizmetler (yayına alma) | `kurumsal_hizmetler[].yayinda` |
| SSS | `sss` |
| Resmî şirket bilgileri (KVKK metni) | `sirket_bilgileri` |
| Google Analytics / Ads kimlikleri | `olcum` |
| Alan adı | `site.site_url` (+ `CNAME` dosyası) |

## Ölçüm (Google Ads)
`olcum` alanına kimlikler girilince: çerez bandı otomatik görünür, etiketler yalnızca izinle yüklenir (Consent Mode v2, varsayılan "denied").
- `google_ads_id`: `AW-XXXXXXXXX`
- `ads_donusum_whatsapp`, `ads_donusum_telefon`: Google Ads'te oluşturulan iki ayrı "İletişim" dönüşümünün etiketleri
- `ga4_id`: `G-XXXXXXX` (olaylar: `whatsapp_tiklamasi`, `telefon_tiklamasi`)
- Ayrıca her tıklamada `dataLayer`'a `iletisim_tiklamasi` olayı gönderilir.

## Alan adı alındığında
1. `data/site.json` → `site_url` değerini `https://alanadi.com` yapın.
2. Depoya `CNAME` adlı dosya ekleyin, içine yalnızca `alanadi.com` yazın.
3. DNS: `A` kayıtları 185.199.108.153 / .109.153 / .110.153 / .111.153, `www` için `CNAME` → `y73755-commits.github.io`.
4. Search Console'a alan adını yeni mülk olarak ekleyip `sitemap.xml` gönderin.

## Yerelde çalıştırma
`python3 build.py` (yalnızca Python 3 gerekir).
