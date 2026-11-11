<?php
/**
 * Plugin Name: Envanter Konu Arşivleri
 * Description: Şirket, ürün, ülke ve teknoloji arşivleri (topic hub), haber altında "İlgili Haber Arşivleri" bağlantıları, editör için akıllı arşiv önerileri, kalite kapılı indeksleme ve WP-CLI ile geri alınabilir toplu sınıflandırma. Mevcut kategori/etiket URL'lerini kullanır; yeni URL yapısı açmaz.
 * Version: 0.1.0
 * Author: Envanter Medya
 * Text Domain: envanter-konu-arsivleri
 * Requires PHP: 7.4
 * Requires at least: 6.0
 *
 * Güvenli varsayılanlar:
 *  - Hiçbir arşiv kendiliğinden indekse açılmaz; terim "hub" olarak işaretlenip kalite kapısını geçmedikçe sitenin mevcut robots ayarı korunur.
 *  - Toplu sınıflandırma varsayılan olarak kuru çalışır (--uygula verilmedikçe yazmaz) ve her yazma işlemi geri alma günlüğüne düşer.
 *  - Mevcut kategori ve etiketler silinmez; yalnız ekleme yapılır.
 */

defined( 'ABSPATH' ) || exit;

define( 'EKA_VERSION', '0.1.0' );
define( 'EKA_FILE', __FILE__ );
define( 'EKA_DIR', plugin_dir_path( __FILE__ ) );
define( 'EKA_URL', plugin_dir_url( __FILE__ ) );

require_once EKA_DIR . 'includes/class-dictionary.php';
require_once EKA_DIR . 'includes/class-matcher.php';
require_once EKA_DIR . 'includes/class-hubs.php';
require_once EKA_DIR . 'includes/class-frontend.php';
require_once EKA_DIR . 'includes/class-seo.php';
require_once EKA_DIR . 'includes/class-admin.php';
require_once EKA_DIR . 'includes/class-log.php';

if ( defined( 'WP_CLI' ) && WP_CLI ) {
	require_once EKA_DIR . 'includes/class-cli.php';
	WP_CLI::add_command( 'eka', 'EKA_CLI' );
}

register_activation_hook( __FILE__, array( 'EKA_Log', 'install' ) );

add_action(
	'plugins_loaded',
	function () {
		EKA_Log::maybe_upgrade();
		EKA_Hubs::init();
		EKA_Frontend::init();
		EKA_SEO::init();
		EKA_Admin::init(); // REST uç noktası ve kayıt kancası admin dışında da (Gutenberg REST ile kaydeder) gerekli.
	}
);

/**
 * Tema şablonları için: arşiv sayfasında hub modüllerini (tanıtım, öne çıkanlar, ilgili arşivler) basar.
 * Tema term_description() kullanıyorsa gerek yoktur; modüller açıklamaya otomatik eklenir.
 */
function eka_hub_modulleri( $term = null ) {
	echo EKA_Frontend::hub_modules_html( $term ? $term : get_queried_object() ); // phpcs:ignore WordPress.Security.EscapeOutput
}

/** Tema şablonları için: tekil haberde "İlgili Haber Arşivleri" kutusunu basar. */
function eka_ilgili_arsivler( $post_id = null ) {
	echo EKA_Frontend::related_box_html( $post_id ? $post_id : get_the_ID() ); // phpcs:ignore WordPress.Security.EscapeOutput
}
