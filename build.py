#!/usr/bin/env python3
"""New Grup Danışmanlık — statik site üretici.

İçerik data/site.json dosyasındadır. Çalıştırma:  python3 build.py
GitHub'da data/site.json değiştiğinde bu betik otomatik çalışır (.github/workflows/build.yml).
Yalnızca Python standart kütüphanesi kullanılır.
"""
import json, os, datetime, urllib.parse
from html import escape as e

ROOT = os.path.dirname(os.path.abspath(__file__))
D = json.load(open(os.path.join(ROOT, "data", "site.json"), encoding="utf-8"))
S, C, O = D["site"], D["iletisim"], D["olcum"]
BASE = S["site_url"].rstrip("/")
TODAY = datetime.date.today().isoformat()
VER = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M")

def wa(msg):
    return C["whatsapp_link"] + "?text=" + urllib.parse.quote(msg)

MSG_RANDEVU = "Merhaba Burak Bey, ev temizliği için randevu almak istiyorum. Daire tipi: … Semt: … Uygun gün: …"
MSG_TEKLIF = "Merhaba Burak Bey, {} için teklif almak istiyorum. Semt: … Alan/kapsam: …"
MSG_GENEL = "Merhaba Burak Bey, temizlik hizmeti hakkında bilgi almak istiyorum."

ICON = {
 "wa": '<svg viewBox="0 0 32 32" aria-hidden="true"><path fill="currentColor" d="M16.04 3C9.08 3 3.43 8.64 3.43 15.6c0 2.22.58 4.39 1.69 6.3L3.33 28.7l6.96-1.83a12.6 12.6 0 0 0 5.75 1.39h.01c6.95 0 12.6-5.65 12.6-12.6 0-3.37-1.31-6.53-3.69-8.91A12.52 12.52 0 0 0 16.04 3Zm0 23.07h-.01a10.5 10.5 0 0 1-5.35-1.46l-.38-.23-4.13 1.08 1.1-4.02-.25-.41a10.44 10.44 0 0 1-1.6-5.43c0-5.79 4.71-10.5 10.51-10.5 2.8 0 5.44 1.1 7.42 3.08a10.43 10.43 0 0 1 3.07 7.43c0 5.79-4.71 10.5-10.5 10.5Zm5.76-7.86c-.32-.16-1.87-.92-2.16-1.03-.29-.1-.5-.16-.71.16-.21.32-.82 1.03-1 1.24-.18.21-.37.24-.68.08-.32-.16-1.33-.49-2.54-1.57-.94-.84-1.57-1.87-1.75-2.18-.18-.32-.02-.49.14-.65.14-.14.32-.37.47-.55.16-.18.21-.32.32-.53.1-.21.05-.4-.03-.55-.08-.16-.71-1.71-.97-2.34-.26-.62-.52-.53-.71-.54h-.6c-.21 0-.55.08-.84.4-.29.32-1.1 1.08-1.1 2.63s1.13 3.05 1.29 3.26c.16.21 2.22 3.39 5.38 4.75.75.32 1.34.52 1.8.66.75.24 1.44.21 1.98.13.6-.09 1.87-.76 2.13-1.5.26-.74.26-1.37.18-1.5-.08-.13-.29-.21-.6-.37Z"/></svg>',
 "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.2.2 2.4.6 3.6.1.3 0 .7-.2 1l-2.3 2.2Z"/></svg>',
 "check": '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="M8.1 14.3 3.8 10l1.4-1.4 2.9 2.9 6.7-6.7 1.4 1.4z"/></svg>',
 "x": '<svg viewBox="0 0 20 20" aria-hidden="true"><path fill="currentColor" d="m5.4 4 4.6 4.6L14.6 4 16 5.4 11.4 10l4.6 4.6-1.4 1.4-4.6-4.6L5.4 16 4 14.6 8.6 10 4 5.4z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a7 7 0 0 0-7 7c0 5.2 7 13 7 13s7-7.8 7-13a7 7 0 0 0-7-7Zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5Z"/></svg>',
}

SVC_ICON = {
 "ev-temizligi": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 22 24 9l16 13v17a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2V22Z" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/><path d="M19 41V29h10v12" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="M35 5l1.2 2.8L39 9l-2.8 1.2L35 13l-1.2-2.8L31 9l2.8-1.2z" fill="currentColor"/></svg>',
 "ofis-temizligi": '<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="7" y="13" width="34" height="22" rx="2" fill="none" stroke="currentColor" stroke-width="2.5"/><path d="M17 41h14M24 35v6" stroke="currentColor" stroke-width="2.5"/><path d="M14 20h12M14 26h8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
 "villa-temizligi": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M4 24 18 13l14 11M10 20v19h28V22l-6-5" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/><path d="M32 17l12 9" stroke="currentColor" stroke-width="2.5"/><rect x="15" y="27" width="7" height="12" fill="none" stroke="currentColor" stroke-width="2.5"/><rect x="27" y="27" width="7" height="6" fill="none" stroke="currentColor" stroke-width="2.5"/></svg>',
 "plaza-temizligi": '<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M12 42V6h16v36M28 16h10v26M6 42h36" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linejoin="round"/><path d="M17 12h6M17 18h6M17 24h6M17 30h6M33 22h1M33 28h1M33 34h1" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
}

def pic(name, alt, cls="", eager=False, sizes="(max-width: 760px) 100vw, 50vw"):
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="assets/img/{name}-800.webp" '
            f'srcset="assets/img/{name}-800.webp 800w, assets/img/{name}-1600.webp 1600w" sizes="{sizes}" '
            f'alt="{e(alt)}" width="1536" height="1024" {load}>')

NAV = [
 ("index.html", "Ana Sayfa"),
 ("temizlik-hizmetleri.html", "Temizlik Hizmetleri"),
 ("fiyatlar.html", "Fiyatlar"),
 ("hizmet-bolgeleri.html", "Hizmet Bölgeleri"),
 ("kurumsal-hizmetler.html", "Kurumsal Hizmetler"),
 ("sss.html", "SSS"),
 ("iletisim.html", "İletişim"),
]

