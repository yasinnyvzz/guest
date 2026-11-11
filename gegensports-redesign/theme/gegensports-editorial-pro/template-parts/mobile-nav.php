<?php
$scout_url = gsx_page_url('gegen-scout') ?: home_url('/dossier/');
$cur = is_front_page() ? 'home' : (get_query_var('gsx_view') === 'news' ? 'news' : '');
$home = function_exists('pll_home_url') ? pll_home_url() : home_url('/');
?>
<nav class="bottom-nav" aria-label="<?php echo esc_attr(gsx_t('menu')); ?>">
  <a href="<?php echo esc_url($home); ?>"<?php echo $cur === 'home' ? ' aria-current="page"' : ''; ?>><?php echo gsx_icon('home'); ?><?php echo esc_html(gsx_t('home')); ?></a>
  <a href="<?php echo esc_url(gsx_news_url()); ?>"<?php echo $cur === 'news' ? ' aria-current="page"' : ''; ?>><?php echo gsx_icon('news'); ?><?php echo esc_html(gsx_t('news')); ?></a>
  <a href="<?php echo esc_url($scout_url); ?>"><?php echo gsx_icon('user'); ?><?php echo esc_html(gsx_t('players')); ?></a>
  <a href="<?php echo esc_url(home_url('/dossier/')); ?>"><?php echo gsx_icon('radar'); ?><?php echo esc_html(gsx_t('scouting')); ?></a>
  <button type="button" data-gsx-drawer aria-controls="drawer" aria-expanded="false"><?php echo gsx_icon('menu'); ?><?php echo esc_html(gsx_t('menu')); ?></button>
</nav>
