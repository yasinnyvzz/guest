<?php
get_header(); the_post();
$id = get_the_ID();
if (get_post_meta($id, 'gsx_ranking', true)) { get_template_part('template-parts/single-ranking'); get_footer(); return; }
$term = gsx_primary_term($id);
$dek = gsx_dek($id);
$upd = gsx_updated_ts($id);
$author = get_the_author_meta('display_name');
$cap = has_post_thumbnail() ? wp_get_attachment_caption(get_post_thumbnail_id()) : '';
$trail = [[gsx_t('home'), home_url('/')]];
if ($term) { $anc = array_reverse(get_ancestors($term->term_id, 'category')); foreach ($anc as $a) { $t = get_term($a, 'category'); $trail[] = [html_entity_decode($t->name), get_term_link($t)]; } $trail[] = [html_entity_decode($term->name), get_term_link($term)]; }
$trail[] = [get_the_title(), ''];
$is_scout = gsx_is_scout_post($id);
?>
<div class="container section">
  <div class="layout">
    <article class="article">
      <header class="article__head">
        <?php gsx_breadcrumbs($trail); ?>
        <h1><?php the_title(); ?></h1>
        <?php if ($dek) echo '<p class="article__dek">' . esc_html($dek) . '</p>'; ?>
        <div class="byline">
          <span><?php echo esc_html(gsx_t('by')); ?> <strong><a href="<?php echo esc_url(get_author_posts_url(get_the_author_meta('ID'))); ?>"><?php echo esc_html($author); ?></a></strong></span>
          <span><?php echo gsx_time_tag($id); ?></span>
          <?php if ($is_scout) echo '<span>' . esc_html(gsx_lang() === 'tr' ? 'Editoryal scouting analizi' : 'Editorial scouting analysis') . '</span>'; ?>
          <?php if ($upd) echo '<span>' . esc_html(gsx_t('updated')) . ': <time datetime="' . esc_attr(gmdate('c', $upd)) . '">' . esc_html(gsx_date($upd)) . '</time></span>'; ?>
          <span><?php echo (int) gsx_reading_minutes(get_the_content()); ?> <?php echo esc_html(gsx_t('min_read')); ?></span>
        </div>
      </header>
      <?php if (has_post_thumbnail()) : ?>
        <figure class="article__cover"><?php echo gsx_thumb($id, 'gsx-lead', true); ?><?php if ($cap) echo '<figcaption>' . esc_html($cap) . '</figcaption>'; ?></figure>
      <?php endif; ?>
      <div class="prose"><?php the_content(); ?></div>
      <?php if ($is_scout) : ?>
      <aside class="disclosure" style="margin-top:32px"><h2><?php echo esc_html(gsx_t('sources')); ?></h2><?php echo esc_html(gsx_t('src_note')); ?></aside>
      <?php endif; ?>
    </article>
    <?php gsx_sidebar($id, $term ? $term->term_id : 0); ?>
  </div>
</div>
<?php get_footer();
