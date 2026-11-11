<?php get_header();
// SECTION 02 — Football strip: yalnızca gerçek maç verisi varsa
$matches = gsx_match_data();
if ($matches) { echo '<div class="section" style="padding-block:12px"><div class="container"><ul class="chip-row">'; foreach ($matches as $m) echo '<li class="chip">' . esc_html($m['label'] ?? '') . '</li>'; echo '</ul></div></div>'; }

// SECTION 03/04 — Lead + yan haberler + son haberler (scout raporları hariç: haber ≠ scouting)
$pool = get_posts(gsx_news_args(['numberposts' => 20, 'fields' => 'ids']));
$with_img = array_values(array_filter($pool, 'has_post_thumbnail'));
$lead = $with_img[0] ?? ($pool[0] ?? 0);
$rest = array_values(array_diff($pool, [$lead]));
$side = array_slice(array_values(array_filter($rest, 'has_post_thumbnail')), 0, 3);
$latest = array_slice(array_values(array_diff($rest, $side)), 0, 10);
?>
<section class="section" aria-labelledby="lead-h">
  <div class="container">
    <h1 class="screen-reader-text" id="lead-h"><?php echo esc_html(get_bloginfo('name') . ' — ' . get_bloginfo('description')); ?></h1>
    <?php if ($lead) : ?>
    <div class="grid-12">
      <div style="grid-column:span 7"><?php gsx_lead_story($lead); ?></div>
      <div style="grid-column:span 5">
        <?php foreach ($side as $i) gsx_side_story($i); ?>
      </div>
    </div>
    <style>@media(max-width:899px){.grid-12>div{grid-column:auto!important}}</style>
    <?php else : gsx_empty_state(gsx_t('no_results'), gsx_t('no_results_d')); endif; ?>
  </div>
</section>

<?php if ($latest) : ?>
<section class="section" style="padding-top:0" aria-labelledby="latest-h">
  <div class="container">
    <div class="section-head"><h2 id="latest-h"><?php echo esc_html(gsx_t('latest')); ?></h2><a href="<?php echo esc_url(gsx_news_url()); ?>"><?php echo esc_html(gsx_t('all_news')); ?> →</a></div>
    <ul class="news-list"><?php foreach ($latest as $i) gsx_news_row($i); ?></ul>
  </div>
</section>
<?php endif; ?>

<?php // SECTION 05 — Scouting spotlight (koyu, kontrollü panel)
$scout_posts = get_posts(gsx_scout_args(['numberposts' => 3, 'fields' => 'ids']));
$use_api = gsx_lang() === 'tr';
$cards = [];
if ($use_api) { $r = gsx_reports(['per_page' => 3]); $cards = $r['items']; }
if ($cards || $scout_posts) : ?>
<section class="panel-dark scout-feature" aria-labelledby="scout-h">
  <div class="container">
    <div class="section-head"><div><h2 id="scout-h"><?php echo esc_html(gsx_t('scout_spot')); ?></h2><p class="muted"><?php echo esc_html(gsx_t('scout_spot_sub')); ?></p></div>
      <a href="<?php echo esc_url(gsx_page_url('gegen-scout') ?: home_url('/dossier/')); ?>" style="color:#fff"><?php echo esc_html(gsx_t('scout_center')); ?> →</a></div>
    <div class="player-grid">
      <?php if ($cards) { foreach ($cards as $c) gsx_player_card($c); }
      else { foreach ($scout_posts as $i) { $t = gsx_primary_term($i); gsx_player_card(['title' => get_the_title($i), 'url' => get_permalink($i), 'excerpt' => gsx_blurb($i, 24), 'player' => ['position' => '', 'photo' => get_the_post_thumbnail_url($i, 'gsx-thumb')]]); } } ?>
    </div>
  </div>
</section>
<?php endif; ?>

<?php // SECTION 06 — Transfer
$tr_url = gsx_term_url('transfer');
$tr = $tr_url ? get_posts(gsx_news_args(['numberposts' => 4, 'fields' => 'ids', 'category_name' => 'transfer'])) : [];
if ($tr) : ?>
<section class="section" aria-labelledby="tr-h"><div class="container">
  <div class="section-head"><div><h2 id="tr-h"><?php echo esc_html(gsx_t('transfer_sec')); ?></h2><p><?php echo esc_html(gsx_t('transfer_note')); ?></p></div><a href="<?php echo esc_url($tr_url); ?>"><?php echo esc_html(gsx_t('all')); ?> →</a></div>
  <div class="card-grid card-grid--4"><?php foreach ($tr as $i) gsx_card($i); ?></div>
</div></section>
<?php endif; ?>

<?php // SECTION 07 — Gegen Rankings: yalnızca ranking içeriği varsa
$rk = get_posts(['numberposts' => 3, 'post_status' => 'publish', 'meta_key' => 'gsx_ranking', 'fields' => 'ids']);
if ($rk) : ?>
<section class="section" aria-labelledby="rk-h"><div class="container">
  <?php gsx_section_head(gsx_t('rankings'), '', gsx_page_url('gegen-rankings')); ?>
  <div class="ranking-grid"><?php foreach ($rk as $i) { $n = count((array) json_decode((string) get_post_meta($i, 'gsx_ranking', true), true)['items'] ?? []); ?>
    <a class="ranking-card" href="<?php echo esc_url(get_permalink($i)); ?>"><span class="ranking-card__n"><?php echo (int) $n; ?></span><h3><?php echo esc_html(get_the_title($i)); ?></h3><span class="muted"><?php echo gsx_time_tag($i); ?></span></a>
  <?php } ?></div>
</div></section>
<?php endif; ?>

<?php // SECTION 08 — Lig kapsamı: veri yoksa yalnızca içerik bağlantıları
$lg = [['super-lig','Süper Lig'],['premier-league','Premier League'],['la-liga','La Liga'],['serie-a','Serie A'],['bundesliga','Bundesliga'],['ligue-1','Ligue 1']];
$tiles = [];
foreach ($lg as [$s, $n]) { $t = get_term_by('slug', $s, 'category'); $u = gsx_term_url($s); if ($t && $u) $tiles[] = [$n, $u, (int) $t->count]; }
if ($tiles) : ?>
<section class="section" aria-labelledby="lg-h"><div class="container">
  <div class="section-head"><div><h2 id="lg-h"><?php echo esc_html(gsx_t('league_cov')); ?></h2><p><?php echo esc_html(gsx_t('league_sub')); ?></p></div></div>
  <div class="league-grid"><?php foreach ($tiles as [$n, $u, $c]) echo '<a class="league-tile" href="' . esc_url($u) . '"><strong>' . esc_html($n) . '</strong><span>' . number_format_i18n($c) . ' ' . esc_html(gsx_t('posts')) . '</span></a>'; ?></div>
</div></section>
<?php endif; ?>

<?php // SECTION 09 — Analiz ve görüş
$an = get_posts(['numberposts' => 3, 'post_status' => 'publish', 'fields' => 'ids', 'category_name' => gsx_lang() === 'en' ? 'analiz-en' : (gsx_lang() === 'es' ? 'analiz-es' : 'analiz')]);
if ($an) : ?>
<section class="section" aria-labelledby="an-h"><div class="container">
  <div class="section-head"><div><h2 id="an-h"><?php echo esc_html(gsx_t('opinion')); ?></h2><p><?php echo esc_html(gsx_t('opinion_sub')); ?></p></div></div>
  <div class="card-grid card-grid--3"><?php foreach ($an as $i) gsx_card($i); ?></div>
</div></section>
<?php endif; ?>
<?php get_footer();
