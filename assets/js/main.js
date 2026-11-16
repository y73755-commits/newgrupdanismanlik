/* New Grup Danışmanlık — menü, çerez izni (Google Consent Mode v2) ve iletişim tıklaması ölçümü */
(function () {
  "use strict";
  var CFG = window.NG_CFG || {};
  var KEY = "ng_consent";
  var MAX_AGE = 365 * 24 * 3600 * 1000;
  var hasTags = !!(CFG.ga4 || CFG.ads);
  var loaded = false;
  var state = { analytics: false, ads: false };

  /* ---------- mobil menü ---------- */
  var burger = document.getElementById("burger");
  var nav = document.getElementById("nav");
  function setMenu(open) {
    nav.classList.toggle("open", open);
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    burger.setAttribute("aria-label", open ? "Menüyü kapat" : "Menüyü aç");
    document.body.classList.toggle("menu-open", open);
  }
  if (burger && nav) {
    burger.addEventListener("click", function () { setMenu(!nav.classList.contains("open")); });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setMenu(false); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });
    window.addEventListener("resize", function () { if (window.innerWidth > 1100) setMenu(false); });
  }

  /* ---------- izin kaydı ---------- */
  function read() {
    try {
      var v = JSON.parse(localStorage.getItem(KEY) || "null");
      if (v && Date.now() - v.t < MAX_AGE) return v;
    } catch (e) {}
    return null;
  }
  function write(a, d) {
    try { localStorage.setItem(KEY, JSON.stringify({ analytics: a, ads: d, t: Date.now(), v: 1 })); } catch (e) {}
  }

  function applyConsent() {
    gtag("consent", "update", {
      analytics_storage: state.analytics ? "granted" : "denied",
      ad_storage: state.ads ? "granted" : "denied",
      ad_user_data: state.ads ? "granted" : "denied",
      ad_personalization: state.ads ? "granted" : "denied"
    });
    loadTags();
  }

  /* Etiketler yalnızca ilgili izin verildiğinde yüklenir (temel/basic Consent Mode). */
  function loadTags() {
    if (loaded) return;
    var useGa = state.analytics && CFG.ga4;
    var useAds = state.ads && CFG.ads;
    if (!useGa && !useAds) return;
    loaded = true;
    var s = document.createElement("script");
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(useGa ? CFG.ga4 : CFG.ads);
    document.head.appendChild(s);
    gtag("js", new Date());
    if (useGa) gtag("config", CFG.ga4);
    if (useAds) gtag("config", CFG.ads);
  }

  /* ---------- banner ve tercih penceresi ---------- */
  var banner = document.getElementById("cc-banner");
  var modal = document.getElementById("cc-modal");
  var boxA = document.getElementById("cc-analytics");
  var boxD = document.getElementById("cc-ads");

  function showBanner(show) {
    if (!banner) return;
    banner.hidden = !show;
    document.body.classList.toggle("cc-open", show);
    if (show) document.body.style.setProperty("--cc-h", banner.offsetHeight + "px");
  }
  function decide(a, d) {
    state.analytics = a; state.ads = d;
    write(a, d);
    showBanner(false);
    if (modal && modal.open) modal.close();
    var wasLoaded = loaded;
    applyConsent();
    toast("Çerez tercihiniz kaydedildi.");
    // İzin geri alındıysa yüklenmiş etiketleri durdurmak için sayfayı yenile
    if (wasLoaded && !a && !d) setTimeout(function () { location.reload(); }, 600);
  }
  function openPrefs() {
    if (!modal) return;
    boxA.checked = state.analytics; boxD.checked = state.ads;
    if (typeof modal.showModal === "function") modal.showModal(); else modal.setAttribute("open", "");
  }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-cc],[data-open-consent],[data-copy]");
    if (!t) return;
    if (t.hasAttribute("data-open-consent")) { e.preventDefault(); openPrefs(); return; }
    if (t.hasAttribute("data-copy")) { copy(t.getAttribute("data-copy")); return; }
    var act = t.getAttribute("data-cc");
    if (act === "accept") decide(true, true);
    else if (act === "reject") decide(false, false);
    else if (act === "save") decide(boxA.checked, boxD.checked);
  });

  var saved = read();
  if (saved) { state.analytics = !!saved.analytics; state.ads = !!saved.ads; applyConsent(); }
  else if (hasTags) showBanner(true);
  window.addEventListener("resize", function () { if (banner && !banner.hidden) showBanner(true); });

  /* ---------- iletişim tıklaması ölçümü ---------- */
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[data-track]");
    if (!a) return;
    var tur = a.getAttribute("data-track");          // "whatsapp" | "telefon"
    var konum = a.getAttribute("data-ctx") || "";
    // dataLayer: Google Etiket Yöneticisi kullanılırsa tetikleyici olarak kullanılabilir
    window.dataLayer.push({ event: "iletisim_tiklamasi", iletisim_turu: tur, iletisim_konumu: konum });
    if (!loaded) return;
    if (state.analytics && CFG.ga4) {
      gtag("event", tur === "whatsapp" ? "whatsapp_tiklamasi" : "telefon_tiklamasi",
        { event_category: "iletisim_tiklamasi", iletisim_turu: tur, iletisim_konumu: konum, send_to: CFG.ga4 });
    }
    if (state.ads && CFG.ads) {
      var label = tur === "whatsapp" ? CFG.adsWa : CFG.adsTel;
      if (label) gtag("event", "conversion", { send_to: CFG.ads + "/" + label });
    }
  }, true);

  /* ---------- yardımcılar ---------- */
  function copy(sel) {
    var el = document.querySelector(sel);
    if (!el) return;
    var txt = el.innerText;
    if (navigator.clipboard) navigator.clipboard.writeText(txt).then(function () { toast("Metin kopyalandı."); });
    else { var r = document.createRange(); r.selectNode(el); getSelection().removeAllRanges(); getSelection().addRange(r); document.execCommand("copy"); toast("Metin kopyalandı."); }
  }
  function toast(msg) {
    var d = document.createElement("div");
    d.className = "toast"; d.setAttribute("role", "status"); d.textContent = msg;
    document.body.appendChild(d);
    setTimeout(function () { d.remove(); }, 2200);
  }
})();
