<?php
/**
 * Varlık eşleştirme motoru — Python referans motorunun (konu-arsivleri/motor/eslestir.py) birebir PHP karşılığı.
 * İki uygulamanın aynı sonucu verdiği tests/parite_testi.py ile doğrulanır.
 *
 * Kurallar:
 *  - Başlıkta geçen varlık güçlüdür; gövdede tek geçen varlık "anılma" sayılır ve önerilmez.
 *  - cs=true takma adlar özgün metinde harf duyarlı aranır (KAAN ≠ "Kaan Onuk").
 *  - amb=true takma adlar yalnız yazıda bağlam deseni (ctx) varsa sayılır.
 *  - neg desenleri eşleşmenin ±60 karakter çevresinde varsa o eşleşme düşer.
 *  - Ürün → üretici, her şey → üst konu çıkarımı; en fazla 7 öneri.
 */

defined( 'ABSPATH' ) || exit;

class EKA_Matcher {

	const WINDOW    = 60;
	const MAX_ONERI = 7;
	const WORD      = 'a-z0-9\x{0621}-\x{064A}';
	const LATIN_ORJ = 'A-Za-z0-9ÇĞİÖŞÜÂÎÛçğıöşüâîû';
	const AR_PROC   = '(?:وال|بال|فال|كال|لل|ال|و|ف|ب|ل|ك)?';
	const WS        = '/[ \t\n\r\f\v\x{00A0}\x{2000}-\x{200B}\x{202F}\x{3000}]+/u';

	private static $map = array(
		'İ' => 'i', 'I' => 'i', 'ı' => 'i', 'Ş' => 's', 'ş' => 's', 'Ğ' => 'g', 'ğ' => 'g', 'Ü' => 'u', 'ü' => 'u',
		'Ö' => 'o', 'ö' => 'o', 'Ç' => 'c', 'ç' => 'c', 'Â' => 'a', 'â' => 'a', 'Î' => 'i', 'î' => 'i', 'Û' => 'u',
		'û' => 'u', 'É' => 'e', 'é' => 'e', 'È' => 'e', 'è' => 'e', 'Ê' => 'e', 'ê' => 'e', 'Á' => 'a', 'á' => 'a',
		'À' => 'a', 'à' => 'a', 'Ó' => 'o', 'ó' => 'o', 'Í' => 'i', 'í' => 'i', 'Ñ' => 'n', 'ñ' => 'n', 'Ã' => 'a',
		'ã' => 'a', 'Õ' => 'o', 'õ' => 'o', 'Ô' => 'o', 'ô' => 'o', 'Ë' => 'e', 'ë' => 'e', 'Ï' => 'i', 'ï' => 'i',
		'’' => "'", '‘' => "'", '`' => "'",
		'أ' => 'ا', 'إ' => 'ا', 'آ' => 'ا', 'ٱ' => 'ا', 'ى' => 'ي', 'ة' => 'ه', 'ؤ' => 'و', 'ئ' => 'ي',
	);

	private static $sira  = array( 'yuksek' => 3, 'orta' => 2, 'dusuk' => 1 );
	private static $ters  = array( 3 => 'yuksek', 2 => 'orta', 1 => 'dusuk' );
	private $v            = array(); // id => compiled entity
	private $tipler       = array();
	private static $inst  = null;

	public static function instance() {
		if ( null === self::$inst ) {
			self::$inst = new self( EKA_Dictionary::data() );
		}
		return self::$inst;
	}

	public static function fold( $s ) {
		$s = preg_replace( '/[\x{064B}-\x{065F}\x{0670}\x{0640}]/u', '', (string) $s );
		$s = strtr( $s, self::$map );
		return mb_strtolower( $s, 'UTF-8' );
	}

	public static function ws( $s ) {
		return preg_replace( self::WS, ' ', (string) $s );
	}

	private static function is_arabic( $s ) {
		return (bool) preg_match( '/[\x{0600}-\x{06FF}]/u', $s );
	}

