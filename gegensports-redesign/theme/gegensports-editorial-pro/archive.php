<?php
// Kategori / etiket / yazar arşivi — takım, lig ve scouting arşivleri aynı şablonu kullanır (URL'ler değişmez).
get_header();
$term = is_category() || is_tag() ? get_queried_object() : null;
$is_team_or_league = $term && is_category();
$kicker = is_category() ? (($term && $term->parent) ? gsx_t('team_hub') : gsx_t('league_hub')) : (is_author() ? gsx_t('author') : gsx_t('archive_of'));
$title = is_author() ? get_the_author_meta('display_name', get_queried_object_id()) : html_entity_decode(single_term_title('', false) ?: get_the_archive_title());
$desc = $term ? term_description() : (is_author() ? get_the_author_meta('description', get_queried_object_id()) : '');
$has_data = $term && $term->count > 0;
$items = [];
while (have_posts()) { the_post(); $items[] = get_the_ID(); }
$first = $items[0] ?? 0; $grid = array_slice($items, 1, 2); $more = array_slice($items, 3);
?>
<header class="archive-head panel-dark" style="padding-block:32px 28px;margin-bottom:32px"><div class="container">
  <div class="breadcrumbs" style="color:var(--color-on-dark-muted)"><?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [$title, '']]); ?></div>
  <div class="kicker" style="color:#ff9a80"><?php echo esc_html($kicker); ?></div>
  <h1 style="color:#fff"><?php echo esc_html($title); ?></h1>
  <?php if ($desc) echo '<div class="muted" style="max-width:64ch">' . wp_kses_post($desc) . '</div>'; ?>
  <?php if ($term) echo '<p class="meta" style="margin-top:12px">' . number_format_i18n((int) $term->count) . ' ' . esc_html(gsx_t('posts')) . '</p>'; ?>
</div></header>
<div class="container">
<?php if ($items) : ?>
  <div class="layout">
    <div>
      <?php if ($first) : ?><div style="margin-bottom:32px"><?php gsx_lead_story($first); ?></div><?php endif; ?>
      <?php if ($grid) : ?><div class="card-grid" style="margin-bottom:32px"><?php foreach ($grid as $i) gsx_card($i); ?></div><?php endif; ?>
      <?php if ($more) : ?><ul class="news-list"><?php foreach ($more as $i) gsx_news_row($i); ?></ul><?php endif; ?>
      <?php gsx_pagination(); ?>
    </div>
    <?php gsx_sidebar(0, $term ? $term->term_id : 0); ?>
  </div>
<?php else : gsx_empty_state(gsx_t('no_results'), gsx_t('no_results_d'), home_url('/'), gsx_t('home')); endif; ?>
</div>
<?php get_footer();
