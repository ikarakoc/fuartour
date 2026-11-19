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

## v2 (19.11.2026) — görseller, müzik, seslendirme
- Kullanıcı onayı: Higgsfield ile üretim (~6,1 kredi): 5 arka plan görseli (gpt_image_2_6), müzik (ElevenLabs Music v2.5, enstrümantal), seslendirme (ElevenLabs, kadın ses "Maya").
- Seslendirme metni: "CES 2027 geliyor. Altmışıncı yılında, 6–9 Ocak'ta Las Vegas'ta. Yapay zekâ, robotik, mobilite, dijital sağlık, akıllı ev. Uçuş, otel, transfer ve Amerika vizesi desteği Fuartour'da. Detaylar fuartour.com'da."
- Sahneler seslendirmeye göre yeniden zamanlandı: 0–3,2 / 3,2–7,2 / 7,2–12,7 / 12,7–17,0 + kapanış kartı; toplam 19,6 sn.
- Videoya özel kompozisyon `reels/src/ReelCes2027.tsx`: kit sahneleri + tam ekran görseller, %66 lacivert karartma.
- Miks: müzik sesin 13 dB altında, parçanın vuruşu kapanış kartına (17,0 sn) denk; master −13,9 LUFS, tepe −2,3 dBFS. Ses efektleri kaldırıldı.
- Çıktı: `ces-2027-reels-v2.mp4`. Kaynaklar: `media/`.
- Ortam: Higgsfield dosyaları için kişisel "fuartour" ortamı oluşturuldu (d8j0ntlcm91z4.cloudfront.net izinli).

## Açık konular (v2)
- Görseller yapay zekâ üretimi ve temsilî; gerçek CES fotoğrafı değil. İlk görsel Las Vegas'ı andırıyor.
- Üretilen müzik ve sesin ticari kullanım koşulları Higgsfield/ElevenLabs plan şartlarından teyit edilecek.
- Seslendirmenin Türkçe telaffuzu dinlenerek kontrol edilmedi (otomatik yazıya döküm kurulu değil).

## v3 (19.11.2026) — Türkçe seslendirme yenilendi
- Geri bildirim: v2 seslendirmesinin Türkçesi çok kötü (İngilizce hazır ses, aksanlı).
- Yeni ses: vidIQ üzerinden ElevenLabs "Gökçe Deniz" (anadili Türkçe, İstanbul aksanı), 28 vidIQ kredisi. "CES" okunuşu: "si-i-es" (kullanıcı seçimi).
- Okunuş için metin fonetik yazıldı: "Si i es iki bin yirmi yedi geliyor! … Fuartur'da. Detaylar, fuartur nokta kom'da."
- Cümleler arasına kısa nefes payı eklendi (`media/vo-tr-timed.wav`); sahneler 0–3,0 / 3,0–7,2 / 7,2–12,5 / 12,5–17,1 + kart; toplam 19,7 sn.
- Çıktı: `ces-2027-reels-v3.mp4` (−14,0 LUFS, tepe −2,4 dBFS).
- Açık: liste maddelerinin sese denk gelişi duraklamalardan tahmin edildi; telaffuz dinlenerek doğrulanmadı.
