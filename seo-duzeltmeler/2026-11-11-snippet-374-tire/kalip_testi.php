<?php
// Snippet 374 başlık filtresinin kalıp testi (WordPress'siz). Kullanım: php kalip_testi.php
$sep = '\s*(?:-|–|—|&ndash;|&mdash;|&#8211;|&#8212;|&#x2013;|&#x2014;)\s*';
$f = function ( $t ) use ( $sep ) {
	return preg_replace( array(
		'/' . $sep . 'Envanter Medya' . $sep . 'Savunma Sanayii Haberleri\s*$/u',
		'/' . $sep . 'Envantermedya\s*$/u',
	), ' | Envanter Medya', $t );
};
$eski = function ( $t ) {
	return str_replace( array( ' - Envanter Medya - Savunma Sanayii Haberleri', ' – Envantermedya' ), ' | Envanter Medya', $t );
};
$durumlar = array(
	// [girdi, beklenen]
	array( 'HÜRJET – Envanter Medya – Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),            // canlıda görülen
	array( 'HÜRJET – Envanter Medya - Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),            // sep uzun, site adı kısa tire
	array( 'HÜRJET &ndash; Envanter Medya - Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),      // HTML varlığı
	array( 'HÜRJET &#8211; Envanter Medya &#8211; Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),
	array( 'HÜRJET - Envanter Medya - Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),            // özgün snippet'in beklediği biçim
	array( 'HÜRJET — Envanter Medya — Savunma Sanayii Haberleri', 'HÜRJET | Envanter Medya' ),
	array( 'Sayfa 2 – HÜRJET – Envanter Medya – Savunma Sanayii Haberleri', 'Sayfa 2 – HÜRJET | Envanter Medya' ),
	array( 'Haber başlığı – Envantermedya', 'Haber başlığı | Envanter Medya' ),
	// DOKUNULMAMASI gerekenler
	array( 'KAAN Fighter Jet – Envanter Medya', 'KAAN Fighter Jet – Envanter Medya' ),                     // Polylang düzeltmesi sonrası EN
	array( 'Erdoğan’ın Kravatında KAAN Detayı - Envanter Medya', 'Erdoğan’ın Kravatında KAAN Detayı - Envanter Medya' ), // yazı şablonu
	array( 'ASELSAN Haberleri: Son Dakika ASELSAN Gelişmeleri', 'ASELSAN Haberleri: Son Dakika ASELSAN Gelişmeleri' ),
	array( 'Envanter Medya - Savunma Sanayii Haberleri ile söyleşi: X', 'Envanter Medya - Savunma Sanayii Haberleri ile söyleşi: X' ), // sonda değil
	array( 'Envantermedya analizi: Y', 'Envantermedya analizi: Y' ),
);
$hata = 0;
foreach ( $durumlar as $d ) {
	$y = $f( $d[0] );
	$ok = $y === $d[1];
	$hata += $ok ? 0 : 1;
	printf( "%s  eski:%s  %s\n      -> %s\n", $ok ? 'GEÇTİ' : 'KALDI', $eski( $d[0] ) === $d[1] ? '✓' : '✗', $d[0], $y );
}
echo count( $durumlar ) . " durum, $hata hata\n";
exit( $hata ? 1 : 0 );
