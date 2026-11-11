<?php
// YALNIZ YEREL TEST: canlı GPScout herkese açık API'sini yerel WP'de taklit eder (salt okunur proxy).
add_action('http_api_curl', function ($h) { if (getenv('HTTPS_PROXY')) { curl_setopt($h, CURLOPT_PROXY, getenv('HTTPS_PROXY')); curl_setopt($h, CURLOPT_CAINFO, '/root/.ccr/ca-bundle.crt'); } });
function gsx_h_fetch($path, $params) {
    $u = 'https://gegensports.com/wp-json/gpscout/v1/' . $path . ($params ? '?' . http_build_query($params) : '');
    $r = wp_remote_get($u, ['timeout' => 30, 'user-agent' => 'Mozilla/5.0']);
    return is_wp_error($r) ? ['ok' => false] : json_decode(wp_remote_retrieve_body($r), true);
}
add_action('rest_api_init', function () {
    register_rest_route('gpscout/v1', '/reports', ['methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => fn($r) => rest_ensure_response(gsx_h_fetch('reports', array_filter($r->get_params())))]);
    register_rest_route('gpscout/v1', '/reports/(?P<slug>[a-z0-9-]+)', ['methods' => 'GET', 'permission_callback' => '__return_true', 'callback' => fn($r) => rest_ensure_response(gsx_h_fetch('reports/' . $r['slug'], []))]);
});