def btn_wa(label, msg, ctx, cls="btn btn-wa"):
    return (f'<a class="{cls}" href="{e(wa(msg))}" target="_blank" rel="noopener" '
            f'data-track="whatsapp" data-ctx="{e(ctx)}">{ICON["wa"]}<span>{e(label)}</span></a>')

def btn_tel(label, ctx, cls="btn btn-ghost"):
    return (f'<a class="{cls}" href="tel:{C["telefon_link"]}" data-track="telefon" '
            f'data-ctx="{e(ctx)}">{ICON["tel"]}<span>{e(label)}</span></a>')

def randevu(ctx, cls="btn btn-wa"):
    return btn_wa("WhatsApp’tan Randevu Al", MSG_RANDEVU, ctx, cls)

def teklif(ctx, konu="ofis temizliği", cls="btn btn-primary"):
    return btn_wa("Teklif Al", MSG_TEKLIF.format(konu), ctx, cls)

LOGO = ('<svg class="logo-mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#0d4f4f"/>'
        '<path d="M11 28V12l11 16V12" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M30 9.5l1.1 2.6 2.6 1.1-2.6 1.1L30 16.9l-1.1-2.6-2.6-1.1 2.6-1.1z" fill="#8fe3c6"/></svg>')

def head_tags():
    cfg = {
        "ga4": O.get("ga4_id", ""), "ads": O.get("google_ads_id", ""),
        "adsWa": O.get("ads_donusum_whatsapp", ""), "adsTel": O.get("ads_donusum_telefon", ""),
    }
    return f"""<script>
window.NG_CFG={json.dumps(cfg)};
window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}
gtag('consent','default',{{ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',analytics_storage:'denied',functionality_storage:'granted',security_storage:'granted',wait_for_update:500}});
gtag('set','ads_data_redaction',true);
</script>"""

def page(fn, title, desc, body, active=None, schema=None, robots="index,follow", base=False):
    url = BASE + "/" + ("" if fn == "index.html" else fn)
    nav = "".join(
        f'<li><a href="{h}"{" aria-current=page" if h == active else ""}>{e(t)}</a></li>' for h, t in NAV)
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in (schema or []))
    verif = f'<meta name="google-site-verification" content="{e(S["google_site_verification"])}">' if S.get("google_site_verification") else ""
    html = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
{f'<base href="{urllib.parse.urlparse(BASE).path.rstrip("/")}/">' if base else ""}
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{e(url)}">
<meta property="og:type" content="website"><meta property="og:locale" content="tr_TR">
<meta property="og:site_name" content="{e(S['ad'])}"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{e(url)}">
<meta property="og:image" content="{BASE}/assets/img/og.jpg">
<meta name="theme-color" content="#0d4f4f">
{verif}
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/plus-jakarta-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
{'<link rel="preload" as="image" href="assets/img/hero-salon-800.webp" imagesrcset="assets/img/hero-salon-800.webp 800w, assets/img/hero-salon-1600.webp 1600w" imagesizes="100vw">' if fn=="index.html" else ""}
<link rel="stylesheet" href="assets/css/style.css?v={VER}">
{head_tags()}
{ld}
</head>
<body>
<a class="skip" href="#icerik">İçeriğe geç</a>
<header class="hdr">
  <div class="wrap hdr-in">
    <a class="brand" href="index.html" aria-label="{e(S['ad'])} ana sayfa">{LOGO}<span><b>New Grup</b> Danışmanlık</span></a>
    <nav class="nav" id="nav" aria-label="Ana menü"><ul>{nav}</ul>
      <div class="nav-cta">{btn_tel(C['telefon_gosterim'], 'menu', 'btn btn-ghost btn-sm')}</div>
    </nav>
    <a class="hdr-tel" href="tel:{C['telefon_link']}" data-track="telefon" data-ctx="header">{ICON['tel']}<span>{e(C['telefon_gosterim'])}</span></a>
    <button class="burger" id="burger" aria-controls="nav" aria-expanded="false" aria-label="Menüyü aç"><span></span><span></span><span></span></button>
  </div>
</header>
<main id="icerik">
{body}
</main>
<footer class="ftr">
  <div class="wrap ftr-grid">
    <div>
      <a class="brand brand-light" href="index.html">{LOGO}<span><b>New Grup</b> Danışmanlık</span></a>
      <p class="muted-l">{e(S['slogan'])}. {e(C['calisma_sekli'])}.</p>
    </div>
    <div>
      <h2 class="ftr-h">Sayfalar</h2>
      <ul class="ftr-list">{"".join(f'<li><a href="{h}">{e(t)}</a></li>' for h, t in NAV)}</ul>
    </div>
    <div>
      <h2 class="ftr-h">İletişim</h2>
      <ul class="ftr-list">
        <li>Yetkili: {e(C['yetkili'])}</li>
        <li><a href="tel:{C['telefon_link']}" data-track="telefon" data-ctx="footer">{e(C['telefon_gosterim'])}</a></li>
        <li><a href="{e(wa(MSG_GENEL))}" target="_blank" rel="noopener" data-track="whatsapp" data-ctx="footer">WhatsApp</a></li>
      </ul>
    </div>
    <div>
      <h2 class="ftr-h">Yasal</h2>
      <ul class="ftr-list">
        <li><a href="odeme-kosullari.html">Ödeme ve İptal Koşulları</a></li>
        <li><a href="kvkk-aydinlatma-metni.html">KVKK Aydınlatma Metni</a></li>
        <li><a href="cerez-politikasi.html">Çerez Politikası</a></li>
        <li><button type="button" class="linklike" data-open-consent>Çerez Tercihleri</button></li>
      </ul>
    </div>
  </div>
  <div class="wrap ftr-bottom"><span>© {datetime.date.today().year} {e(S['ad'])}</span><span>{e(D['kapsam_disi'])}</span></div>
