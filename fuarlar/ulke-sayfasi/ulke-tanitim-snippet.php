<?php
// Fuartour: ülke filtreli fuar listesi (/fuarlar/ulke-<slug>/) için ülke tanıtım kutusu ve ay filtresi.
// Kullanım: Fuarlar sayfasına (16904) [ulke_tanitim] kısa kodu. Ay filtresi: ?ay=YYYY-MM (Loop Grid sorgu kimliği ft_tarih).

function ft_ulke_aktif_terim() {
	$uri = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '';
	$yol = strtok( $uri, '?' );
	if ( preg_match( '#/ulke-([^/]+)#', $yol, $m ) && strpos( $m[1], '-or-' ) === false ) {
		$t = get_term_by( 'slug', sanitize_title( $m[1] ), 'ulkeler' );
		if ( $t && ! is_wp_error( $t ) ) {
			return $t;
		}
	}
	return null;
}

function ft_ulke_secili_ay() {
	if ( isset( $_GET['ay'] ) && preg_match( '/^(20\d\d)-(0[1-9]|1[0-2])$/', $_GET['ay'], $m ) ) {
		return array( $m[1], $m[2] );
	}
	return null;
}

// Ay filtresi: seçilen ayda başlayan fuarlar.
add_action( 'elementor/query/ft_tarih', function ( $query ) {
	$ay = ft_ulke_secili_ay();
	if ( ! $ay ) {
		return;
	}
	$mq   = (array) $query->get( 'meta_query' );
	$mq[] = array(
		'key'     => 'baslangic_tarihi',
		'value'   => array( $ay[0] . $ay[1] . '01', $ay[0] . $ay[1] . '31' ),
		'compare' => 'BETWEEN',
	);
	$query->set( 'meta_query', $mq );
}, 20 );

// Ülkede bugünden sonraki 12 ayın fuar sayıları (başlangıç ayına göre).
function ft_ulke_ay_sayilari( $term_id ) {
	$anahtar = 'ft_ulke_aylar_' . $term_id . '_' . current_time( 'Ym' );
	$veri    = get_transient( $anahtar );
	if ( is_array( $veri ) ) {
		return $veri;
	}
	global $wpdb;
	$bas  = current_time( 'Ym' ) . '01';
	$rows = $wpdb->get_results( $wpdb->prepare(
		"SELECT LEFT(pm.meta_value, 6) AS ym, COUNT(DISTINCT p.ID) AS n
		 FROM {$wpdb->posts} p
		 JOIN {$wpdb->term_relationships} tr ON tr.object_id = p.ID
		 JOIN {$wpdb->term_taxonomy} tt ON tt.term_taxonomy_id = tr.term_taxonomy_id AND tt.taxonomy = 'ulkeler' AND tt.term_id = %d
		 JOIN {$wpdb->postmeta} pm ON pm.post_id = p.ID AND pm.meta_key = 'baslangic_tarihi'
		 WHERE p.post_type = 'fuarlar' AND p.post_status = 'publish' AND pm.meta_value >= %s
		 GROUP BY ym ORDER BY ym ASC LIMIT 12",
		$term_id,
		$bas
	) );
	$veri = array();
	foreach ( (array) $rows as $r ) {
		if ( preg_match( '/^\d{6}$/', $r->ym ) ) {
			$veri[ $r->ym ] = (int) $r->n;
		}
	}
	set_transient( $anahtar, $veri, 6 * HOUR_IN_SECONDS );
	return $veri;
}

// Terim açıklamasının ilk iki cümlesi (sitedeki ülke metni).
function ft_ulke_kisa_metin( $term ) {
	$ozel = array(
		'hong-kong-fuarlari' => 'Hong Kong, Asya’nın ticaret ve finans merkezlerinden biridir; elektronik, aydınlatma, oyuncak, hediyelik eşya, mücevher ve moda alanlarında Asya’nın önde gelen fuarlarına ev sahipliği yapar. Türk vatandaşları 90 güne kadar kalışlarda Hong Kong’a vizesiz girebilir; Çin anakarası için ayrı vize gerekir.',
	);
	if ( isset( $ozel[ $term->slug ] ) ) {
		return $ozel[ $term->slug ];
	}
	$d = trim( preg_replace( '/\s+/u', ' ', wp_strip_all_tags( strip_shortcodes( $term->description ) ) ) );
	if ( $d === '' ) {
		return '';
	}
	$parcalar = preg_split( '/(?<=[.!?])\s+/u', $d, 3 );
	$metin    = implode( ' ', array_slice( $parcalar, 0, 2 ) );
	if ( mb_strlen( $metin ) > 420 ) {
		$metin = rtrim( mb_substr( $metin, 0, 400 ) ) . '…';
	}
	return $metin;
}

