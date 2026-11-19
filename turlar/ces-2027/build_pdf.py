#!/usr/bin/env python3
"""CES 2027 tur PDF'lerini üretir: python3 build_pdf.py  (Playwright + Chromium gerekir)."""
import pathlib, subprocess, json
H = pathlib.Path(__file__).parent
FONT = (H / "../../brands/fuartour/assets/fonts").resolve()

CSS = """
@font-face{font-family:R;font-weight:500;src:url('file://%(f)s/Rubik-Medium.ttf')}
@font-face{font-family:R;font-weight:600;src:url('file://%(f)s/Rubik-SemiBold.ttf')}
@font-face{font-family:R;font-weight:700;src:url('file://%(f)s/Rubik-Bold.ttf')}
@font-face{font-family:R;font-weight:800;src:url('file://%(f)s/Rubik-ExtraBold.ttf')}
@page{size:A4;margin:0}
*{box-sizing:border-box}
body{margin:0;font-family:R,sans-serif;font-weight:500;font-size:8.6pt;line-height:1.42;color:#2a3140}
.page{width:210mm;height:297mm;position:relative;page-break-after:always;overflow:hidden}
.hd{background:#16213E;height:19mm;padding:0 13mm;display:flex;align-items:center;justify-content:space-between;border-bottom:1.1mm solid #FF5722}
.hd img{height:8mm}
.hd div{color:#fff;text-align:right;font-size:7.6pt;line-height:1.35}.hd b{font-weight:700;font-size:8.4pt}
.ft{position:absolute;left:13mm;right:13mm;bottom:7mm;border-top:.3mm solid #e5e7eb;padding-top:2.2mm;display:flex;justify-content:space-between;font-size:7pt;color:#6b7280}
.ft b{color:#FF5722;font-weight:700}
.bd{padding:8mm 13mm 0}
.kick{color:#FF5722;font-weight:700;font-size:7.2pt;letter-spacing:.08em;text-transform:uppercase}
h1{font-size:19pt;font-weight:800;color:#16213E;margin:.6mm 0 1.2mm;line-height:1.1}
.sub{color:#4b5563;font-size:9pt}
.top{display:flex;gap:5mm;align-items:center}.top img{width:19mm;height:19mm;object-fit:contain;border-radius:2mm;border:.3mm solid #e5e7eb}
h2{font-size:10.6pt;font-weight:700;color:#16213E;margin:5.5mm 0 2.2mm;padding-left:2.4mm;border-left:1.1mm solid #FF5722;line-height:1.15}
h2 small{font-weight:500;color:#6b7280;font-size:7.6pt}
.ph{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm;margin-top:4.5mm}.ph img{width:100%%;height:33mm;object-fit:cover;border-radius:1.4mm;display:block}
.kv{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm}.kv div{display:flex;gap:3mm;padding:1.3mm 0;border-bottom:.25mm solid #eef0f4}
.kv span{color:#6b7280;width:24mm;flex:none;font-size:7.8pt}.kv b{font-weight:600;color:#1f2937}
.st{display:grid;grid-template-columns:repeat(4,1fr);gap:2.4mm}.st div{background:#fff7f3;border:.3mm solid #ffe1d6;border-radius:1.6mm;padding:2.2mm 3mm}
.st b{display:block;color:#FF5722;font-size:13pt;font-weight:800;line-height:1.15}.st span{font-size:7pt;color:#6b7280}
.day{display:flex;gap:4mm;padding:1.7mm 0;border-bottom:.25mm solid #eef0f4}.day .d{width:33mm;flex:none}
.day .n{display:inline-block;background:#16213E;color:#fff;font-weight:700;font-size:6.8pt;border-radius:1mm;padding:.3mm 1.8mm}
.day .d b{display:block;font-weight:600;font-size:7.8pt;margin-top:.7mm;color:#1f2937}.day p{margin:0}.day p b{font-weight:700;color:#16213E}
.two{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm}
.fl{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm}.fl div{background:#f3f4f6;border-radius:1.4mm;padding:1.8mm 3mm;font-size:7.8pt}.fl b{font-weight:700;color:#16213E}
.pr{display:grid;grid-template-columns:1fr 1fr;gap:2.4mm;margin-top:2.4mm}.pr div{border:.5mm solid #FF5722;border-radius:1.8mm;padding:2.4mm 3.4mm}
.pr span{font-size:7.6pt;color:#6b7280;display:block}.pr b{font-size:15pt;font-weight:800;color:#16213E}.pr i{font-style:normal;font-size:8pt;color:#6b7280;font-weight:600}
ul{margin:0;padding:0;list-style:none}li{padding-left:3.4mm;position:relative;margin:.9mm 0}li:before{content:'';position:absolute;left:0;top:1.5mm;width:1.3mm;height:1.3mm;border-radius:50%%;background:#FF5722}
ul.x li:before{background:#9ca3af}
.note{background:#f3f4f6;border-radius:1.6mm;padding:2.6mm 3.4mm;margin-top:3mm}.note b{font-weight:700;color:#16213E}
.chips{display:flex;flex-wrap:wrap;gap:1.8mm;margin-top:2.6mm}.chips span{background:#f3f4f6;border-radius:1.2mm;padding:1mm 2.6mm;font-size:7.6pt}.chips b{font-weight:700;color:#16213E}
.pl{display:grid;grid-template-columns:1fr 1fr;gap:1.6mm 8mm}.pl div b{display:block;font-weight:700;color:#16213E}.pl div{padding:1.2mm 0;border-bottom:.25mm solid #eef0f4}
p{margin:0 0 1.6mm}.tbd{color:#b45309;font-weight:700}
.draft{position:absolute;top:22mm;right:13mm;background:#fef3c7;color:#92400e;font-weight:700;font-size:6.8pt;letter-spacing:.08em;border-radius:1mm;padding:.5mm 2.2mm}

.ph4{display:grid;grid-template-columns:repeat(4,1fr);gap:2.2mm;margin:2.6mm 0 3mm}.ph4 img{width:100%%;height:27mm;object-fit:cover;border-radius:1.4mm;display:block}
.hn{font-size:13pt;font-weight:800;color:#16213E;margin:4.5mm 0 .4mm;line-height:1.15}.hs{color:#6b7280;font-size:8pt}
.dist{display:grid;grid-template-columns:1fr 1fr;gap:0 8mm}.dist div{display:flex;justify-content:space-between;gap:3mm;padding:1.2mm 0;border-bottom:.25mm solid #eef0f4}.dist b{font-weight:700;color:#16213E;white-space:nowrap}
.sight{display:grid;grid-template-columns:repeat(4,1fr);gap:2.2mm}.sight img{width:100%%;height:25mm;object-fit:cover;border-radius:1.4mm;display:block}.sight b{display:block;font-weight:700;color:#16213E;margin-top:1mm}.sight span{font-size:7.4pt;color:#4b5563;line-height:1.3;display:block}
.cred{font-size:6pt;color:#9ca3af;margin-top:2mm}
.frm{width:100%%;border-collapse:collapse;font-size:7.8pt}.frm td,.frm th{border:.3mm solid #cbd5e1;padding:1.6mm 2mm;height:7.4mm;text-align:left;vertical-align:middle}.frm th{background:#f3f4f6;font-weight:700;color:#16213E;font-size:7.2pt}.frm td.l{background:#f8fafc;font-weight:600;width:34mm;color:#374151}
.terms{font-size:6.9pt;line-height:1.38;color:#374151;text-align:justify}.terms b{font-weight:700;color:#16213E}
.sig{display:grid;grid-template-columns:1fr 1fr;gap:6mm;margin-top:3mm}.sig div{border:.3mm solid #cbd5e1;border-radius:1.4mm;padding:2.4mm 3mm;font-size:7.6pt;min-height:27mm}
""" % {"f": FONT}

