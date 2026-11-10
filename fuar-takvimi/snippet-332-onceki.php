/**
 * Envanter Medya — Fuar Takvimi v2
 * - /em/v1/fuarlar REST ucu: anlik fuar listesi (dil filtreli, tekillestirilmis)
 * - [fuar_takvimi] shortcode override: Leaflet CSS dahil inline (LiteSpeed UCSS korumali), veri client-side fetch
 * - Fuar tekil sayfalarina "Zaman Tuneli" (iliskili haberler + diger edisyonlar)
 */

/* ---------- yardimcilar ---------- */
function em_ftv2_meta_pick($m, $keys) {
    foreach ($keys as $k) { if (!empty($m[$k][0])) return $m[$k][0]; }
    return '';
}

function em_ftv2_collect($lang) {
    $args = array(
        'post_type' => 'fuar', 'post_status' => 'publish',
        'posts_per_page' => 300, 'no_found_rows' => true,
    );
    if (function_exists('pll_languages_list')) { $args['lang'] = $lang; }
    $q = new WP_Query($args);
    $out = array(); $seen = array();
    foreach ($q->posts as $p) {
        $m = get_post_meta($p->ID);
        $bas  = em_ftv2_meta_pick($m, array('baslangic','em_fuar_baslangic','_em_fuar_baslangic','fuar_baslangic','_fuar_baslangic','start_date','_start_date','tarih_baslangic'));
        $bit  = em_ftv2_meta_pick($m, array('bitis','em_fuar_bitis','_em_fuar_bitis','fuar_bitis','_fuar_bitis','end_date','_end_date','tarih_bitis'));
        $sehir= em_ftv2_meta_pick($m, array('sehir','em_fuar_sehir','_em_fuar_sehir','fuar_sehir','_fuar_sehir','city'));
        $ulke = em_ftv2_meta_pick($m, array('ulke','em_fuar_ulke','_em_fuar_ulke','fuar_ulke','_fuar_ulke','country'));
        $lat  = em_ftv2_meta_pick($m, array('lat','em_fuar_lat','_em_fuar_lat','fuar_lat','_fuar_lat'));
        $lng  = em_ftv2_meta_pick($m, array('lng','em_fuar_lng','_em_fuar_lng','fuar_lng','_fuar_lng','lon'));
        $web  = em_ftv2_meta_pick($m, array('web','em_fuar_web','_em_fuar_web','fuar_web','_fuar_web','website','site'));
        if (!$bas) continue;
        $key = mb_strtolower(get_the_title($p)) . '|' . $bas;
        if (isset($seen[$key])) continue;
        $seen[$key] = 1;
        $out[] = array(
            'id' => $p->ID,
            'title' => html_entity_decode(get_the_title($p), ENT_QUOTES, 'UTF-8'),
            'url' => get_permalink($p),
            'baslangic' => $bas, 'bitis' => ($bit ? $bit : $bas),
            'sehir' => $sehir, 'ulke' => $ulke,
            'lat' => ($lat !== '' ? floatval($lat) : null),
            'lng' => ($lng !== '' ? floatval($lng) : null),
            'web' => $web,
        );
    }
    usort($out, function($a, $b){ return strcmp($a['baslangic'], $b['baslangic']); });
    return $out;
}

/* ---------- REST: anlik fuar listesi ---------- */
add_action('rest_api_init', function(){
    register_rest_route('em/v1', '/fuarlar', array(
        'methods' => 'GET',
        'permission_callback' => '__return_true',
        'callback' => function($req){
            $lang = sanitize_key($req->get_param('lang'));
            if (!$lang) { $lang = 'tr'; }
            if ($req->get_param('meta_dump')) {
                $q = get_posts(array('post_type'=>'fuar','posts_per_page'=>1,'post_status'=>'publish'));
                $keys = $q ? array_keys(get_post_meta($q[0]->ID)) : array();
                return new WP_REST_Response(array('meta_keys' => $keys), 200);
            }
            $items = em_ftv2_collect($lang);
            $res = new WP_REST_Response(array('bugun' => current_time('Y-m-d'), 'items' => $items), 200);
            $res->header('Cache-Control', 'no-cache, must-revalidate, max-age=0');
            return $res;
        },
    ));
});

/* ---------- shortcode override ---------- */
add_action('init', function(){
    remove_shortcode('fuar_takvimi');
    add_shortcode('fuar_takvimi', 'em_ftv2_render');
}, 99);