add_shortcode( 'ulke_tanitim', function () {
	$t = ft_ulke_aktif_terim();
	if ( ! $t ) {
		return '';
	}
	$aylar_tr = array( '01' => 'Ocak', '02' => 'Şubat', '03' => 'Mart', '04' => 'Nisan', '05' => 'Mayıs', '06' => 'Haziran', '07' => 'Temmuz', '08' => 'Ağustos', '09' => 'Eylül', '10' => 'Ekim', '11' => 'Kasım', '12' => 'Aralık' );
	$uri      = isset( $_SERVER['REQUEST_URI'] ) ? wp_unslash( $_SERVER['REQUEST_URI'] ) : '/';
	$yol      = strtok( $uri, '?' );
	$yol      = preg_replace( '#/page/\d+/?$#', '/', $yol );
	$taban    = home_url( $yol );
	$secili   = ft_ulke_secili_ay();
	$secili_k = $secili ? $secili[0] . $secili[1] : '';
	$aylar    = ft_ulke_ay_sayilari( $t->term_id );
	$gelecek  = array_sum( $aylar );
	$metin    = ft_ulke_kisa_metin( $t );
	$rehber   = get_term_link( $t );

	ob_start();
	?>
	<div class="ft-ulke-tanitim">
		<div class="ft-ulke-ust">
			<div class="ft-ulke-metin">
				<?php if ( $metin ) : ?><p><?php echo esc_html( $metin ); ?></p><?php endif; ?>
				<?php if ( ! is_wp_error( $rehber ) ) : ?>
					<a class="ft-ulke-rehber" href="<?php echo esc_url( $rehber ); ?>"><?php echo esc_html( $t->name ); ?> rehberi ve vize bilgileri →</a>
				<?php endif; ?>
			</div>
			<div class="ft-ulke-sayilar">
				<div><strong><?php echo esc_html( number_format_i18n( (int) $t->count ) ); ?></strong><span>fuar</span></div>
				<div><strong><?php echo esc_html( number_format_i18n( $gelecek ) ); ?></strong><span>yaklaşan fuar (12 ay)</span></div>
			</div>
		</div>
		<?php if ( $aylar ) : ?>
		<div class="ft-ulke-aylar">
			<span class="ft-ulke-aylar-baslik">Aya göre:</span>
			<a class="ft-ay<?php echo $secili ? '' : ' aktif'; ?>" href="<?php echo esc_url( $taban ); ?>">Tüm aylar</a>
			<?php foreach ( $aylar as $ym => $n ) :
				$ym = (string) $ym;
				$y = substr( $ym, 0, 4 );
				$a = substr( $ym, 4, 2 ); ?>
				<a class="ft-ay<?php echo (string) $ym === $secili_k ? ' aktif' : ''; ?>" href="<?php echo esc_url( add_query_arg( 'ay', $y . '-' . $a, $taban ) ); ?>"><?php echo esc_html( $aylar_tr[ $a ] . ' ' . $y ); ?> <span><?php echo (int) $n; ?></span></a>
			<?php endforeach; ?>
		</div>
		<?php endif; ?>
	</div>
	<style>
	.ft-ulke-tanitim{max-width:1290px;margin:28px auto 0;padding:24px 28px;border:1px solid #e7eaf3;border-radius:12px;background:#fff;box-sizing:border-box}
	.ft-ulke-ust{display:flex;gap:28px;align-items:flex-start;justify-content:space-between}
	.ft-ulke-metin p{margin:0 0 10px;color:#3b4250;font-size:15px;line-height:1.65}
	.ft-ulke-rehber{font-weight:600;color:#f25c05;font-size:14px}
	.ft-ulke-sayilar{display:flex;gap:12px;flex-shrink:0}
	.ft-ulke-sayilar div{min-width:110px;padding:12px 14px;border-radius:10px;background:#fff4ec;text-align:center}
	.ft-ulke-sayilar strong{display:block;font-size:24px;line-height:1.1;color:#f25c05}
	.ft-ulke-sayilar span{font-size:12px;color:#5a6270}
	.ft-ulke-aylar{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-top:18px;padding-top:16px;border-top:1px solid #eef0f5}
	.ft-ulke-aylar-baslik{font-weight:600;font-size:14px;color:#1e2022;margin-right:4px}
	.ft-ay{display:inline-block;padding:6px 12px;border:1px solid #e1e5ee;border-radius:999px;font-size:13px;color:#1e2022;background:#fff;text-decoration:none}
	.ft-ay span{color:#8c93a1;margin-left:2px}
	.ft-ay:hover,.ft-ay.aktif{border-color:#f25c05;background:#f25c05;color:#fff}
	.ft-ay:hover span,.ft-ay.aktif span{color:#ffe3d1}
	@media (max-width:767px){.ft-ulke-tanitim{margin:20px 16px 0;padding:18px}.ft-ulke-ust{flex-direction:column;gap:16px}.ft-ulke-sayilar{width:100%}.ft-ulke-sayilar div{flex:1;min-width:0}}
	</style>
	<?php
	return ob_get_clean();
} );
