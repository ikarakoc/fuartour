# 25.11.2026 – WordPress denetimi ve temizlik (kullanıcı onayıyla)

## Silinen dosyalar (Hostinger dosya yöneticisi API'si)
- wp-content: 2.250 boş `temp-write-test-*` dosyası
- themes/mytravel.zip, themes/mytravel(eski).zip, plugins/codecanyon-…filter-everything….zip (~21 MB)
- wp-content/debug.log (Tem 2025), kök error_log (Eki 2026)
- .htaccess.agent-bak-* (3), .htaccess.bk
- Eski oturum iş kayıtları: fuartour-cin-*, fuartour-hk-*, fuartour-logo-log, fuartour-webp-log, fuartour-perf-log
- uploads/wpallimport, uploads/smack_uci_uploads (Nisan 2025 içe aktarma artıkları)
- Boş klasörler: ai1wm-backups, lc-migrator-backups, upgrade-temp-backup

## Sayfalar
- Çöp kutusuna: 27352 (Fuar Turları TEST), 26907 (Fuar Rehberi TASLAK), 26890 (Anasayfa TASLAK), 27356 (Fuar Turları YEDEK)
- Taslağa: 28674 (CIFF mail şablonu, herkese açıktı)

## Güncellemeler
- Elementor + Elementor Pro 4.4.0 → 4.4.2, Yoast SEO 28.8 → 28.9 (güvenlik açıkları). Güncelleme sırasında ~2 dk 521 kesintisi oldu.

## Dokunulmayanlar / açık konular
- Aynı gün başka bir oturum çalışıyordu: mu-plugins/fuartour-404.php, fuartour-llms-cache.php, .htaccess.claude-bak-20261125185205, fuartour-404-prof.json, fuartour-htaccess-llms-log.json — onun dosyaları, dokunulmadı.
- Şüpheli üyelikler (Eki–Kas yabancı "customer" hesapları, "Implement Employee Feedback Software" spam) — karar kullanıcıda.
- Pasif eklentiler: Post SMTP, Easy WP SMTP, AI Provider for Anthropic — kaldırılmadı.
- wp-content/db.php: localhost bağlantısı tutmazsa uzak MySQL'e geçen bağlantı koruması (drop-in), bilerek duruyor.