</footer>
<a class="wa-float" href="{e(wa(MSG_GENEL))}" target="_blank" rel="noopener" data-track="whatsapp" data-ctx="sabit-ikon" aria-label="WhatsApp ile yazın">{ICON['wa']}</a>
{consent_ui()}
<script src="assets/js/main.js?v={VER}" defer></script>
</body>
</html>
"""
    with open(os.path.join(ROOT, fn), "w", encoding="utf-8") as f:
        f.write(html)
    return url

def consent_ui():
    return """<div class="cc-banner" id="cc-banner" role="region" aria-label="Çerez bildirimi" hidden>
  <div class="cc-in">
    <p><b>Çerez tercihiniz</b><br>Siteyi ölçmek ve reklamlarımızın etkisini görmek için analiz ve reklam çerezlerini yalnızca izninizle kullanırız. Ayrıntılar: <a href="cerez-politikasi.html">Çerez Politikası</a>.</p>
    <div class="cc-actions">
      <button type="button" class="btn btn-sm btn-outline" data-cc="reject">Reddet</button>
      <button type="button" class="btn btn-sm btn-outline" data-open-consent>Tercihler</button>
      <button type="button" class="btn btn-sm btn-outline" data-cc="accept">Kabul Et</button>
    </div>
  </div>
</div>
<dialog class="cc-modal" id="cc-modal" aria-labelledby="cc-title">
  <form method="dialog" class="cc-form">
    <h2 id="cc-title">Çerez Tercihleri</h2>
    <p class="small">Tercihinizi istediğiniz zaman sayfanın altındaki “Çerez Tercihleri” bağlantısından değiştirebilirsiniz.</p>
    <div class="cc-row"><div><b>Zorunlu</b><p class="small">Çerez tercihinizi hatırlamak için tarayıcınızda küçük bir kayıt tutulur. Kapatılamaz.</p></div><span class="pill">Her zaman açık</span></div>
    <label class="cc-row"><div><b>Analiz</b><p class="small">Google Analytics ile ziyaret istatistikleri.</p></div><input type="checkbox" class="sw" id="cc-analytics"></label>
    <label class="cc-row"><div><b>Reklam</b><p class="small">Google Ads ile WhatsApp ve telefon tıklamalarının ölçümü.</p></div><input type="checkbox" class="sw" id="cc-ads"></label>
    <div class="cc-actions">
      <button type="button" class="btn btn-sm btn-outline" data-cc="reject">Tümünü Reddet</button>
      <button type="button" class="btn btn-sm btn-outline" data-cc="save">Seçimi Kaydet</button>
      <button type="button" class="btn btn-sm btn-outline" data-cc="accept">Tümünü Kabul Et</button>
    </div>
  </form>
</dialog>"""

# ---------- ortak parçalar ----------
def price_table(cta=True):
    rows = "".join(
        f'<tr><th scope="row">{e(p["hizmet"])}</th><td class="num">{e(p["fiyat"])}</td></tr>' for p in D["ev_fiyatlari"])
    o = D["ofis_fiyati"]
    rows += f'<tr class="row-alt"><th scope="row">{e(o["hizmet"])}<span class="cell-note">{e(o["not"])}</span></th><td class="num">{e(o["fiyat"])}</td></tr>'
    return f'<div class="table-wrap"><table class="ptable"><caption class="sr">Temizlik fiyat listesi</caption><thead><tr><th scope="col">Hizmet</th><th scope="col" class="num">Fiyat</th></tr></thead><tbody>{rows}</tbody></table></div>'

def kapsam_box():
    return f'<div class="note note-warn">{ICON["x"]}<p><b>Kapsam dışı:</b> {e(D["kapsam_disi"])}</p></div>'

DAHIL = [("banyo","Banyo","Banyo tezgâhını silen temizlik görevlisi"),
         ("teras","Teras","Terası paspaslayan temizlik görevlisi"),
         ("cam","İçeriden erişilebilen camlar","Pencere camını içeriden silen temizlik görevlisi")]

def dahil_gallery():
    items = "".join(f'<figure class="dahil">{pic(n, alt, sizes="(max-width: 760px) 100vw, 33vw")}<figcaption>{ICON["check"]}{e(t)}</figcaption></figure>' for n, t, alt in DAHIL)
    return f'<div class="dahil-grid">{items}</div>'

def includes_list():
    items = ["Banyo", "Teras", "İçeriden güvenle erişilebilen camlar"]
    return '<ul class="ticks">' + "".join(f'<li>{ICON["check"]}{e(i)}</li>' for i in items) + "</ul>"

def odeme_list():
    return '<ul class="ticks">' + "".join(f'<li>{ICON["check"]}{e(i)}</li>' for i in D["odeme_kosullari"]) + "</ul>"

def memnuniyet_block():
    return f"""<section class="sec"><div class="wrap"><div class="promise">
<div><p class="eyebrow">Memnuniyet</p><h2>Bir sorun olursa doğrudan Burak Bey’e ulaşın</h2><p class="lead">{e(D['memnuniyet'])}</p></div>
<div class="promise-cta">{btn_wa('Burak Bey’e Yaz', 'Merhaba Burak Bey, aldığım temizlik hizmetiyle ilgili bildirimde bulunmak istiyorum.', 'memnuniyet', 'btn btn-wa')}{btn_tel('Ara', 'memnuniyet')}</div>
</div></div></section>"""

def cta_band(title="Fiyat belli, randevu bir mesaj uzağınızda", text="Daire tipinizi, semtinizi ve uygun gününüzü WhatsApp’tan yazın; Burak Bey size dönüş yapsın."):
    return f"""<section class="band"><div class="wrap band-in"><div><h2>{e(title)}</h2><p>{e(text)}</p></div>
