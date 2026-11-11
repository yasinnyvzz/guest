/* Title soneki kisaltma: ana sayfa haric " - Envanter Medya - Savunma Sanayii Haberleri" -> " | Envanter Medya" */
add_filter('rank_math/frontend/title', function($t){
  if (is_front_page() || is_home()) return $t;
  return str_replace(array(' - Envanter Medya - Savunma Sanayii Haberleri',' – Envantermedya'), ' | Envanter Medya', $t);
}, 99);
