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
D2 = ("2. GÜN", "6 Ocak Çarşamba", "<b>CES 1. gün.</b> Las Vegas Convention Center'da fuar ziyareti, yaka kartlarının alınması ve firma görüşmeleri.")
D3 = ("3.–4. GÜN", "7–8 Ocak Perşembe–Cuma", "<b>CES 2. ve 3. gün.</b> Tam gün fuar ziyareti: The Venetian'daki sergi alanları ve girişimlere ayrılan Eureka Park. Akşamlar serbest.")

TOURS = {
 "CES-Las-Vegas-2027-4-Gece-Fuar-Turu": dict(
  short="CES Las Vegas 2027 · 4 gece", kick="4 GECE · 5 – 10 OCAK 2027", title="CES Las Vegas 2027 Fuar Turu",
  sub="Dünyanın en büyük tüketici teknolojileri fuarı · THY ile Los Angeles'a direkt uçuş · Las Vegas'ta fuara yakın otel",
  days=[D1, D2, D3,
   ("5. GÜN", "9 Ocak Cumartesi", "<b>Las Vegas – Los Angeles – İstanbul.</b> Sabah odaların boşaltılması ve kara yoluyla Los Angeles Havalimanı'na transfer (yaklaşık 4,5 saat; bu gün fuar ziyareti yoktur). <b>18:30</b> THY <b>TK10</b> ile İstanbul'a direkt uçuş."),
   ("6. GÜN", "10 Ocak Pazar", "<b>İstanbul.</b> 18:55 İstanbul Havalimanı'na varış ve turumuzun sonu.")],
  stay="4 gece Las Vegas", hotel=[("Las Vegas · 5–9 Ocak (4 gece)", "Fuara yakın otel")],
  ret="Dönüş TK10 · 9 Ocak Cumartesi 18:30 → 10 Ocak Pazar 18:55", per="4 gece, kişi başı",
  inc=["THY ile İstanbul – Los Angeles – İstanbul direkt uçak bileti (TK9 / TK10, 23 kg bagaj) ve havalimanı vergileri",
       "Las Vegas'ta fuara yakın otelde 4 gece konaklama", "Los Angeles Havalimanı – Las Vegas oteli – Los Angeles Havalimanı transferleri"],
  cities=["lv"]),
 "CES-Las-Vegas-2027-6-Gece-Las-Vegas-Los-Angeles-Turu": dict(
  short="CES 2027 · 6 gece Las Vegas + Los Angeles", kick="6 GECE · 5 – 12 OCAK 2027", title="CES 2027 Las Vegas + Los Angeles Turu",
  sub="4 gece Las Vegas (CES) + 2 gece Los Angeles · THY ile Los Angeles'a direkt uçuş · panoramik şehir turu ve alışveriş turu",
  days=[D1, D2, D3,
   ("5. GÜN", "9 Ocak Cumartesi", "<b>CES son gün / Las Vegas – Los Angeles.</b> Sabah son fuar ziyaretleri. Öğleden sonra kara yoluyla Los Angeles'a geçiş (yaklaşık 4,5 saat), otele yerleşme."),
   ("6. GÜN", "10 Ocak Pazar", "<b>Los Angeles panoramik tur.</b> Hollywood Bulvarı ve Şöhretler Kaldırımı, Hollywood yazısı manzarası, Beverly Hills ve Rodeo Drive, Santa Monica sahili."),
   ("7. GÜN", "11 Ocak Pazartesi", "<b>Alışveriş turu / Los Angeles – İstanbul.</b> Odaların boşaltılması ve outlet alışveriş turu. Öğleden sonra havalimanına transfer, <b>18:30</b> THY <b>TK10</b> ile İstanbul'a direkt uçuş."),
   ("8. GÜN", "12 Ocak Salı", "<b>İstanbul.</b> 18:55 İstanbul Havalimanı'na varış ve turumuzun sonu.")],
  stay="4 gece Las Vegas + 2 gece Los Angeles", hotel=[("Las Vegas · 5–9 Ocak (4 gece)", "Fuara yakın otel"), ("Los Angeles · 9–11 Ocak (2 gece)", "Şehir oteli")],
  ret="Dönüş TK10 · 11 Ocak Pazartesi 18:30 → 12 Ocak Salı 18:55", per="6 gece, kişi başı",
  inc=["THY ile İstanbul – Los Angeles – İstanbul direkt uçak bileti (TK9 / TK10, 23 kg bagaj) ve havalimanı vergileri",
       "Las Vegas'ta fuara yakın otelde 4 gece konaklama", "Los Angeles'ta 2 gece konaklama",
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

def page(t, body, n, total):
    return f"""<div class=page><div class=hd><img src="assets/logo-on-dark.png"><div><b>{t['short']}</b><br>fuartour.com · 0850 255 58 58</div></div>
<div class=draft>TASLAK</div><div class=bd>{body}</div>
<div class=ft><span><b>Fuartour</b> · Fuar ve iş seyahati organizasyonu</span><span>fuartour.com · 0850 255 58 58</span><span>{n} / {total}</span></div></div>"""

def build(name, t):
    days = "".join(f"<div class=day><div class=d><span class=n>{a}</span><b>{b}</b></div><p>{c}</p></div>" for a, b, c in t["days"])
    p1 = f"""<div class=top><img src="assets/ces-logo.jpg"><div><div class=kick>{t['kick']}</div><h1>{t['title']}</h1><div class=sub>{t['sub']}</div></div></div>
<div class=ph><img src="assets/ces-2026.jpg"><img src="assets/ces-2026-1.jpg"><img src="assets/ces-2026-2.jpg"></div>
<h2>Fuar Bilgileri</h2>{FAIR_KV}<h2>Gün Gün Program</h2>{days}"""
    hotels = "".join(f"<div><span>{a}</span><b>{b} <span class=tbd style='width:auto'>– otel adı belirlenecek</span></b></div>" for a, b in t["hotel"])
    p2 = f"""<div class=kick>KONAKLAMA · {t['stay'].upper()}</div><h1>Konaklama ve Tur Ücreti</h1>
<h2>Konaklama</h2><div class=kv style="grid-template-columns:1fr">{hotels}</div>
<h2>Uçuş ve Tur Ücreti <small>· {t['per']}</small></h2>
<div class=fl><div><b>Gidiş TK9</b> · 5 Ocak Salı 13:50 → 16:35 (İstanbul – Los Angeles, direkt)</div><div><b>{t['ret'].split(' · ')[0]}</b> · {t['ret'].split(' · ')[1]} (Los Angeles – İstanbul, direkt)</div></div>
<div class=pr><div><span>Çift kişilik odada kişi başı</span><b class=tbd>belirlenecek</b> <i>USD</i></div><div><span>Tek kişilik odada</span><b class=tbd>belirlenecek</b> <i>USD</i></div></div>
<div class=two><div><h2>Fiyata Dahil Hizmetler</h2><ul>{''.join(f'<li>{x}</li>' for x in t['inc'])}</ul></div>
<div><h2>Fiyata Dahil Olmayanlar</h2><ul class=x>{''.join(f'<li>{x}</li>' for x in EXC)}</ul></div></div>"""
    p3 = f"<div class=kick>ŞEHİR REHBERİ</div><h1>{' ve '.join('Las Vegas' if c=='lv' else 'Los Angeles' for c in t['cities'])}</h1>" + "".join(CITY[c] for c in t["cities"]) + TIPS
    html = f"<!doctype html><meta charset=utf-8><title>{t['title']}</title><style>{CSS}</style>" + page(t, p1, 1, 3) + page(t, p2, 2, 3) + page(t, p3, 3, 3)
    (H / f"{name}.html").write_text(html, encoding="utf8")
    js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage();
await p.goto('file://{H}/{name}.html');await p.evaluate(()=>document.fonts.ready);
const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map(pg=>{{const bd=pg.querySelector('.bd');const ft=pg.querySelector('.ft');return Math.round(bd.getBoundingClientRect().bottom-ft.getBoundingClientRect().top)}}));
console.log('overflow(px, <0 iyi):',JSON.stringify(over));
await p.pdf({{path:'{H}/{name}.pdf',format:'A4',printBackground:true}});await b.close()}})()"""
    print(name, subprocess.run(["node", "-e", js], capture_output=True, text=True, cwd=str(H)).stdout.strip() or "hata")

for n, t in TOURS.items(): build(n, t)