function em_ftv2_labels($lang) {
    $L = array(
        'tr' => array('tb'=>'Tüm Fuarları Takvimime Ekle','ta'=>'{N} savunma fuarı tek tıkla takviminize abone olur, yeni eklenenler otomatik gelir','g'=>'Google Takvim','o'=>'Outlook','f'=>'Office 365','a'=>'Apple / iCal','i'=>'.ics indir','k'=>'Bağlantıyı kopyala','kd'=>'Kopyalandı','ara'=>'Fuar ara (isim, şehir, ülke)...','ty'=>'Tüm Yıllar','tu'=>'Tüm Ülkeler','bos'=>'Bu filtre için fuar bulunamadı.','kal'=>'{N} gün kaldı','bb'=>'Bugün başlıyor','cn'=>'Devam ediyor','bt'=>'Tamamlandı','gc'=>'Takvime Ekle','ic'=>'iCal/Outlook','rs'=>'Resmi Site','yk'=>'Fuarlar yükleniyor...','ay'=>array('','Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık')),
        'en' => array('tb'=>'Add All Fairs to My Calendar','ta'=>'Subscribe to {N} defence exhibitions in one click, new ones arrive automatically','g'=>'Google Calendar','o'=>'Outlook','f'=>'Office 365','a'=>'Apple / iCal','i'=>'Download .ics','k'=>'Copy link','kd'=>'Copied','ara'=>'Search fairs (name, city, country)...','ty'=>'All Years','tu'=>'All Countries','bos'=>'No fairs match this filter.','kal'=>'{N} days left','bb'=>'Starts today','cn'=>'Ongoing','bt'=>'Finished','gc'=>'Add to Calendar','ic'=>'iCal/Outlook','rs'=>'Official Site','yk'=>'Loading fairs...','ay'=>array('','January','February','March','April','May','June','July','August','September','October','November','December')),
        'ar' => array('tb'=>'أضف جميع المعارض إلى تقويمي','ta'=>'اشترك في {N} معرضًا دفاعيًا بنقرة واحدة، والجديد يصل تلقائيًا','g'=>'تقويم Google','o'=>'Outlook','f'=>'Office 365','a'=>'Apple / iCal','i'=>'تنزيل .ics','k'=>'نسخ الرابط','kd'=>'تم النسخ','ara'=>'ابحث عن معرض (الاسم، المدينة، الدولة)...','ty'=>'كل السنوات','tu'=>'كل الدول','bos'=>'لا توجد معارض لهذا الفلتر.','kal'=>'باقٍ {N} يومًا','bb'=>'يبدأ اليوم','cn'=>'جارٍ الآن','bt'=>'انتهى','gc'=>'أضف إلى التقويم','ic'=>'iCal/Outlook','rs'=>'الموقع الرسمي','yk'=>'جارٍ تحميل المعارض...','ay'=>array('','يناير','فبراير','مارس','أبريل','مايو','يونيو','يوليو','أغسطس','سبتمبر','أكتوبر','نوفمبر','ديسمبر')),
        'es' => array('tb'=>'Añadir todas las ferias a mi calendario','ta'=>'Suscríbete a {N} ferias de defensa con un clic, las nuevas llegan automáticamente','g'=>'Google Calendar','o'=>'Outlook','f'=>'Office 365','a'=>'Apple / iCal','i'=>'Descargar .ics','k'=>'Copiar enlace','kd'=>'Copiado','ara'=>'Buscar feria (nombre, ciudad, país)...','ty'=>'Todos los años','tu'=>'Todos los países','bos'=>'No hay ferias para este filtro.','kal'=>'Faltan {N} días','bb'=>'Empieza hoy','cn'=>'En curso','bt'=>'Finalizada','gc'=>'Añadir al calendario','ic'=>'iCal/Outlook','rs'=>'Sitio oficial','yk'=>'Cargando ferias...','ay'=>array('','enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre')),
        'ru' => array('tb'=>'Добавить все выставки в мой календарь','ta'=>'Подпишитесь на {N} оборонных выставок в один клик, новые добавляются автоматически','g'=>'Google Календарь','o'=>'Outlook','f'=>'Office 365','a'=>'Apple / iCal','i'=>'Скачать .ics','k'=>'Копировать ссылку','kd'=>'Скопировано','ara'=>'Поиск выставки (название, город, страна)...','ty'=>'Все годы','tu'=>'Все страны','bos'=>'По этому фильтру выставок нет.','kal'=>'Осталось {N} дн.','bb'=>'Начинается сегодня','cn'=>'Идёт сейчас','bt'=>'Завершена','gc'=>'В календарь','ic'=>'iCal/Outlook','rs'=>'Офиц. сайт','yk'=>'Загрузка выставок...','ay'=>array('','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря')),
    );
    if (!isset($L[$lang])) { $lang = ($lang === 'zh') ? 'en' : 'tr'; if (!isset($L[$lang])) $lang = 'en'; }
    return $L[$lang];
}

