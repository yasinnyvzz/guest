<?php
/**
 * Envanter Medya — Türkçe dışı sayfalarda başlığa eklenen Türkçe site adı/sloganı düzeltmesi.
 *
 * Kök neden: WordPress site başlığı "Envanter Medya - Savunma Sanayii Haberleri" ve slogan
 * "Türkiye'nin Savunma Sanayii Haber ve Analiz Platformu" Polylang'de diğer diller için çevrilmemiş.
 * Rank Math'in %sitename% / %sitedesc% değişkenleri bu yüzden EN/AR/ES/RU/ZH sayfalarına Türkçe metin basıyor.
 *
 * Bu betik Rank Math şablonuna ve Türkçe başlıklara DOKUNMAZ. Yalnız Polylang "Site Title" ve "Tagline"
 * dizelerinin TR dışı çevirilerini yazar:
 *   - Önce mevcut çevirileri eka_backup_pll_site_20261111 seçeneğine yedekler (yedek varsa üzerine yazmaz).
 *   - Bir dilde çeviri zaten varsa (özgün metinden farklıysa) ona dokunmaz.
 * Çalıştırma: Code Snippets › Yeni › "Yalnız bir kez çalıştır" (single-use) ya da `wp eval-file uygula.php`.
 * Geri alma: geri-al.php
 */

if ( ! function_exists( 'PLL' ) || ! class_exists( 'PLL_MO' ) ) {
	return;
}

global $wpdb;
$eka_name = $wpdb->get_var( "SELECT option_value FROM {$wpdb->options} WHERE option_name = 'blogname'" );
$eka_desc = $wpdb->get_var( "SELECT option_value FROM {$wpdb->options} WHERE option_name = 'blogdescription'" );

$eka_hedef = array(
	'en' => array( 'Envanter Medya', 'Defence Industry News and Analysis from Türkiye' ),
	'ar' => array( 'Envanter Medya', 'أخبار وتحليلات الصناعات الدفاعية من تركيا' ),
	'es' => array( 'Envanter Medya', 'Noticias y análisis de la industria de defensa desde Türkiye' ),
	'ru' => array( 'Envanter Medya', 'Новости и аналитика оборонной промышленности Турции' ),
	'zh' => array( 'Envanter Medya', '来自土耳其的国防工业新闻与分析' ),
);

$eka_yedek = get_option( 'eka_backup_pll_site_20261111' );
$eka_ilk   = ! is_array( $eka_yedek );
if ( $eka_ilk ) {
	$eka_yedek = array( 'blogname' => $eka_name, 'blogdescription' => $eka_desc, 'diller' => array() );
}
$eka_rapor = array();

foreach ( PLL()->model->get_languages_list() as $eka_lang ) {
	if ( ! isset( $eka_hedef[ $eka_lang->slug ] ) ) {
		continue; // varsayılan dil (tr) ve listede olmayanlar
	}
	$mo = new PLL_MO();
	$mo->import_from_db( $eka_lang );
	$once_ad    = $mo->translate( $eka_name );
	$once_slogan = $mo->translate( $eka_desc );
	if ( $eka_ilk ) {
		$eka_yedek['diller'][ $eka_lang->slug ] = array( 'blogname' => $once_ad, 'blogdescription' => $once_slogan );
	}
	$degisti = false;
	if ( $once_ad === $eka_name ) {
		$mo->add_entry( $mo->make_entry( $eka_name, $eka_hedef[ $eka_lang->slug ][0] ) );
		$degisti = true;
	}
	if ( $once_slogan === $eka_desc ) {
		$mo->add_entry( $mo->make_entry( $eka_desc, $eka_hedef[ $eka_lang->slug ][1] ) );
		$degisti = true;
	}
	if ( $degisti ) {
		$mo->export_to_db( $eka_lang );
	}
	$eka_rapor[ $eka_lang->slug ] = $degisti ? 'yazıldı' : 'zaten çevrili, dokunulmadı';
}

if ( $eka_ilk ) {
	update_option( 'eka_backup_pll_site_20261111', $eka_yedek, false );
}
update_option( 'eka_baslik_slogan_rapor_20261111', array( 'zaman' => current_time( 'mysql', true ), 'sonuc' => $eka_rapor ), false );

// LiteSpeed önbelleği (varsa) tamamen temizlenir; başlıklar yeni sürümle sunulsun.
do_action( 'litespeed_purge_all' );

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::log( wp_json_encode( $eka_rapor, JSON_UNESCAPED_UNICODE ) );
}