<div class="band-cta">{randevu('cta-band')}{teklif('cta-band', 'ofis / kurumsal hizmet', 'btn btn-light')}</div></div></section>"""

def page_hero(eyebrow, h1, lead, ctas=""):
    return f"""<section class="phero"><div class="wrap"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(h1)}</h1><p class="lead">{e(lead)}</p>{f'<div class="hero-cta">{ctas}</div>' if ctas else ''}</div></section>"""

def bc(name, fn):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Ana Sayfa", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{BASE}/{fn}"}]}

REGION_NAMES = [r["ad"] for r in D["bolgeler"]]
BUSINESS = {
    "@context": "https://schema.org", "@type": "LocalBusiness", "@id": BASE + "/#isletme",
    "name": S["ad"], "url": BASE + "/", "telephone": C["telefon_link"],
    "description": S["slogan"], "image": BASE + "/assets/img/og.jpg", "priceRange": "2.500 TL – 6.500 TL",
    "areaServed": [{"@type": "Place", "name": f"{r}, İstanbul"} for r in REGION_NAMES],
    "contactPoint": {"@type": "ContactPoint", "telephone": C["telefon_link"], "contactType": "customer service", "availableLanguage": "Turkish"},
    "makesOffer": [{"@type": "Offer", "name": p["hizmet"], "price": p["fiyat"].replace(".", "").replace(" TL", ""), "priceCurrency": "TRY"} for p in D["ev_fiyatlari"]],
}
if D["sirket_bilgileri"].get("adres"):
    BUSINESS["address"] = D["sirket_bilgileri"]["adres"]

pages = []

# ---------- ANA SAYFA ----------
svc_cards = "".join(f"""<article class="card svc">
<div class="svc-img">{pic(s['gorsel'], s['gorsel_alt'], sizes="(max-width: 760px) 100vw, 25vw")}</div><h3>{e(s['baslik'])}</h3><p>{e(s['ozet'])}</p>
<p class="svc-price">{e(s['fiyat_metni'])}</p>
<a class="more" href="temizlik-hizmetleri.html#{s['id']}">Kapsamı gör →</a></article>""" for s in D["temizlik_hizmetleri"])

mini_prices = "".join(f'<li><span>{e(p["kisa"])}</span><b>{e(p["fiyat"])}</b></li>' for p in D["ev_fiyatlari"])
region_chips = "".join(f'<li>{e(r)}</li>' for r in REGION_NAMES)
kurumsal_pub = [k for k in D["kurumsal_hizmetler"] if k["yayinda"]]

home = f"""
<section class="hero"><div class="hero-bg">{pic('hero-salon', 'İstanbul manzaralı bir salonda süpürge ve toz alma yapan iki temizlik görevlisi', 'hero-img', True, '100vw')}</div><div class="wrap hero-grid">
  <div class="hero-txt">
    <p class="eyebrow">{e(S['sehir'])} · Randevulu temizlik</p>
    <h1>Ev temizliğinde fiyat baştan belli. <span class="hl">Randevunuz WhatsApp’ta.</span></h1>
    <p class="lead">Ev, ofis, villa ve plaza iç mekân temizliği. Ev temizliğinde banyo, teras ve içeriden güvenle erişilebilen camlar fiyata dahildir.</p>
    <div class="hero-cta">{randevu('hero')}{teklif('hero', 'ofis temizliği')}</div>
    <p class="hero-meta">{ICON['tel']}<a href="tel:{C['telefon_link']}" data-track="telefon" data-ctx="hero">{e(C['telefon_gosterim'])}</a> · Yetkili: {e(C['yetkili'])}</p>
  </div>
  <aside class="price-card" aria-label="Ev temizliği fiyatları">
    <div class="pc-head"><span>Ev temizliği</span><span class="pill pill-mint">Sabit fiyat</span></div>
    <ul class="pc-list">{mini_prices}</ul>
    <div class="pc-foot"><span>Ofis: <b>{e(D['ofis_fiyati']['fiyat'])}</b></span><a href="fiyatlar.html">Tüm fiyatlar →</a></div>
  </aside>
</div></section>

<section class="sec"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Hizmetler</p><h2>Temizlik hizmetlerimiz</h2></div>
  <div class="grid-4">{svc_cards}</div>
  <h3 class="dahil-h">Ev temizliği fiyatına dahil</h3>
  {dahil_gallery()}
  {kapsam_box()}
</div></section>

<section class="sec sec-tint"><div class="wrap">
  <div class="sec-head"><p class="eyebrow">Nasıl çalışır</p><h2>Üç adımda randevu</h2></div>
  <ol class="steps">
    <li><span class="step-n">1</span><h3>WhatsApp’tan yazın</h3><p>Daire tipinizi, semtinizi ve uygun gününüzü iletin.</p></li>
    <li><span class="step-n">2</span><h3>Randevu ve ödeme</h3><p>Tarih netleşir, koşullar size yazılı iletilir ve ödeme peşin alınır.</p></li>
    <li><span class="step-n">3</span><h3>Temizlik günü</h3><p>Ekibimiz randevu saatinde gelir. Bir sorun olursa Burak Bey’e ulaşırsınız.</p></li>
  </ol>
</div></section>

<section class="sec"><div class="wrap split">
  <div><p class="eyebrow">Hizmet bölgeleri</p><h2>İstanbul’da {len(REGION_NAMES)} bölgede hizmet</h2>
  <p>Avrupa ve Anadolu yakasında aşağıdaki bölgelerde randevu veriyoruz.</p>
  <a class="more" href="hizmet-bolgeleri.html">Bölgeleri incele →</a></div>
  <ul class="chips">{region_chips}</ul>
</div></section>

<section class="sec sec-dark"><div class="wrap split">
  <div class="dark-photo">{pic('bahcivan', 'Villa bahçesinde çiçek diken bahçıvan', sizes="(max-width: 860px) 100vw, 50vw")}</div>
  <div><p class="eyebrow eyebrow-l">Kurumsal</p><h2>Personel temini</h2>
  <p>{", ".join(e(k['baslik']) for k in kurumsal_pub)} hizmetleri; günlük, haftalık ve aylık seçeneklerle.</p>
  <div class="dark-cta">{teklif('home-kurumsal', 'kurumsal personel', 'btn btn-light')}<a class="more more-l" href="kurumsal-hizmetler.html">Kurumsal hizmetler →</a></div></div>
</div></section>

