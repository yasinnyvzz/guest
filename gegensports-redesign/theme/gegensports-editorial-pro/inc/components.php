<?php
defined('ABSPATH') || exit;

function gsx_section_head(string $title, string $sub = '', string $url = '', string $link_label = ''): void {
    echo '<div class="section-head"><div><h2>' . esc_html($title) . '</h2>' . ($sub ? '<p>' . esc_html($sub) . '</p>' : '') . '</div>';
    if ($url) echo '<a href="' . esc_url($url) . '">' . esc_html($link_label ?: gsx_t('all')) . ' →</a>';
    echo '</div>';
}

function gsx_time_tag(int $id, string $fmt = 'long'): string {
    $ts = (int) get_post_time('U', true, $id);
    return '<time datetime="' . esc_attr(get_post_time('c', true, $id)) . '">' . esc_html(gsx_date($ts, $fmt)) . '</time>';
}

/** A — Lead (büyük görsel, güçlü başlık, 2 satır spot, kategori + tarih). */
function gsx_lead_story(int $id): void {
    $dek = gsx_blurb($id, 30); ?>
    <article class="lead-story">
      <?php $img = gsx_thumb($id, 'gsx-lead', true); ?>
      <a class="media<?php echo $img ? '' : ' media--empty'; ?>" href="<?php echo esc_url(get_permalink($id)); ?>" tabindex="-1" aria-hidden="true"><?php echo $img ?: 'GEGENSPORTS'; ?></a>
      <div>
        <div class="kicker"><?php echo gsx_kicker($id); ?></div>
        <h2 style="margin:6px 0 12px"><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h2>
        <?php if ($dek) echo '<p class="lead-story__dek">' . esc_html($dek) . '</p>'; ?>
        <div class="meta" style="margin-top:12px"><?php echo gsx_time_tag($id); ?></div>
      </div>
    </article>
<?php }

/** Lead yanındaki küçük haber. */
function gsx_side_story(int $id): void { ?>
    <article class="side-story">
      <?php $img = gsx_thumb($id, 'gsx-thumb'); ?>
      <a class="media<?php echo $img ? '' : ' media--empty'; ?>" href="<?php echo esc_url(get_permalink($id)); ?>" tabindex="-1" aria-hidden="true"><?php echo $img ?: 'GS'; ?></a>
      <div><div class="kicker"><?php echo gsx_kicker($id); ?></div>
        <h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3>
        <div class="meta"><?php echo gsx_time_tag($id); ?></div></div>
    </article>
<?php }

/** B — Standart kart (16:9, 2–3 satır başlık, kategori, tarih). */
function gsx_card(int $id): void { ?>
    <article class="card">
      <?php $img = gsx_thumb($id, 'gsx-card'); ?>
      <a class="media<?php echo $img ? '' : ' media--empty'; ?>" href="<?php echo esc_url(get_permalink($id)); ?>" tabindex="-1" aria-hidden="true"><?php echo $img ?: 'GEGENSPORTS'; ?></a>
      <div class="kicker"><?php echo gsx_kicker($id); ?></div>
      <h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3>
      <div class="meta"><?php echo gsx_time_tag($id); ?></div>
    </article>
<?php }

/** C — Kompakt satır (saat/tarih, kategori, başlık). */
function gsx_news_row(int $id): void {
    $ts = (int) get_post_time('U', true, $id);
    $today = wp_date('Ymd', $ts) === wp_date('Ymd');
    $when = $today ? wp_date('H:i', $ts) : gsx_date($ts, 'short'); ?>
    <li class="news-row"><time datetime="<?php echo esc_attr(get_post_time('c', true, $id)); ?>"><?php echo esc_html($when); ?></time>
      <div><span class="kicker"><?php echo gsx_kicker($id); ?></span><h3><a href="<?php echo esc_url(get_permalink($id)); ?>"><?php echo esc_html(get_the_title($id)); ?></a></h3></div></li>
<?php }

