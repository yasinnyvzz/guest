<?php get_header(); global $wp_query; ?>
<div class="container">
  <header class="archive-head"><?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [gsx_t('search'), '']]); ?>
    <h1><?php echo esc_html(sprintf('“%s”', get_search_query())); ?></h1>
    <p><?php echo (int) $wp_query->found_posts; ?> <?php echo esc_html(gsx_t('posts')); ?></p>
    <form class="search-form" role="search" method="get" action="<?php echo esc_url(home_url('/')); ?>" style="margin-top:16px;max-width:560px">
      <label class="screen-reader-text" for="sq"><?php echo esc_html(gsx_t('search')); ?></label>
      <input id="sq" type="search" name="s" value="<?php echo esc_attr(get_search_query()); ?>"><button class="btn" type="submit"><?php echo esc_html(gsx_t('search')); ?></button></form></header>
  <?php if (have_posts()) : ?>
    <ul class="news-list"><?php while (have_posts()) { the_post(); gsx_news_row(get_the_ID()); } ?></ul>
    <?php gsx_pagination(); ?>
  <?php else : gsx_empty_state(gsx_t('no_results'), gsx_t('no_results_d'), gsx_news_url(), gsx_t('all_news')); endif; ?>
</div>
<?php get_footer();