FAIR_KV = """<div class=kv>
<div><span>Fuar</span><b>CES 2027 – Tüketici Elektroniği ve Teknoloji Fuarı (60. yıl)</b></div>
<div><span>Ürün grupları</span><b>Yapay zekâ ve çipler, robotik, mobilite, dijital sağlık ve giyilebilir cihazlar, akıllı ev, enerji, XR, girişimler (Eureka Park)</b></div>
<div><span>Fuar tarihi</span><b>6–9 Ocak 2027</b></div>
<div><span>Ziyaretçi profili</span><b>Yalnızca ticari ziyaretçiler</b></div>
<div><span>Yer</span><b>Las Vegas Convention Center ve çevre mekânlar, Las Vegas</b></div>
<div><span>Organizatör</span><b>Consumer Technology Association (CTA)</b></div></div>
<h2>Geçmiş Fuar İstatistikleri <small>· CES 2026</small></h2>
<div class=st><div><b>4.100+</b><span>katılımcı firma</span></div><div><b>148.392</b><span>ziyaretçi</span></div>
<div><b>55.841</b><span>ABD dışından ziyaretçi</span></div><div><b>141</b><span>ülke, bölge ve toprak</span></div></div>"""

D1 = ("1. GÜN", "5 Ocak Salı", "<b>İstanbul – Los Angeles – Las Vegas.</b> 10:50 İstanbul Havalimanı dış hatlar gidiş katında buluşma, check-in ve pasaport işlemleri. <b>13:50</b> THY <b>TK9</b> ile Los Angeles'a direkt uçuş, yerel saatle 16:35 varış. Karşılama ve kara yoluyla Las Vegas'a transfer (yaklaşık 4,5 saat), otele yerleşme.")
D2 = ("2. GÜN", "6 Ocak Çarşamba", "<b>CES 1. gün.</b> Otelde kahvaltı. Las Vegas Convention Center'da fuar ziyareti, yaka kartlarının alınması ve firma görüşmeleri.")
D3 = ("3.–4. GÜN", "7–8 Ocak Perşembe–Cuma", "<b>CES 2. ve 3. gün.</b> Otelde kahvaltı. Tam gün fuar ziyareti: The Venetian'daki sergi alanları ve girişimlere ayrılan Eureka Park. Akşamlar serbest.")

