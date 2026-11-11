<?php
defined('ABSPATH') || exit;
/**
 * Yalnızca EKLEYEN yeni rotalar (mevcut URL'ler değişmez):
 *   /haberler/            → tüm haberler arşivi (scout raporları hariç)
 *   /dossier/             → güncel oyuncu dosyaları dizini (GPScout verisi)
 *   /dossier/{rapor-slug} → Gegen Dossier oyuncu dosyası
 */
add_action('init', function () {
    add_rewrite_rule('^haberler/page/([0-9]+)/?$', 'index.php?gsx_view=news&paged=$matches[1]', 'top');
    add_rewrite_rule('^haberler/?$', 'index.php?gsx_view=news', 'top');
    add_rewrite_rule('^dossier/?$', 'index.php?gsx_view=dossier_index', 'top');
    add_rewrite_rule('^dossier/([a-z0-9-]+)/?$', 'index.php?gsx_view=dossier&gsx_report=$matches[1]', 'top');
});
add_filter('query_vars', function ($v) { array_push($v, 'gsx_view', 'gsx_report'); return $v; });

add_action('pre_get_posts', function (WP_Query $q) {
    if (!$q->is_main_query() || is_admin()) return;
    $v = $q->get('gsx_view');
    if ($v === 'news') {
        $q->set('post_type', 'post');
        $q->set('posts_per_page', 18);
        $ids = array_map(fn($a) => $a, (array) (gsx_news_args()['category__not_in'] ?? []));
        $q->set('category__not_in', $ids);
    } elseif ($v === 'dossier' || $v === 'dossier_index') {
        $q->set('post_type', 'post');
        $q->set('posts_per_page', 1);
        $q->set('no_found_rows', true);
    }
});

add_action('template_redirect', function () {
    $v = get_query_var('gsx_view');
    if (!$v) return;
    global $wp_query;
    if ($v === 'dossier' && !gsx_report((string) get_query_var('gsx_report'))) { return; } // gerçek 404
    $wp_query->is_404 = false;
    status_header(200);
});

add_filter('template_include', function ($tpl) {
    $v = get_query_var('gsx_view');
    $map = ['news' => 'archive-news.php', 'dossier_index' => 'page-templates/dossier-index.php', 'dossier' => 'page-templates/dossier.php'];
    if ($v && isset($map[$v])) {
        if ($v === 'dossier' && !gsx_report((string) get_query_var('gsx_report'))) return $tpl;
        $f = locate_template($map[$v]);
        if ($f) return $f;
    }
    return $tpl;
});

add_filter('pre_get_document_title', function ($t) {
    $v = get_query_var('gsx_view');
    $site = get_bloginfo('name');
    if ($v === 'news') return gsx_t('all_news') . ' – ' . $site;
    if ($v === 'dossier_index') return gsx_t('dossier_idx') . ' – ' . $site;
    if ($v === 'dossier') { $r = gsx_report((string) get_query_var('gsx_report')); if ($r) return gsx_clean_text($r['title']) . ' – ' . gsx_t('dossier') . ' – ' . $site; }
    return $t;
}, 20);

add_action('after_switch_theme', 'flush_rewrite_rules');