{memnuniyet_block()}
"""
pages.append(page("index.html", "New Grup Danışmanlık | İstanbul Ev ve Ofis Temizliği, Sabit Fiyat",
    "İstanbul'da ev, ofis, villa ve plaza iç mekân temizliği. 1+1 ev temizliği 2.500 TL'den başlayan sabit fiyatlar. WhatsApp'tan hemen randevu alın.",
    home, "index.html", [BUSINESS]))

# ---------- TEMİZLİK HİZMETLERİ ----------
detail = ""
for s in D["temizlik_hizmetleri"]:
    cta = randevu('hizmet-' + s['id']) if s["tip"] == "randevu" else teklif('hizmet-' + s['id'], s['baslik'].lower())
    ticks = "".join(f'<li>{ICON["check"]}{e(m)}</li>' for m in s["maddeler"])
    detail += f"""<article class="svc-row" id="{s['id']}"><div class="svc-photo">{pic(s['gorsel'], s['gorsel_alt'], sizes="(max-width: 760px) 100vw, 40vw")}</div>
<div class="svc-body"><h2>{e(s['baslik'])}</h2><p class="lead-s">{e(s['ozet'])}</p><ul class="ticks ticks-2">{ticks}</ul>
<div class="svc-foot"><span class="svc-price">{e(s['fiyat_metni'])}</span>{cta}</div></div></article>"""
svc_page = page_hero("Temizlik Hizmetleri", "İstanbul’da ev, ofis, villa ve plaza temizliği",
    "Ev temizliği sabit fiyatlıdır. Ofis, villa ve plaza işlerinde fiyat alan ve kapsama göre belirlenir.",
    randevu('svc-hero') + teklif('svc-hero', 'ofis temizliği')) + f"""
<section class="sec"><div class="wrap">
<h2 class="h3">Ev temizliği fiyatına dahil</h2>{dahil_gallery()}{kapsam_box()}<div class="spacer"></div>
<div class="svc-list">{detail}</div></div></section>{cta_band()}"""
pages.append(page("temizlik-hizmetleri.html", "Temizlik Hizmetleri İstanbul | Ev, Ofis, Villa, Plaza – New Grup",
    "İstanbul'da ev, ofis, villa ve plaza iç mekân temizliği. Banyo, teras ve içeriden erişilebilen camlar ev temizliği fiyatına dahil.",
    svc_page, "temizlik-hizmetleri.html", [bc("Temizlik Hizmetleri", "temizlik-hizmetleri.html")]))

# ---------- FİYATLAR ----------
notes = "".join(f'<li>{ICON["check"]}{e(n)}</li>' for n in D["fiyat_notlari"])
fiyat = page_hero("Fiyatlar", "İstanbul ev ve ofis temizliği fiyatları",
    "Ev temizliği fiyatları daire tipine göre sabittir. Fiyatı görün, WhatsApp’tan randevunuzu alın.") + f"""
<section class="sec"><div class="wrap price-layout">
  <div>{price_table()}
    <div class="price-ctas">{randevu('fiyatlar-tablo')}{teklif('fiyatlar-tablo', 'ofis temizliği')}</div>
  </div>
  <aside class="side">
    <div class="card"><h2 class="h3">Fiyat notları</h2><ul class="ticks">{notes}</ul></div>
    {kapsam_box()}
    <div class="card"><h2 class="h3">Villa ve plaza</h2><p>Villa ve plaza iç mekân temizliği için alan ve kapsam bilgisine göre teklif hazırlanır.</p>{teklif('fiyatlar-villa', 'villa / plaza temizliği')}</div>
  </aside>
</div></section>
<section class="sec sec-tint"><div class="wrap narrow">
  <h2>Randevu ve ödeme</h2>{odeme_list()}
  <p><a class="more" href="odeme-kosullari.html">Ödeme ve iptal koşullarının tamamı →</a></p>
</div></section>"""
offer_schema = {"@context": "https://schema.org", "@type": "OfferCatalog", "name": "Temizlik fiyatları",
    "itemListElement": [{"@type": "Offer", "name": p["hizmet"], "price": p["fiyat"].replace(".", "").replace(" TL", ""), "priceCurrency": "TRY", "areaServed": "İstanbul"} for p in D["ev_fiyatlari"]]}
pages.append(page("fiyatlar.html", "Ev Temizliği Fiyatları 2026 İstanbul | 1+1, 2+1, 3+1 – New Grup",
    "1+1 ev temizliği 2.500 TL, 2+1 3.250 TL, 3+1 4.000 TL, 4+1 5.000 TL, dubleks 6.500 TL. Ofis temizliği 2.500–5.000 TL. İstanbul.",
    fiyat, "fiyatlar.html", [offer_schema, bc("Fiyatlar", "fiyatlar.html")]))

# ---------- HİZMET BÖLGELERİ ----------
def yaka_block(yaka):
    items = [r["ad"] for r in D["bolgeler"] if r["yaka"] == yaka]
    lis = "".join(f'<li class="region">{ICON["pin"]}<span><b>{e(r)}</b><small>Ev, ofis, villa ve plaza temizliği</small></span></li>' for r in items)
    return f'<div class="card"><h2 class="h3">{e(yaka)} Yakası</h2><ul class="regions">{lis}</ul></div>'
bolge = page_hero("Hizmet Bölgeleri", "İstanbul’da hizmet verdiğimiz bölgeler",
    "Aşağıdaki bölgelerde randevulu ev, ofis, villa ve plaza iç mekân temizliği yapıyoruz.") + f"""