	public function __construct( $data ) {
		$this->tipler = isset( $data['tipler'] ) ? $data['tipler'] : array();
		foreach ( $data['varliklar'] as $d ) {
			$e = array( 'd' => $d, 'id' => $d['id'], 'tip' => $d['tip'], 'ctx' => array(), 'neg' => array(), 'pat' => array() );
			foreach ( isset( $d['ctx'] ) ? $d['ctx'] : array() as $p ) {
				$e['ctx'][] = '~' . $p . '~u';
			}
			foreach ( isset( $d['neg'] ) ? $d['neg'] : array() as $p ) {
				$e['neg'][] = '~' . $p . '~u';
			}
			foreach ( $d['alias'] as $a ) {
				$t   = $a['t'];
				$cs  = ! empty( $a['cs'] );
				$amb = ! empty( $a['amb'] );
				$suf = ! empty( $a['suf'] );
				if ( $cs ) {
					$core = str_replace( ' ', '[\s\-]+', preg_quote( $t, '~' ) );
					$rx   = '~(?<![' . self::LATIN_ORJ . '])' . $core . ( $suf ? '' : '(?![' . self::LATIN_ORJ . '])' ) . '~u';
				} else {
					$ft   = self::fold( $t );
					$core = str_replace( ' ', '[\s\-]+', preg_quote( $ft, '~' ) );
					if ( self::is_arabic( $ft ) ) {
						$rx = '~(?<![' . self::WORD . '])' . self::AR_PROC . $core . ( $suf ? '' : '(?![' . self::WORD . '])' ) . '~u';
					} else {
						$rx = '~(?<![a-z0-9])' . $core . ( $suf ? '' : '(?![a-z0-9])' ) . '~u';
					}
				}
				$e['pat'][] = array( $rx, $cs, $amb );
			}
			$this->v[ $d['id'] ] = $e;
		}
	}

	/** Bayt ofsetini karakter ofsetine çevirir. */
	private static function cpos( $s, $byte ) {
		return mb_strlen( substr( $s, 0, $byte ), 'UTF-8' );
	}

	private function say( $e, $orj, $kat, $ctx_var ) {
		$n = 0;
		foreach ( $e['pat'] as $p ) {
			list( $rx, $cs, $amb ) = $p;
			if ( $amb && ! $ctx_var ) {
				continue;
			}
			$hedef = $cs ? $orj : $kat;
			if ( ! preg_match_all( $rx, $hedef, $mm, PREG_OFFSET_CAPTURE ) ) {
				continue;
			}
			foreach ( $mm[0] as $m ) {
				if ( $e['neg'] ) {
					$start = self::cpos( $hedef, $m[1] );
					$len   = mb_strlen( $m[0], 'UTF-8' );
					$from  = max( 0, $start - self::WINDOW );
					$win   = mb_substr( $hedef, $from, ( $start + $len + self::WINDOW ) - $from, 'UTF-8' );
					if ( $cs ) {
						$win = self::fold( $win );
					}
					$skip = false;
					foreach ( $e['neg'] as $ng ) {
						if ( preg_match( $ng, $win ) ) {
							$skip = true;
							break;
						}
					}
					if ( $skip ) {
						continue;
					}
				}
				$n++;
			}
		}
		return $n;
	}

	public function puanla( $baslik, $ozet, $govde ) {
		$baslik   = self::ws( $baslik );
		$ozet     = self::ws( $ozet );
		$govde    = self::ws( $govde );
		$lead_orj = trim( $ozet . ' ' . mb_substr( $govde, 0, 400, 'UTF-8' ), ' ' );
		$doc_orj  = $baslik . ' ' . $govde;
		$k_b      = self::fold( $baslik );
		$k_l      = self::fold( $lead_orj );
		$k_d      = self::fold( $doc_orj );
		$k_g      = self::fold( $govde );
		$sonuc    = array();
		foreach ( $this->v as $id => $e ) {
			$ctx_var = empty( $e['ctx'] );
			if ( ! $ctx_var ) {
				foreach ( $e['ctx'] as $c ) {
					if ( preg_match( $c, $k_d ) ) {
						$ctx_var = true;
						break;
					}
				}
			}
			$t   = $this->say( $e, $baslik, $k_b, $ctx_var );
			$gov = $this->say( $e, $govde, $k_g, $ctx_var );
			if ( 0 === $t && 0 === $gov ) {
				continue;
			}
			$l            = $this->say( $e, $lead_orj, $k_l, $ctx_var );
			$sonuc[ $id ] = array( 'T' => $t, 'L' => $l, 'B' => $gov );
		}
		return $sonuc;
	}

