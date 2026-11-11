/* Title soneki kisaltma: ana sayfa haric " - Envanter Medya - Savunma Sanayii Haberleri" -> " | Envanter Medya"
 * 2026-11-11: ayirici her bicimde eslesir (- – — ve &ndash; &mdash; &#8211; &#8212;); yalniz basligin SONUNDA. */
add_filter('rank_math/frontend/title', function($t){
  if (is_front_page() || is_home()) return $t;
  $sep = '\s*(?:-|–|—|&ndash;|&mdash;|&#8211;|&#8212;|&#x2013;|&#x2014;)\s*';
  return preg_replace(array(
    '/' . $sep . 'Envanter Medya' . $sep . 'Savunma Sanayii Haberleri\s*$/u',
    '/' . $sep . 'Envantermedya\s*$/u',
  ), ' | Envanter Medya', $t);
}, 99);
