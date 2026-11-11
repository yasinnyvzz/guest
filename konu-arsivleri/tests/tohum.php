<?php
/**
 * TEST ORTAMI tohumlama (yalnız yerel test WordPress'inde çalıştırın; canlıda ÇALIŞTIRMAYIN).
 * Kullanım: wp eval-file tests/tohum.php <ornek_yazilar.json>
 *  - Polylang dilleri: tr (varsayılan), en, ar
 *  - Her varlık için her dilde bir arşiv terimi (şirket/ürün/ana konu → kategori, ülke/teknoloji → etiket)
 *  - Hub eşlemesi (eka_hublar) bu terimlerle kurulur
 *  - Örnek yazılar yalnız genel "Haberler" kategorisiyle eklenir (sınıflandırma işi kalsın)
 */
if ( ! defined( 'WP_CLI' ) ) {
	exit;
}
$file = $args[0];
$langs = array(
	'tr' => array( 'name' => 'Türkçe', 'slug' => 'tr', 'locale' => 'tr_TR', 'rtl' => 0, 'term_group' => 0, 'flag' => 'tr' ),
	'en' => array( 'name' => 'English', 'slug' => 'en', 'locale' => 'en_GB', 'rtl' => 0, 'term_group' => 1, 'flag' => 'gb' ),
	'ar' => array( 'name' => 'العربية', 'slug' => 'ar', 'locale' => 'ar', 'rtl' => 1, 'term_group' => 2, 'flag' => 'sa' ),
);
foreach ( $langs as $l ) {
	if ( ! PLL()->model->get_language( $l['slug'] ) ) {
		$r = PLL()->model->add_language( $l );
		WP_CLI::log( 'dil ' . $l['slug'] . ': ' . ( is_wp_error( $r ) ? $r->get_error_message() : 'ok' ) );
	}
}
PLL()->model->clean_languages_cache();
$opt                 = get_option( 'polylang' );
$opt['default_lang'] = 'tr';
$opt['sync']         = array( 'taxonomies' );
update_option( 'polylang', $opt );

$d      = EKA_Dictionary::data();
$hubmap = array();
$genel  = array();
foreach ( array_keys( $langs ) as $l ) {
	$name = array( 'tr' => 'Haberler', 'en' => 'News', 'ar' => 'الأخبار' )[ $l ];
	$t    = term_exists( $name . ( 'tr' === $l ? '' : '' ), 'category' );
	if ( ! $t ) {
		$t = wp_insert_term( $name, 'category', array( 'slug' => sanitize_title( 'haberler-' . $l ) ) );
	}
	$genel[ $l ] = (int) $t['term_id'];
	pll_set_term_language( $genel[ $l ], $l );
}
pll_save_term_translations( $genel );

foreach ( $d['varliklar'] as $v ) {
	$tax = in_array( $v['tip'], array( 'ulke', 'teknoloji' ), true ) ? 'post_tag' : 'category';
	$tr  = array();
	foreach ( array_keys( $langs ) as $l ) {
		$name = isset( $v['ad'][ $l ] ) ? $v['ad'][ $l ] : $v['ad']['en'];
		$slug = $v['id'] . ( 'tr' === $l ? '' : '-' . $l );
		$ex   = get_term_by( 'slug', $slug, $tax );
		$tid  = $ex ? $ex->term_id : 0;
		if ( ! $tid ) {
			$r = wp_insert_term( $name, $tax, array( 'slug' => $slug ) );
			if ( is_wp_error( $r ) ) {
				WP_CLI::warning( $slug . ': ' . $r->get_error_message() );
				continue;
			}
			$tid = $r['term_id'];
		}
		pll_set_term_language( $tid, $l );
		$tr[ $l ]                         = $tid;
		$hubmap[ $l . ':' . $v['id'] ] = array( 'tax' => $tax, 'id' => (int) $tid, 'kopya' => array() );
	}
	pll_save_term_translations( $tr );
}
update_option( 'eka_hublar', $hubmap, false );
foreach ( $hubmap as $k => $h ) {
	update_term_meta( $h['id'], 'eka_varlik', substr( $k, strpos( $k, ':' ) + 1 ) );
}

$posts = json_decode( file_get_contents( $file ), true ); // phpcs:ignore
$n     = 0;
foreach ( $posts as $p ) {
	if ( get_page_by_path( $p['slug'], OBJECT, 'post' ) ) {
		continue;
	}
	$id = wp_insert_post(
		array(
			'post_title'    => $p['title'],
			'post_excerpt'  => $p['excerpt'],
			'post_content'  => $p['content'],
			'post_name'     => $p['slug'],
			'post_status'   => 'publish',
			'post_date'     => str_replace( 'T', ' ', $p['date'] ),
			'post_category' => array( $genel[ $p['lang'] ] ),
		)
	);
	pll_set_post_language( $id, $p['lang'] );
	update_post_meta( $id, '_kaynak_id', $p['src_id'] );
	$n++;
}
// Bir yazıyı önceden KAAN arşivine bağla: "zaten bağlı" durumunu sınamak için.
WP_CLI::success( "$n yazı, " . count( $hubmap ) . ' hub eşlemesi' );
