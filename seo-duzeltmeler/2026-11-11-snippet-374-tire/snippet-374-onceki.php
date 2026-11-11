/* EV Haber Hub v1 - [ev_haber_hub] canli akis + haber alti hub kutusu + hub purge (post 35529) */
if (!defined('EV_HUB_ID')) define('EV_HUB_ID', 35529);
if (!function_exists('ev_hub_cats')) { function ev_hub_cats(){ return array(58,315); } }

if (!function_exists('ev_hub_tr_kw')) { function ev_hub_tr_kw($t){
  return (bool) preg_match('/ASELSAN|TUSAŞ|TUSAS|ROKETSAN|BAYKAR|Bayraktar|HAVELSAN|MKE|STM|FNSS|OTOKAR|BMC|ASFAT|SDT|SSB|TÜBİTAK|SAGE|TEI|TRMOTOR|Meteksan|Nurol|Sarsılmaz|CANİK|Canik|Repkon|Altınay|Katmerciler|Kale |TAIS|Sedef|Türk|Türkiye|TSK|MSB|TCG|MİLGEM|KAAN|HÜRJET|HÜRKUŞ|ALTAY|KIZILELMA|ANKA|AKINCI|GÖKBEY|ATAK|SİPER|HİSAR|ATMACA|TAYFUN|GÜRZ|KORKUT|Çelik Kubbe|IDEF|SAHA|TEKNOFEST/u', $t);
}}
if (!function_exists('ev_hub_query')) {
function ev_hub_query($n){
  $ids = get_transient('ev_hub_ids_v6');
  if (!is_array($ids)) {
    $a = array('post_type'=>'post','post_status'=>'publish','posts_per_page'=>600,'fields'=>'ids','post__not_in'=>array(EV_HUB_ID),'ignore_sticky_posts'=>true,'no_found_rows'=>true,
      'tax_query'=>array('relation'=>'AND',
        array('relation'=>'OR',
          array('taxonomy'=>'category','field'=>'term_id','terms'=>array(58,315,54,56,57),'include_children'=>true),
          array('taxonomy'=>'category','field'=>'term_id','terms'=>array(53),'include_children'=>false)),
        array('taxonomy'=>'category','field'=>'term_id','terms'=>array(55,2346,3766,38429,3964,31179,71,11870,65),'include_children'=>true,'operator'=>'NOT IN')));
    if (function_exists('pll_current_language')) $a['lang']='tr';
    $q = new WP_Query($a); $ids = array();
    foreach ($q->posts as $pid) {
      $t = html_entity_decode(get_the_title($pid), ENT_QUOTES, 'UTF-8');
      if (preg_match('/Nedir|nedir|Nerede|Ne Kadar|Rehber|rehber| vs | kimin|Kimin|Kimdir|Nasıl|nasıl|karşılaştır|Karşılaştır|Maaş|maaş|Dünyanın En|En (İyi|Büyük|Güçlü)|Staj|İlan|ilanı|Ne Zaman|ne zaman|Neden|neden|[Kk]aç |Tam Liste|Tarihçe|Dünyada Kaçıncı|Sağlık Bilişimi|dosyas|Medef|AVCI av|Tedarik Zincirinde|\p{Han}|\p{Arabic}|\p{Cyrillic}|\?/u', $t)) continue;
      $direct = wp_get_post_categories($pid);
      if (count($direct)===1 && $direct[0]==53 && !ev_hub_tr_kw($t)) continue;
      $ids[] = $pid; if (count($ids) >= 40) break;
    }
    set_transient('ev_hub_ids_v6', $ids, 15 * MINUTE_IN_SECONDS);
  }
  $ids = array_slice($ids, 0, $n);
  if (!$ids) $ids = array(0);
  return new WP_Query(array('post_type'=>'post','post__in'=>$ids,'orderby'=>'post__in','posts_per_page'=>count($ids),'ignore_sticky_posts'=>true,'no_found_rows'=>true,'lang'=>''));
}}

