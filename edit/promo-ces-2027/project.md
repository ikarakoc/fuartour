# promo-ces-2027 — CES 2027 Reels tanıtımı (footage'sız, "yalnızca sahneler")

## Oturum
- 19.11.2026 — ilk taslak. Marka: fuartour (ton: tech, stil: Brand, sahne tonu: feature).

## Brief (kullanıcı yanıtları)
- Ton: Tech. CTA: site ("fuartour.com" / "CES 2027 turu ve ABD vizesi için"), kapanış kartında logo ile.
- İçerik: tarih ve yer, öne çıkan temalar, Fuartour hizmetleri (2026 rakamları seçilmedi).
- Ses: ses efektleri (kodla üretilen tonlar, `sfx/`); müzik gömülmedi.

## Kurgu (20,6 sn, 1080×1920, 30 fps)
1. 0,0–3,0 kanca: "CES 2027 geliyor"
2. 3,0–7,0 sayı: "60. yıl" + "6–9 Ocak 2027 / Las Vegas"
3. 7,0–12,6 liste: CES'te öne çıkanlar — Yapay zekâ, Robotik, Mobilite, Dijital sağlık, Akıllı ev
4. 12,6–18,0 liste: Fuartour ile — Uçuş, Otel, Transfer, ABD vizesi desteği
5. 18,0–20,6 kapanış kartı: logo, slogan, fuartour.com

## Kararlar
- Kanca "CES 2027'ye hazır mısınız?" yerine "CES 2027 geliyor": plan denetimi Türkçe harfleri kelime ayırıcı sayıyor.
- Rubik yerel dosyadan yükleniyor (render tarayıcısı Google Fonts'a erişemiyor): `brands/fuartour/assets/fonts/`.
- Render: `npx remotion render ReelKit … --browser-executable=<chrome-headless-shell>` (bu ortamda Remotion kendi tarayıcısını indiremiyor).
- Kapak 0. kareye gömülmedi (poster.py bake denetimi geçmedi); kapak `cover.jpg` olarak ayrı ve dosyaya küçük resim olarak ekli.

## Açık konular (teyit)
- CES 2027 için yayında tur paketi yok (sitede yalnızca 2026 turu); videoda fiyat/otel/uçuş ayrıntısı verilmedi.
- "Uçuş, otel, transfer, ABD vizesi desteği" genel hizmet olarak anasayfadan alındı; CES 2027 paketinde geçerliliği teyit edilecek.
- Tarih (6–9 Ocak 2027), 60. yıl ve temalar fuartour.com CES sayfasından; resmi kaynakla son kontrol.
- Logo 330 px PNG'den büyütüldü; vektör/yüksek çözünürlüklü özgün dosya gerekli.
- Koyu lacivert #16213E ve turuncu #FF5722 siteden alındı; resmi marka renkleri teyit edilecek.
