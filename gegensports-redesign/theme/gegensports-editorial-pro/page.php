<?php get_header(); the_post(); ?>
<div class="container section"><div class="layout"><article class="article"><header class="article__head"><?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [get_the_title(), '']]); ?><h1><?php the_title(); ?></h1></header><div class="prose"><?php the_content(); ?></div></article><?php gsx_sidebar(get_the_ID()); ?></div></div>
<?php get_footer();