TOURS = {
 "CES-Las-Vegas-2027-4-Gece-Fuar-Turu": dict(
  short="CES Las Vegas 2027 · 4 gece", kick="4 GECE · 5 – 10 OCAK 2027", title="CES Las Vegas 2027 Fuar Turu",
  sub="Dünyanın en büyük tüketici teknolojileri fuarı · THY ile Los Angeles'a direkt uçuş · Las Vegas'ta 4* The STRAT Hotel",
  days=[D1, D2, D3,
   ("5. GÜN", "9 Ocak Cumartesi", "<b>Las Vegas – Los Angeles – İstanbul.</b> Otelde kahvaltı, odaların boşaltılması ve kara yoluyla Los Angeles Havalimanı'na transfer (yaklaşık 4,5 saat; bu gün fuar ziyareti yoktur). <b>18:30</b> THY <b>TK10</b> ile İstanbul'a direkt uçuş."),
   ("6. GÜN", "10 Ocak Pazar", "<b>İstanbul.</b> 18:55 İstanbul Havalimanı'na varış ve turumuzun sonu.")],
  stay="4 gece Las Vegas", hotel=[("Las Vegas · 5–9 Ocak (4 gece)", "4* The STRAT Hotel, Casino & Tower – Las Vegas Strip, fuar alanına yaklaşık 1,8 km")], price=("2.820","3.600"),
  ret="Dönüş TK10 · 9 Ocak Cumartesi 18:30 → 10 Ocak Pazar 18:55", per="4 gece, kişi başı",
  inc=["THY ile İstanbul – Los Angeles – İstanbul direkt uçak bileti (TK9 / TK10, 23 kg bagaj) ve havalimanı vergileri",
       "Las Vegas'ta 4* The STRAT Hotel, Casino & Tower'da 4 gece kahvaltı dahil konaklama ve otel vergileri", "Los Angeles Havalimanı – Las Vegas oteli – Los Angeles Havalimanı transferleri"],
  cities=["lv"]),
 "CES-Las-Vegas-2027-6-Gece-Las-Vegas-Los-Angeles-Turu": dict(
  short="CES 2027 · 6 gece Las Vegas + Los Angeles", kick="6 GECE · 5 – 12 OCAK 2027", title="CES 2027 Las Vegas + Los Angeles Turu",
  sub="4 gece Las Vegas (4* The STRAT) + 2 gece Los Angeles (4* DoubleTree by Hilton Downtown) · THY ile Los Angeles'a direkt uçuş · panoramik şehir turu ve alışveriş turu",
  days=[D1, D2, D3,
   ("5. GÜN", "9 Ocak Cumartesi", "<b>CES son gün / Las Vegas – Los Angeles.</b> Otelde kahvaltı ve son fuar ziyaretleri. Öğleden sonra kara yoluyla Los Angeles'a geçiş (yaklaşık 4,5 saat), otele yerleşme."),
   ("6. GÜN", "10 Ocak Pazar", "<b>Los Angeles panoramik tur.</b> Otelde kahvaltı. Hollywood Bulvarı ve Şöhretler Kaldırımı, Hollywood yazısı manzarası, Beverly Hills ve Rodeo Drive, Santa Monica sahili."),
   ("7. GÜN", "11 Ocak Pazartesi", "<b>Alışveriş turu / Los Angeles – İstanbul.</b> Otelde kahvaltı, odaların boşaltılması ve outlet alışveriş turu. Öğleden sonra havalimanına transfer, <b>18:30</b> THY <b>TK10</b> ile İstanbul'a direkt uçuş."),
   ("8. GÜN", "12 Ocak Salı", "<b>İstanbul.</b> 18:55 İstanbul Havalimanı'na varış ve turumuzun sonu.")],
  stay="4 gece Las Vegas + 2 gece Los Angeles", hotel=[("Las Vegas · 5–9 Ocak (4 gece)", "4* The STRAT Hotel, Casino & Tower – Las Vegas Strip, fuar alanına yaklaşık 1,8 km"), ("Los Angeles · 9–11 Ocak (2 gece)", "4* DoubleTree by Hilton Los Angeles Downtown – şehir merkezi")], price=("2.870","3.850"),
  ret="Dönüş TK10 · 11 Ocak Pazartesi 18:30 → 12 Ocak Salı 18:55", per="6 gece, kişi başı",
  inc=["THY ile İstanbul – Los Angeles – İstanbul direkt uçak bileti (TK9 / TK10, 23 kg bagaj) ve havalimanı vergileri",
       "Las Vegas'ta 4* The STRAT Hotel, Casino & Tower'da 4 gece kahvaltı dahil konaklama ve otel vergileri", "Los Angeles'ta 4* DoubleTree by Hilton Los Angeles Downtown'da 2 gece kahvaltı dahil konaklama ve otel vergileri",
       "Los Angeles Havalimanı – Las Vegas – Los Angeles – havalimanı transferleri", "Los Angeles panoramik şehir turu (10 Ocak)", "Alışveriş turu (11 Ocak)"],
  cities=["lv", "la"]),
}
EXC = ["ABD (B1/B2) vizesi ve başvuru harcı", "Fuar giriş kaydı", "Programda belirtilmeyen öğle ve akşam yemekleri", "Seyahat sağlık sigortası", "Yurt dışı çıkış harcı", "Opsiyonel turlar ve kişisel harcamalar"]

