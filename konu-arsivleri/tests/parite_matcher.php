<?php
// Parite testi yardımcı betiği: PHP motorunu WordPress'siz çalıştırır.
// Kullanım: php parite_matcher.php <varliklar.json> <girdi.json> <cikti.json>
define( 'ABSPATH', __DIR__ );
require __DIR__ . '/../eklenti/envanter-konu-arsivleri/includes/class-matcher.php';
$m   = new EKA_Matcher( json_decode( file_get_contents( $argv[1] ), true ) );
$in  = json_decode( file_get_contents( $argv[2] ), true );
$out = array();
foreach ( $in as $p ) {
	list( $g, $z ) = $m->oner( $p['title'], $p['excerpt'], $p['body'] );
	$out[ $p['site'] . ':' . $p['id'] ] = array(
		'g' => array_map( function ( $o ) { return array( $o['id'], $o['guven'], $o['kaynak'], $o['T'], $o['L'], $o['B'] ); }, $g ),
		'z' => array_map( function ( $o ) { return $o['id']; }, $z ),
	);
}
file_put_contents( $argv[3], json_encode( $out, JSON_UNESCAPED_UNICODE ) );