/** Scout oyuncu kartı — veri dizisinden (GPScout API) ya da yazıdan. */
function gsx_player_card(array $r): void {
    $p = $r['player'] ?? []; $name = gsx_clean_text($p['name'] ?? ($r['title'] ?? '')); if ($name === '') return;
    $url = isset($r['slug']) ? gsx_report_url($r['slug']) : ($r['url'] ?? '#');
    $facts = [];
    if (!empty($p['club'])) $facts[] = '<li><strong>' . esc_html($p['club']) . '</strong></li>';
    if (!empty($p['age'])) $facts[] = '<li>' . (int) $p['age'] . ' ' . esc_html(strtolower(gsx_t('age'))) . '</li>';
    if (!empty($p['nationality']) && strlen($p['nationality']) > 2) $facts[] = '<li>' . esc_html($p['nationality']) . '</li>';
    $blurb = gsx_clean_text(wp_strip_all_tags($r['excerpt'] ?? '')); ?>
    <article class="player-card">
      <a class="player-card__photo" href="<?php echo esc_url($url); ?>" tabindex="-1" aria-hidden="true"><?php if (!empty($p['photo'])) echo '<img src="' . esc_url($p['photo']) . '" alt="" loading="lazy" decoding="async" width="88" height="88">'; ?></a>
      <div>
        <?php if (!empty($p['position'])) echo '<span class="pos">' . esc_html($p['position']) . '</span>'; ?>
        <h3 style="margin-top:6px"><a href="<?php echo esc_url($url); ?>"><?php echo esc_html($name); ?></a></h3>
        <ul class="player-card__facts"><?php echo implode('', $facts); ?></ul>
      </div>
      <?php if ($blurb) echo '<p>' . esc_html($blurb) . '</p>'; ?>
    </article>
<?php }

function gsx_empty_state(string $title, string $text, string $action_url = '', string $action_label = ''): void {
    echo '<div class="state" role="status"><h2>' . esc_html($title) . '</h2><p>' . esc_html($text) . '</p>';
    if ($action_url) echo '<a class="btn" href="' . esc_url($action_url) . '">' . esc_html($action_label) . '</a>';
    echo '</div>';
}

function gsx_pagination(?WP_Query $q = null): void {
    $q = $q ?: $GLOBALS['wp_query'];
    $links = paginate_links(['total' => $q->max_num_pages, 'current' => max(1, get_query_var('paged')), 'type' => 'array', 'prev_text' => '←', 'next_text' => '→', 'mid_size' => 1]);
    if ($links) echo '<nav class="pagination" aria-label="' . esc_attr(gsx_t('page')) . '">' . implode('', $links) . '</nav>';
}

/** Sağ panel: son haberler (+ ilgili). Boş sidebar bırakılmaz. */
function gsx_sidebar(int $exclude = 0, int $cat = 0): void {
    $latest = get_posts(gsx_news_args(['numberposts' => 6, 'post__not_in' => [$exclude], 'fields' => 'ids']));
    $rel = $cat ? get_posts(['numberposts' => 4, 'category' => $cat, 'post__not_in' => [$exclude], 'fields' => 'ids', 'post_status' => 'publish']) : [];
    echo '<aside class="sidebar" aria-label="' . esc_attr(gsx_t('latest')) . '">';
    if ($rel) { echo '<section class="panel"><h2>' . esc_html(gsx_t('related')) . '</h2><ul class="mini-list">'; foreach ($rel as $i) echo '<li><a href="' . esc_url(get_permalink($i)) . '">' . esc_html(get_the_title($i)) . '</a></li>'; echo '</ul></section>'; }
    if ($latest) { echo '<section class="panel"><h2>' . esc_html(gsx_t('latest')) . '</h2><ul class="mini-list">'; foreach ($latest as $i) echo '<li><a href="' . esc_url(get_permalink($i)) . '">' . esc_html(get_the_title($i)) . '</a><div class="meta">' . gsx_time_tag($i, 'short') . '</div></li>'; echo '</ul></section>'; }
    echo '</aside>';
}