CITY = {"lv": """<h2>Las Vegas</h2>
<p>Nevada çölünün ortasındaki Las Vegas, dünyanın en büyük kongre ve fuar şehirlerinden biridir. CES, Las Vegas Convention Center salonlarının yanı sıra The Venetian'daki sergi alanlarına yayılır.</p>
<div class=chips><span><b>Saat farkı</b> Türkiye'den 11 saat geri</span><span><b>Para birimi</b> ABD doları (USD)</span><span><b>Elektrik</b> 120 V · A ve B tipi priz</span></div>
<div class=pl style="margin-top:3mm"><div><b>The Strip</b>Las Vegas Bulvarı boyunca temalı oteller ve gösteriler.</div><div><b>Bellagio Çeşmeleri</b>Akşam saatlerinde müzikli su gösterisi.</div>
<div><b>Fremont Street</b>Eski şehir merkezi ve ışık tavanı.</div><div><b>Sphere</b>Dev LED küre; dışarıdan da izlenebilir.</div></div>""",
 "la": """<h2>Los Angeles</h2>
<p>Pasifik kıyısındaki Los Angeles, eğlence endüstrisinin merkezi ve ABD'nin en büyük ikinci şehridir. Panoramik tur ve alışveriş turu program dahilindedir.</p>
<div class=chips><span><b>Saat farkı</b> Türkiye'den 11 saat geri</span><span><b>Para birimi</b> ABD doları (USD)</span><span><b>Elektrik</b> 120 V · A ve B tipi priz</span></div>
<div class=pl style="margin-top:3mm"><div><b>Hollywood Bulvarı</b>Şöhretler Kaldırımı ve Çin Tiyatrosu.</div><div><b>Griffith Gözlemevi</b>Hollywood yazısı ve şehir manzarası.</div>
<div><b>Beverly Hills</b>Rodeo Drive ve çevresi.</div><div><b>Santa Monica</b>İskele ve okyanus kıyısı.</div></div>"""}

TIPS = """<h2>Fuar Ziyaretinde Dikkat Edilecekler</h2>
<p><b>Kayıt ve giriş.</b> CES yalnızca sektör profesyonellerine açıktır; kayıt önceden yapılır, yaka kartı fotoğraflı kimlikle teslim alınır.</p>
<p><b>Alanlar.</b> Fuar birden çok mekâna yayılır: Las Vegas Convention Center, The Venetian'daki sergi alanları ve girişimlere ayrılan Eureka Park. Günlük rotanızı salonlara göre planlayın.</p>
<p><b>Kartvizit ve notlar.</b> Bol miktarda İngilizce kartvizit getirin; görüştüğünüz firmaların kartlarına ürün ve fiyat notlarını aynı gün yazın.</p>
<p><b>Kıyafet.</b> Rahat ayakkabı şart; salonlar arası mesafeler uzundur. Ocak ayında sabah ve akşam saatleri serindir.</p>
<div class=note><b>Vize ve pasaport.</b> Umuma mahsus pasaportla ABD'deki bir fuarı ziyaret etmek için göçmen olmayan ziyaretçi vizesi (B1/B2) gerekir; başvuru DS-160 formu ve kural olarak yüz yüze mülakatla yapılır. Vize başvuru desteği için Fuartour'a ulaşabilirsiniz.</div>"""

import os
def img(name): return f'<img src="assets/{name}">' if (H/"assets"/name).exists() else ""

