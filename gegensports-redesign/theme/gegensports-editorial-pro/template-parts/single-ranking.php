<?php
/** Gegen Rankings şablonu. Veri: yazı meta "gsx_ranking" (JSON): {"period","criteria","items":[{"report":"slug","why":"gerekçe"}]}. Oyuncu verisi GPScout API'den çekilir. */
$id = get_the_ID();
$cfg = json_decode((string) get_post_meta($id, 'gsx_ranking', true), true) ?: [];
$rows = [];
foreach ((array) ($cfg['items'] ?? []) as $it) { $r = gsx_report((string) ($it['report'] ?? '')); if ($r) $rows[] = [$r, (string) ($it['why'] ?? '')]; }
?>
<header class="archive-head"><div class="container">
  <?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [gsx_t('rankings'), gsx_page_url('gegen-rankings')], [get_the_title(), '']]); ?>
  <h1 style="max-width:22ch"><?php the_title(); ?></h1>
  <?php $d = gsx_dek($id); if ($d) echo '<p>' . esc_html($d) . '</p>'; ?>
  <dl class="kv" style="max-width:640px;margin-top:20px;text-align:left">
    <?php if (!empty($cfg['period'])) echo '<dt>' . esc_html(gsx_t('period')) . '</dt><dd>' . esc_html($cfg['period']) . '</dd>'; ?>
    <?php if (!empty($cfg['criteria'])) echo '<dt>' . esc_html(gsx_t('criteria')) . '</dt><dd>' . esc_html($cfg['criteria']) . '</dd>'; ?>
    <dt><?php echo esc_html(gsx_t('by')); ?></dt><dd><?php the_author(); ?></dd>
  </dl>
</div></header>
<div class="container" style="max-width:960px">
  <?php if ($rows) : foreach ($rows as $n => [$r, $why]) { $p = $r['player'] ?? []; ?>
    <article class="rank-item"><div class="rank-item__no"><?php echo str_pad((string) ($n + 1), 2, '0', STR_PAD_LEFT); ?></div>
      <div class="rank-item__body">
        <div class="player-card__photo" style="width:200px;height:200px;max-width:100%"><?php if (!empty($p['photo'])) echo '<img src="' . esc_url($p['photo']) . '" alt="' . esc_attr($p['name'] ?? '') . '" loading="lazy" width="200" height="200">'; ?></div>
        <div>
          <h2 style="font-size:1.375rem"><a href="<?php echo esc_url(gsx_report_url($r['slug'])); ?>"><?php echo esc_html(gsx_clean_text($p['name'] ?? $r['title'])); ?></a></h2>
          <ul class="player-card__facts" style="margin:6px 0 12px"><li><strong><?php echo esc_html($p['club'] ?? ''); ?></strong></li><li><?php echo (int) ($p['age'] ?? 0); ?> <?php echo esc_html(strtolower(gsx_t('age'))); ?></li><li><span class="pos"><?php echo esc_html($p['position'] ?? ''); ?></span></li></ul>
          <?php if ($why) echo '<p>' . esc_html($why) . '</p>'; ?>
          <a class="btn btn--ghost" href="<?php echo esc_url(gsx_report_url($r['slug'])); ?>"><?php echo esc_html(gsx_t('read_report')); ?></a>
        </div></div></article>
  <?php } ?>
  <section style="margin-top:48px"><?php gsx_section_head(gsx_t('compare')); ?>
    <div class="table-scroll"><table class="table"><thead><tr><th>#</th><th><?php echo esc_html(gsx_t('players')); ?></th><th><?php echo esc_html(gsx_t('club')); ?></th><th class="num"><?php echo esc_html(gsx_t('age')); ?></th><th><?php echo esc_html(gsx_t('foot')); ?></th><th class="num"><?php echo esc_html(gsx_t('height')); ?></th></tr></thead><tbody>
    <?php foreach ($rows as $n => [$r]) { $p = $r['player'] ?? []; ?><tr><td><?php echo (int) $n + 1; ?></td><td><a href="<?php echo esc_url(gsx_report_url($r['slug'])); ?>"><strong><?php echo esc_html(gsx_clean_text($p['name'] ?? '')); ?></strong></a></td><td><?php echo esc_html($p['club'] ?? '—'); ?></td><td class="num"><?php echo !empty($p['age']) ? (int) $p['age'] : '<span class="na">—</span>'; ?></td><td><?php echo !empty($p['foot']) ? esc_html($p['foot']) : '<span class="na">—</span>'; ?></td><td class="num"><?php echo !empty($p['height']) ? (int) $p['height'] . ' cm' : '<span class="na">—</span>'; ?></td></tr><?php } ?>
    </tbody></table></div></section>
  <?php else : gsx_empty_state(gsx_t('no_data'), ''); endif; ?>
  <div class="prose" style="margin-top:32px"><?php the_content(); ?></div>
</div>
