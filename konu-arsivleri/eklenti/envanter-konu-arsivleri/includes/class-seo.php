<?php
/**
 * Robots, site haritası ve yapılandırılmış veri.
 *  - Hub değilse hiçbir şeye dokunulmaz (sitenin mevcut Rank Math ayarı geçerli).
 *  - Hub + kalite kapısı INDEX → index,follow; NOINDEX → noindex,follow.
 *  - INDEX olan hub etiketleri ayrı bir site haritasına girer ve Rank Math site haritası dizinine eklenir
 *    (kategoriler zaten Rank Math kategori haritasında).
 *  - Rank Math'in CollectionPage çıktısına "about" eklenir; Rank Math yoksa CollectionPage + BreadcrumbList basılır.
 */

defined( 'ABSPATH' ) || exit;

class EKA_SEO {

	const SITEMAP = 'eka-konu-sitemap.xml';

	public static function init() {
		add_filter( 'rank_math/frontend/robots', array( __CLASS__, 'rank_math_robots' ), 20 );
		add_filter( 'wp_robots', array( __CLASS__, 'wp_robots' ), 20 );
		add_filter( 'rank_math/json_ld', array( __CLASS__, 'rank_math_json_ld' ), 30, 2 );
		add_action( 'wp_head', array( __CLASS__, 'fallback_json_ld' ), 30 );
		add_action( 'init', array( __CLASS__, 'rewrite' ) );
		add_filter( 'query_vars', function ( $v ) { $v[] = 'eka_sitemap'; return $v; } );
		add_action( 'template_redirect', array( __CLASS__, 'sitemap' ), 0 );
		add_filter( 'rank_math/sitemap/index', array( __CLASS__, 'sitemap_index' ), 20 );
	}

	/** Terim arşivi indekslenebilir mi? (hub kapısı, yoksa Rank Math/site varsayılanı) */
	public static function indexable( $term ) {
		$q = EKA_Hubs::quality( $term );
		if ( 'INDEX' === $q['karar'] ) {
			return true;
		}
		if ( 'NOINDEX' === $q['karar'] ) {
			return false;
		}
		// Hub değil: Rank Math terim ayarı > taksonomi ayarı.
		$robots = get_term_meta( $term->term_id, 'rank_math_robots', true );
		if ( is_array( $robots ) && $robots ) {
			return ! in_array( 'noindex', $robots, true );
		}
		if ( class_exists( 'RankMath\\Helper' ) ) {
			$tax_robots = \RankMath\Helper::get_settings( 'titles.tax_' . $term->taxonomy . '_robots' );
			$custom     = \RankMath\Helper::get_settings( 'titles.tax_' . $term->taxonomy . '_custom_robots' );
			if ( $custom && is_array( $tax_robots ) ) {
				return ! in_array( 'noindex', $tax_robots, true );
			}
		}
		return 'category' === $term->taxonomy || (bool) apply_filters( 'eka_varsayilan_indeks', false, $term );
	}

	private static function current_hub_decision() {
		if ( ! ( is_category() || is_tag() || is_tax() ) ) {
			return null;
		}
		$q = get_queried_object();
		if ( ! $q instanceof WP_Term ) {
			return null;
		}
		$d = EKA_Hubs::quality( $q );
		return 'DEFAULT' === $d['karar'] ? null : $d['karar'];
	}

	public static function rank_math_robots( $robots ) {
		$k = self::current_hub_decision();
		if ( 'INDEX' === $k ) {
			$robots['index']  = 'index';
			$robots['follow'] = 'follow';
		} elseif ( 'NOINDEX' === $k ) {
			$robots['index']  = 'noindex';
			$robots['follow'] = 'follow';
		}
		return $robots;
	}

	public static function wp_robots( $robots ) {
		if ( defined( 'RANK_MATH_VERSION' ) ) {
			return $robots; // Rank Math yönetiyor.
		}
		$k = self::current_hub_decision();
		if ( 'INDEX' === $k ) {
			unset( $robots['noindex'] );
			$robots['index']  = true;
			$robots['follow'] = true;
		} elseif ( 'NOINDEX' === $k ) {
			unset( $robots['index'] );
			$robots['noindex'] = true;
			$robots['follow']  = true;
		}
		return $robots;
	}

	private static function about_node( $term ) {
		$eid = EKA_Dictionary::entity_for_term( $term->taxonomy, $term->term_id );
		$e   = $eid ? EKA_Dictionary::entity( $eid ) : null;
		if ( ! $e ) {
			return null;
		}
		$lang = EKA_Dictionary::term_lang( $term->term_id );
		$type = array( 'sirket' => 'Organization', 'ulke' => 'Country' );
		$node = array(
			'@type' => isset( $type[ $e['tip'] ] ) ? $type[ $e['tip'] ] : 'Thing',
			'name'  => EKA_Dictionary::label( $eid, $lang ),
		);
		$alt = array();
		foreach ( $e['alias'] as $a ) {
			if ( empty( $a['amb'] ) && mb_strlen( $a['t'] ) > 2 ) {
				$alt[] = $a['t'];
			}
		}
		if ( $alt ) {
			$node['alternateName'] = array_values( array_unique( array_slice( $alt, 0, 6 ) ) );
		}
		return $node;
	}