add_shortcode('ev_haber_hub', function(){
  $q = ev_hub_query(34);
  if (!$q->have_posts()) return '';
  $posts = $q->posts;
  $latest = get_post_time('U', true, $posts[0]);
  $o  = '<style data-no-optimize="1">.evh{margin:0 0 28px}.evh-up{font-size:13px;color:#555;border-left:3px solid #b3131b;padding:4px 10px;margin:0 0 18px;background:#f6f6f6}.evh-up time{font-weight:700;color:#111}.evh h2{margin:26px 0 12px}.evh-top{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.evh-card{display:block;text-decoration:none;color:#111;border:1px solid #e3e3e3;border-radius:6px;overflow:hidden;background:#fff}.evh-card img{width:100%;height:130px;object-fit:cover;display:block}.evh-card span{display:block;padding:10px;font-size:14px;font-weight:700;line-height:1.35}.evh-list{list-style:none;margin:0;padding:0}.evh-list li{display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #ececec;margin:0}.evh-list time{flex:0 0 96px;font-size:12px;color:#777;padding-top:3px}.evh-list a{font-weight:600;text-decoration:none;color:#111;line-height:1.4}.evh-list a:hover,.evh-card:hover span{color:#b3131b}.evh-list em{display:block;font-style:normal;font-size:12px;color:#777;font-weight:400}.evh-chips{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 8px}.evh-chips a{border:1px solid #cfcfcf;border-radius:16px;padding:5px 12px;font-size:13px;text-decoration:none;color:#222;background:#fff}.evh-chips a:hover{border-color:#b3131b;color:#b3131b}.evh-more{display:inline-block;margin:16px 0 0;font-weight:700;color:#b3131b}@media(max-width:782px){.evh-top{grid-template-columns:repeat(2,1fr)}.evh-card img{height:100px}.evh-list li{flex-direction:column;gap:2px}.evh-list time{flex:none}}</style>';
  $o .= '<div class="evh">';
  $o .= '<p class="evh-up">Son güncelleme: <time datetime="'.esc_attr(wp_date('c',$latest)).'">'.esc_html(wp_date('j F Y – H:i',$latest)).'</time></p>';
  $o .= '<h2 id="gunun-gelismeleri">Günün Öne Çıkan Türk Savunma Sanayii Gelişmeleri</h2><div class="evh-top">';
  for ($i=0; $i<4 && $i<count($posts); $i++){ $p=$posts[$i];
    $img = get_the_post_thumbnail($p->ID,'medium',array('loading'=>($i<2?'eager':'lazy'),'alt'=>get_the_title($p)));
    $o .= '<a class="evh-card" href="'.esc_url(get_permalink($p)).'">'.$img.'<span>'.esc_html(get_the_title($p)).'</span></a>';
  }
  $o .= '</div>';
  $co = array('ASELSAN'=>'envanter/as','TUSAŞ'=>'envanter/tusas','ROKETSAN'=>'envanter/roketsan','BAYKAR'=>'envanter/baykar','HAVELSAN'=>'envanter/havelsan','MKE'=>'envanter/mke','STM'=>'envanter/stm','FNSS'=>'envanter/fnss','OTOKAR'=>'envanter/otokar','BMC'=>'envanter/bmc','ASFAT'=>'envanter/asfat');
  $o .= '<h2 id="sirket-haberleri">Şirketlere Göre Savunma Haberleri</h2><div class="evh-chips">';
  foreach($co as $k=>$v) $o .= '<a href="'.esc_url(home_url('/category/'.$v.'/')).'">'.esc_html($k).' haberleri</a>';
  $o .= '</div>';
  $ct = array('Havacılık ve Uzay'=>'havacilik-uzay','Kara Sistemleri'=>'kara-sistemleri','Deniz Sistemleri'=>'deniz-sistemleri','Hava Savunma'=>'hava-savunma','Radar'=>'radar','Elektronik Harp ve Aviyonik'=>'aviyonik-elektronik-harp','Siber Güvenlik'=>'siber-guvenlik','SSB Haberleri'=>'savunma-sanayii-baskanligi-haberleri');
  $o .= '<h2 id="kategori-haberleri">Alanlara Göre Haberler</h2><div class="evh-chips">';
  foreach($ct as $k=>$v) $o .= '<a href="'.esc_url(home_url('/category/turk-savunma-sanayi/'.$v.'/')).'">'.esc_html($k).'</a>';
  $o .= '</div>';
  $o .= '<h2 id="son-haberler">Son Dakika Savunma Sanayii Haberleri</h2><ul class="evh-list">';
  for ($i=4; $i<count($posts); $i++){ $p=$posts[$i];
    $t = get_post_time('U', true, $p); $c = get_the_category($p->ID); $cn='';
    foreach($c as $cc){ if(!in_array($cc->term_id,array(53,58,315))){ $cn=$cc->name; break; } }
    $o .= '<li><time datetime="'.esc_attr(wp_date('c',$t)).'">'.esc_html(wp_date('j M H:i',$t)).'</time><a href="'.esc_url(get_permalink($p)).'">'.esc_html(get_the_title($p)).($cn?'<em>'.esc_html($cn).'</em>':'').'</a></li>';
  }
  $o .= '</ul><a class="evh-more" href="'.esc_url(home_url('/category/turk-savunma-sanayi/')).'">Tüm Türk savunma sanayii haber arşivi</a></div>';
  return $o;
});

