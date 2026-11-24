<?php
/**
 * Plugin Name: Fuartour Özel Tur Talebi
 * Description: Fuar sayfasında "Fuara Ait Turlar" sekmesinde aktif tur yoksa özel paket tur talep formu gösterir. Talepler "Özel Tur Talepleri" menüsünde saklanır ve e-posta ile bildirilir. reCAPTCHA v2 korumalı. Kısa kod: [fuartour_ozel_tur_formu]
 * Version: 1.1.0
 * Author: Fuartour
 * Text Domain: fuartour-ozel-tur
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

define( 'FTOT_VERSION', '1.1.0' );
define( 'FTOT_CPT', 'ft_tur_talebi' );
define( 'FTOT_OPT', 'ftot_ayarlar' );

/* -------------------------------------------------------------------------
 * Ayarlar
 * ---------------------------------------------------------------------- */

function ftot_ayarlar() {
	$v = get_option( FTOT_OPT, array() );
	return wp_parse_args( is_array( $v ) ? $v : array(), array(
		'bildirim'   => 'info@fuartour.com',
		'site_key'   => '',
		'secret_key' => '',
	) );
}

/** Kendi anahtar girilmediyse Elementor Pro'nun reCAPTCHA (v2) anahtarları kullanılır. */
function ftot_site_key() {
	$a = ftot_ayarlar();
	return $a['site_key'] ? $a['site_key'] : (string) get_option( 'elementor_pro_recaptcha_site_key', '' );
}

function ftot_secret_key() {
	$a = ftot_ayarlar();
	return $a['secret_key'] ? $a['secret_key'] : (string) get_option( 'elementor_pro_recaptcha_secret_key', '' );
}

/** Alan tanımları: anahtar => [etiket, seçenekler]. */
function ftot_secimler() {
	$eh = array( 'evet' => 'Evet', 'hayir' => 'Hayır' );
	return array(
		'ucus_tipi'   => array( 'Uçuş tipi', array( 'direkt' => 'Direkt', 'aktarmali' => 'Aktarmalı' ) ),
		'kabin'       => array( 'Kabin sınıfı', array( 'ekonomi' => 'Ekonomi', 'business' => 'Business' ) ),
		'otel_yildiz' => array( 'Otel sınıfı', array( '5' => '5 yıldız', '4' => '4 yıldız' ) ),
		'otel_konum'  => array( 'Otel konumu', array( 'fuara-yakin' => 'Fuara yakın', 'sehir-merkezi' => 'Şehir merkezinde' ) ),
		'vize'        => array( 'Vize ihtiyacınız var mı?', $eh ),
		'transfer_ha' => array( 'Havalimanı – otel – havalimanı transferleri', $eh ),
		'transfer_fu' => array( 'Otel – fuar – otel transferleri', $eh ),
		'rehber'      => array( 'Rehberlik', $eh ),
		'giris_karti' => array( 'Fuar giriş kartı', $eh ),
	);
}

add_action( 'admin_menu', function () {
	add_submenu_page(
		'edit.php?post_type=' . FTOT_CPT,
		'Özel Tur Talebi Ayarları',
		'Ayarlar',
		'manage_options',
		'ftot-ayarlar',
		'ftot_ayar_sayfasi'
	);
} );

