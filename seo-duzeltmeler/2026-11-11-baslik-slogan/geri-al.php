<?php
/**
 * uygula.php'nin geri alınması: Polylang site adı/slogan çevirilerini yedekteki hâline döndürür.
 * Yedekte çeviri özgün metne eşitse (yani önceden çevrilmemişse) çeviri kaydı özgün metinle yazılır;
 * Polylang bunu "çeviri yok" ile aynı şekilde gösterir.
 * Çalıştırma: Code Snippets single-use ya da `wp eval-file geri-al.php`.
 */

if ( ! function_exists( 'PLL' ) || ! class_exists( 'PLL_MO' ) ) {
	return;
}
$eka_yedek = get_option( 'eka_backup_pll_site_20261111' );
if ( ! is_array( $eka_yedek ) ) {
	return;
}
foreach ( PLL()->model->get_languages_list() as $eka_lang ) {
	if ( empty( $eka_yedek['diller'][ $eka_lang->slug ] ) ) {
		continue;
	}
	$eski = $eka_yedek['diller'][ $eka_lang->slug ];
	$mo   = new PLL_MO();
	$mo->import_from_db( $eka_lang );
	$mo->add_entry( $mo->make_entry( $eka_yedek['blogname'], $eski['blogname'] ) );
	$mo->add_entry( $mo->make_entry( $eka_yedek['blogdescription'], $eski['blogdescription'] ) );
	$mo->export_to_db( $eka_lang );
}
delete_option( 'eka_backup_pll_site_20261111' );
do_action( 'litespeed_purge_all' );
if ( defined( 'WP_CLI' ) && WP_CLI ) {
	WP_CLI::log( 'geri alındı' );
}