	public static function guven( $h, $tip, $baskin = false, $govde_bos = false ) {
		$T = $h['T'];
		$L = $h['L'];
		$B = $h['B'];
		if ( $T >= 1 && ( $B >= 1 || $govde_bos ) ) {
			return 'yuksek';
		}
		if ( 'sirket' === $tip && $baskin && $L >= 1 && $B >= 4 ) {
			return 'yuksek';
		}
		if ( $T >= 1 ) {
			return 'orta';
		}
		if ( 'ulke' === $tip ) {
			return ( $L >= 1 && $B >= 6 && $baskin ) ? 'orta' : ( $B >= 2 ? 'dusuk' : null );
		}
		if ( ( $L >= 1 && $B >= 2 ) || $B >= 5 ) {
			return 'orta';
		}
		if ( $B >= 2 ) {
			return 'dusuk';
		}
		return null;
	}

	private function ekle( &$g, $hid, $seviye, $neden ) {
		if ( ! isset( $this->v[ $hid ] ) || $seviye < 1 ) {
			return;
		}
		$mevcut = isset( $g[ $hid ] ) ? $g[ $hid ] : null;
		if ( $mevcut && self::$sira[ $mevcut['guven'] ] >= $seviye ) {
			return;
		}
		if ( ! $mevcut ) {
			$g[ $hid ] = array( 'guven' => self::$ters[ $seviye ], 'kaynak' => 'cikarim:' . $neden, 'T' => 0, 'L' => 0, 'B' => 0 );
		} else {
			$mevcut['guven']  = self::$ters[ $seviye ];
			$mevcut['kaynak'] = $mevcut['kaynak'] . '+cikarim:' . $neden;
			$g[ $hid ]        = $mevcut;
		}
	}

