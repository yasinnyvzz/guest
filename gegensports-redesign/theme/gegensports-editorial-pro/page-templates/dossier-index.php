<?php
get_header();
$page = max(1, (int) ($_GET['sayfa'] ?? 1));
$pos = sanitize_text_field($_GET['mevki'] ?? '');
$q = sanitize_text_field($_GET['q'] ?? '');
$args = ['page' => $page, 'per_page' => 12] + ($pos ? ['position' => $pos] : []) + ($q ? ['q' => $q] : []);
$res = gsx_reports($args);
$facets = $res['facets']['positions'] ?? [];
?>
<section class="panel-dark scout-hero"><div class="container">
  <?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [gsx_t('dossier'), '']]); ?>
  <h1><?php echo esc_html(gsx_t('dossier_idx')); ?></h1>
  <p><?php echo esc_html(gsx_t('scout_sub')); ?></p>
  <form class="filters" method="get" action="<?php echo esc_url(home_url('/dossier/')); ?>" style="grid-template-columns:1fr">
    <?php if ($facets) : ?>
    <div class="chip-row" role="group" aria-label="<?php echo esc_attr(gsx_t('pos')); ?>">
      <a class="chip" href="<?php echo esc_url(home_url('/dossier/')); ?>"<?php echo !$pos ? ' aria-current="true" style="background:var(--color-primary);color:#fff;border-color:var(--color-primary)"' : ''; ?>><?php echo esc_html(gsx_t('all_pos')); ?></a>
      <?php foreach ($facets as $k => $c) echo '<a class="chip" href="' . esc_url(add_query_arg('mevki', $k, home_url('/dossier/'))) . '"' . ($pos === $k ? ' aria-current="true" style="background:var(--color-primary);color:#fff;border-color:var(--color-primary)"' : '') . '>' . esc_html($k) . '<small>' . (int) $c . '</small></a>'; ?>
    </div><?php endif; ?>
  </form>
</div></section>
<div class="container section">
  <?php if ($res['items']) : ?>
    <div class="player-grid"><?php foreach ($res['items'] as $r) gsx_player_card($r); ?></div>
    <?php if ($res['pages'] > 1) { echo '<nav class="pagination" aria-label="' . esc_attr(gsx_t('page')) . '">'; for ($i = max(1, $page - 2); $i <= min($res['pages'], $page + 2); $i++) echo $i === $page ? '<span class="current">' . $i . '</span>' : '<a href="' . esc_url(add_query_arg(array_filter(['sayfa' => $i, 'mevki' => $pos]), home_url('/dossier/'))) . '">' . $i . '</a>'; echo '</nav>'; } ?>
  <?php else : gsx_empty_state(gsx_t('no_results'), $pos ? sprintf('“%s” — %s', $pos, gsx_t('no_results_d')) : gsx_t('no_results_d'), home_url('/dossier/'), gsx_t('reset')); endif; ?>
</div>
<?php get_footer();
