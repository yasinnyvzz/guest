<?php get_header(); ?>
<div class="container">
  <header class="archive-head"><?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [gsx_t('all_news'), '']]); ?><h1><?php echo esc_html(gsx_t('all_news')); ?></h1></header>
  <?php if (have_posts()) : ?>
    <div class="card-grid card-grid--3"><?php while (have_posts()) { the_post(); gsx_card(get_the_ID()); } ?></div>
    <?php gsx_pagination(); ?>
  <?php else : gsx_empty_state(gsx_t('no_results'), gsx_t('no_results_d'), home_url('/'), gsx_t('home')); endif; ?>
</div>
<?php get_footer();