/* ItemList schema (hub) */
add_action('wp_head', function(){
  if (!is_single(EV_HUB_ID)) return;
  $q = ev_hub_query(20); $items=array(); $i=1;
  foreach($q->posts as $p){ $items[]=array('@type'=>'ListItem','position'=>$i++,'url'=>get_permalink($p),'name'=>get_the_title($p)); }
  echo '<script type="application/ld+json" data-no-optimize="1">'.wp_json_encode(array('@context'=>'https://schema.org','@type'=>'ItemList','name'=>'Savunma Sanayii Haberleri','itemListElement'=>$items)).'</script>';
}, 40);

/* Haber alti hub kutusu: yalniz TR + Turk savunma sanayii kategorileri */
add_filter('the_content', function($c){
  if (is_admin() || is_feed() || !is_singular('post')) return $c;
  $id = get_the_ID();
  if (!$id || $id != get_queried_object_id()) return $c;
  if ($id == EV_HUB_ID || strpos($c,'/savunma-sanayii-haberleri/')!==false) return $c;
  if (function_exists('pll_get_post_language') && pll_get_post_language($id) !== 'tr') return $c;
  $ok=false; $deny=false;
  foreach(get_the_category($id) as $t){
    $chain = array_merge(array($t->term_id), get_ancestors($t->term_id,'category'));
    if (array_intersect($chain, array(55,2346,3766))) { $deny=true; break; }
    if (array_intersect($chain, array(58,315,54,56,57)) || ($t->term_id==53 && ev_hub_tr_kw(html_entity_decode(get_the_title($id), ENT_QUOTES, 'UTF-8')))) $ok=true;
  }
  if ($deny) $ok=false;
  if(!$ok) return $c;
  $anch = array('Savunma Sanayii Haberleri','Türk savunma sanayii haberleri','son dakika savunma sanayii haberleri','savunma haberleri');
  $a = $anch[$id % count($anch)];
  $box = '<div class="ev-hubbox" style="border-left:3px solid #b3131b;background:#f6f6f6;padding:14px 16px;margin:28px 0 8px;font-size:15px;line-height:1.55"><strong>Türk savunma sanayiindeki son gelişmeler:</strong> ASELSAN, TUSAŞ, ROKETSAN, BAYKAR, HAVELSAN, MKE ve diğer savunma şirketlerinden en yeni gelişmeleri <a href="'.esc_url(home_url('/savunma-sanayii-haberleri/')).'">'.esc_html($a).'</a> sayfamızdan takip edebilirsiniz.</div>';
  return $c.$box;
}, 18);

/* Yeni TR haber yayinlaninca hub'in degisiklik zamani + onbellek */
add_action('transition_post_status', function($new,$old,$post){
  if ($new!=='publish' || $old==='publish' || $post->post_type!=='post' || $post->ID==EV_HUB_ID) return;
  if (function_exists('pll_get_post_language')) { $l=pll_get_post_language($post->ID); if ($l && $l!=='tr') return; }
  global $wpdb; $wpdb->update($wpdb->posts, array('post_modified'=>current_time('mysql'),'post_modified_gmt'=>current_time('mysql',1)), array('ID'=>EV_HUB_ID));
  delete_transient('ev_hub_ids_v6');
  clean_post_cache(EV_HUB_ID);
  do_action('litespeed_purge_post', EV_HUB_ID);
}, 20, 3);

/* Title soneki kisaltma: ana sayfa haric " - Envanter Medya - Savunma Sanayii Haberleri" -> " | Envanter Medya" */
add_filter('rank_math/frontend/title', function($t){
  if (is_front_page() || is_home()) return $t;
  return str_replace(array(' - Envanter Medya - Savunma Sanayii Haberleri',' – Envantermedya'), ' | Envanter Medya', $t);
}, 99);
