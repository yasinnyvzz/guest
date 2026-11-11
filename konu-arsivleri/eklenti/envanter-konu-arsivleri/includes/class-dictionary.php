<?php
/**
 * Varlık sözlüğü (eşanlamlılar) ve site bazlı hub eşlemesi.
 *
 * Sözlük: data/varliklar.json (repo: konu-arsivleri/sozluk/varliklar.json ile aynı dosya).
 * Hub eşlemesi: 'eka_hublar' seçeneği — anahtar "<dil>:<varlik>", değer array('tax'=>..., 'id'=>..., 'kopya'=>[[tax,id],...]).
 * `wp eka hub-ice-aktar hublar.json --site=ev` ile doldurulur.
 */

defined( 'ABSPATH' ) || exit;

class EKA_Dictionary {

	private static $data = null;

	public static function data() {
		if ( null === self::$data ) {
			$custom = get_option( 'eka_sozluk_json' );
			$json   = $custom ? $custom : file_get_contents( EKA_DIR . 'data/varliklar.json' ); // phpcs:ignore WordPress.WP.AlternativeFunctions
			$d      = json_decode( $json, true );
			if ( ! is_array( $d ) || empty( $d['varliklar'] ) ) {
				$d = array( 'tipler' => array(), 'varliklar' => array() );
			}
			$by_id = array();
			foreach ( $d['varliklar'] as $v ) {
				$by_id[ $v['id'] ] = $v;
			}
			$d['by_id'] = $by_id;
			self::$data = $d;
		}
		return self::$data;
	}

	public static function reset() {
		self::$data = null;
	}

	public static function entity( $id ) {
		$d = self::data();
		return isset( $d['by_id'][ $id ] ) ? $d['by_id'][ $id ] : null;
	}

	public static function type_priority( $tip ) {
		$d = self::data();
		return isset( $d['tipler'][ $tip ]['oncelik'] ) ? (int) $d['tipler'][ $tip ]['oncelik'] : 9;
	}

	/** Varlığın verilen dildeki görünen adı. */
	public static function label( $id, $lang ) {
		$v = self::entity( $id );
		if ( ! $v ) {
			return $id;
		}
		foreach ( array( $lang, 'en', 'tr' ) as $l ) {
			if ( ! empty( $v['ad'][ $l ] ) ) {
				return $v['ad'][ $l ];
			}
		}
		return $id;
	}

	public static function hubs() {
		$h = get_option( 'eka_hublar', array() );
		return is_array( $h ) ? $h : array();
	}

	/** @return array|null array('tax','id','kopya') */
	public static function hub_for( $lang, $entity_id ) {
		$h = self::hubs();
		$k = $lang . ':' . $entity_id;
		return isset( $h[ $k ] ) ? $h[ $k ] : null;
	}

	/** Terim → varlık ters eşlemesi (kopya terimler dahil). */
	public static function entity_for_term( $taxonomy, $term_id ) {
		$meta = get_term_meta( $term_id, 'eka_varlik', true );
		if ( $meta ) {
			return $meta;
		}
		foreach ( self::hubs() as $key => $h ) {
			if ( $h['tax'] === $taxonomy && (int) $h['id'] === (int) $term_id ) {
				return substr( $key, strpos( $key, ':' ) + 1 );
			}
		}
		return '';
	}

	/** Yazının dili: Polylang varsa ondan, yoksa site varsayılanı. Polylang var ama dil atanmamışsa null. */
	public static function post_lang( $post_id ) {
		if ( function_exists( 'pll_get_post_language' ) ) {
			$l = pll_get_post_language( $post_id, 'slug' );
			return $l ? $l : null;
		}
		$def = get_option( 'eka_varsayilan_dil' );
		return $def ? $def : substr( get_locale(), 0, 2 );
	}

	public static function term_lang( $term_id ) {
		if ( function_exists( 'pll_get_term_language' ) ) {
			$l = pll_get_term_language( $term_id, 'slug' );
			if ( $l ) {
				return $l;
			}
		}
		$def = get_option( 'eka_varsayilan_dil' );
		return $def ? $def : substr( get_locale(), 0, 2 );
	}
}