function ftot_ayar_sayfasi() {
	if ( ! current_user_can( 'manage_options' ) ) {
		return;
	}
	if ( isset( $_POST['ftot_kaydet'] ) && check_admin_referer( 'ftot_ayar' ) ) {
		$a             = ftot_ayarlar();
		$bildirim      = array_filter( array_map( 'trim', explode( ',', sanitize_text_field( wp_unslash( $_POST['bildirim'] ?? '' ) ) ) ), 'is_email' );
		$a['bildirim'] = implode( ', ', $bildirim );
		$a['site_key'] = sanitize_text_field( wp_unslash( $_POST['site_key'] ?? '' ) );
		$sk            = sanitize_text_field( wp_unslash( $_POST['secret_key'] ?? '' ) );
		if ( '' !== $sk ) {
			$a['secret_key'] = $sk;
		}
		if ( ! empty( $_POST['secret_sil'] ) ) {
			$a['secret_key'] = '';
		}
		update_option( FTOT_OPT, $a, false );
		echo '<div class="notice notice-success"><p>Kaydedildi.</p></div>';
	}
	$a = ftot_ayarlar();
	?>
	<div class="wrap">
		<h1>Özel Tur Talebi Ayarları</h1>
		<form method="post">
			<?php wp_nonce_field( 'ftot_ayar' ); ?>
			<table class="form-table">
				<tr><th><label for="bildirim">Bildirim e-postası</label></th>
					<td><input type="text" class="regular-text" id="bildirim" name="bildirim" value="<?php echo esc_attr( $a['bildirim'] ); ?>">
					<p class="description">Birden fazla adresi virgülle ayırın.</p></td></tr>
				<tr><th><label for="site_key">reCAPTCHA v2 site anahtarı</label></th>
					<td><input type="text" class="regular-text" id="site_key" name="site_key" value="<?php echo esc_attr( $a['site_key'] ); ?>">
					<p class="description">Boş bırakılırsa Elementor → Ayarlar → Entegrasyonlar'daki reCAPTCHA anahtarı kullanılır<?php echo get_option( 'elementor_pro_recaptcha_site_key' ) ? ' (tanımlı)' : ' (tanımlı değil)'; ?>.</p></td></tr>
				<tr><th><label for="secret_key">reCAPTCHA v2 gizli anahtar</label></th>
					<td><input type="password" class="regular-text" id="secret_key" name="secret_key" value="" autocomplete="off" placeholder="<?php echo $a['secret_key'] ? '•••••• kayıtlı' : ''; ?>">
					<?php if ( $a['secret_key'] ) : ?><label><input type="checkbox" name="secret_sil" value="1"> Kayıtlı anahtarı sil</label><?php endif; ?>
					<p class="description">Boş bırakılırsa Elementor'daki gizli anahtar kullanılır<?php echo get_option( 'elementor_pro_recaptcha_secret_key' ) ? ' (tanımlı)' : ' (tanımlı değil)'; ?>.</p></td></tr>
			</table>
			<p><button class="button button-primary" name="ftot_kaydet" value="1">Kaydet</button></p>
		</form>
	</div>
	<?php
}

add_action( 'admin_notices', function () {
	if ( current_user_can( 'manage_options' ) && ( ! ftot_site_key() || ! ftot_secret_key() ) ) {
		echo '<div class="notice notice-warning"><p><strong>Özel Tur Talebi:</strong> reCAPTCHA anahtarları tanımlı değil; form gönderimleri reddedilir. <a href="' . esc_url( admin_url( 'edit.php?post_type=' . FTOT_CPT . '&page=ftot-ayarlar' ) ) . '">Ayarlar</a></p></div>';
	}
} );

/* -------------------------------------------------------------------------
 * Kayıt türü: Özel Tur Talepleri
 * ---------------------------------------------------------------------- */

