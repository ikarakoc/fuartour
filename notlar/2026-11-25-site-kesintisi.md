# 25.11.2026 – Site kesintisi (500 / 404)

- Belirti: önbellekte olmayan tüm sayfalar, wp-admin ve REST API 500 "ciddi sorun" hatası veriyordu.
- Neden: `u250001132_fuartourdb` veritabanı kullanıcısının sunucudaki yetkileri kaybolmuştu. SHOW GRANTS yalnızca
  `DELETE HISTORY, SHOW CREATE ROUTINE` gösteriyordu; hPanel ise "Tam erişim" gösteriyordu. İlk çöken MailPoet oldu
  (SELECT denied → yakalanmamış hata); geri kalan sorgular sessizce boş döndüğü için sayfalar 404 verdi.
- Çözüm: hPanel → Veritabanları → u250001132_fuartourdb → Erişim → Değiştir → Tam erişim → Kaydet (kullanıcı yaptı).
  Ardından Memcached nesne önbelleği temizlendi (kesintide kaydedilen boş sonuçlar anasayfayı 404 yapıyordu) ve sunucu önbelleği temizlendi.
- Geçici adımlar geri alındı: MailPoet klasörü eski adına döndü (aktif), mu-plugins altındaki teşhis dosyaları ve loglar silindi.
- Tekrarlarsa: hata kaydı için mu-plugin ile `error_get_last()` yazdır; `SHOW GRANTS` kontrol et; yetkileri hPanel'den yeniden kaydet; `wp_cache_flush()`.
