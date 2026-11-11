<?php
require_once ABSPATH . 'wp-admin/includes/media.php'; require_once ABSPATH . 'wp-admin/includes/file.php'; require_once ABSPATH . 'wp-admin/includes/image.php'; require_once ABSPATH . 'wp-admin/includes/plugin.php';
$seed = json_decode(file_get_contents(getenv('SEED')), true);
// Polylang dilleri
global $polylang;
if (function_exists('pll_languages_list') && !pll_languages_list()) {
    $m = $polylang->model ?? null;
    foreach ([['tr','Türkçe','tr_TR',0],['en','English','en_US',1],['es','Español','es_ES',2]] as [$s,$n,$l,$o]) {
        PLL()->model->add_language(['name'=>$n,'slug'=>$s,'locale'=>$l,'rtl'=>0,'term_group'=>$o,'flag'=>$s==='en'?'gb':$s]);
    }
    update_option('polylang', array_merge((array) get_option('polylang'), ['default_lang'=>'tr','force_lang'=>1,'hide_default'=>1,'browser'=>0]));
}
$users = [];
function u($name) { global $users; if (isset($users[$name])) return $users[$name]; $l = sanitize_user(strtolower(remove_accents($name)) . '', true) ?: 'gegen'; $id = username_exists($l) ?: wp_insert_user(['user_login'=>$l,'user_pass'=>wp_generate_password(),'display_name'=>$name,'role'=>'author']); return $users[$name] = $id; }
function cat_id($slug, $name, $lang) { $t = get_term_by('slug', $slug, 'category'); if ($t) return $t->term_id; $r = wp_insert_term(html_entity_decode($name), 'category', ['slug'=>$slug]); if (is_wp_error($r)) return 0; if (function_exists('pll_set_term_language')) pll_set_term_language($r['term_id'], $lang); return $r['term_id']; }
$n = 0;
foreach (['tr','en','es'] as $lang) foreach ($seed[$lang] as $p) {
    if (get_page_by_path($p['slug'], OBJECT, 'post')) continue;
    $cats = []; foreach ($p['terms'] as [$tx,$tn,$ts]) { $cats[] = cat_id($ts, $tn, $lang); }
    $id = wp_insert_post(['post_title'=>html_entity_decode($p['title']),'post_name'=>$p['slug'],'post_content'=>$p['content'],'post_excerpt'=>'','post_status'=>'publish','post_date'=>$p['date'],'post_modified'=>$p['modified'],'post_author'=>u($p['author']),'post_category'=>array_filter($cats)], true);
    if (is_wp_error($id)) { echo "ERR {$p['slug']}\n"; continue; }
    if (function_exists('pll_set_post_language')) pll_set_post_language($id, $lang);
    if (!empty($p['thumb'])) { $att = media_sideload_image($p['thumb'], $id, $p['thumb_alt'] ?: $p['title'], 'id'); if (!is_wp_error($att)) set_post_thumbnail($id, $att); else echo "IMG ERR " . $att->get_error_message() . "\n"; }
    $n++;
}
echo "seeded $n\n";