add_action( 'init', function () {
	register_post_type( FTOT_CPT, array(
		'labels'          => array(
			'name'               => 'Özel Tur Talepleri',
			'singular_name'      => 'Özel Tur Talebi',
			'menu_name'          => 'Özel Tur Talepleri',
			'all_items'          => 'Tüm Talepler',
			'edit_item'          => 'Talep',
			'search_items'       => 'Talep ara',
			'not_found'          => 'Talep yok.',
			'not_found_in_trash' => 'Çöp kutusunda talep yok.',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'show_in_rest'    => false,
		'menu_position'   => 26,
		'menu_icon'       => 'dashicons-email-alt',
		'supports'        => array( 'title' ),
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
	) );
} );

add_filter( 'manage_' . FTOT_CPT . '_posts_columns', function ( $c ) {
	return array(
		'cb'         => $c['cb'],
		'title'      => 'Talep',
		'ftot_fuar'  => 'Fuar',
		'ftot_eposta'=> 'E-posta',
		'ftot_tel'   => 'Telefon',
		'ftot_kisi'  => 'Kişi',
		'date'       => 'Tarih',
	);
} );

add_action( 'manage_' . FTOT_CPT . '_posts_custom_column', function ( $col, $id ) {
	switch ( $col ) {
		case 'ftot_fuar':
			$f = (int) get_post_meta( $id, 'fuar_id', true );
			echo $f ? '<a href="' . esc_url( get_permalink( $f ) ) . '" target="_blank">' . esc_html( get_the_title( $f ) ) . '</a>' : '—';
			break;
		case 'ftot_eposta':
			$e = get_post_meta( $id, 'eposta', true );
			echo '<a href="mailto:' . esc_attr( $e ) . '">' . esc_html( $e ) . '</a>';
			break;
		case 'ftot_tel':
			echo esc_html( get_post_meta( $id, 'telefon', true ) );
			break;
		case 'ftot_kisi':
			echo esc_html( get_post_meta( $id, 'katilimci', true ) );
			break;
	}
}, 10, 2 );

add_action( 'add_meta_boxes_' . FTOT_CPT, function () {
	add_meta_box( 'ftot_detay', 'Talep ayrıntıları', function ( $post ) {
		echo ftot_ozet_tablosu( $post->ID ); // phpcs:ignore -- içerik ftot_ozet_tablosu içinde kaçışlandı.
	}, FTOT_CPT, 'normal', 'high' );
} );

/** Talebin HTML özet tablosu (yönetim ekranı ve e-posta için). */
function ftot_ozet_tablosu( $id ) {
	$f     = (int) get_post_meta( $id, 'fuar_id', true );
	$satir = array(
		'Fuar'          => $f ? '<a href="' . esc_url( get_permalink( $f ) ) . '">' . esc_html( get_the_title( $f ) ) . '</a>' : '—',
		'Ad soyad'      => esc_html( get_post_meta( $id, 'ad_soyad', true ) ),
		'E-posta'       => '<a href="mailto:' . esc_attr( get_post_meta( $id, 'eposta', true ) ) . '">' . esc_html( get_post_meta( $id, 'eposta', true ) ) . '</a>',
		'Telefon'       => esc_html( get_post_meta( $id, 'telefon', true ) ),
		'Katılımcı sayısı' => esc_html( get_post_meta( $id, 'katilimci', true ) ),
	);
	foreach ( ftot_secimler() as $k => $tanim ) {
		$v              = get_post_meta( $id, $k, true );
		$satir[ $tanim[0] ] = esc_html( $tanim[1][ $v ] ?? '—' );
	}
	$diger = get_post_meta( $id, 'diger', true );
	$satir['Talep edilen diğer hizmetler'] = $diger ? nl2br( esc_html( $diger ) ) : '—';

	$h = '<table style="border-collapse:collapse;width:100%;max-width:640px;font:14px/1.5 Arial,sans-serif">';
	foreach ( $satir as $k => $v ) {
		$h .= '<tr><th style="text-align:left;vertical-align:top;padding:7px 10px;border:1px solid #e5e7eb;background:#f9fafb;width:42%">' . esc_html( $k ) . '</th><td style="padding:7px 10px;border:1px solid #e5e7eb">' . $v . '</td></tr>';
	}
	return $h . '</table>';
}

/* -------------------------------------------------------------------------
 * Form
 * ---------------------------------------------------------------------- */

function ftot_form_html( $fuar_id = 0, $kontrol = false ) {
	$fuar_id = $fuar_id ? (int) $fuar_id : (int) get_the_ID();
	$uid     = 'ftot-' . wp_rand( 1000, 999999 );
	$secim   = ftot_secimler();
	$radyo   = function ( $k ) use ( $secim, $uid ) {
		$h = '<fieldset class="ftot-grup"><legend>' . esc_html( $secim[ $k ][0] ) . ' <span class="ftot-z">*</span></legend><div class="ftot-secenek">';
		foreach ( $secim[ $k ][1] as $v => $et ) {
			$h .= '<label><input type="radio" name="' . esc_attr( $k ) . '" value="' . esc_attr( $v ) . '" required> <span>' . esc_html( $et ) . '</span></label>';
		}
		return $h . '</div></fieldset>';
	};

	ob_start();
	ftot_css();
	?>
	<div class="ftot" id="ozel-tur-talebi"<?php echo $kontrol ? ' hidden' : ''; ?>>
		<div class="ftot-baslik">
			<h3>Size özel paket tur hazırlayalım</h3>
			<p>Bu fuar için henüz turumuz bulunmamaktadır. Size özel paket tur oluşturmak için lütfen aşağıdaki bilgileri doldurup iletiniz.</p>
		</div>
		<form class="ftot-form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" novalidate>
			<input type="hidden" name="action" value="ftot_gonder">
			<input type="hidden" name="fuar_id" value="<?php echo esc_attr( $fuar_id ); ?>">
			<div class="ftot-hp" aria-hidden="true"><label>Web sitesi <input type="text" name="web_sitesi" tabindex="-1" autocomplete="off"></label></div>

			<div class="ftot-satir ftot-3">
				<label>Ad soyad <span class="ftot-z">*</span><input type="text" name="ad_soyad" maxlength="100" autocomplete="name" required></label>
				<label>E-posta <span class="ftot-z">*</span><input type="email" name="eposta" maxlength="120" autocomplete="email" required></label>
				<label>Telefon <span class="ftot-z">*</span><input type="tel" name="telefon" maxlength="25" autocomplete="tel" placeholder="05xx xxx xx xx" required></label>
			</div>
			<div class="ftot-satir ftot-3">
				<label>Katılımcı sayısı <span class="ftot-z">*</span><input type="number" name="katilimci" min="1" max="500" step="1" inputmode="numeric" required></label>
			</div>

			<div class="ftot-blok"><h4>Uçak tercihi</h4><div class="ftot-satir ftot-2"><?php echo $radyo( 'ucus_tipi' ) . $radyo( 'kabin' ); // phpcs:ignore ?></div></div>
			<div class="ftot-blok"><h4>Otel tercihi</h4><div class="ftot-satir ftot-2"><?php echo $radyo( 'otel_yildiz' ) . $radyo( 'otel_konum' ); // phpcs:ignore ?></div></div>
			<div class="ftot-blok"><h4>Hizmetler</h4><div class="ftot-satir ftot-2">
				<?php foreach ( array( 'vize', 'transfer_ha', 'transfer_fu', 'rehber', 'giris_karti' ) as $k ) { echo $radyo( $k ); } // phpcs:ignore ?>
			</div></div>

			<label class="ftot-tam">Talep ettiğiniz diğer hizmetler<textarea name="diger" rows="4" maxlength="2000" placeholder="Ör. tercih ettiğiniz tarihler, kalkış şehri, ek geceleme, tercüman, stand ziyareti…"></textarea></label>

			<div class="ftot-alt">
				<div class="ftot-captcha" id="<?php echo esc_attr( $uid ); ?>-rc" data-sitekey="<?php echo esc_attr( ftot_site_key() ); ?>"></div>
				<button type="submit" class="ftot-gonder">Gönder</button>
			</div>
			<p class="ftot-mesaj" role="status" aria-live="polite"></p>
			<p class="ftot-not">Bilgileriniz yalnızca size teklif hazırlamak ve sizinle iletişime geçmek için kullanılır.</p>
		</form>
	</div>
	<?php if ( $kontrol ) : ?>
	<script>
	/* Formu "Fuara Ait Turlar" sekmesine taşı. Sekmede tur kartı varsa formu kaldır. */
	(function(){
		var f=document.getElementById('ozel-tur-talebi'); if(!f) return;
		var k=<?php echo wp_json_encode( ftot_widget_kimlikleri() ); ?>, liste=null, i;
		for(i=0;i<k.tur_listeleri.length&&!liste;i++){ liste=document.querySelector('[data-id="'+k.tur_listeleri[i]+'"]'); }
		var panel=liste?liste.closest('[role=tabpanel]'):null;
		if(!panel){ [].some.call(document.querySelectorAll('.e-n-tab-title'),function(b){ if(/Fuara Ait Turlar/i.test(b.textContent)){ panel=document.getElementById(b.getAttribute('aria-controls')); return true; } }); }
		if(!panel||panel.querySelector('.e-loop-item')){ f.parentNode.removeChild(f); return; }
		var yer=panel.querySelector('[data-id="'+k.yerlesim+'"]')||liste;
		if(yer&&yer.parentNode){ yer.parentNode.insertBefore(f,yer.nextSibling); } else { panel.appendChild(f); }
		f.hidden=false;
	})();
	</script>
	<?php endif; ?>
	<?php
	ftot_js();
	return ob_get_clean();
}

add_shortcode( 'fuartour_ozel_tur_formu', function ( $atts ) {
	$atts = shortcode_atts( array( 'fuar' => 0 ), $atts );
	return ftot_form_html( (int) $atts['fuar'] );
} );

function ftot_css() {
	static $bitti = false;
	if ( $bitti ) {
		return;
	}
	$bitti = true;
	?>
	<style id="ftot-css">
	.ftot{--o:#ff5722;--k:#1f2430;--g:#6b7280;--c:#e5e7eb;margin:8px 0 24px;padding:24px;border:1px solid #f3e1d8;border-radius:16px;background:linear-gradient(135deg,#fff 0%,#fff7f3 100%);color:var(--k);box-sizing:border-box;width:100%}
	.ftot *{box-sizing:border-box}
	.ftot-baslik h3{margin:0 0 6px;font-size:21px;font-weight:700;color:var(--k)}
	.ftot-baslik p{margin:0 0 18px;color:var(--g);font-size:15px;line-height:1.55}
	.ftot-satir{display:grid;gap:14px 16px;margin-bottom:14px}
	.ftot-3{grid-template-columns:repeat(3,minmax(0,1fr))}
	.ftot-2{grid-template-columns:repeat(2,minmax(0,1fr))}
	.ftot label{display:block;font-size:14px;font-weight:600;color:var(--k)}
	.ftot input[type=text],.ftot input[type=email],.ftot input[type=tel],.ftot input[type=number],.ftot textarea{display:block;width:100%;margin-top:6px;padding:10px 12px;border:1px solid var(--c);border-radius:10px;background:#fff;font:inherit;font-weight:400;font-size:15px;color:var(--k)}
	.ftot input:focus,.ftot textarea:focus{outline:2px solid rgba(255,87,34,.25);border-color:var(--o)}
	.ftot-blok{margin:6px 0 4px}
	.ftot-blok h4{margin:0 0 10px;font-size:16px;font-weight:700;color:var(--k)}
	.ftot-grup{margin:0;padding:12px 14px;border:1px solid var(--c);border-radius:12px;background:#fff;min-width:0}
	.ftot-grup legend{padding:0;margin:0 0 8px;font-size:14px;font-weight:600;float:left;width:100%}
	.ftot-secenek{clear:both;display:flex;flex-wrap:wrap;gap:8px 18px}
	.ftot-secenek label{display:inline-flex;align-items:center;gap:6px;font-weight:400;cursor:pointer}
	.ftot-secenek input{accent-color:var(--o);width:17px;height:17px;margin:0}
	.ftot-tam{margin:4px 0 16px}
	.ftot-z{color:var(--o)}
	.ftot-alt{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:14px}
	.ftot-gonder{background:var(--o);color:#fff;border:0;border-radius:10px;padding:12px 34px;font-size:16px;font-weight:700;cursor:pointer}
	.ftot-gonder:hover{background:#f4511e}
	.ftot-gonder[disabled]{opacity:.6;cursor:wait}
	.ftot-mesaj{margin:12px 0 0;font-size:15px;font-weight:600}
	.ftot-mesaj.hata{color:#b91c1c}
	.ftot-mesaj.ok{color:#15803d}
	.ftot-not{margin:8px 0 0;font-size:12.5px;color:var(--g)}
	.ftot-hp{position:absolute!important;left:-9999px!important;width:1px;height:1px;overflow:hidden}
	.ftot .ftot-hatali{border-color:#dc2626!important}
	.ftot-grup.ftot-hatali{border-color:#dc2626}
	.ftot-tesekkur{padding:18px 0 4px;font-size:16px;line-height:1.6}
	.ftot-tesekkur strong{display:block;font-size:19px;margin-bottom:4px;color:#15803d}
	@media(max-width:767px){.ftot{padding:18px 14px}.ftot-3,.ftot-2{grid-template-columns:1fr}.ftot-gonder{width:100%}}
	</style>
	<?php
}

function ftot_js() {
	static $bitti = false;
	if ( $bitti ) {
		return;
	}
	$bitti = true;
	?>
	<script>
	(function(){
		function hazir(cb){ if(window.grecaptcha&&grecaptcha.render){cb();return;} var t=0,i=setInterval(function(){ if(window.grecaptcha&&grecaptcha.render){clearInterval(i);cb();} else if(++t>200){clearInterval(i);} },100); }
		function yukle(){ if(!document.querySelector('script[src*="recaptcha/api.js"]')){ var s=document.createElement('script'); s.src='https://www.google.com/recaptcha/api.js?render=explicit&hl=tr'; s.async=true; s.defer=true; document.head.appendChild(s);} }
		function kur(form){
			if(form.dataset.kuruldu) return; form.dataset.kuruldu=1;
			var rc=form.querySelector('.ftot-captcha'), wid=null, msg=form.querySelector('.ftot-mesaj'), btn=form.querySelector('.ftot-gonder');
			function ciz(){ if(wid!==null||!rc.dataset.sitekey) return; hazir(function(){ try{ wid=grecaptcha.render(rc,{sitekey:rc.dataset.sitekey,hl:'tr'}); }catch(e){} }); }
			// reCAPTCHA'yı form görünür olduğunda (sekme açıldığında) yükle.
			if('IntersectionObserver' in window){ var io=new IntersectionObserver(function(es){ es.forEach(function(e){ if(e.isIntersecting){ yukle(); ciz(); io.disconnect(); } }); }); io.observe(form); } else { yukle(); ciz(); }
			form.addEventListener('focusin',function(){ yukle(); ciz(); });
			function yaz(t,tur){ msg.textContent=t; msg.className='ftot-mesaj '+(tur||''); }
			form.addEventListener('submit',function(ev){
				ev.preventDefault();
				[].forEach.call(form.querySelectorAll('.ftot-hatali'),function(x){x.classList.remove('ftot-hatali');});
				var eksik=null;
				[].forEach.call(form.querySelectorAll('input[required]:not([type=radio])'),function(x){ if(!x.checkValidity()){ x.classList.add('ftot-hatali'); eksik=eksik||x; } });
				[].forEach.call(form.querySelectorAll('.ftot-grup'),function(g){ if(!g.querySelector('input:checked')){ g.classList.add('ftot-hatali'); eksik=eksik||g; } });
				if(eksik){ yaz('Lütfen işaretli alanları eksiksiz doldurun.','hata'); if(eksik.focus) eksik.focus(); eksik.scrollIntoView({block:'center',behavior:'smooth'}); return; }
				var fd=new FormData(form);
				if(wid!==null){ var tok=grecaptcha.getResponse(wid); if(!tok){ yaz('Lütfen "Ben robot değilim" kutusunu işaretleyin.','hata'); return; } fd.set('g-recaptcha-response',tok); }
				else { yaz('Güvenlik doğrulaması yükleniyor, lütfen birkaç saniye sonra tekrar deneyin.','hata'); yukle(); ciz(); return; }
				fd.set('ajax','1'); btn.disabled=true; yaz('Gönderiliyor…');
				fetch(form.action,{method:'POST',body:fd,credentials:'same-origin'}).then(function(r){return r.json();}).then(function(j){
					if(j&&j.success){ form.innerHTML='<div class="ftot-tesekkur"><strong>Talebiniz alındı, teşekkür ederiz.</strong>'+(j.data&&j.data.mesaj?j.data.mesaj:'')+'</div>'; form.scrollIntoView({block:'center',behavior:'smooth'}); }
					else { yaz((j&&j.data&&j.data.mesaj)||'Gönderilemedi, lütfen tekrar deneyin.','hata'); btn.disabled=false; try{grecaptcha.reset(wid);}catch(e){} }
				}).catch(function(){ yaz('Bağlantı hatası, lütfen tekrar deneyin.','hata'); btn.disabled=false; try{grecaptcha.reset(wid);}catch(e){} });
			});
		}
		function hepsi(){ [].forEach.call(document.querySelectorAll('.ftot-form'),kur); }
		if(document.readyState!=='loading') hepsi(); else document.addEventListener('DOMContentLoaded',hepsi);
	})();
	</script>
	<?php
}

/* -------------------------------------------------------------------------
 * Fuar sayfasına otomatik yerleştirme
 *
 * Form sayfa sonuna gizli olarak basılır; küçük bir betik onu "Fuara Ait
 * Turlar" sekmesine (devre sekmelerinin arkasına) taşır. Sekmede tur kartı
 * varsa form kaldırılır. Elementor'un bileşen önbelleği şablon çıktısını
 * fuarlar arasında paylaştığı için form Elementor bileşenine eklenmez.
 * Kimlikler tek fuar şablonundaki widget'lardır; filtreyle değiştirilebilir.
 * ---------------------------------------------------------------------- */

function ftot_widget_kimlikleri() {
	return apply_filters( 'ftot_widget_kimlikleri', array(
		'tur_listeleri' => array( '3d30071', 'e160ce8', 'bcd1d6e', '8e392dc' ),
		'yerlesim'      => '3327950', // Devre sekmeleri: form bunun arkasına taşınır.
	) );
}

add_action( 'wp_footer', function () {
	if ( is_singular( 'fuarlar' ) ) {
		echo ftot_form_html( get_queried_object_id(), true ); // phpcs:ignore -- çıktı içeride kaçışlandı.
	}
}, 5 );

/**
 * Tek seferlik temizlik: 1.0.0 sürümü formu Elementor bileşen çıktısına
 * eklediği için önbelleğe girmiş olabilir. Elementor bileşen önbelleği ve
 * LiteSpeed sayfa önbelleği bir kez temizlenir.
 */
add_action( 'init', function () {
	if ( get_option( 'ftot_onbellek_temizlendi' ) === FTOT_VERSION ) {
		return;
	}
	update_option( 'ftot_onbellek_temizlendi', FTOT_VERSION, true );
	delete_post_meta_by_key( '_elementor_element_cache' );
	if ( class_exists( '\\Elementor\\Plugin' ) && isset( \Elementor\Plugin::$instance->files_manager ) ) {
		\Elementor\Plugin::$instance->files_manager->clear_cache();
	}
	do_action( 'litespeed_purge_all' );
}, 99 );

/* -------------------------------------------------------------------------
 * Gönderim
 * ---------------------------------------------------------------------- */

add_action( 'admin_post_nopriv_ftot_gonder', 'ftot_gonder' );
add_action( 'admin_post_ftot_gonder', 'ftot_gonder' );

function ftot_ip() {
	return isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
}

function ftot_gonder() {
	$ajax = ! empty( $_POST['ajax'] );
	$geri = function ( $ok, $mesaj ) use ( $ajax ) {
		if ( $ajax ) {
			$ok ? wp_send_json_success( array( 'mesaj' => $mesaj ) ) : wp_send_json_error( array( 'mesaj' => $mesaj ), 200 );
		}
		$fuar = isset( $_POST['fuar_id'] ) ? get_permalink( (int) $_POST['fuar_id'] ) : home_url( '/' );
		wp_safe_redirect( add_query_arg( 'ozel_tur', $ok ? 'ok' : 'hata', $fuar ? $fuar : home_url( '/' ) ) . '#ozel-tur-talebi' );
		exit;
	};

	$p = wp_unslash( $_POST ); // phpcs:ignore WordPress.Security.NonceVerification -- önbellekli sayfalar için nonce yerine reCAPTCHA kullanılır.

	// Bal küpü: botlar doldurur.
	if ( ! empty( $p['web_sitesi'] ) ) {
		$geri( true, '' );
	}

	// Basit hız sınırı: aynı IP'den 10 dakikada en fazla 5 talep.
	$ip  = ftot_ip();
	$rk  = 'ftot_rl_' . md5( $ip );
	$say = (int) get_transient( $rk );
	if ( $say >= 5 ) {
		$geri( false, 'Çok fazla deneme yapıldı. Lütfen biraz sonra tekrar deneyin veya bizi arayın.' );
	}

	$fuar_id = (int) ( $p['fuar_id'] ?? 0 );
	if ( ! $fuar_id || 'fuarlar' !== get_post_type( $fuar_id ) ) {
		$geri( false, 'Fuar bilgisi bulunamadı. Sayfayı yenileyip tekrar deneyin.' );
	}

	$v = array(
		'ad_soyad'  => trim( sanitize_text_field( $p['ad_soyad'] ?? '' ) ),
		'eposta'    => trim( sanitize_email( $p['eposta'] ?? '' ) ),
		'telefon'   => trim( sanitize_text_field( $p['telefon'] ?? '' ) ),
		'katilimci' => (int) ( $p['katilimci'] ?? 0 ),
		'diger'     => trim( sanitize_textarea_field( $p['diger'] ?? '' ) ),
	);
	$hata = array();
	if ( '' === $v['ad_soyad'] || mb_strlen( $v['ad_soyad'] ) > 100 ) {
		$hata[] = 'ad soyad';
	}
	if ( ! is_email( $v['eposta'] ) ) {
		$hata[] = 'e-posta';
	}
	$rakam = preg_replace( '/\D+/', '', $v['telefon'] );
	if ( strlen( $rakam ) < 7 || strlen( $rakam ) > 15 || mb_strlen( $v['telefon'] ) > 25 ) {
		$hata[] = 'telefon';
	}
	if ( $v['katilimci'] < 1 || $v['katilimci'] > 500 ) {
		$hata[] = 'katılımcı sayısı';
	}
	foreach ( ftot_secimler() as $k => $tanim ) {
		$s = sanitize_key( $p[ $k ] ?? '' );
		if ( ! isset( $tanim[1][ $s ] ) ) {
			$hata[] = mb_strtolower( $tanim[0] );
		} else {
			$v[ $k ] = $s;
		}
	}
	$v['diger'] = mb_substr( $v['diger'], 0, 2000 );
	if ( $hata ) {
		$geri( false, 'Lütfen şu alanları kontrol edin: ' . implode( ', ', array_unique( $hata ) ) . '.' );
	}

	// reCAPTCHA doğrulaması.
	$secret = ftot_secret_key();
	$token  = sanitize_text_field( $p['g-recaptcha-response'] ?? '' );
	if ( ! $secret || ! $token ) {
		$geri( false, 'Güvenlik doğrulaması başarısız. Lütfen "Ben robot değilim" kutusunu işaretleyin.' );
	}
	$r = wp_remote_post( 'https://www.google.com/recaptcha/api/siteverify', array(
		'timeout' => 10,
		'body'    => array( 'secret' => $secret, 'response' => $token, 'remoteip' => $ip ),
	) );
	$j = is_wp_error( $r ) ? null : json_decode( wp_remote_retrieve_body( $r ), true );
	if ( empty( $j['success'] ) ) {
		$geri( false, 'Güvenlik doğrulaması başarısız. Lütfen tekrar deneyin.' );
	}

	set_transient( $rk, $say + 1, 10 * MINUTE_IN_SECONDS );

	$fuar_adi = get_the_title( $fuar_id );
	$talep_id = wp_insert_post( array(
		'post_type'   => FTOT_CPT,
		'post_status' => 'publish',
		'post_title'  => $v['ad_soyad'] . ' – ' . wp_strip_all_tags( $fuar_adi ),
	), true );
	if ( is_wp_error( $talep_id ) ) {
		$geri( false, 'Talebiniz kaydedilemedi. Lütfen bizi arayın: 0850 255 58 58' );
	}
	$v['fuar_id'] = $fuar_id;
	$v['ip']      = $ip;
	foreach ( $v as $k => $deger ) {
		update_post_meta( $talep_id, $k, $deger );
	}

	// E-posta bildirimi.
	$a     = ftot_ayarlar();
	$kime  = $a['bildirim'] ? $a['bildirim'] : get_option( 'admin_email' );
	$konu  = 'Özel tur talebi: ' . wp_strip_all_tags( html_entity_decode( $fuar_adi ) ) . ' – ' . $v['ad_soyad'];
	$govde = '<div style="font:14px/1.5 Arial,sans-serif;color:#1f2430"><p>fuartour.com üzerinden yeni bir özel paket tur talebi geldi.</p>'
		. ftot_ozet_tablosu( $talep_id )
		. '<p style="margin-top:14px"><a href="' . esc_url( admin_url( 'post.php?post=' . $talep_id . '&action=edit' ) ) . '">Talebi panelde aç</a></p></div>';
	$basl  = array(
		'Content-Type: text/html; charset=UTF-8',
		'Reply-To: ' . str_replace( array( "\r", "\n", '<', '>' ), '', $v['ad_soyad'] ) . ' <' . $v['eposta'] . '>',
	);
	$gitti = wp_mail( array_map( 'trim', explode( ',', $kime ) ), $konu, $govde, $basl );
	update_post_meta( $talep_id, 'eposta_gonderildi', $gitti ? 1 : 0 );

	$geri( true, ' Ekibimiz en kısa sürede ' . esc_html( $v['eposta'] ) . ' adresinden veya telefonla size dönüş yapacak.' );
}

/** JS kapalıyken yönlendirme sonrası mesaj. */
add_action( 'wp_footer', function () {
	if ( ! is_singular( 'fuarlar' ) || empty( $_GET['ozel_tur'] ) ) { // phpcs:ignore
		return;
	}
	$ok = 'ok' === $_GET['ozel_tur']; // phpcs:ignore
	echo '<div style="position:fixed;left:16px;right:16px;bottom:16px;z-index:99999;max-width:520px;margin:auto;padding:14px 18px;border-radius:12px;background:' . ( $ok ? '#15803d' : '#b91c1c' ) . ';color:#fff;font:600 15px/1.5 Arial,sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.2)" onclick="this.remove()">'
		. ( $ok ? 'Talebiniz alındı, teşekkür ederiz. En kısa sürede size dönüş yapacağız.' : 'Talebiniz gönderilemedi. Lütfen formu eksiksiz doldurup tekrar deneyin.' )
		. '</div>';
} );
