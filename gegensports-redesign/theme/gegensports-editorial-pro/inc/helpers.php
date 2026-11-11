<?php
defined('ABSPATH') || exit;

/** Kategori kalabalığını önlemek için kartlarda gösterilmeyen genel/teknik kategoriler. */
function gsx_generic_cats(): array {
    return ['uncategorized', 'genel', 'english', 'espanol', 'scout-raporlari', 'scout-raporlari-en', 'scout-raporlari-es', 'gp-scout', 'gp-scout-en', 'gp-scout-es', 'son-dakika'];
}

/** Bir yazının tek, en anlamlı kategorisi (rozet kalabalığı yok). */
function gsx_primary_term(int $post_id = 0): ?WP_Term {
    $terms = get_the_terms($post_id ?: get_the_ID(), 'category');
    if (!$terms || is_wp_error($terms)) return null;
    $skip = gsx_generic_cats();
    foreach ($terms as $t) if (!in_array($t->slug, $skip, true)) return $t;
    return null; // yalnızca genel/teknik kategori varsa rozet gösterme
}

function gsx_kicker(int $post_id = 0): string {
    $t = gsx_primary_term($post_id);
    return $t ? esc_html(html_entity_decode($t->name)) : '';
}

/** Dil duyarlı kategori bağlantısı; kategori yoksa '' (menü öğesi gizlenir). */
function gsx_term_url(string $slug): string {
    $t = get_term_by('slug', $slug, 'category');
    if (!$t) return '';
    if (function_exists('pll_get_term')) {
        $tr = pll_get_term($t->term_id, gsx_lang());
        if ($tr) $t = get_term($tr, 'category');
    }
    $l = get_term_link($t);
    return is_wp_error($l) ? '' : $l;
}

function gsx_page_url(string $slug): string {
    $p = get_page_by_path($slug);
    if (!$p) return '';
    if (function_exists('pll_get_post')) {
        $tr = pll_get_post($p->ID, gsx_lang());
        if ($tr) $p = get_post($tr);
    }
    return $p ? get_permalink($p) : '';
}

function gsx_news_url(): string { return home_url('/haberler/'); }

/** Görsel: gerçek öne çıkan görsel yoksa nötr yer tutucu (hatalı/boş görsel basma). */
function gsx_thumb(int $post_id, string $size = 'gsx-card', bool $priority = false): string {
    if (has_post_thumbnail($post_id)) {
        $attr = ['alt' => esc_attr(get_the_title($post_id))];
        if ($priority) { $attr['loading'] = 'eager'; $attr['fetchpriority'] = 'high'; $attr['decoding'] = 'async'; }
        else { $attr['loading'] = 'lazy'; $attr['decoding'] = 'async'; }
        return get_the_post_thumbnail($post_id, $size, $attr);
    }
    return '';
}

function gsx_reading_minutes(string $html): int {
    return max(1, (int) ceil(str_word_count(wp_strip_all_tags($html)) / 200));
}

/** Gerçekten güncellendiyse (yayından ≥ 1 saat sonra) güncelleme tarihi. */
function gsx_updated_ts(int $post_id): ?int {
    $p = (int) get_post_time('U', true, $post_id);
    $m = (int) get_post_modified_time('U', true, $post_id);
    return ($m - $p) >= HOUR_IN_SECONDS ? $m : null;
}

/** İlk 2 cümlelik spot: yalnız elle yazılmış özet varsa. "Özet bulunamadı" gibi sistem metni asla basılmaz. */
function gsx_dek(int $post_id): string {
    $p = get_post($post_id);
    if (!$p || trim($p->post_excerpt) === '') return '';
    $t = trim(wp_strip_all_tags($p->post_excerpt));
    if (preg_match('/özet\s*bulunamad|no summary|sin resumen/iu', $t)) return '';
    return $t;
}

/** Kart özeti: elle özet yoksa içerikten kısa alıntı (boşsa ''). */
function gsx_blurb(int $post_id, int $words = 26): string {
    $d = gsx_dek($post_id);
    if ($d !== '') return wp_trim_words($d, $words, '…');
    $c = wp_strip_all_tags(strip_shortcodes(get_post_field('post_content', $post_id)));
    return wp_trim_words($c, $words, '…');
}

