<?php
/** Gegen Dossier — oyuncu dosyası. Veri: GPScout /reports/{slug}. Veri yoksa bileşen gizlenir; sahte puan üretilmez. */
get_header();
$r = gsx_report((string) get_query_var('gsx_report'));
$p = $r['player'] ?? [];
$name = gsx_clean_text($p['name'] ?? $r['title']);
$strong = array_values(array_filter((array) ($r['highlights']['strong'] ?? []), fn($s) => trim((string) $s) !== ''));
$weak = array_values(array_filter((array) ($r['highlights']['weak'] ?? []), fn($s) => trim((string) $s) !== ''));
$ev = (array) ($r['scoutEval'] ?? []);
$created = !empty($r['createdAt']) ? strtotime($r['createdAt']) : 0;
$body = gsx_clean_text(wp_strip_all_tags($r['content'] ?? ''));
$paras = array_filter(array_map('trim', preg_split('/\n+/', wp_strip_all_tags(str_replace('</p>', "</p>\n", $r['content'] ?? '')))));
$kind = ($r['reportKind'] ?? '') === 'mac' ? 'Maç gözlemi' : (($r['reportKind'] ?? '') === 'istihbarat' ? 'Veri ve kaynak taraması' : 'Scout raporu');
?>
<section class="panel-dark dossier-head"><div class="container">
  <div class="breadcrumbs" style="color:var(--color-on-dark-muted)"><?php gsx_breadcrumbs([[gsx_t('home'), home_url('/')], [gsx_t('dossier'), home_url('/dossier/')], [$name, '']]); ?></div>
  <div class="dossier-head__grid">
    <div class="dossier-photo"><?php if (!empty($p['photo'])) echo '<img src="' . esc_url($p['photo']) . '" alt="' . esc_attr($name) . '" width="160" height="160" fetchpriority="high">'; ?></div>
    <div>
      <div class="kicker" style="color:#ff9a80"><?php echo esc_html(gsx_t('dossier')); ?> · <?php echo esc_html($kind); ?></div>
      <h1><?php echo esc_html($name); ?></h1>
      <ul class="fact-strip">
        <?php foreach ([[gsx_t('club'), $p['club'] ?? ''], [gsx_t('pos'), $p['position'] ?? ''], [gsx_t('age'), !empty($p['age']) ? (int) $p['age'] : ''], [gsx_t('nation'), (isset($p['nationality']) && strlen($p['nationality']) > 2) ? $p['nationality'] : ''], [gsx_t('foot'), $p['foot'] ?? ''], [gsx_t('height'), !empty($p['height']) ? (int) $p['height'] . ' cm' : '']] as [$k, $v]) if ($v !== '') echo '<li>' . esc_html($k) . '<strong>' . esc_html((string) $v) . '</strong></li>'; ?>
      </ul>
      <?php if ($created) echo '<p class="meta" style="margin:16px 0 0">' . esc_html(gsx_t('author')) . ': ' . esc_html($r['author']['displayName'] ?? '—') . ' · ' . esc_html(gsx_date($created)) . '</p>'; ?>
    </div>
  </div>
</div></section>

