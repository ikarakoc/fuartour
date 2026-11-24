# Fuartour Özel Tur Talebi (24.11.2026)

- Eklenti: `wp-content/plugins/fuartour-ozel-tur-talebi/` (etkin, sürüm 1.1.3). Hostinger dosya yükleme + "Deploy WordPress plugin" ile kuruldu.
- Fuar sayfasında (fuarlar) form sayfa sonuna gizli basılır; betik onu "Fuara Ait Turlar" sekmesine, devre sekmelerinin (3327950) arkasına taşır. Sekmede tur kartı (.e-loop-item) varsa form kaldırılır.
  - Elementor bileşen önbelleği tek fuar şablonunun çıktısını fuarlar arasında paylaştığı için form Elementor bileşenine eklenmiyor (1.0.x'te bu yüzden ilk fuarın ID'si tüm sayfalara gitmişti; 1.1.0 ilk yüklemede `_elementor_element_cache` ve LiteSpeed önbelleğini bir kez temizledi).
- Kısa kod: `[fuartour_ozel_tur_formu fuar="ID"]` (sekme dışında kullanmak için).
- reCAPTCHA v2: varsayılan olarak Elementor Pro'nun anahtarları (elementor_pro_recaptcha_site_key / _secret_key). Panel: Özel Tur Talepleri → Ayarlar'dan ayrı anahtar ve bildirim adresi girilebilir.
- Kayıtlar: wp-admin → Özel Tur Talepleri (ft_tur_talebi, herkese kapalı). Bildirim: info@fuartour.com (Reply-To müşteri).
- Koruma: bal küpü alanı, IP başına 10 dakikada 5 talep, sunucu tarafı alan doğrulaması.
- Geri alma: Eklentiler'den "Fuartour Özel Tur Talebi"ni devre dışı bırak.
- 1.1.3: "Bağlantı hatası" düzeltildi. Formdaki gizli `action` alanı yüzünden `form.action` adres yerine alanı döndürüyordu; istek geçersiz yola gidip 404 alıyordu. Artık `getAttribute('action')` kullanılıyor. Yanıt tamponlanıyor (başka eklentilerin uyarıları JSON'u bozmasın).
- Teknik hata günlüğü: `wp-content/uploads/ftot-gunluk.log` (reCAPTCHA reddi, beklenmeyen çıktı, e-posta hatası; kişisel veri yazılmaz).