HOTELS = {
 "strat": dict(name="The STRAT Hotel, Casino & Tower", star="4*", where="2000 Las Vegas Blvd S · Las Vegas Strip (kuzey ucu)", imgs=["strat-0.jpg","strat-1.jpg","strat-3.jpg","strat-4.jpg"],
  about="Las Vegas Strip'in kuzey ucundaki otel, şehrin simgelerinden olan gözlem kulesiyle tanınır; kulenin tepesinde seyir terası ve döner restoran bulunur. Tesiste açık havuz, kumarhane, restoranlar ve barlar vardır. Odalar yenilenmiş, sade ve ferah bir düzendedir.",
  dist=[("Las Vegas Convention Center (CES ana alanı)","≈ 1,8 km"),("The Venetian Expo (CES sergi alanı, Eureka Park)","≈ 2,9 km"),("Fremont Street","≈ 2,8 km"),("Los Angeles Havalimanı (kara yolu)","≈ 430 km · 4,5 saat")]),
 "dt": dict(name="DoubleTree by Hilton Los Angeles Downtown", star="4*", where="120 S Los Angeles St · Downtown, Little Tokyo", imgs=["dt-0.jpg","dt-2.jpg","dt-1.jpg","dt-3.jpg"],
  about="Şehir merkezinde, Little Tokyo semtindeki otel, çatı katındaki Japon bahçesiyle bilinir. Odalar geniş pencereli ve çalışma masalıdır; tesiste restoran, bar ve fitness merkezi bulunur. Açık büfe kahvaltı otelin kafesinde verilir.",
  dist=[("Hollywood Bulvarı / Şöhretler Kaldırımı","≈ 9,6 km"),("Rodeo Drive, Beverly Hills","≈ 14,6 km"),("Santa Monica İskelesi","≈ 23,7 km"),("Los Angeles Havalimanı (LAX)","≈ 19,4 km")]),
}
def hotel_block(k, when):
    h = HOTELS[k]
    return (f"<div class=hn>{h['star']} {h['name']}</div><div class=hs>{when} · kahvaltı dahil · {h['where']}</div>"
            f"<div class=ph4>{''.join(img(i) for i in h['imgs'])}</div><p>{h['about']}</p>"
            f"<h2>Mesafeler <small>· kuş uçuşu, yaklaşık</small></h2><div class=dist>{''.join(f'<div><span>{a}</span><b>{b}</b></div>' for a,b in h['dist'])}</div>")

CRED = json.loads((H/"assets/credits.json").read_text(encoding="utf8")) if (H/"assets/credits.json").exists() else {}
def sights(items):
    cells = "".join(f"<div>{img(k+'.jpg')}<b>{n}</b><span>{d}</span></div>" for k, n, d in items)
    cr = " · ".join(f"{n}: {(CRED[k]['artist']+', ') if CRED[k]['artist'] else ''}{CRED[k]['lic']}" for k, n, d in items if k in CRED and (H/'assets'/(k+'.jpg')).exists())
    return f"<div class=sight>{cells}</div>" + (f"<div class=cred>Fotoğraflar Wikimedia Commons — {cr}</div>" if cr else "")

