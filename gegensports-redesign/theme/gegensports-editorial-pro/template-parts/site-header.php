<?php
$lang = gsx_lang();
$logo = has_custom_logo() ? get_custom_logo() : '';
$scout_url = gsx_page_url('gegen-scout') ?: home_url('/dossier/');
$leagues = [['super-lig','Süper Lig'],['premier-league','Premier League'],['la-liga','La Liga'],['serie-a','Serie A'],['bundesliga','Bundesliga'],['ligue-1','Ligue 1'],['1-lig','1. Lig'],['sampiyonlar-ligi','Şampiyonlar Ligi']];
$matches = gsx_match_data();
?>
<a class="skip-link" href="#main"><?php echo esc_html($lang === 'tr' ? 'İçeriğe geç' : ($lang === 'es' ? 'Saltar al contenido' : 'Skip to content')); ?></a>
<header class="site-header">
  <div class="container site-header__bar">
    <a class="brand" href="<?php echo esc_url(function_exists('pll_home_url') ? pll_home_url() : home_url('/')); ?>" aria-label="GegenSports — <?php echo esc_attr(gsx_t('home')); ?>">
      <?php if ($logo) { echo wp_get_attachment_image(get_theme_mod('custom_logo'), 'full', false, ['alt' => 'GegenSports']); } else { ?>
        <span class="brand__mark" aria-hidden="true">G</span><span class="brand__word">GEGEN<span>SPORTS</span></span>
      <?php } ?>
    </a>
    <nav class="primary-nav" aria-label="<?php echo esc_attr(gsx_t('menu')); ?>">
      <ul>
        <li><a href="<?php echo esc_url(gsx_news_url()); ?>"<?php echo get_query_var('gsx_view') === 'news' ? ' aria-current="page"' : ''; ?>><?php echo esc_html(gsx_t('news')); ?></a></li>
        <?php if ($matches) : ?><li><a href="<?php echo esc_url(gsx_page_url('maclar') ?: '#'); ?>"><?php echo esc_html(gsx_t('matches')); ?></a></li><?php endif; ?>
        <li><details class="nav-drop"><summary><?php echo esc_html(gsx_t('leagues')); ?></summary>
          <div class="nav-drop__panel">
            <?php foreach ($leagues as [$s, $n]) { $u = gsx_term_url($s); if ($u) echo '<a href="' . esc_url($u) . '">' . esc_html($n) . '</a>'; } ?>
          </div></details></li>
        <li><a href="<?php echo esc_url($scout_url); ?>"><?php echo esc_html(gsx_t('players')); ?></a></li>
        <li><details class="nav-drop"><summary><?php echo esc_html(gsx_t('scouting')); ?></summary>
          <div class="nav-drop__panel">
            <a href="<?php echo esc_url($scout_url); ?>"><?php echo esc_html(gsx_t('scout_center')); ?></a>
            <a href="<?php echo esc_url(home_url('/dossier/')); ?>"><?php echo esc_html(gsx_t('dossier')); ?></a>
            <?php foreach ([['scout-raporlari','Scout raporları'],['gp-report','GP Report'],['gp-radar','GP Radar'],['gp-watch','GP Watch'],['gp-signal','GP Signal']] as [$s,$n]) { $u = gsx_term_url($s); if ($u) echo '<a href="' . esc_url($u) . '">' . esc_html($n) . '</a>'; } ?>
          </div></details></li>
        <?php $au = gsx_term_url('analiz') ?: gsx_term_url('analiz-en'); if ($au) : ?><li><a href="<?php echo esc_url($au); ?>"><?php echo esc_html(gsx_t('analysis')); ?></a></li><?php endif; ?>
      </ul>
    </nav>
    <div class="header-tools">
      <?php $ll = gsx_lang_links(); if ($ll) : ?>
      <div class="lang-switch" role="group" aria-label="<?php echo esc_attr(gsx_t('language')); ?>">
        <?php foreach ($ll as $l) echo '<a href="' . esc_url($l['url']) . '" hreflang="' . esc_attr($l['slug']) . '"' . ($l['current'] ? ' aria-current="true"' : '') . '>' . esc_html(strtoupper($l['slug'])) . '</a>'; ?>
      </div>
      <?php endif; ?>
      <button class="icon-btn" type="button" data-gsx-search aria-expanded="false" aria-controls="search-panel" aria-label="<?php echo esc_attr(gsx_t('search')); ?>"><?php echo gsx_icon('search'); ?></button>
      <button class="icon-btn menu-btn" type="button" data-gsx-drawer aria-expanded="false" aria-controls="drawer" aria-label="<?php echo esc_attr(gsx_t('menu')); ?>"><?php echo gsx_icon('menu'); ?></button>
    </div>
  </div>
  <?php
  $sec = [
    ['transfer', gsx_t('transfers'), 'term'], ['super-lig', 'Süper Lig', 'term'], ['premier-league', 'Premier League', 'term'],
    ['genc-yetenek-hub', gsx_t('young'), 'page'], ['gegen-rankings', gsx_t('rankings'), 'page'], ['gegen-fit', gsx_t('fit'), 'page'],
  ];
  $items = [];
  foreach ($sec as [$s, $n, $k]) { $u = $k === 'term' ? gsx_term_url($s) : gsx_page_url($s); if ($u) $items[] = [$n, $u]; }
  $items[] = [gsx_t('dossier'), home_url('/dossier/')];
  ?>
  <div class="secondary-nav"><div class="container"><ul>
    <?php foreach ($items as [$n, $u]) echo '<li><a href="' . esc_url($u) . '">' . esc_html($n) . '</a></li>'; ?>
  </ul></div></div>
  <div class="search-panel" id="search-panel"><div class="container">
    <form class="search-form" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>">
      <label class="screen-reader-text" for="hs"><?php echo esc_html(gsx_t('search')); ?></label>
      <input id="hs" type="search" name="s" placeholder="<?php echo esc_attr(gsx_t('search_ph')); ?>" value="<?php echo esc_attr(get_search_query()); ?>">
      <button class="btn" type="submit"><?php echo esc_html(gsx_t('search')); ?></button>
    </form>
  </div></div>
