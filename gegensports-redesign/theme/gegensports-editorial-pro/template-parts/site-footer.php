<?php
$home = function_exists('pll_home_url') ? pll_home_url() : home_url('/');
$corp = [['hakkimizda', gsx_t('about')], ['iletisim', gsx_t('contact')], ['yazarlarimiz', gsx_t('authors')], ['kaynak-politikasi', gsx_t('sources')], ['gizlilik-politikasi', 'Gizlilik']];
$exp  = [['rehber', gsx_t('guide')], ['futbol-sozlugu', gsx_t('glossary')], ['taktik-dosyasi', gsx_t('tactics')]];
$ll = gsx_lang_links();
?>
<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a class="brand" href="<?php echo esc_url($home); ?>" style="color:#fff"><span class="brand__mark" style="background:#fff;color:var(--color-primary)" aria-hidden="true">G</span>GEGENSPORTS</a>
        <p style="margin-top:12px;max-width:36ch"><?php echo esc_html(gsx_t('footer_about')); ?></p>
      </div>
      <div><h2><?php echo esc_html(gsx_t('corporate')); ?></h2><ul>
        <?php foreach ($corp as [$s, $n]) { $u = gsx_page_url($s); if ($u) echo '<li><a href="' . esc_url($u) . '">' . esc_html($n) . '</a></li>'; } ?></ul></div>
      <div><h2><?php echo esc_html(gsx_t('scouting')); ?></h2><ul>
        <li><a href="<?php echo esc_url(gsx_page_url('gegen-scout') ?: home_url('/dossier/')); ?>"><?php echo esc_html(gsx_t('scout_center')); ?></a></li>
        <li><a href="<?php echo esc_url(home_url('/dossier/')); ?>"><?php echo esc_html(gsx_t('dossier')); ?></a></li>
        <?php foreach ($exp as [$s, $n]) { $u = gsx_page_url($s); if ($u) echo '<li><a href="' . esc_url($u) . '">' . esc_html($n) . '</a></li>'; } ?></ul></div>
      <div><h2><?php echo esc_html(gsx_t('language')); ?></h2><ul>
        <?php foreach ($ll as $l) echo '<li><a href="' . esc_url($l['url']) . '" hreflang="' . esc_attr($l['slug']) . '">' . esc_html(['tr' => 'Türkçe', 'en' => 'English', 'es' => 'Español'][$l['slug']] ?? strtoupper($l['slug'])) . '</a></li>'; ?></ul></div>
    </div>
    <div class="footer-base"><span>© <?php echo esc_html(wp_date('Y')); ?> GegenSports</span><span><?php echo esc_html(get_bloginfo('description')); ?></span></div>
  </div>
</footer>
<?php gsx_template_part('mobile-nav'); ?>
