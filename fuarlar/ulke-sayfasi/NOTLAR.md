# Ülke fuar listesi sayfası (22.11.2026)

- Ana sayfa (231) "En İyi Destinasyonlar" kutuları artık /ulkeler/<slug>/ (vize sayfası) yerine filtreli listeye gidiyor: /fuarlar/ulke-<slug>/ (Fuarlar sayfası 16904 + Filter Everything; şehir ve sektör filtreleri hazır).
- Code Snippets 42 "Ülke fuar listesi: tanıtım kutusu ve ay filtresi (ulke_tanitim)" eklendi ve etkin: kaynak `ulke-tanitim-snippet.php`.
  - [ulke_tanitim] kısa kodu 16904'teki boş c9dffdd kapsayıcısına eklendi (widget a7c41e2).
  - Metin: ülke teriminin açıklamasının ilk iki cümlesi (Hong Kong'da açıklama vize ile başladığı için özel metin).
  - Sayaçlar: toplam fuar (terim sayısı) ve önümüzdeki 12 ayda başlayan fuarlar (veritabanından, 6 saat önbellek).
  - Ay filtresi: ?ay=YYYY-MM, ft_tarih sorgusuna başlangıç tarihi aralığı ekler; sonsuz kaydırmada korunuyor.
- Çin ve Hong Kong: /fuarlar/ulke-cin-fuarlari/ ve /fuarlar/ulke-hong-kong-fuarlari/ Redirection eklentisiyle /cin-fuarlari/ ve /hong-kong-fuarlari/ sayfalarına yönleniyor (dokunulmadı).
- Yedekler: fuarlar-16904-yedek-2026-11-22.json, fuarlar-16904-sayfa-ayarlari-yedek.json, anasayfa-231-yedek-2026-11-22.json.
- Geri alma: snippet 42'yi pasifleştir; 16904'ten a7c41e2'yi kaldır; 231'de kutu bağlantılarını /ulkeler/<slug>/ yap.