CITY_LV = """<div class=kick>ŞEHİR REHBERİ</div><h1>Las Vegas</h1>
<p class=sub>Nevada çölünün ortasındaki Las Vegas, dünyanın en büyük kongre ve fuar şehirlerinden biridir. Şehrin ana caddesi olan Las Vegas Bulvarı'nın ("The Strip") iki yanında temalı dev oteller sıralanır; CES de bu bölgedeki Las Vegas Convention Center ile The Venetian'a yayılır.</p>
<div class=chips><span><b>Saat farkı</b> Türkiye'den 11 saat geri</span><span><b>Para birimi</b> ABD doları (USD)</span><span><b>Ocak havası</b> gündüz ≈ 14 °C, gece ≈ 4 °C, kuru</span><span><b>Elektrik</b> 120 V · A ve B tipi priz (adaptör gerekir)</span><span><b>Bahşiş</b> restoran ve takside %15–20</span><span><b>Dil</b> İngilizce</span></div>
<h2>Gezilecek Yerler</h2>""" + "{sights}" + """
<p style="margin-top:2.4mm"><b>Diğer duraklar:</b> The Venetian'ın kanalları ve Grand Canal Shoppes · Caesars Palace Forum Shops · High Roller dönme dolabı · The STRAT gözlem kulesi · Las Vegas North Premium Outlets · günübirlik Hoover Barajı ve Büyük Kanyon turları.</p>
<h2>Şehir İçi Ulaşım</h2>
<div class=two><p><b>Las Vegas Monorail.</b> Strip'in doğusunda SAHARA ile MGM Grand arasında çalışır ve Las Vegas Convention Center'da durur. The STRAT'a en yakın durak SAHARA'dır (yaklaşık 800 m).</p><p><b>Taksi ve Uber/Lyft.</b> Fuar günlerinde sabah ve akşam saatlerinde yoğunluk olur; otellerin belirlenmiş biniş noktaları kullanılır.</p>
<p><b>Yürüyüş.</b> Oteller haritada yakın görünse de mesafeler uzundur; salonlar arası geçişlere zaman ayırın.</p><p><b>Havalimanı.</b> Tur uçuşları Los Angeles üzerindendir; Las Vegas'a kara yoluyla gidilir (yaklaşık 430 km, 4,5 saat).</p></div>
<h2>Fuar Ziyaretinde Dikkat Edilecekler</h2>
<div class=two><p><b>Kayıt ve giriş.</b> CES yalnızca sektör profesyonellerine açıktır; kayıt önceden yapılır, yaka kartı fotoğraflı kimlikle teslim alınır.</p><p><b>Alanlar.</b> Las Vegas Convention Center, The Venetian'daki sergi alanları ve girişimlere ayrılan Eureka Park. Günlük rotanızı salonlara göre planlayın.</p>
<p><b>Kartvizit.</b> Bol miktarda İngilizce kartvizit getirin; görüşme notlarını aynı gün yazın.</p><p><b>Kıyafet.</b> Rahat ayakkabı şart. Salonlar klimalıdır, sabah ve akşam saatleri serindir.</p></div>
<div class=note><b>Vize ve pasaport.</b> Umuma mahsus pasaportla ABD'deki bir fuarı ziyaret etmek için göçmen olmayan ziyaretçi vizesi (B1/B2) gerekir; başvuru DS-160 formu ve kural olarak yüz yüze mülakatla yapılır. Vize başvuru desteği için Fuartour'a ulaşabilirsiniz.</div>"""
LV_S = [("strip","The Strip","Las Vegas Bulvarı boyunca temalı oteller ve gösteriler."),("bellagio","Bellagio Çeşmeleri","Akşamları müzik eşliğinde su gösterisi."),("fremont","Fremont Street","Eski şehir merkezi ve dev ışık tavanı."),("sphere","Sphere","Dev LED küre; dışarıdan da izlenir.")]

CITY_LA = """<div class=kick>ŞEHİR REHBERİ</div><h1>Los Angeles</h1>
<p class=sub>Pasifik kıyısındaki Los Angeles, ABD'nin en büyük ikinci şehri ve dünya eğlence endüstrisinin merkezidir. Şehir çok geniş bir alana yayılır; semtler arası ulaşım araçla yapılır. Panoramik şehir turu ve alışveriş turu programa dahildir.</p>
<div class=chips><span><b>Saat farkı</b> Türkiye'den 11 saat geri</span><span><b>Para birimi</b> ABD doları (USD)</span><span><b>Ocak havası</b> gündüz ≈ 20 °C, gece ≈ 9 °C</span><span><b>Elektrik</b> 120 V · A ve B tipi priz</span><span><b>Bahşiş</b> restoran ve takside %15–20</span><span><b>Satış vergisi</b> etiket fiyatına kasada eklenir</span></div>
<h2>Gezilecek Yerler</h2>""" + "{sights}" + """
<p style="margin-top:2.4mm"><b>Diğer duraklar:</b> Beverly Hills ve Rodeo Drive · Hollywood yazısı manzarası · The Grove ve Farmers Market · Venice Beach · Getty Center · Universal Studios Hollywood · Downtown'da Walt Disney Konser Salonu ve Grand Central Market.</p>
<h2>Program Dahilindeki Turlar</h2>
<div class=two><p><b>Panoramik şehir turu (10 Ocak).</b> Hollywood Bulvarı ve Şöhretler Kaldırımı, Hollywood yazısı manzarası, Beverly Hills ve Rodeo Drive, Santa Monica sahili.</p><p><b>Alışveriş turu (11 Ocak).</b> Odalar boşaltıldıktan sonra outlet alışverişi; ardından havalimanına transfer ve 18:30 THY TK10 ile dönüş.</p></div>
<h2>Pratik Bilgiler</h2>
<div class=two><p><b>Ulaşım.</b> Uber/Lyft yaygındır. Trafik sabah 07–10 ve akşam 16–19 arasında çok yoğundur; havalimanına erken çıkın.</p><p><b>Alışveriş.</b> Outlet merkezlerinde pasaportla ziyaretçi indirim kuponu alınabilir. Fiyatlara satış vergisi kasada eklenir.</p>
<p><b>Yemek.</b> Otelin bulunduğu Little Tokyo ve çevresinde çok sayıda restoran vardır; helal ve Akdeniz mutfağı seçenekleri şehir genelinde bulunur.</p><p><b>İletişim.</b> ABD'de kullanım için e-SIM ya da uluslararası paket önerilir; otellerde ücretsiz Wi-Fi vardır.</p></div>"""
LA_S = [("hollywood","Hollywood Bulvarı","Şöhretler Kaldırımı ve Çin Tiyatrosu."),("griffith","Griffith Gözlemevi","Hollywood yazısı ve şehir manzarası."),("santamonica","Santa Monica","İskele, lunapark ve okyanus kıyısı."),("rodeo","Rodeo Drive","Beverly Hills'in lüks alışveriş caddesi.")]