</header>
<div class="drawer" id="drawer" role="dialog" aria-modal="true" aria-label="<?php echo esc_attr(gsx_t('menu')); ?>">
  <div class="drawer__scrim" data-gsx-drawer-close></div>
  <div class="drawer__panel">
    <div class="drawer__head"><strong><?php echo esc_html(gsx_t('menu')); ?></strong><button class="icon-btn" type="button" data-gsx-drawer-close aria-label="Kapat / Close"><?php echo gsx_icon('close'); ?></button></div>
    <ul>
      <li><a href="<?php echo esc_url(gsx_news_url()); ?>"><?php echo esc_html(gsx_t('news')); ?></a></li>
      <li><a href="<?php echo esc_url($scout_url); ?>"><?php echo esc_html(gsx_t('players')); ?></a></li>
      <li><a href="<?php echo esc_url(home_url('/dossier/')); ?>"><?php echo esc_html(gsx_t('dossier')); ?></a></li>
      <?php foreach ($items as [$n, $u]) echo '<li><a href="' . esc_url($u) . '">' . esc_html($n) . '</a></li>'; ?>
    </ul>
    <h2><?php echo esc_html(gsx_t('leagues')); ?></h2>
    <ul><?php foreach ($leagues as [$s, $n]) { $u = gsx_term_url($s); if ($u) echo '<li><a href="' . esc_url($u) . '">' . esc_html($n) . '</a></li>'; } ?></ul>
    <?php if ($ll) : ?><h2><?php echo esc_html(gsx_t('language')); ?></h2>
    <ul><?php foreach ($ll as $l) echo '<li><a href="' . esc_url($l['url']) . '" hreflang="' . esc_attr($l['slug']) . '">' . esc_html(strtoupper($l['slug'])) . '</a></li>'; ?></ul><?php endif; ?>
  </div>
</div>