<section class="sec"><div class="wrap grid-2">{yaka_block('Avrupa')}{yaka_block('Anadolu')}</div>
<div class="wrap"><p class="muted center">Bölgeniz listede yoksa WhatsApp’tan sorabilirsiniz.</p></div></section>{cta_band('Bölgenizde randevu alın')}"""
pages.append(page("hizmet-bolgeleri.html", "Temizlik Hizmet Bölgeleri | Sarıyer, Şişli, Beşiktaş, Kadıköy – New Grup",
    "Maslak, Şişli, Sarıyer, Ayazağa, Beşiktaş, Kağıthane, Levent, Etiler, Kadıköy, Pendik, Kartal, Maltepe, Üsküdar ve Ünalan'da ev ve ofis temizliği.",
    bolge, "hizmet-bolgeleri.html", [bc("Hizmet Bölgeleri", "hizmet-bolgeleri.html")]))

# ---------- KURUMSAL ----------
k_cards = "".join(f"""<article class="card k-card{' card-img' if k.get('gorsel') else ''}">{pic(k['gorsel'], k.get('gorsel_alt',''), sizes="(max-width: 760px) 100vw, 25vw") if k.get('gorsel') else ''}<h3>{e(k['baslik'])}</h3><p>{e(k['ozet'])}</p>
<div class="k-terms">{"".join(f'<span class="pill">{e(t)}</span>' for t in D['personel_sureleri'])}</div>
{teklif('kurumsal-' + k['baslik'].lower(), k['baslik'].lower() + ' personeli', 'btn btn-primary btn-sm')}</article>""" for k in kurumsal_pub)
kurumsal = page_hero("Kurumsal Hizmetler", "Kurumsal temizlik ve personel temini",
    "Ofis ve plaza temizliğinin yanında bahçıvan, şoför, vale ve danışma personeli için günlük, haftalık ve aylık seçenekler.",
    teklif('kurumsal-hero', 'kurumsal hizmet')) + f"""
<section class="sec"><div class="wrap"><div class="sec-head"><h2>Personel hizmetleri</h2><p>Her hizmet için ihtiyaç süresini seçerek teklif isteyebilirsiniz.</p></div>
<div class="grid-4">{k_cards}</div></div></section>
<section class="sec sec-tint"><div class="wrap grid-2">
  <div class="card card-img">{pic('ofis', 'Ofiste halıyı süpüren temizlik görevlisi', sizes="(max-width: 760px) 100vw, 50vw")}<h2 class="h3">Ofis temizliği</h2><p>{e(D['ofis_fiyati']['not'])} Fiyat aralığı: <b>{e(D['ofis_fiyati']['fiyat'])}</b>.</p>{teklif('kurumsal-ofis', 'ofis temizliği', 'btn btn-primary btn-sm')}</div>
  <div class="card card-img">{pic('plaza', 'Plaza lobisinde zemin temizleme makinesi kullanan görevli', sizes="(max-width: 760px) 100vw, 50vw")}<h2 class="h3">Plaza iç mekân temizliği</h2><p>Plaza katları ve ortak iç alanlar için kapsamınıza göre teklif hazırlanır.</p>{teklif('kurumsal-plaza', 'plaza temizliği', 'btn btn-primary btn-sm')}</div>
</div></section>"""
pages.append(page("kurumsal-hizmetler.html", "Kurumsal Hizmetler İstanbul | Şoför, Vale, Bahçıvan, Danışma Personeli",
    "İstanbul'da bahçıvan, şoför, vale ve danışma personeli temini; günlük, haftalık ve aylık seçenekler. Ofis ve plaza temizliği için teklif alın.",
    kurumsal, "kurumsal-hizmetler.html", [bc("Kurumsal Hizmetler", "kurumsal-hizmetler.html")]))

# ---------- SSS ----------
faq_html = "".join(f'<details class="faq"><summary>{e(q["s"])}</summary><p>{e(q["c"])}</p></details>' for q in D["sss"])
faq_schema = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q["s"], "acceptedAnswer": {"@type": "Answer", "text": q["c"]}} for q in D["sss"]]}
sss = page_hero("Sık Sorulan Sorular", "Kapsam, ödeme ve randevu hakkında",
    "Temizlik kapsamı, ödeme ve randevu koşulları hakkında kısa yanıtlar.") + f"""
<section class="sec"><div class="wrap narrow">{faq_html}</div></section>{cta_band('Sorunuz mu var?', 'WhatsApp’tan yazın, Burak Bey yanıtlasın.')}"""
pages.append(page("sss.html", "Sık Sorulan Sorular | Temizlik Kapsamı, Ödeme, Randevu – New Grup",
    "Ev temizliği fiyatına neler dahil, ödeme nasıl alınır, randevu iptali nasıl olur? New Grup Danışmanlık SSS.",
    sss, "sss.html", [faq_schema, bc("Sık Sorulan Sorular", "sss.html")]))

# ---------- İLETİŞİM ----------
iletisim = page_hero("İletişim", "Randevu ve teklif için bize ulaşın", f"{C['calisma_sekli']}. En hızlı yanıt için WhatsApp’tan yazın.") + f"""
<section class="sec"><div class="wrap grid-3">
  <div class="card contact"><h2 class="h3">Ev temizliği</h2><p>Daire tipinizi, semtinizi ve uygun gününüzü yazın.</p>{randevu('iletisim-ev')}</div>
  <div class="card contact"><h2 class="h3">Ofis ve kurumsal</h2><p>Alan, kapsam ve sıklık bilgisini yazın, teklif hazırlayalım.</p>{teklif('iletisim-kurumsal', 'ofis / kurumsal hizmet')}</div>
  <div class="card contact"><h2 class="h3">Telefon</h2><p>Yetkili: <b>{e(C['yetkili'])}</b></p>{btn_tel(C['telefon_gosterim'], 'iletisim', 'btn btn-ghost')}</div>
</div>
<div class="wrap narrow"><div class="card"><h2 class="h3">Hizmet bölgeleri</h2><p>{e(", ".join(REGION_NAMES))}.</p></div></div></section>
{memnuniyet_block()}"""
pages.append(page("iletisim.html", "İletişim | New Grup Danışmanlık İstanbul Temizlik – WhatsApp Randevu",
    f"New Grup Danışmanlık iletişim: {C['telefon_gosterim']}. Yetkili {C['yetkili']}. WhatsApp'tan ev temizliği randevusu ve ofis temizliği teklifi alın.",
    iletisim, "iletisim.html", [bc("İletişim", "iletisim.html")]))

# ---------- ÖDEME KOŞULLARI (ödeme öncesi metin) ----------
pre_text = ("New Grup Danışmanlık – Ödeme Öncesi Bilgilendirme\n"
    "• Hizmetlerimiz randevu ile verilir ve ödeme hizmetten önce peşin alınır.\n"
    "• Randevuyu iptal etmeniz halinde, randevunuz uygunluğa göre başka bir tarihe alınabilir.\n"
    "• Yasal cayma ve iade haklarınız saklıdır. Bu hakların doğmadığı durumlarda ücret iadesi yapılmaz.\n"
    "• " + D["kapsam_disi"] + "\n"
    "• " + D["memnuniyet"] + f" ({C['telefon_gosterim']})\n"
    "Ödemeyi yaparak bu koşulları okuduğunuzu onaylamış olursunuz.")
odeme = page_hero("Ödeme ve İptal Koşulları", "Randevu, ödeme ve iptal koşulları",
    "Bu koşullar ödeme öncesinde size WhatsApp’tan yazılı olarak da iletilir.") + f"""