TERMS = """<b>Genel Şartlar:</b> 1- Katılımcı müracaatı ile şartları okuyup kabul ettiğini beyan etmektedir. 2- Havayolu şirketi / şirketlerine bağlı aksaklıklardan dolayı firmamız sorumlu değildir. 3- Varılacak / geçilecek noktalar için ilgili ülke veya yönetimlerin vize veya geçiş izni vermesi konusunda Fuar Tour herhangi bir taahhüt altına girmez. Vize reddi – geçiş izni verilmemesi gibi bahsedilen durumlar oluşursa, Fuar Tour iptal işlemleri için geçerli hükümleri uygular. 4- Hareket saatine 25 günden az kala olan iptallerde katılımcı tur bedelinin tamamını ödemek durumundadır. Tüm iptal talepleri yazılı olarak yapılmak zorundadır. 5- Tur bedellerinin bir kısmının dahi ödenmemesi durumunda Fuar Tour tur kaydı iptal hakkı mahfuzdur. 6- Tek kişilik başvurularda kişi Fuar Tour'un vereceği paylaşımlı odayı peşinen kabul etmiştir veya tek kişilik oda farkını ödeme durumundadır. 7- Katılımcı tur programına uymak zorundadır. Değişiklik talepleri teknik şartlar dahilinde değerlendirilecektir. 8- Ödemelerde TCMB USD satış kuru esastır. 9- Zorunlu durumlarda Fuar Tour, kendi iradesi dışında oluşan sebepler yüzünden, program süresi ve standartlarını değiştirmeden, otel, hareket saatleri – transfer araçları ve şehirleri önceden haber imkânı bulamasa dahi değiştirme hakkına sahiptir."""

def form(t):
    rows = "".join(f"<tr><td>{i}-)</td><td></td><td></td><td style='text-align:center'>☐</td><td style='text-align:center'>☐</td><td></td></tr>" for i in range(1, 5))
    fields = "".join(f"<tr><td class=l>{a}</td><td></td></tr>" for a in ["FİRMA ADI / ÜNVANI","FATURA ADRESİ","İL / İLÇE","VERGİ DAİRESİ / NUMARASI","TELEFON","E-MAIL / WEB ADRESİ"])
    return f"""<div class=kick>TUR KAYIT FORMU VE SÖZLEŞMESİ</div><h1>{t['title']} – Katılım Formu</h1>
<div class=sub>{t['kick'].title().replace('Ocak','Ocak')} · çift kişilik odada kişi başı {t['price'][0]} USD · tek kişilik odada {t['price'][1]} USD</div>
<div class=two style="margin-top:4mm;grid-template-columns:1.25fr 1fr"><table class=frm>{fields}</table>
<div class=note style="margin-top:0"><b>ÖDEME BİLGİLERİ</b><br>Tur kaydı esnasında ödemenin %100'ü yapılmalıdır.<br><br><b>Kuveyt Türk Bankası – USD</b><br>TR30 0020 5000 0984 8446 3001 01<br><b>Kuveyt Türk Bankası – TL</b><br>TR86 0006 2000 0780 0006 2984 48<br><br>Hesap adı: FUAR TURİZM DIŞ TİC. LTD. ŞTİ.<br>Lütfen havalelerinizi katılımcı firma adına yapınız.</div></div>
<h2>Katılımcılar</h2>
<table class=frm><tr><th style="width:9mm"></th><th>ADI SOYADI (pasaporta göre yazınız)</th><th style="width:36mm">CEP TELEFONU</th><th style="width:21mm">2 KİŞİLİK ODA</th><th style="width:21mm">1 KİŞİLİK ODA</th><th style="width:26mm">TUTAR (USD)</th></tr>{rows}
<tr><td colspan=3 style="font-weight:700">☐ Nakit / Havale &nbsp;&nbsp;&nbsp; ☐ Kredi kartı (tek çekim) · Kart türü: ...............</td><td colspan=2 style="font-weight:700;text-align:right">TOPLAM (USD)</td><td></td></tr></table>
<h2>Sözleşme Şartları</h2><div class=terms>{TERMS}</div>
<div class=sig><div><b>Katılımcı Onayı</b><br>Formda verdiğimiz tüm bilgi ve şartları teyit ederiz.<br><br>Yetkili isim: ........................................<br><br>Tarih: ...... / ...... / 20....<br><br>Kaşe / İmza</div>
<div><b>FUAR TURİZM DIŞ TİCARET LTD. ŞTİ.</b><br>TÜRSAB A-5672 FUARİST TRAVEL<br>Kurtuluş Cad. No:1 Köşe Apt. Kat:3 Daire:5 Şişli / İstanbul<br>Tel: +90 212 230 91 93 · Faks: +90 212 230 91 95<br>0850 255 58 58 · www.fuartour.com</div></div>"""

