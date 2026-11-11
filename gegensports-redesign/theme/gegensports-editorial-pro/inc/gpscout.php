<?php
defined('ABSPATH') || exit;
/**
 * GPScout eklentisinin herkese açık REST API'si (gpscout/v1) üzerinden veri okur.
 * Eklenti iç yapısına bağımlı değildir; yalnızca belgelenmiş uç noktaları kullanır.
 * Sonuçlar kısa süreli önbelleğe alınır; hata/boş durumda [] döner (bileşen gizlenir).
 */
function gsx_rest_get(string $route, array $params = [], int $ttl = 600): array {
    $key = 'gsx_' . md5($route . serialize($params));
    $c = get_transient($key);
    if ($c !== false) return $c;
    $req = new WP_REST_Request('GET', $route);
    foreach ($params as $k => $v) $req->set_param($k, $v);
    $res = rest_do_request($req);
    $data = $res->is_error() ? [] : (array) $res->get_data();
    if (!empty($data['ok'])) set_transient($key, $data, $ttl);
    return $data;
}

function gsx_reports(array $params = []): array {
    $d = gsx_rest_get('/gpscout/v1/reports', $params + ['per_page' => 12]);
    return ['items' => $d['items'] ?? [], 'total' => (int) ($d['total'] ?? 0), 'pages' => (int) ($d['pages'] ?? 0), 'facets' => $d['facets'] ?? []];
}

function gsx_report(string $slug): array {
    $d = gsx_rest_get('/gpscout/v1/reports/' . sanitize_title($slug), [], HOUR_IN_SECONDS);
    return !empty($d['ok']) ? $d : [];
}

/** Metin temizliği: eklenti şablonundan gelen boş "()" kalıplarını ve çift boşlukları temizler. */
function gsx_clean_text(string $s): string {
    $s = preg_replace('/\s*\(\s*\)/u', '', $s);
    $s = preg_replace('/\s{2,}/u', ' ', $s);
    return trim($s);
}

function gsx_report_url(string $slug): string { return home_url('/dossier/' . $slug . '/'); }