	public static function rank_math_json_ld( $data, $jsonld = null ) {
		if ( ! ( is_category() || is_tag() || is_tax() ) ) {
			return $data;
		}
		$q = get_queried_object();
		if ( ! $q instanceof WP_Term || ! EKA_Hubs::is_hub( $q ) ) {
			return $data;
		}
		$about = self::about_node( $q );
		foreach ( $data as $k => $node ) {
			if ( is_array( $node ) && isset( $node['@type'] ) && in_array( 'CollectionPage', (array) $node['@type'], true ) ) {
				if ( $about ) {
					$data[ $k ]['about'] = $about;
				}
				$upd = EKA_Hubs::last_updated( $q );
				if ( $upd ) {
					$data[ $k ]['dateModified'] = gmdate( 'c', strtotime( $upd . ' UTC' ) );
				}
			}
		}
		return $data;
	}

	public static function fallback_json_ld() {
		if ( defined( 'RANK_MATH_VERSION' ) || ! ( is_category() || is_tag() || is_tax() ) ) {
			return;
		}
		$q = get_queried_object();
		if ( ! $q instanceof WP_Term || ! EKA_Hubs::is_hub( $q ) ) {
			return;
		}
		$url  = get_term_link( $q );
		$lang = EKA_Dictionary::term_lang( $q->term_id );
		$page = array(
			'@type'    => 'CollectionPage',
			'@id'      => $url . '#webpage',
			'url'      => $url,
			'name'     => EKA_Frontend::display_name( $q, $lang ),
			'isPartOf' => array( '@id' => home_url( '/' ) . '#website' ),
		);
		$about = self::about_node( $q );
		if ( $about ) {
			$page['about'] = $about;
		}
		$crumbs = array( array( '@type' => 'ListItem', 'position' => 1, 'name' => get_bloginfo( 'name' ), 'item' => home_url( '/' ) ) );
		$anc    = array_reverse( get_ancestors( $q->term_id, $q->taxonomy, 'taxonomy' ) );
		foreach ( $anc as $aid ) {
			$a        = get_term( $aid, $q->taxonomy );
			$crumbs[] = array( '@type' => 'ListItem', 'position' => count( $crumbs ) + 1, 'name' => $a->name, 'item' => get_term_link( $a ) );
		}
		$crumbs[] = array( '@type' => 'ListItem', 'position' => count( $crumbs ) + 1, 'name' => $page['name'], 'item' => $url );
		$graph    = array( '@context' => 'https://schema.org', '@graph' => array( $page, array( '@type' => 'BreadcrumbList', 'itemListElement' => $crumbs ) ) );
		echo '<script type="application/ld+json">' . wp_json_encode( $graph, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES ) . '</script>' . "\n";
	}

	public static function rewrite() {
		add_rewrite_rule( '^' . preg_quote( self::SITEMAP, '/' ) . '$', 'index.php?eka_sitemap=1', 'top' );
	}

	/** INDEX kararı almış hub ETİKETLERİ (kategoriler Rank Math haritasında). */
	public static function sitemap_terms() {
		$terms = get_terms(
			array(
				'taxonomy'   => 'post_tag',
				'hide_empty' => true,
				'meta_query' => array( array( 'key' => 'eka_hub', 'value' => '1' ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
				'lang'       => '',
			)
		);
		$out = array();
		foreach ( is_wp_error( $terms ) ? array() : $terms as $t ) {
			$q = EKA_Hubs::quality( $t );
			if ( 'INDEX' === $q['karar'] ) {
				$out[] = $t;
			}
		}
		return $out;
	}

	public static function sitemap() {
		if ( ! get_query_var( 'eka_sitemap' ) ) {
			return;
		}
		header( 'Content-Type: application/xml; charset=UTF-8' );
		header( 'X-Robots-Tag: noindex, follow' );
		echo '<?xml version="1.0" encoding="UTF-8"?>' . "\n" . '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' . "\n";
		foreach ( self::sitemap_terms() as $t ) {
			$upd = EKA_Hubs::last_updated( $t );
			echo "\t<url><loc>" . esc_url( get_term_link( $t ) ) . '</loc>' . ( $upd ? '<lastmod>' . esc_html( gmdate( 'c', strtotime( $upd . ' UTC' ) ) ) . '</lastmod>' : '' ) . "</url>\n";
		}
		echo '</urlset>';
		exit;
	}

	public static function sitemap_index( $xml ) {
		if ( ! self::sitemap_terms() ) {
			return $xml;
		}
		return $xml . "\t<sitemap>\n\t\t<loc>" . esc_url( home_url( '/' . self::SITEMAP ) ) . "</loc>\n\t</sitemap>\n";
	}
}