	/**
	 * @return array array( güçlü öneriler (en fazla 7), zayıf öneriler )
	 *               Her öneri: id, guven (yuksek|orta|dusuk), kaynak, T, L, B
	 */
	public function oner( $baslik, $ozet, $govde, $haric = array() ) {
		$hits      = $this->puanla( $baslik, $ozet, $govde );
		$govde_bos = '' === trim( self::ws( $govde ), ' ' );
		$g         = array();
		$enust     = array();
		foreach ( $hits as $vid => $h ) {
			$t = $this->v[ $vid ]['tip'];
			if ( $h['B'] > ( isset( $enust[ $t ] ) ? $enust[ $t ][0] : 0 ) ) {
				$enust[ $t ] = array( $h['B'], $vid );
			}
		}
		foreach ( $hits as $vid => $h ) {
			$t      = $this->v[ $vid ]['tip'];
			$baskin = isset( $enust[ $t ] ) && $enust[ $t ][1] === $vid;
			$c      = self::guven( $h, $t, $baskin, $govde_bos );
			if ( $c ) {
				$g[ $vid ] = array( 'guven' => $c, 'kaynak' => 'dogrudan', 'T' => $h['T'], 'L' => $h['L'], 'B' => $h['B'] );
			}
		}
		// Liste tipi yazı: çok sayıda şirket varsa yalnız başlıktakiler ve en güçlü ikisi kalır.
		$sirketler = array();
		foreach ( $g as $k => $x ) {
			if ( 'sirket' === $this->v[ $k ]['tip'] && 'dusuk' !== $x['guven'] ) {
				$sirketler[] = $k;
			}
		}
		if ( count( $sirketler ) > 4 ) {
			$sirali = $sirketler;
			$idx    = array_flip( $sirketler );
			usort(
				$sirali,
				function ( $a, $b ) use ( $g, $idx ) {
					return array( -$g[ $a ]['T'], -$g[ $a ]['B'], $idx[ $a ] ) <=> array( -$g[ $b ]['T'], -$g[ $b ]['B'], $idx[ $b ] );
				}
			);
			$koru = array_slice( $sirali, 0, 2 );
			foreach ( $sirketler as $k ) {
				if ( $g[ $k ]['T'] >= 1 ) {
					$koru[] = $k;
				}
			}
			foreach ( $sirketler as $k ) {
				if ( ! in_array( $k, $koru, true ) ) {
					$g[ $k ]['guven'] = 'dusuk';
					$g[ $k ]['not']   = 'liste_yazisi';
				}
			}
		}
		// Üretici yükseltmesi.
		foreach ( $g as $k => $x ) {
			if ( 'yuksek' === $x['guven'] && 'dogrudan' === $x['kaynak'] ) {
				$yapan = isset( $this->v[ $k ]['d']['yapan'] ) ? $this->v[ $k ]['d']['yapan'] : array();
				foreach ( $yapan as $y ) {
					$hy = isset( $hits[ $y ] ) ? $hits[ $y ] : null;
					if ( $hy && ( $hy['T'] + $hy['B'] ) >= 1 && isset( $this->v[ $y ] ) ) {
						$onceki = isset( $g[ $y ] ) ? $g[ $y ] : null;
						if ( ! $onceki || 'yuksek' !== $onceki['guven'] ) {
							$g[ $y ] = array( 'guven' => 'yuksek', 'kaynak' => 'dogrudan+uretici:' . $k, 'T' => $hy['T'], 'L' => $hy['L'], 'B' => $hy['B'] );
						}
					}
				}
			}
		}
		// Çıkarım: ürün → üretici, her şey → üst konu (üç kademe).
		for ( $i = 0; $i < 3; $i++ ) {
			foreach ( $g as $k => $x ) {
				$s = self::$sira[ $x['guven'] ];
				if ( $s < 2 ) {
					continue;
				}
				$d = $this->v[ $k ]['d'];
				foreach ( isset( $d['yapan'] ) ? $d['yapan'] : array() as $y ) {
					$this->ekle( $g, $y, 3 === $s ? $s - 1 : 1, $k );
				}
				$tip = $this->v[ $k ]['tip'];
				// Başlıkta geçmeyen doğrudan varlıktan yapılan çıkarım en fazla "orta" olur.
				$tavan = ( 0 === strpos( $x['kaynak'], 'dogrudan' ) && 0 === $x['T'] ) ? 2 : 3;
				foreach ( isset( $d['ust'] ) ? $d['ust'] : array() as $u ) {
					$lvl = in_array( $tip, array( 'teknoloji', 'kategori' ), true ) ? $s : $s - ( 3 === $s ? 0 : 1 );
					$this->ekle( $g, $u, min( $tavan, $lvl ), $k );
				}
			}
		}
		$oneriler = array();
		$n        = 0;
		foreach ( $g as $k => $x ) {
			if ( in_array( $k, $haric, true ) ) {
				continue;
			}
			$oneriler[] = array_merge( array( 'id' => $k, '_i' => $n++ ), $x );
		}
		$tipler = $this->tipler;
		$v      = $this->v;
		usort(
			$oneriler,
			function ( $a, $b ) use ( $tipler, $v ) {
				$pa = isset( $tipler[ $v[ $a['id'] ]['tip'] ]['oncelik'] ) ? $tipler[ $v[ $a['id'] ]['tip'] ]['oncelik'] : 9;
				$pb = isset( $tipler[ $v[ $b['id'] ]['tip'] ]['oncelik'] ) ? $tipler[ $v[ $b['id'] ]['tip'] ]['oncelik'] : 9;
				return array( -self::$sira[ $a['guven'] ], $pa, -$a['T'], -$a['B'], $a['_i'] )
					<=> array( -self::$sira[ $b['guven'] ], $pb, -$b['T'], -$b['B'], $b['_i'] );
			}
		);
		$guclu = array();
		$zayif = array();
		foreach ( $oneriler as $o ) {
			unset( $o['_i'] );
			if ( 'dusuk' === $o['guven'] ) {
				$zayif[] = $o;
			} elseif ( count( $guclu ) < self::MAX_ONERI ) {
				$guclu[] = $o;
			}
		}
		return array( $guclu, $zayif );
	}

	public function tip( $id ) {
		return isset( $this->v[ $id ] ) ? $this->v[ $id ]['tip'] : '';
	}
}