<section class="sec"><div class="wrap narrow">
  <div class="card"><h2 class="h3">Koşullar</h2>{odeme_list()}</div>
  <div class="card"><h2 class="h3">Memnuniyet</h2><p>{e(D['memnuniyet'])}</p></div>
  {kapsam_box()}
  <div class="card"><h2 class="h3">Ödeme öncesi müşteriye gönderilecek metin</h2>
  <p class="small">Ödeme alınmadan önce bu metni WhatsApp’tan müşteriye gönderin.</p>
  <pre class="pre" id="pre-text">{e(pre_text)}</pre>
  <button type="button" class="btn btn-sm btn-outline" data-copy="#pre-text">Metni kopyala</button></div>
</div></section>"""
pages.append(page("odeme-kosullari.html", "Ödeme ve İptal Koşulları | New Grup Danışmanlık",
    "Randevu ile çalışılır, ödeme peşin alınır. İptalde randevu uygunluğa göre ertelenebilir. Yasal cayma ve iade hakları saklıdır.",
    odeme, None, [bc("Ödeme ve İptal Koşulları", "odeme-kosullari.html")]))
with open(os.path.join(ROOT, "odeme-oncesi-bilgilendirme.txt"), "w", encoding="utf-8") as f:
    f.write(pre_text + "\n")

# ---------- KVKK ----------
SB = D["sirket_bilgileri"]
vs_lines = [S["ad"]]
for key, lbl in [("resmi_unvan", "Unvan"), ("adres", "Adres"), ("mersis_no", "MERSİS No"), ("vergi_dairesi_no", "Vergi Dairesi / No"), ("eposta", "E-posta")]:
    if SB.get(key): vs_lines.append(f"{lbl}: {SB[key]}")
basvuru = (f"yazılı olarak {e(SB['adres'])} adresine" if SB.get("adres") else "")
basvuru_txt = (f"Başvurularınızı {basvuru}" + (f" veya {e(SB['eposta'])} e-posta adresine" if SB.get('eposta') else "") + " iletebilirsiniz."
               if SB.get("adres") else
               f"Yazılı başvuru adresimizi öğrenmek ve başvurunuzu iletmek için {e(C['telefon_gosterim'])} numarasından bize ulaşabilirsiniz.")
kvkk = page_hero("KVKK", "Kişisel Verilerin Korunması Aydınlatma Metni",
    "6698 sayılı Kişisel Verilerin Korunması Kanunu’nun 10. maddesi uyarınca hazırlanmıştır.") + f"""
