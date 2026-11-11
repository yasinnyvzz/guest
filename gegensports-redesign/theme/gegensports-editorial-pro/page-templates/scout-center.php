<?php
/* Template Name: Gegen Scout Merkezi */
get_header();
$page = max(1, (int) ($_GET['sayfa'] ?? 1));
$pos = sanitize_text_field($_GET['mevki'] ?? '');
$res = gsx_reports(['page' => $page, 'per_page' => 12] + ($pos ? ['position' => $pos] : []));
$facets = $res['facets']['positions'] ?? [];
?>
<section class="panel-dark scout-hero"><div class="container">
  <div class="kicker" style="color:#ff9a80">GEGEN SCOUT</div>
  <h1><?php echo esc_html(gsx_t('scout_sub')); ?></h1>
  <p><?php echo esc_html(gsx_lang() === 'tr' ? 'Oyuncu ara, mevkiye göre filtrele, scout dosyalarını incele.' : 'Search players, filter by position, browse scouting files.'); ?></p>
  <form class="filters" method="get" action="<?php echo esc_url(get_permalink()); ?>">
    <input type="search" name="q" placeholder="<?php echo esc_attr(gsx_t('search_ph')); ?>" aria-label="<?php echo esc_attr(gsx_t('search')); ?>">
    <select name="mevki" aria-label="<?php echo esc_attr(gsx_t('pos')); ?>"><option value=""><?php echo esc_html(gsx_t('all_pos')); ?></option><?php foreach ($facets as $k => $c) echo '<option' . selected($pos, $k, false) . ' value="' . esc_attr($k) . '">' . esc_html($k) . ' (' . (int) $c . ')</option>'; ?></select>
    <button class="btn btn--accent" type="submit"><?php echo esc_html(gsx_t('apply')); ?></button>
  </form>
  <p class="filter-note"><?php echo (int) $res['total']; ?> <?php echo esc_html(gsx_t('posts')); ?></p>
</div></section>
<div class="container section">
  <?php if ($res['items']) : ?><div class="player-grid"><?php foreach ($res['items'] as $r) gsx_player_card($r); ?></div>
  <?php else : gsx_empty_state(gsx_t('no_results'), gsx_t('no_results_d'), get_permalink(), gsx_t('reset')); endif; ?>
  <div style="margin-top:32px"><a class="btn" href="<?php echo esc_url(home_url('/dossier/')); ?>"><?php echo esc_html(gsx_t('dossier_idx')); ?> →</a></div>
</div>
<?php get_footer();