function gsx_icon(string $n): string {
    static $i = [
        'search' => '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>',
        'menu'   => '<path d="M4 7h16M4 12h16M4 17h16"/>',
        'close'  => '<path d="M6 6l12 12M18 6 6 18"/>',
        'home'   => '<path d="M4 11.5 12 5l8 6.5V19a1 1 0 0 1-1 1h-4v-5H9v5H5a1 1 0 0 1-1-1z"/>',
        'news'   => '<path d="M5 5h11v14H7a2 2 0 0 1-2-2zM16 9h3v8a2 2 0 0 1-2 2M8 9h5M8 13h5"/>',
        'user'   => '<circle cx="12" cy="8" r="3.5"/><path d="M5 20c1-4 4-5.5 7-5.5s6 1.5 7 5.5"/>',
        'radar'  => '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="3.5"/><path d="M12 12 18 6"/>',
    ];
    return '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">' . ($i[$n] ?? '') . '</svg>';
}

function gsx_lang_links(): array {
    $out = [];
    if (function_exists('pll_the_languages')) {
        foreach ((array) pll_the_languages(['raw' => 1, 'hide_if_empty' => 0]) as $l) {
            $out[] = ['slug' => $l['slug'], 'url' => $l['url'], 'current' => !empty($l['current_lang'])];
        }
    }
    return $out;
}

function gsx_breadcrumbs(array $trail): void {
    $trail = array_values(array_filter($trail));
    echo '<nav class="breadcrumbs" aria-label="Breadcrumb"><ol>';
    foreach ($trail as $k => $c) {
        $last = $k === array_key_last($trail);
        echo '<li>' . (!$last && !empty($c[1]) ? '<a href="' . esc_url($c[1]) . '">' . esc_html($c[0]) . '</a>' : '<span' . ($last ? ' aria-current="page"' : '') . '>' . esc_html($c[0]) . '</span>') . '</li>';
    }
    echo '</ol></nav>';
}

/** Haber (editoryal) ile scout dosyasını ayırmak için: scout kategorisinde mi? */
function gsx_is_scout_post(int $post_id): bool {
    $scout = ['scout-raporlari', 'scout-raporlari-en', 'scout-raporlari-es', 'gp-scout', 'gp-scout-en', 'gp-scout-es', 'gp-radar', 'gp-report', 'gp-watch', 'gp-signal', 'genc-yetenek-havuzu'];
    return has_term($scout, 'category', $post_id);
}

/** Haber sorgusu: scout raporu olmayanlar (ana sayfada haberle scouting karışmasın). */
function gsx_news_args(array $extra = []): array {
    $ids = [];
    foreach (['scout-raporlari', 'scout-raporlari-en', 'scout-raporlari-es', 'gp-scout', 'gp-scout-en', 'gp-scout-es', 'genc-yetenek-havuzu'] as $s) {
        $t = get_term_by('slug', $s, 'category');
        if ($t) $ids[] = $t->term_id;
    }
    return array_merge(['post_type' => 'post', 'post_status' => 'publish', 'ignore_sticky_posts' => true, 'no_found_rows' => true, 'category__not_in' => $ids], $extra);
}

function gsx_scout_args(array $extra = []): array {
    $t = [];
    foreach (['scout-raporlari', 'scout-raporlari-en', 'scout-raporlari-es'] as $s) { $x = get_term_by('slug', $s, 'category'); if ($x) $t[] = $x->term_id; }
    return array_merge(['post_type' => 'post', 'post_status' => 'publish', 'ignore_sticky_posts' => true, 'no_found_rows' => true, 'category__in' => $t ?: [0]], $extra);
}

/** Eşleşme verisi kaynağı (varsayılan boş → şerit gizli). Gerçek fikstür API'si bağlanınca filtre ile doldurulur. */
function gsx_match_data(): array {
    return (array) apply_filters('gsx_match_data', []);
}

function gsx_template_part(string $name, array $args = []): void {
    get_template_part('template-parts/' . $name, null, $args);
}