<div class="container"><div class="layout" style="margin-top:0">
  <div>
    <?php if ($strong || $weak || !empty($ev['tactical_fit']) || !empty($ev['observation_confidence'])) : ?>
    <section class="verdict" aria-labelledby="verdict-h">
      <h2 id="verdict-h"><?php echo esc_html(gsx_t('verdict')); ?> · <?php echo esc_html(gsx_t('verdict_sub')); ?></h2>
      <?php if (!empty($r['tactic'][0])) echo '<p style="font-size:1.125rem;font-weight:700;margin:0 0 16px">' . esc_html(gsx_t('role')) . ': ' . esc_html(implode(' · ', array_slice((array) $r['tactic'], 0, 2))) . '</p>'; ?>
      <div class="verdict__grid">
        <?php if ($strong) { echo '<div class="verdict__good"><h3>' . esc_html(gsx_t('strengths')) . '</h3><ul>'; foreach ($strong as $s) echo '<li>' . esc_html($s) . '</li>'; echo '</ul></div>'; } ?>
        <?php if ($weak) { echo '<div class="verdict__risk"><h3>' . esc_html(gsx_t('questions')) . '</h3><ul>'; foreach ($weak as $s) echo '<li>' . esc_html($s) . '</li>'; echo '</ul></div>'; } ?>
        <?php if (!empty($ev['tactical_fit'])) echo '<div><h3>' . esc_html(gsx_t('fit_label')) . '</h3><p style="margin:0">' . esc_html($ev['tactical_fit']) . '</p></div>'; ?>
        <?php if (!empty($ev['observation_confidence'])) echo '<div><h3>' . esc_html(gsx_t('reliab')) . '</h3><p style="margin:0">' . esc_html($ev['observation_confidence']) . '</p></div>'; ?>
      </div>
      <p class="verdict__foot">Bu özet, rapor yazarının notlarından derlenmiştir; kendi başına bir izlenmiş-maç gözlemi değildir.</p>
    </section>
    <?php endif; ?>

    <?php if ($paras) : ?><section class="panel"><h2><?php echo esc_html(gsx_t('career')); ?></h2><div class="prose"><?php foreach ($paras as $t) echo '<p>' . esc_html(gsx_clean_text($t)) . '</p>'; ?></div></section><?php endif; ?>

    <?php if (!empty($r['recommendation'])) : ?><section class="panel"><h2><?php echo esc_html(gsx_lang() === 'tr' ? 'Yazarın önerisi' : 'Author recommendation'); ?></h2><p style="margin:0"><?php echo esc_html($r['recommendation']); ?></p></section><?php endif; ?>

    <?php $fm = (array) ($r['hiddenAttrs'] ?? []); $labels = ['sureklilik' => 'Süreklilik', 'onemli_mac' => 'Önemli maçlar', 'baski' => 'Baskı altında', 'profesyonellik' => 'Profesyonellik', 'hirs' => 'Hırs', 'uyum' => 'Uyum'];
    if ($fm) : ?>
    <section class="panel"><h2><?php echo esc_html(gsx_t('fm_panel')); ?></h2><p class="muted" style="font-size:.875rem"><?php echo esc_html(gsx_t('fm_note')); ?></p>
      <?php foreach ($labels as $k => $lab) if (isset($fm[$k])) { $v = (int) $fm[$k]; echo '<div class="bar"><span>' . esc_html($lab) . '</span><span class="bar__track"><span class="bar__fill" style="width:' . (int) round($v / 20 * 100) . '%"></span></span><strong>' . $v . '</strong></div>'; } ?>
    </section><?php endif; ?>
  </div>

  <aside class="sidebar">
    <section class="panel"><h2><?php echo esc_html(gsx_t('profile')); ?></h2>
      <dl class="kv">
        <?php foreach ((array) ($r['playerProfile'] ?? []) as $k => $v) if (trim((string) $v) !== '' && !in_array($k, ['Kulüp', 'Mevki', 'Boy'], true)) echo '<dt>' . esc_html($k) . '</dt><dd>' . esc_html($v) . '</dd>'; ?>
        <?php if (!empty($p['club'])) echo '<dt>' . esc_html(gsx_t('club')) . '</dt><dd>' . esc_html($p['club']) . '</dd>'; ?>
      </dl></section>
    <?php if (!empty($r['statsLink'])) : ?><section class="disclosure"><h3><?php echo esc_html(gsx_t('sources')); ?></h3><a href="<?php echo esc_url($r['statsLink']); ?>" rel="noopener nofollow" target="_blank"><?php echo esc_html(gsx_t('external_stats')); ?>: <?php echo esc_html(preg_replace('#^https?://(www\.)?([^/]+).*#', '$2', $r['statsLink'])); ?></a></section><?php endif; ?>
    <?php $rel = gsx_reports(['per_page' => 4]); if ($rel['items']) : ?><section class="panel"><h2><?php echo esc_html(gsx_t('dossier_idx')); ?></h2><ul class="mini-list"><?php foreach ($rel['items'] as $x) if (($x['slug'] ?? '') !== ($r['slug'] ?? '')) echo '<li><a href="' . esc_url(gsx_report_url($x['slug'])) . '">' . esc_html(gsx_clean_text($x['player']['name'] ?? $x['title'])) . '</a><div class="meta">' . esc_html(($x['player']['club'] ?? '') . ' · ' . ($x['player']['position'] ?? '')) . '</div></li>'; ?></ul></section><?php endif; ?>
  </aside>
</div></div>
<?php get_footer();
