<?php
/**
 * GegenSports Editorial Pro — yalnızca sunum katmanı.
 * Veri/iş mantığı eklentilerde kalır (GPScout, Polylang, Rank Math / GSX SEO).
 */
defined('ABSPATH') || exit;

define('GSX_VER', '0.1.0');
define('GSX_DIR', get_template_directory());

require_once GSX_DIR . '/inc/i18n.php';
require_once GSX_DIR . '/inc/helpers.php';
require_once GSX_DIR . '/inc/gpscout.php';
require_once GSX_DIR . '/inc/components.php';
require_once GSX_DIR . '/inc/routes.php';

add_action('after_setup_theme', function () {
    add_theme_support('title-tag');            // başlığı SEO eklentisi yönetir
    add_theme_support('post-thumbnails');
    add_theme_support('html5', ['search-form', 'comment-form', 'comment-list', 'gallery', 'caption', 'style', 'script']);
    add_theme_support('custom-logo', ['height' => 72, 'width' => 220, 'flex-width' => true, 'flex-height' => true]);
    add_theme_support('responsive-embeds');
    add_theme_support('align-wide');
    add_image_size('gsx-lead', 1200, 750, true);   // 16:10
    add_image_size('gsx-card', 640, 360, true);    // 16:9
    add_image_size('gsx-thumb', 240, 180, true);   // 4:3
    register_nav_menus([
        'primary'   => 'Ana menü',
        'secondary' => 'İkincil menü',
        'footer'    => 'Alt bilgi menüsü',
    ]);
});

add_action('wp_enqueue_scripts', function () {
    $u = get_template_directory_uri() . '/assets/';
    foreach (['tokens', 'base', 'components'] as $h) {
        wp_enqueue_style("gsx-$h", $u . "css/$h.css", $h === 'tokens' ? [] : ['gsx-tokens'], GSX_VER);
    }
    wp_enqueue_script('gsx-ui', $u . 'js/ui.js', [], GSX_VER, ['strategy' => 'defer', 'in_footer' => true]);
});

// Gereksiz yükleri kaldır (performans)
remove_action('wp_head', 'print_emoji_detection_script', 7);
remove_action('wp_print_styles', 'print_emoji_styles');
remove_action('wp_head', 'wp_generator');
add_action('wp_enqueue_scripts', function () {
    wp_dequeue_style('wp-block-library-theme');
    wp_dequeue_style('global-styles');
}, 100);

// Ana sayfa dışı sayfalarda ilk büyük görseli geciktirme: WP varsayılan lazy-load'u ilk görselde fetchpriority ile dengelenir
add_filter('wp_img_tag_add_loading_attr', function ($v, $tag, $ctx) {
    return $v;
}, 10, 3);

// Gövde sınıfları
add_filter('body_class', function ($c) {
    $c[] = 'has-bottom-nav';
    return $c;
});

// Özet kelime sayısı
add_filter('excerpt_length', fn() => 32);
add_filter('excerpt_more', fn() => '…');