def page(t, body, n, total):
    return f"""<div class=page><div class=hd><img src="assets/logo-on-dark.png"><div><b>{t['short']}</b><br>fuartour.com · 0850 255 58 58</div></div>
<div class=bd>{body}</div>
<div class=ft><span><b>Fuartour</b> · Fuar ve iş seyahati organizasyonu</span><span>fuartour.com · 0850 255 58 58</span><span>{n} / {total}</span></div></div>"""

def build(name, t):
    two = "la" in t["cities"]
    days = "".join(f"<div class=day><div class=d><span class=n>{a}</span><b>{b}</b></div><p>{c}</p></div>" for a, b, c in t["days"])
    p1 = f"""<div class=top><img src="assets/ces-logo.jpg"><div><div class=kick>{t['kick']}</div><h1>{t['title']}</h1><div class=sub>{t['sub']}</div></div></div>
<div class=ph><img src="assets/ces-2026.jpg"><img src="assets/ces-2026-1.jpg"><img src="assets/ces-2026-2.jpg"></div>
<h2>Fuar Bilgileri</h2>{FAIR_KV}<h2>Gün Gün Program</h2>{days}"""
    price = f"""<h2>Uçuş ve Tur Ücreti <small>· {t['per']}</small></h2>
<div class=fl><div><b>Gidiş TK9</b> · 5 Ocak Salı 13:50 → 16:35 (İstanbul – Los Angeles, direkt)</div><div><b>{t['ret'].split(' · ')[0]}</b> · {t['ret'].split(' · ')[1]} (Los Angeles – İstanbul, direkt)</div></div>
<div class=pr><div><span>Çift kişilik odada kişi başı</span><b>{t['price'][0]}</b> <i>USD</i></div><div><span>Tek kişilik odada</span><b>{t['price'][1]}</b> <i>USD</i></div></div>
<div class=two><div><h2>Fiyata Dahil Hizmetler</h2><ul>{''.join(f'<li>{x}</li>' for x in t['inc'])}</ul></div>
<div><h2>Fiyata Dahil Olmayanlar</h2><ul class=x>{''.join(f'<li>{x}</li>' for x in EXC)}</ul></div></div>"""
    head = f"<div class=kick>KONAKLAMA · {t['stay'].upper()} · KAHVALTI DAHİL</div><h1>Konaklama</h1>"
    pages = [p1]
    if two:
        pages += [head + hotel_block("strat", "Las Vegas · 5–9 Ocak · 4 gece") + hotel_block("dt", "Los Angeles · 9–11 Ocak · 2 gece"),
                  "<div class=kick>UÇUŞ VE ÜCRET</div><h1>Uçuş ve Tur Ücreti</h1>" + price]
    else:
        pages += [head.replace("<h1>Konaklama</h1>", "<h1>Konaklama ve Tur Ücreti</h1>") + hotel_block("strat", "Las Vegas · 5–9 Ocak · 4 gece") + price]
    pages.append(CITY_LV.replace("{sights}", sights(LV_S)))
    if two: pages.append(CITY_LA.replace("{sights}", sights(LA_S)))
    pages.append(form(t))
    html = f"<!doctype html><meta charset=utf-8><title>{t['title']}</title><style>{CSS}</style>" + "".join(page(t, b, i + 1, len(pages)) for i, b in enumerate(pages))
    (H / f"{name}.html").write_text(html, encoding="utf8")
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{H}/{name}.html');await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map(pg=>{{const bd=pg.querySelector('.bd');const ft=pg.querySelector('.ft');return Math.round(bd.getBoundingClientRect().bottom-ft.getBoundingClientRect().top)}}));
console.log('sayfa taşması (px, <0 iyi):',JSON.stringify(over));
await p.pdf({{path:'{H}/{name}.pdf',format:'A4',printBackground:true}});await b.close()}})()"""
    r = subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd=str(H)); print(name, r.stdout.strip() or r.stderr[-300:])

for n, t in TOURS.items(): build(n, t)