function em_ftv2_render() {
    $lang = function_exists('pll_current_language') ? pll_current_language() : 'tr';
    if (!$lang) $lang = 'tr';
    $t = em_ftv2_labels($lang);
    $feed_raw  = home_url('/wp-json/em/v1/ics-feed');
    $feed_enc  = rawurlencode($feed_raw);
    $webcal    = 'webcal://' . preg_replace('#^https?://#', '', $feed_raw);
    $gcal_all  = 'https://calendar.google.com/calendar/r?cid=' . rawurlencode($webcal);
    $olive_all = 'https://outlook.live.com/calendar/0/addfromweb?url=' . $feed_enc . '&name=Envantermedya%20Fuar%20Takvimi';
    $o365_all  = 'https://outlook.office.com/calendar/0/addfromweb?url=' . $feed_enc . '&name=Envantermedya%20Fuar%20Takvimi';
    $api       = home_url('/wp-json/em/v1/fuarlar?lang=' . $lang);
    $ics_base  = home_url('/wp-json/em/v1/ics/');
    $rtl       = ($lang === 'ar') ? ' dir="rtl"' : '';

    $svg_cal  = '<svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18"/></svg>';
    $svg_big  = '<svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M8 3v4M16 3v4M3 10h18M8 14h3M13 14h3M8 17h3"/></svg>';
    $svg_link = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3.2-3.2a4 4 0 1 0-5.7-5.7L11.6 6.7"/><path d="M14 10a4 4 0 0 0-5.7 0L5.1 13.2a4 4 0 1 0 5.7 5.7l1.6-1.6"/></svg>';
    $svg_dl   = '<svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 4v11m0 0 4-4m-4 4-4-4M4 19h16"/></svg>';

    ob_start();
    ?>
<style data-no-optimize="1">.leaflet-pane,.leaflet-tile,.leaflet-marker-icon,.leaflet-marker-shadow,.leaflet-tile-container,.leaflet-pane>svg,.leaflet-pane>canvas,.leaflet-zoom-box,.leaflet-image-layer,.leaflet-layer{position:absolute;left:0;top:0}.leaflet-container{overflow:hidden}.leaflet-tile,.leaflet-marker-icon,.leaflet-marker-shadow{-webkit-user-select:none;-moz-user-select:none;user-select:none;-webkit-user-drag:none}.leaflet-tile::selection{background:transparent}.leaflet-safari .leaflet-tile{image-rendering:-webkit-optimize-contrast}.leaflet-safari .leaflet-tile-container{width:1600px;height:1600px;-webkit-transform-origin:0 0}.leaflet-marker-icon,.leaflet-marker-shadow{display:block}.leaflet-container .leaflet-overlay-pane svg{max-width:none !important;max-height:none !important}.leaflet-container .leaflet-marker-pane img,.leaflet-container .leaflet-shadow-pane img,.leaflet-container .leaflet-tile-pane img,.leaflet-container img.leaflet-image-layer,.leaflet-container .leaflet-tile{max-width:none !important;max-height:none !important;width:auto;padding:0}.leaflet-container img.leaflet-tile{mix-blend-mode:plus-lighter}.leaflet-container.leaflet-touch-zoom{-ms-touch-action:pan-x pan-y;touch-action:pan-x pan-y}.leaflet-container.leaflet-touch-drag{-ms-touch-action:pinch-zoom;touch-action:none;touch-action:pinch-zoom}.leaflet-container.leaflet-touch-drag.leaflet-touch-zoom{-ms-touch-action:none;touch-action:none}.leaflet-container{-webkit-tap-highlight-color:transparent}.leaflet-container a{-webkit-tap-highlight-color:rgba(51,181,229,0.4)}.leaflet-tile{filter:inherit;visibility:hidden}.leaflet-tile-loaded{visibility:inherit}.leaflet-zoom-box{width:0;height:0;-moz-box-sizing:border-box;box-sizing:border-box;z-index:800}.leaflet-overlay-pane svg{-moz-user-select:none}.leaflet-pane{z-index:400}.leaflet-tile-pane{z-index:200}.leaflet-overlay-pane{z-index:400}.leaflet-shadow-pane{z-index:500}.leaflet-marker-pane{z-index:600}.leaflet-tooltip-pane{z-index:650}.leaflet-popup-pane{z-index:700}.leaflet-map-pane canvas{z-index:100}.leaflet-map-pane svg{z-index:200}.leaflet-vml-shape{width:1px;height:1px}.lvml{behavior:url(#default#VML);display:inline-block;position:absolute}.leaflet-control{position:relative;z-index:800;pointer-events:visiblePainted;pointer-events:auto}.leaflet-top,.leaflet-bottom{position:absolute;z-index:1000;pointer-events:none}.leaflet-top{top:0}.leaflet-right{right:0}.leaflet-bottom{bottom:0}.leaflet-left{left:0}.leaflet-control{float:left;clear:both}.leaflet-right .leaflet-control{float:right}.leaflet-top .leaflet-control{margin-top:10px}.leaflet-bottom .leaflet-control{margin-bottom:10px}.leaflet-left .leaflet-control{margin-left:10px}.leaflet-right .leaflet-control{margin-right:10px}.leaflet-fade-anim .leaflet-popup{opacity:0;-webkit-transition:opacity 0.2s linear;-moz-transition:opacity 0.2s linear;transition:opacity 0.2s linear}.leaflet-fade-anim .leaflet-map-pane .leaflet-popup{opacity:1}.leaflet-zoom-animated{-webkit-transform-origin:0 0;-ms-transform-origin:0 0;transform-origin:0 0}svg.leaflet-zoom-animated{will-change:transform}.leaflet-zoom-anim .leaflet-zoom-animated{-webkit-transition:-webkit-transform 0.25s cubic-bezier(0,0,0.25,1);-moz-transition:-moz-transform 0.25s cubic-bezier(0,0,0.25,1);transition:transform 0.25s cubic-bezier(0,0,0.25,1)}.leaflet-zoom-anim .leaflet-tile,.leaflet-pan-anim .leaflet-tile{-webkit-transition:none;-moz-transition:none;transition:none}.leaflet-zoom-anim .leaflet-zoom-hide{visibility:hidden}.leaflet-interactive{cursor:pointer}.leaflet-grab{cursor:-webkit-grab;cursor:-moz-grab;cursor:grab}.leaflet-crosshair,.leaflet-crosshair .leaflet-interactive{cursor:crosshair}.leaflet-popup-pane,.leaflet-control{cursor:auto}.leaflet-dragging .leaflet-grab,.leaflet-dragging .leaflet-grab .leaflet-interactive,.leaflet-dragging .leaflet-marker-draggable{cursor:move;cursor:-webkit-grabbing;cursor:-moz-grabbing;cursor:grabbing}.leaflet-marker-icon,.leaflet-marker-shadow,.leaflet-image-layer,.leaflet-pane>svg path,.leaflet-tile-container{pointer-events:none}.leaflet-marker-icon.leaflet-interactive,.leaflet-image-layer.leaflet-interactive,.leaflet-pane>svg path.leaflet-interactive,svg.leaflet-image-layer.leaflet-interactive path{pointer-events:visiblePainted;pointer-events:auto}.leaflet-container{background:#ddd;outline-offset:1px}.leaflet-container a{color:#0078A8}.leaflet-zoom-box{border:2px dotted #38f;background:rgba(255,255,255,0.5)}.leaflet-container{font-family:"Helvetica Neue",Arial,Helvetica,sans-serif;font-size:12px;font-size:0.75rem;line-height:1.5}.leaflet-bar{box-shadow:0 1px 5px rgba(0,0,0,0.65);border-radius:4px}.leaflet-bar a{background-color:#fff;border-bottom:1px solid #ccc;width:26px;height:26px;line-height:26px;display:block;text-align:center;text-decoration:none;color:black}.leaflet-bar a,.leaflet-control-layers-toggle{background-position:50% 50%;background-repeat:no-repeat;display:block}.leaflet-bar a:hover,.leaflet-bar a:focus{background-color:#f4f4f4}.leaflet-bar a:first-child{border-top-left-radius:4px;border-top-right-radius:4px}.leaflet-bar a:last-child{border-bottom-left-radius:4px;border-bottom-right-radius:4px;border-bottom:none}.leaflet-bar a.leaflet-disabled{cursor:default;background-color:#f4f4f4;color:#bbb}.leaflet-touch .leaflet-bar a{width:30px;height:30px;line-height:30px}.leaflet-touch .leaflet-bar a:first-child{border-top-left-radius:2px;border-top-right-radius:2px}.leaflet-touch .leaflet-bar a:last-child{border-bottom-left-radius:2px;border-bottom-right-radius:2px}.leaflet-control-zoom-in,.leaflet-control-zoom-out{font:bold 18px 'Lucida Console',Monaco,monospace;text-indent:1px}.leaflet-touch .leaflet-control-zoom-in,.leaflet-touch .leaflet-control-zoom-out{font-size:22px}.leaflet-control-layers{box-shadow:0 1px 5px rgba(0,0,0,0.4);background:#fff;border-radius:5px}.leaflet-control-layers-toggle{background-image:url(https://unpkg.com/leaflet@1.9.4/dist/images/layers.png);width:36px;height:36px}.leaflet-retina .leaflet-control-layers-toggle{background-image:url(https://unpkg.com/leaflet@1.9.4/dist/images/layers-2x.png);background-size:26px 26px}.leaflet-touch .leaflet-control-layers-toggle{width:44px;height:44px}.leaflet-control-layers .leaflet-control-layers-list,.leaflet-control-layers-expanded .leaflet-control-layers-toggle{display:none}.leaflet-control-layers-expanded .leaflet-control-layers-list{display:block;position:relative}.leaflet-control-layers-expanded{padding:6px 10px 6px 6px;color:#333;background:#fff}.leaflet-control-layers-scrollbar{overflow-y:scroll;overflow-x:hidden;padding-right:5px}.leaflet-control-layers-selector{margin-top:2px;position:relative;top:1px}.leaflet-control-layers label{display:block;font-size:13px;font-size:1.08333em}.leaflet-control-layers-separator{height:0;border-top:1px solid #ddd;margin:5px -10px 5px -6px}.leaflet-default-icon-path{background-image:url(https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png)}.leaflet-container .leaflet-control-attribution{background:#fff;background:rgba(255,255,255,0.8);margin:0}.leaflet-control-attribution,.leaflet-control-scale-line{padding:0 5px;color:#333;line-height:1.4}.leaflet-control-attribution a{text-decoration:none}.leaflet-control-attribution a:hover,.leaflet-control-attribution a:focus{text-decoration:underline}.leaflet-attribution-flag{display:inline !important;vertical-align:baseline !important;width:1em;height:0.6669em}.leaflet-left .leaflet-control-scale{margin-left:5px}.leaflet-bottom .leaflet-control-scale{margin-bottom:5px}.leaflet-control-scale-line{border:2px solid #777;border-top:none;line-height:1.1;padding:2px 5px 1px;white-space:nowrap;-moz-box-sizing:border-box;box-sizing:border-box;background:rgba(255,255,255,0.8);text-shadow:1px 1px #fff}.leaflet-control-scale-line:not(:first-child){border-top:2px solid #777;border-bottom:none;margin-top:-2px}.leaflet-control-scale-line:not(:first-child):not(:last-child){border-bottom:2px solid #777}.leaflet-touch .leaflet-control-attribution,.leaflet-touch .leaflet-control-layers,.leaflet-touch .leaflet-bar{box-shadow:none}.leaflet-touch .leaflet-control-layers,.leaflet-touch .leaflet-bar{border:2px solid rgba(0,0,0,0.2);background-clip:padding-box}.leaflet-popup{position:absolute;text-align:center;margin-bottom:20px}.leaflet-popup-content-wrapper{padding:1px;text-align:left;border-radius:12px}.leaflet-popup-content{margin:13px 24px 13px 20px;line-height:1.3;font-size:13px;font-size:1.08333em;min-height:1px}.leaflet-popup-content p{margin:17px 0;margin:1.3em 0}.leaflet-popup-tip-container{width:40px;height:20px;position:absolute;left:50%;margin-top:-1px;margin-left:-20px;overflow:hidden;pointer-events:none}.leaflet-popup-tip{width:17px;height:17px;padding:1px;margin:-10px auto 0;pointer-events:auto;-webkit-transform:rotate(45deg);-moz-transform:rotate(45deg);-ms-transform:rotate(45deg);transform:rotate(45deg)}.leaflet-popup-content-wrapper,.leaflet-popup-tip{background:white;color:#333;box-shadow:0 3px 14px rgba(0,0,0,0.4)}.leaflet-container a.leaflet-popup-close-button{position:absolute;top:0;right:0;border:none;text-align:center;width:24px;height:24px;font:16px/24px Tahoma,Verdana,sans-serif;color:#757575;text-decoration:none;background:transparent}.leaflet-container a.leaflet-popup-close-button:hover,.leaflet-container a.leaflet-popup-close-button:focus{color:#585858}.leaflet-popup-scrolled{overflow:auto}.leaflet-oldie .leaflet-popup-content-wrapper{-ms-zoom:1}.leaflet-oldie .leaflet-popup-tip{width:24px;margin:0 auto;-ms-filter:"progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678,M12=0.70710678,M21=-0.70710678,M22=0.70710678)";filter:progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678,M12=0.70710678,M21=-0.70710678,M22=0.70710678)}.leaflet-oldie .leaflet-control-zoom,.leaflet-oldie .leaflet-control-layers,.leaflet-oldie .leaflet-popup-content-wrapper,.leaflet-oldie .leaflet-popup-tip{border:1px solid #999}.leaflet-div-icon{background:#fff;border:1px solid #666}.leaflet-tooltip{position:absolute;padding:6px;background-color:#fff;border:1px solid #fff;border-radius:3px;color:#222;white-space:nowrap;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;pointer-events:none;box-shadow:0 1px 3px rgba(0,0,0,0.4)}.leaflet-tooltip.leaflet-interactive{cursor:pointer;pointer-events:auto}.leaflet-tooltip-top:before,.leaflet-tooltip-bottom:before,.leaflet-tooltip-left:before,.leaflet-tooltip-right:before{position:absolute;pointer-events:none;border:6px solid transparent;background:transparent;content:""}.leaflet-tooltip-bottom{margin-top:6px}.leaflet-tooltip-top{margin-top:-6px}.leaflet-tooltip-bottom:before,.leaflet-tooltip-top:before{left:50%;margin-left:-6px}.leaflet-tooltip-top:before{bottom:0;margin-bottom:-12px;border-top-color:#fff}.leaflet-tooltip-bottom:before{top:0;margin-top:-12px;margin-left:-6px;border-bottom-color:#fff}.leaflet-tooltip-left{margin-left:-6px}.leaflet-tooltip-right{margin-left:6px}.leaflet-tooltip-left:before,.leaflet-tooltip-right:before{top:50%;margin-top:-6px}.leaflet-tooltip-left:before{right:0;margin-right:-12px;border-left-color:#fff}.leaflet-tooltip-right:before{left:0;margin-left:-12px;border-right-color:#fff}@media print{.leaflet-control{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style>
<style data-no-optimize="1">.em-fuar-takvimi,.em-fuar-takvimi *{font-family:inherit;box-sizing:border-box}.em-ft-toplu-takvim{background:#fafafa;border:1px solid #eaeaea;border-left:4px solid var(--olivin_1,#b20000);padding:18px 22px;border-radius:6px;margin-bottom:22px}.em-fuar-takvimi[dir=rtl] .em-ft-toplu-takvim{border-left:1px solid #eaeaea;border-right:4px solid var(--olivin_1,#b20000)}.em-ft-tt-baslik{display:flex;align-items:center;gap:12px;margin-bottom:14px}.em-ft-tt-ikon{color:var(--olivin_1,#b20000);display:inline-flex;flex-shrink:0}.em-ft-tt-baslik strong{display:block;font-size:15px;font-weight:700;color:#222}.em-ft-tt-baslik small{display:block;font-size:12px;color:#777;margin-top:3px;font-weight:400}.em-ft-tt-btnlar{display:flex;flex-wrap:wrap;gap:6px;align-items:center}.em-ft-tt-btn{display:inline-flex;align-items:center;gap:6px;font-size:12px;padding:7px 12px;border-radius:4px;text-decoration:none;font-weight:600;color:#333;background:#fff;border:1px solid #ddd;transition:.15s;cursor:pointer;line-height:1.2}.em-ft-tt-btn:hover{background:var(--olivin_1,#b20000);color:#fff;border-color:var(--olivin_1,#b20000)}.em-ft-tt-kopya.kopyalandi{background:#22a85a!important;border-color:#22a85a!important;color:#fff!important}.em-ft-tt-btn svg{flex-shrink:0;opacity:.75}.em-ft-tt-btn:hover svg{opacity:1}@media(max-width:600px){.em-ft-tt-baslik{flex-direction:column;text-align:center}.em-ft-tt-btnlar{justify-content:center}}.em-ft-toolbar{display:flex;gap:8px;margin-bottom:14px;flex-wrap:wrap}.em-ft-toolbar input,.em-ft-toolbar select{padding:8px 12px;border:1px solid #ddd;border-radius:4px;font-size:13px;background:#fff;color:#222}.em-ft-toolbar input{flex:1;min-width:220px}#em-ft-harita{height:440px;border-radius:6px;margin-bottom:22px;border:1px solid #eaeaea;z-index:1;background:#f2f0ed;position:relative}#em-ft-harita .em-ft-yukleniyor{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;color:#888;font-size:13px}.em-ft-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}.em-ft-card{background:#fff;border:1px solid #eaeaea;border-radius:6px;padding:16px;transition:.15s;position:relative;overflow:hidden}.em-ft-card::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--olivin_1,#b20000)}.em-ft-card.em-ft-gecmis::before{background:#bbb}.em-ft-card:hover{border-color:#ccc;box-shadow:0 2px 8px rgba(0,0,0,.06)}.em-ft-card h4{margin:0 0 8px;font-size:15px;line-height:1.3;font-weight:700;padding-right:74px}.em-fuar-takvimi[dir=rtl] .em-ft-card h4{padding-right:0;padding-left:74px}.em-ft-card h4 a{color:#1a1a1a;text-decoration:none}.em-ft-card h4 a:hover{color:var(--olivin_1,#b20000)}.em-ft-tarih{color:var(--olivin_1,#b20000);font-weight:700;font-size:13px;margin-bottom:3px}.em-ft-konum{color:#666;font-size:12px;margin-bottom:12px;display:flex;align-items:center;gap:5px}.em-ft-konum svg{flex-shrink:0;opacity:.6}.em-ft-actions{display:flex;gap:5px;flex-wrap:wrap}.em-ft-btn{font-size:11px;padding:5px 9px;background:#f5f5f5;border-radius:3px;text-decoration:none;color:#444;transition:.15s;font-weight:600;border:1px solid transparent}.em-ft-btn:hover{background:var(--olivin_1,#b20000);color:#fff}.em-ft-gun-rozet{position:absolute;top:12px;right:12px;background:var(--olivin_1,#b20000);color:#fff;font-size:10px;padding:3px 8px;border-radius:3px;font-weight:700;letter-spacing:.2px}.em-fuar-takvimi[dir=rtl] .em-ft-gun-rozet{right:auto;left:12px}.em-ft-gun-rozet.canli{background:#1d8a4b}.em-ft-gun-rozet.gecmis{background:#999}.em-ft-popup{font-size:13px}.em-ft-popup strong{display:block;margin-bottom:4px;font-size:14px}.em-ft-skel{color:#888;font-size:13px;padding:26px 0;text-align:center;grid-column:1/-1}@media(max-width:600px){#em-ft-harita{height:300px}}</style>
<div class="em-fuar-takvimi"<?php echo $rtl; ?>>
  <div class="em-ft-toplu-takvim">
    <div class="em-ft-tt-baslik">
      <span class="em-ft-tt-ikon"><?php echo $svg_big; ?></span>
      <div><strong><?php echo esc_html($t['tb']); ?></strong><small id="em-ft-altbilgi" data-sablon="<?php echo esc_attr($t['ta']); ?>"><?php echo esc_html(str_replace('{N}', '...', $t['ta'])); ?></small></div>
    </div>
    <div class="em-ft-tt-btnlar">
      <a href="<?php echo esc_url($gcal_all); ?>" target="_blank" rel="noopener" class="em-ft-tt-btn"><?php echo $svg_cal; ?><?php echo esc_html($t['g']); ?></a>
      <a href="<?php echo esc_url($olive_all); ?>" target="_blank" rel="noopener" class="em-ft-tt-btn"><?php echo $svg_cal; ?><?php echo esc_html($t['o']); ?></a>
      <a href="<?php echo esc_url($o365_all); ?>" target="_blank" rel="noopener" class="em-ft-tt-btn"><?php echo esc_html($t['f']); ?></a>
      <a href="<?php echo esc_url($webcal); ?>" class="em-ft-tt-btn"><?php echo esc_html($t['a']); ?></a>
      <a href="<?php echo esc_url($feed_raw); ?>" download="envantermedya-fuar-takvimi.ics" class="em-ft-tt-btn"><?php echo $svg_dl; ?><?php echo esc_html($t['i']); ?></a>
      <button type="button" class="em-ft-tt-btn em-ft-tt-kopya" data-feed="<?php echo esc_attr($feed_raw); ?>" data-ok="<?php echo esc_attr($t['kd']); ?>"><?php echo $svg_link; ?><span><?php echo esc_html($t['k']); ?></span></button>
    </div>
  </div>
  <div class="em-ft-toolbar">
    <input type="text" id="em-ft-arama" placeholder="<?php echo esc_attr($t['ara']); ?>">
    <select id="em-ft-yil"><option value=""><?php echo esc_html($t['ty']); ?></option></select>
    <select id="em-ft-ulke"><option value=""><?php echo esc_html($t['tu']); ?></option></select>
  </div>
  <div id="em-ft-harita"><div class="em-ft-yukleniyor"><?php echo esc_html($t['yk']); ?></div></div>
  <div id="em-ft-liste" class="em-ft-grid"><div class="em-ft-skel"><?php echo esc_html($t['yk']); ?></div></div>
  <div id="em-ft-bos" style="display:none;text-align:center;padding:30px;color:#888"><?php echo esc_html($t['bos']); ?></div>
</div>
<script data-no-optimize="1">
(function(){
var API=<?php echo wp_json_encode($api); ?>,ICSB=<?php echo wp_json_encode($ics_base); ?>,DIL=<?php echo wp_json_encode($lang); ?>;
var T=<?php echo wp_json_encode(array('kal'=>$t['kal'],'bb'=>$t['bb'],'cn'=>$t['cn'],'bt'=>$t['bt'],'gc'=>$t['gc'],'ic'=>$t['ic'],'rs'=>$t['rs'])); ?>;
var AY=<?php echo wp_json_encode($t['ay']); ?>;
var ULKE_TR={"Turkiye":"Türkiye","Misir":"Mısır","Birlesik Krallik":"Birleşik Krallık","Cekya":"Çekya","Fildisi Sahili":"Fildişi Sahili","Guney Afrika":"Güney Afrika","Guney Kore":"Güney Kore","Israil":"İsrail","Sirbistan":"Sırbistan"};
var PIN='<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-6.1-7-11a7 7 0 0 1 14 0c0 4.9-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>';
var items=[],map=null,markers=[];
function uad(u){return (DIL==='tr'&&ULKE_TR[u])?ULKE_TR[u]:u}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function bugunStr(){var d=new Date();return d.getFullYear()+'-'+('0'+(d.getMonth()+1)).slice(-2)+'-'+('0'+d.getDate()).slice(-2)}
function tarihTR(s){if(!s)return'';var a=s.split('-');return parseInt(a[2],10)+' '+AY[parseInt(a[1],10)]+' '+a[0]}
function durum(it){var b=bugunStr();if(b<it.baslangic){var g=Math.round((new Date(it.baslangic)-new Date(b))/864e5);return{k:g===0?'bb':'kal',n:g,cls:''}}if(b<=it.bitis)return{k:'cn',n:0,cls:'canli'};return{k:'bt',n:0,cls:'gecmis'}}
function rozet(it){var d=durum(it);var y=d.k==='kal'?T.kal.replace('{N}',d.n):T[d.k];return'<span class="em-ft-gun-rozet '+d.cls+'">'+esc(y)+'</span>'}
function sira(it){var b=bugunStr();if(it.baslangic<=b&&b<=it.bitis)return'0'+it.baslangic;if(b<it.baslangic)return'1'+it.baslangic;return'2'+(99999999-parseInt(it.baslangic.replace(/-/g,''),10))}
function gcalUrl(it){var d1=it.baslangic.replace(/-/g,'');var bd=new Date(it.bitis||it.baslangic);bd.setDate(bd.getDate()+1);var d2=bd.toISOString().slice(0,10).replace(/-/g,'');return'https://www.google.com/calendar/render?action=TEMPLATE&text='+encodeURIComponent(it.title)+'&dates='+d1+'/'+d2+'&details='+encodeURIComponent((it.web||'')+' '+it.url)+'&location='+encodeURIComponent((it.sehir||'')+', '+uad(it.ulke||''))}
function kart(it){return'<div class="em-ft-card'+(durum(it).cls==='gecmis'?' em-ft-gecmis':'')+'">'+rozet(it)+'<h4><a href="'+esc(it.url)+'">'+esc(it.title)+'</a></h4><div class="em-ft-tarih">'+tarihTR(it.baslangic)+' &ndash; '+tarihTR(it.bitis)+'</div><div class="em-ft-konum">'+PIN+esc((it.sehir?it.sehir+', ':'')+uad(it.ulke||''))+'</div><div class="em-ft-actions"><a class="em-ft-btn" href="'+gcalUrl(it)+'" target="_blank" rel="noopener">'+esc(T.gc)+'</a><a class="em-ft-btn" href="'+ICSB+it.id+'">'+esc(T.ic)+'</a>'+(it.web?'<a class="em-ft-btn" href="'+esc(it.web)+'" target="_blank" rel="noopener">'+esc(T.rs)+'</a>':'')+'</div></div>'}
function cizdir(list){list=list.slice().sort(function(a,b){return sira(a)<sira(b)?-1:1});document.getElementById('em-ft-liste').innerHTML=list.map(kart).join('');document.getElementById('em-ft-bos').style.display=list.length?'none':'block';if(map){markers.forEach(function(m){map.removeLayer(m)});markers=[];var bounds=[];list.forEach(function(it){if(it.lat!=null&&it.lng!=null){var m=L.marker([it.lat,it.lng]).addTo(map);m.bindPopup('<div class="em-ft-popup"><strong>'+esc(it.title)+'</strong>'+tarihTR(it.baslangic)+' &ndash; '+tarihTR(it.bitis)+'<br>'+esc((it.sehir?it.sehir+', ':'')+uad(it.ulke||''))+'<br><a href="'+esc(it.url)+'">&rarr;</a></div>');markers.push(m);bounds.push([it.lat,it.lng])}});if(bounds.length){map.fitBounds(bounds,{padding:[40,40],maxZoom:5})}}}
function filtrele(){var q=(document.getElementById('em-ft-arama').value||'').toLowerCase();var y=document.getElementById('em-ft-yil').value;var u=document.getElementById('em-ft-ulke').value;cizdir(items.filter(function(i){if(q&&((i.title+' '+(i.sehir||'')+' '+uad(i.ulke||'')).toLowerCase().indexOf(q)===-1))return false;if(y&&i.baslangic.indexOf(y)!==0)return false;if(u&&i.ulke!==u)return false;return true}))}
function selectDoldur(){var ys={},us={};items.forEach(function(i){ys[i.baslangic.slice(0,4)]=1;if(i.ulke)us[i.ulke]=1});var sy=document.getElementById('em-ft-yil');Object.keys(ys).sort().forEach(function(y){var o=document.createElement('option');o.value=y;o.textContent=y;sy.appendChild(o)});var su=document.getElementById('em-ft-ulke');Object.keys(us).sort(function(a,b){return uad(a).localeCompare(uad(b),DIL)}).forEach(function(u){var o=document.createElement('option');o.value=u;o.textContent=uad(u);su.appendChild(o)})}
function haritaKur(){if(typeof L==='undefined')return;var el=document.getElementById('em-ft-harita');el.innerHTML='';map=L.map('em-ft-harita',{scrollWheelZoom:false}).setView([30,30],2);L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{attribution:'&copy; OpenStreetMap'}).addTo(map);filtrele()}
function leafletYukle(){if(typeof L!=='undefined'){haritaKur();return}var s=document.createElement('script');s.src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';s.onload=haritaKur;document.head.appendChild(s)}
function baslat(){['em-ft-arama','em-ft-yil','em-ft-ulke'].forEach(function(id){var el=document.getElementById(id);el.addEventListener('input',filtrele);el.addEventListener('change',filtrele)});var kb=document.querySelector('.em-ft-tt-kopya');if(kb){kb.addEventListener('click',function(){var self=this;function ok(){self.classList.add('kopyalandi');var sp=self.querySelector('span');if(sp)sp.textContent=self.getAttribute('data-ok');setTimeout(function(){self.classList.remove('kopyalandi')},2200)}if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(this.getAttribute('data-feed')).then(ok)}else{var ta=document.createElement('textarea');ta.value=this.getAttribute('data-feed');document.body.appendChild(ta);ta.select();try{document.execCommand('copy');ok()}catch(e){}document.body.removeChild(ta)}})}
fetch(API,{cache:'no-store'}).then(function(r){return r.json()}).then(function(d){items=(d&&d.items)?d.items:[];var ab=document.getElementById('em-ft-altbilgi');if(ab)ab.textContent=ab.getAttribute('data-sablon').replace('{N}',items.length);selectDoldur();cizdir(items);leafletYukle()}).catch(function(){document.getElementById('em-ft-liste').innerHTML='';document.getElementById('em-ft-bos').style.display='block'})}
if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',baslat)}else{baslat()}
})();
</script>
    <?php
    return ob_get_clean();
}

/* ---------- fuar tekil: zaman tuneli + diger edisyonlar ---------- */
function em_ftv2_kok($title) {
    $k = trim(preg_replace('/\s*20\d{2}.*$/u', '', $title));
    if (mb_strlen($k) < 3) $k = $title;
    return $k;
}

function em_ftv2_tr_rozet($title) {
    return preg_match('/(ASELSAN|ROKETSAN|TUSA\x{015E}|TUSAS|Baykar|Bayraktar|HAVELSAN|FNSS|Otokar|\bBMC\b|\bMKE\b|\bSTM\b|Sars\x{0131}lmaz|Nurol|Repkon|Dearsan|Meteksan|Alt\x{0131}nay|\bKAAN\b|H\x{00DC}RJET|HURJET|\bANKA\b|AKINCI|AKINCI|K\x{0131}z\x{0131}lelma|\bATAK\b|G\x{00D6}KDEN\x{0130}Z|H\x{0130}SAR|S\x{0130}PER|ALTAY|T\x{00FC}rk savunma|T\x{00FC}rkiye)/iu', $title);
}

add_filter('the_content', function($content){
    if (!is_singular('fuar') || is_admin() || is_feed()) return $content;
    if (doing_filter('get_the_excerpt')) return $content;
    if (mb_strlen(wp_strip_all_tags($content)) < 400) return $content;
    static $done = false;
    if ($done) return $content;
    $done = true;

    $id    = get_the_ID();
    $title = html_entity_decode(get_the_title($id), ENT_QUOTES, 'UTF-8');
    $kok   = em_ftv2_kok($title);
    $lang  = function_exists('pll_current_language') ? pll_current_language() : 'tr';

    $hq_args = array('post_type' => 'post', 'post_status' => 'publish', 's' => $kok,
        'search_columns' => array('post_title'), 'posts_per_page' => 14,
        'orderby' => 'date', 'order' => 'DESC', 'no_found_rows' => true);
    if (function_exists('pll_languages_list') && $lang) $hq_args['lang'] = $lang;
    $hq = new WP_Query($hq_args);

    $eq = new WP_Query(array('post_type' => 'fuar', 'post_status' => 'publish', 's' => $kok,
        'search_columns' => array('post_title'), 'posts_per_page' => 12,
        'post__not_in' => array($id), 'no_found_rows' => true,
        'lang' => (function_exists('pll_current_language') ? $lang : '')));

    $css = '.em-ftl{margin:34px 0 8px;border-top:2px solid var(--olivin_1,#b20000);padding-top:22px}.em-ftl h3{font-size:19px;margin:0 0 4px;font-weight:800}.em-ftl-alt{color:#777;font-size:12px;margin:0 0 18px}.em-ftl-tl{position:relative;margin:0;padding:0 0 0 22px;list-style:none;border-left:2px solid #e5e5e5}.em-ftl-yil{position:relative;margin:18px 0 8px;font-weight:800;font-size:14px;color:var(--olivin_1,#b20000)}.em-ftl-yil::before{content:"";position:absolute;left:-28px;top:4px;width:10px;height:10px;border-radius:50%;background:var(--olivin_1,#b20000)}.em-ftl-it{position:relative;margin:0 0 10px;padding:10px 12px;background:#fafafa;border:1px solid #eee;border-radius:5px}.em-ftl-it::before{content:"";position:absolute;left:-26px;top:16px;width:6px;height:6px;border-radius:50%;background:#c9c9c9}.em-ftl-it a{color:#1a1a1a;text-decoration:none;font-weight:600;font-size:14px;line-height:1.35}.em-ftl-it a:hover{color:var(--olivin_1,#b20000)}.em-ftl-tarih{display:block;color:#888;font-size:11px;margin-top:3px}.em-ftl-tr{display:inline-block;background:var(--olivin_1,#b20000);color:#fff;font-size:9px;font-weight:800;padding:2px 6px;border-radius:3px;margin-left:7px;vertical-align:2px;letter-spacing:.4px}.em-ftl-ed{display:flex;flex-wrap:wrap;gap:7px;margin:16px 0 4px}.em-ftl-ed a{font-size:12px;font-weight:700;color:#333;background:#f4f4f4;border:1px solid #e2e2e2;border-radius:4px;padding:6px 11px;text-decoration:none;transition:.15s}.em-ftl-ed a:hover{background:var(--olivin_1,#b20000);color:#fff;border-color:var(--olivin_1,#b20000)}.em-ftl-bos{color:#888;font-size:13px;background:#fafafa;border:1px dashed #ddd;border-radius:5px;padding:14px 16px}';

    $html  = '<style data-no-optimize="1">' . $css . '</style>';
    $html .= '<div class="em-ftl"><h3>' . esc_html($kok) . ' — Zaman Tüneli</h3>';
    $html .= '<p class="em-ftl-alt">Envanter Medya arşivinden ' . esc_html($kok) . ' gelişmeleri, ürün lansmanları ve Türk savunma sanayii katılımları</p>';

    if ($hq->have_posts()) {
        $yil = '';
        $html .= '<ul class="em-ftl-tl">';
        foreach ($hq->posts as $p) {
            $py = get_the_date('Y', $p);
            if ($py !== $yil) { $yil = $py; $html .= '<li class="em-ftl-yil">' . esc_html($py) . '</li>'; }
            $rozet = em_ftv2_tr_rozet($p->post_title) ? '<span class="em-ftl-tr">TR</span>' : '';
            $html .= '<li class="em-ftl-it"><a href="' . esc_url(get_permalink($p)) . '">' . esc_html(html_entity_decode(get_the_title($p), ENT_QUOTES, 'UTF-8')) . '</a>' . $rozet . '<span class="em-ftl-tarih">' . esc_html(get_the_date('j F Y', $p)) . '</span></li>';
        }
        $html .= '</ul>';
    } else {
        $html .= '<div class="em-ftl-bos">Bu fuar için haber arşivi oluşuyor. Fuar yaklaştıkça gelişmeler, ürün lansmanları ve Türk katılımcı haberleri burada listelenecek.</div>';
    }

    if ($eq->have_posts()) {
        $eds = array();
        foreach ($eq->posts as $p) {
            $et = html_entity_decode(get_the_title($p), ENT_QUOTES, 'UTF-8');
            if (em_ftv2_kok($et) !== $kok) continue;
            $eds[$et] = get_permalink($p);
        }
        if ($eds) {
            ksort($eds);
            $html .= '<div class="em-ftl-ed">';
            foreach ($eds as $et => $eu) { $html .= '<a href="' . esc_url($eu) . '">' . esc_html($et) . ' &rarr;</a>'; }
            $html .= '</div>';
        }
    }

    $html .= '</div>';
    return $content . $html;
});