<section class="sec"><div class="wrap narrow prose">
<h2>1. Veri sorumlusu</h2><p>{'<br>'.join(e(x) for x in vs_lines)}</p>
<h2>2. Bu sitede hangi veriler işlenir?</h2>
<p>Sitemizde form, üyelik veya ödeme alanı yoktur. Kişisel veriler yalnızca aşağıdaki durumlarda işlenir:</p>
<ul>
<li><b>WhatsApp veya telefonla bize ulaştığınızda:</b> adınız, telefon numaranız ve mesajınızda paylaştığınız bilgiler (adres, semt, daire tipi, randevu tarihi, hizmet talebi).</li>
<li><b>Siteyi ziyaret ettiğinizde:</b> sitenin barındırıldığı hizmet sağlayıcının güvenlik amacıyla tuttuğu teknik kayıtlar (IP adresi, tarayıcı bilgisi, ziyaret zamanı).</li>
<li><b>Yalnızca izin verirseniz:</b> analiz ve reklam çerezleri aracılığıyla elde edilen kullanım verileri (ziyaret edilen sayfalar, WhatsApp/telefon bağlantısına tıklama). Ayrıntılar <a href="cerez-politikasi.html">Çerez Politikası</a>’ndadır.</li>
</ul>
<h2>3. İşleme amaçları ve hukuki sebepler</h2>
<ul>
<li>Randevu ve teklif taleplerinizi yanıtlamak, hizmeti planlamak ve yerine getirmek — sözleşmenin kurulması ve ifası (KVKK m.5/2-c).</li>
<li>Ödeme, fatura ve yasal kayıt yükümlülükleri — hukuki yükümlülük (KVKK m.5/2-ç).</li>
<li>Hizmetle ilgili şikâyet ve bildirimleri değerlendirmek; sitenin güvenliğini sağlamak — meşru menfaat (KVKK m.5/2-f).</li>
<li>Site kullanımını ölçmek ve reklamların etkisini görmek — açık rızanız (KVKK m.5/1). Rızanızı dilediğiniz zaman “Çerez Tercihleri” üzerinden geri alabilirsiniz.</li>
</ul>
<h2>4. Verilerin aktarılması</h2>
<p>Kişisel verileriniz, hizmetin sunulması için gerekli olduğu ölçüde ve KVKK m.8 ve m.9’daki şartlara uygun olarak şu taraflarla paylaşılabilir: sitenin barındırma hizmetini sağlayan GitHub, Inc. (ABD); WhatsApp üzerinden yazdığınızda WhatsApp/Meta; izin vermeniz halinde Google (Google Analytics ve Google Ads); talep halinde yetkili kamu kurumları. Bu hizmet sağlayıcıların bir kısmı yurt dışında bulunmaktadır.</p>
<h2>5. Toplama yöntemi</h2>
<p>Verileriniz WhatsApp, telefon görüşmesi ve (izninize bağlı olarak) çerezler aracılığıyla elektronik ortamda toplanır.</p>
<h2>6. Saklama süresi</h2>
<p>Veriler, işleme amacının gerektirdiği süre ve ilgili mevzuattaki saklama süreleri boyunca saklanır; süre sonunda silinir, yok edilir veya anonim hale getirilir.</p>
<h2>7. Haklarınız (KVKK m.11)</h2>
<p>Kişisel verilerinizin işlenip işlenmediğini öğrenme, bilgi talep etme, işleme amacını öğrenme, aktarıldığı tarafları bilme, eksik veya yanlış işlenmişse düzeltilmesini, silinmesini veya yok edilmesini isteme, bu işlemlerin aktarılan taraflara bildirilmesini isteme, otomatik analiz sonucu aleyhinize bir sonuca itiraz etme ve kanuna aykırı işleme nedeniyle zarara uğramanız halinde zararın giderilmesini talep etme haklarına sahipsiniz.</p>
<p>{basvuru_txt} Başvurular en geç 30 gün içinde ücretsiz olarak sonuçlandırılır.</p>
<p class="small muted">Son güncelleme: {TODAY}</p>
</div></section>"""
pages.append(page("kvkk-aydinlatma-metni.html", "KVKK Aydınlatma Metni | New Grup Danışmanlık",
    "New Grup Danışmanlık kişisel verilerin korunması aydınlatma metni: hangi veriler, hangi amaçla işlenir, haklarınız nelerdir.",
    kvkk))

# ---------- ÇEREZ POLİTİKASI ----------
ga_on = bool(O.get("ga4_id")); ads_on = bool(O.get("google_ads_id"))
st = lambda on: '<span class="pill pill-mint">Etkin – yalnızca izinle</span>' if on else '<span class="pill">Şu anda kullanılmıyor</span>'
cerez = page_hero("Çerez Politikası", "Çerez Politikası", "Bu sitede hangi çerezlerin ve benzeri teknolojilerin kullanıldığını açıklar.") + f"""
<section class="sec"><div class="wrap narrow prose">
<h2>Kısaca</h2>
<p>Analiz ve reklam çerezleri, siz izin vermeden çalışmaz. Siteyi ilk ziyaretinizde tüm Google etiketleri kapalıdır (Google Consent Mode v2 varsayılanı: “reddedildi”). İzin verdiğiniz kategori için ilgili Google etiketi yüklenir.</p>
<p><button type="button" class="btn btn-sm btn-outline" data-open-consent>Çerez tercihlerimi değiştir</button></p>
<h2>Kullanılan teknolojiler</h2>
<div class="table-wrap"><table class="ptable small-t">
<thead><tr><th>Kategori</th><th>Ad / sağlayıcı</th><th>Amaç</th><th>Süre</th><th>Durum</th></tr></thead>
<tbody>
<tr><td>Zorunlu</td><td><code>ng_consent</code> (tarayıcı yerel depolaması, bu site)</td><td>Çerez tercihinizi hatırlamak</td><td>12 ay</td><td><span class="pill pill-mint">Etkin</span></td></tr>
<tr><td>Analiz</td><td><code>_ga</code>, <code>_ga_*</code> (Google Analytics 4)</td><td>Ziyaret istatistikleri</td><td>En fazla 2 yıl</td><td>{st(ga_on)}</td></tr>
<tr><td>Reklam</td><td><code>_gcl_au</code>, <code>_gcl_aw</code> ve Google reklam çerezleri (Google Ads)</td><td>WhatsApp ve telefon tıklamalarını reklam dönüşümü olarak ölçmek</td><td>En fazla 90 gün – 13 ay</td><td>{st(ads_on)}</td></tr>
</tbody></table></div>
<h2>Üçüncü taraf bağlantılar</h2>
<p>WhatsApp bağlantısına dokunduğunuzda WhatsApp (Meta) uygulamasına veya sitesine yönlendirilirsiniz; orada WhatsApp’ın kendi gizlilik koşulları geçerlidir. Bu sitede yazı tipleri dahil hiçbir içerik üçüncü taraf sunucudan yüklenmez.</p>
<h2>Tercihlerinizi yönetme</h2>
<p>Tercihlerinizi her sayfanın altındaki “Çerez Tercihleri” bağlantısından değiştirebilir veya tarayıcı ayarlarınızdan çerezleri silebilirsiniz. İzni geri aldığınızda etiketler bir sonraki sayfa yüklemesinden itibaren çalışmaz.</p>
<p>Kişisel verilerinize ilişkin ayrıntılar için <a href="kvkk-aydinlatma-metni.html">KVKK Aydınlatma Metni</a>’ni inceleyebilirsiniz.</p>
<p class="small muted">Son güncelleme: {TODAY}</p>
</div></section>"""
pages.append(page("cerez-politikasi.html", "Çerez Politikası | New Grup Danışmanlık",
    "New Grup Danışmanlık çerez politikası: analiz ve reklam çerezleri yalnızca izninizle çalışır. Tercihlerinizi istediğiniz zaman değiştirin.",
    cerez))

# ---------- 404 ----------
page("404.html", "Sayfa bulunamadı | New Grup Danışmanlık", "Aradığınız sayfa bulunamadı.",
     page_hero("404", "Sayfa bulunamadı", "Aradığınız sayfa taşınmış veya kaldırılmış olabilir.",
               '<a class="btn btn-primary" href="index.html">Ana sayfaya dön</a>' + randevu('404')), robots="noindex", base=True)

# ---------- sitemap & robots ----------
prio = {"": "1.0", "fiyatlar.html": "0.9", "temizlik-hizmetleri.html": "0.9"}
sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in pages:
    tail = u[len(BASE) + 1:]
    sm.append(f"  <url><loc>{e(u)}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(tail, '0.6')}</priority></url>")
sm.append("</urlset>")
open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(sm) + "\n")
open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n")
print(f"{len(pages)} sayfa üretildi → {BASE}")
