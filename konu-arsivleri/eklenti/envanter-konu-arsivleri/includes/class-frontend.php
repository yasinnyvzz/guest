<?php
/**
 * Ön yüz: haber altında "İlgili Haber Arşivleri" kutusu ve hub arşiv sayfası modülleri.
 * Tüm bağlantılar sunucu tarafında üretilen gerçek <a href> bağlantılarıdır; JavaScript gerekmez.
 */

defined( 'ABSPATH' ) || exit;

class EKA_Frontend {

	private static $printed_hub = false;
	private static $css_done    = false;

	public static $i18n = array(
		'related'  => array( 'tr' => 'İlgili Haber Arşivleri', 'en' => 'Related News Topics', 'ar' => 'مواضيع إخبارية ذات صلة', 'es' => 'Temas relacionados', 'ru' => 'Связанные темы', 'fr' => 'Sujets liés', 'pt' => 'Tópicos relacionados' ),
		'featured' => array( 'tr' => 'Öne Çıkan Haberler', 'en' => 'Featured Stories', 'ar' => 'أبرز الأخبار', 'es' => 'Noticias destacadas', 'ru' => 'Главное', 'fr' => 'À la une', 'pt' => 'Destaques' ),
		'hubrel'   => array( 'tr' => 'İlgili Arşivler', 'en' => 'Related Topics', 'ar' => 'أرشيفات ذات صلة', 'es' => 'Archivos relacionados', 'ru' => 'Связанные разделы', 'fr' => 'Rubriques liées', 'pt' => 'Arquivos relacionados' ),
		'updated'  => array( 'tr' => 'Son güncelleme', 'en' => 'Last updated', 'ar' => 'آخر تحديث', 'es' => 'Última actualización', 'ru' => 'Обновлено', 'fr' => 'Dernière mise à jour', 'pt' => 'Última atualização' ),
		'count'    => array( 'tr' => '%d haber', 'en' => '%d stories', 'ar' => '%d خبراً', 'es' => '%d noticias', 'ru' => 'Материалов: %d', 'fr' => '%d articles', 'pt' => '%d notícias' ),
		'latest'   => array( 'tr' => 'Son %s', 'en' => 'Latest %s', 'ar' => 'أحدث %s', 'es' => 'Últimas %s', 'ru' => 'Последние: %s', 'fr' => 'Dernières %s', 'pt' => 'Últimas %s' ),
		'news'     => array( 'tr' => '%s Haberleri', 'en' => '%s News', 'ar' => 'أخبار %s', 'es' => 'Noticias de %s', 'ru' => '%s: новости', 'fr' => 'Actualités %s', 'pt' => 'Notícias de %s' ),
	);

	public static function init() {
		if ( '0' !== get_option( 'eka_otomatik_kutu', '1' ) ) {
			add_filter( 'the_content', array( __CLASS__, 'append_related' ), 20 );
		}
		if ( '0' !== get_option( 'eka_otomatik_hub', '1' ) ) {
			add_filter( 'term_description', array( __CLASS__, 'append_hub' ), 20, 4 );
		}
		add_filter( 'single_term_title', array( __CLASS__, 'h1' ), 20 );
		add_filter( 'single_cat_title', array( __CLASS__, 'h1' ), 20 );
		add_filter( 'single_tag_title', array( __CLASS__, 'h1' ), 20 );
	}

	public static function t( $key, $lang ) {
		$a = self::$i18n[ $key ];
		return isset( $a[ $lang ] ) ? $a[ $lang ] : $a['en'];
	}

	/** Dil öznitelikleri: tema gövdeyi LTR'ye zorlasa da (EV: body.rtl{direction:ltr}) kutu doğru yönde kalır. */
	public static function lang_attrs( $lang ) {
		$rtl = in_array( $lang, array( 'ar', 'fa', 'he', 'ur' ), true );
		return ' lang="' . esc_attr( $lang ) . '" dir="' . ( $rtl ? 'rtl' : 'ltr' ) . '"';
	}

	private static function lang_now() {
		if ( function_exists( 'pll_current_language' ) && pll_current_language() ) {
			return pll_current_language( 'slug' );
		}
		return substr( get_locale(), 0, 2 );
	}

	/** Arşivin okura görünen adı: editör H1'i > "<varlık> Haberleri" > terim adı. */
	public static function display_name( $term, $lang ) {
		$h1 = (string) get_term_meta( $term->term_id, 'eka_h1', true );
		if ( $h1 ) {
			return $h1;
		}
		$eid = EKA_Dictionary::entity_for_term( $term->taxonomy, $term->term_id );
		if ( $eid ) {
			return sprintf( self::t( 'news', $lang ), EKA_Dictionary::label( $eid, $lang ) );
		}
		return $term->name;
	}

	public static function css() {
		if ( self::$css_done ) {
			return '';
		}
		self::$css_done = true;
		// Mantıksal CSS özellikleri: RTL'de kendiliğinden doğru hizalanır. Renkler temadan miras alınır.
		return '<style id="eka-css">.eka-related,.eka-hub{text-align:start}.eka-related{margin-block:2rem 1.5rem;padding-block-start:1rem;border-block-start:1px solid currentColor;border-color:rgba(127,127,127,.25)}'
			. '.eka-related__title,.eka-hub h2{font-size:1rem;font-weight:700;margin:0 0 .75rem;letter-spacing:.01em}'
			. '.eka-chips{display:flex;flex-wrap:wrap;gap:.5rem;list-style:none;margin:0;padding:0}'
			. '.eka-chips li{margin:0;padding:0}.eka-chips li::before{content:none}'
			. '.eka-chips a{display:inline-block;padding:.4rem .8rem;border:1px solid rgba(127,127,127,.35);border-radius:999px;font-size:.875rem;line-height:1.3;text-decoration:none;color:inherit}'
			. '.eka-chips a:hover,.eka-chips a:focus-visible{border-color:currentColor;text-decoration:underline}'
			. '.eka-hub{margin-block:1rem 1.5rem}.eka-hub__intro{max-inline-size:70ch;line-height:1.6}.eka-hub__intro p{margin:0 0 .75rem}'
			. '.eka-hub__meta{font-size:.8125rem;opacity:.75;margin:.25rem 0 1.25rem}'
			. '.eka-hub__featured ol{margin:0 0 1.5rem;padding-inline-start:1.25rem}.eka-hub__featured li{margin:0 0 .5rem;line-height:1.4}'
			. '.eka-hub__featured time{display:block;font-size:.75rem;opacity:.7}.eka-hub__latest{margin-block:1.5rem .5rem}</style>';
	}

	/** Yazının bağlı olduğu, indekslenebilir hub arşivleri (en çok 7), tür önceliğine göre. @return WP_Term[] */
	public static function related_terms_for_post( $post_id, $max = 7 ) {
		$lang = EKA_Dictionary::post_lang( $post_id );
		if ( ! $lang ) {
			return array();
		}
		$hubs  = EKA_Dictionary::hubs();
		$canon = array(); // "tax:id" => entity
		foreach ( $hubs as $key => $h ) {
			if ( 0 === strpos( $key, $lang . ':' ) ) {
				$canon[ $h['tax'] . ':' . $h['id'] ] = substr( $key, strlen( $lang ) + 1 );
			}
		}
		$terms = array_merge(
			(array) wp_get_post_terms( $post_id, 'category' ),
			(array) wp_get_post_terms( $post_id, 'post_tag' )
		);
		$out = array();
		foreach ( $terms as $t ) {
			if ( ! $t instanceof WP_Term ) {
				continue;
			}
			$k   = $t->taxonomy . ':' . $t->term_id;
			$eid = isset( $canon[ $k ] ) ? $canon[ $k ] : ( EKA_Hubs::is_hub( $t ) ? EKA_Dictionary::entity_for_term( $t->taxonomy, $t->term_id ) : '' );
			if ( ! $eid || ! EKA_SEO::indexable( $t ) || $t->count < 2 ) {
				continue;
			}
			$e     = EKA_Dictionary::entity( $eid );
			$out[] = array( 't' => $t, 'p' => $e ? EKA_Dictionary::type_priority( $e['tip'] ) : 9 );
		}
		usort(
			$out,
			function ( $a, $b ) {
				return array( $a['p'], -$a['t']->count ) <=> array( $b['p'], -$b['t']->count );
			}
		);
		return array_slice( wp_list_pluck( $out, 't' ), 0, $max );
	}

	public static function related_box_html( $post_id ) {
		$terms = self::related_terms_for_post( $post_id );
		if ( count( $terms ) < 2 ) {
			return '';
		}
		$lang  = EKA_Dictionary::post_lang( $post_id );
		$title = self::t( 'related', $lang );
		$html  = self::css() . '<nav class="eka-related"' . self::lang_attrs( $lang ) . ' aria-label="' . esc_attr( $title ) . '"><h2 class="eka-related__title">' . esc_html( $title ) . '</h2><ul class="eka-chips">';
		foreach ( $terms as $t ) {
			$html .= '<li><a href="' . esc_url( get_term_link( $t ) ) . '">' . esc_html( self::display_name( $t, $lang ) ) . '</a></li>';
		}
		return $html . '</ul></nav>';
	}

	public static function append_related( $content ) {
		if ( ! is_singular( 'post' ) || ! in_the_loop() || ! is_main_query() || is_feed() ) {
			return $content;
		}
		return $content . self::related_box_html( get_the_ID() );
	}

	public static function hub_modules_html( $term ) {
		if ( ! $term instanceof WP_Term || ! EKA_Hubs::is_hub( $term ) ) {
			return '';
		}
		$lang = EKA_Dictionary::term_lang( $term->term_id );
		$name = self::display_name( $term, $lang );
		$html = self::css() . '<div class="eka-hub"' . self::lang_attrs( $lang ) . '>';
		if ( ! is_paged() ) {
			$intro = (string) get_term_meta( $term->term_id, 'eka_intro', true );
			if ( $intro ) {
				$html .= '<div class="eka-hub__intro">' . wpautop( wp_kses_post( $intro ) ) . '</div>';
			}
		}
		$upd = EKA_Hubs::last_updated( $term );
		$html .= '<p class="eka-hub__meta">';
		if ( $upd ) {
			$ts    = strtotime( $upd . ' UTC' );
			$html .= esc_html( self::t( 'updated', $lang ) ) . ': <time datetime="' . esc_attr( gmdate( 'c', $ts ) ) . '">' . esc_html( date_i18n( get_option( 'date_format' ), $ts ) ) . '</time> · ';
		}
		$html .= esc_html( sprintf( self::t( 'count', $lang ), (int) $term->count ) ) . '</p>';

		if ( ! is_paged() ) {
			$ids = array_filter( array_map( 'absint', explode( ',', (string) get_term_meta( $term->term_id, 'eka_featured', true ) ) ) );
			if ( $ids ) {
				$posts = get_posts( array( 'post__in' => $ids, 'orderby' => 'post__in', 'posts_per_page' => 6, 'no_found_rows' => true, 'ignore_sticky_posts' => true ) );
				if ( $posts ) {
					$html .= '<section class="eka-hub__featured"><h2>' . esc_html( self::t( 'featured', $lang ) ) . '</h2><ol>';
					foreach ( $posts as $p ) {
						$html .= '<li><a href="' . esc_url( get_permalink( $p ) ) . '">' . esc_html( get_the_title( $p ) ) . '</a><time datetime="' . esc_attr( get_post_time( 'c', true, $p ) ) . '">' . esc_html( get_the_date( '', $p ) ) . '</time></li>';
					}
					$html .= '</ol></section>';
				}
			}
		}
		$rel = EKA_Hubs::related_terms( $term );
		if ( $rel ) {
			$html .= '<nav class="eka-hub__related" aria-label="' . esc_attr( self::t( 'hubrel', $lang ) ) . '"><h2>' . esc_html( self::t( 'hubrel', $lang ) ) . '</h2><ul class="eka-chips">';
			foreach ( $rel as $t ) {
				$html .= '<li><a href="' . esc_url( get_term_link( $t ) ) . '">' . esc_html( self::display_name( $t, $lang ) ) . '</a></li>';
			}
			$html .= '</ul></nav>';
		}
		$html .= '<h2 class="eka-hub__latest">' . esc_html( sprintf( self::t( 'latest', $lang ), $name ) ) . '</h2>';
		return $html . '</div>';
	}

	/** Temanın arşiv açıklamasına modülleri ekler (yalnız ana sorgunun arşiv terimi için, bir kez). */
	public static function append_hub( $value, $term_id = 0, $taxonomy = '', $context = 'display' ) {
		if ( is_admin() || is_feed() || self::$printed_hub || 'display' !== $context || ! ( is_category() || is_tag() || is_tax() ) || ! did_action( 'template_redirect' ) || doing_action( 'wp_head' ) ) {
			return $value;
		}
		$q = get_queried_object();
		if ( ! $q instanceof WP_Term || (int) $q->term_id !== (int) $term_id || ! EKA_Hubs::is_hub( $q ) ) {
			return $value;
		}
		self::$printed_hub = true;
		return $value . self::hub_modules_html( $q );
	}

	/** Gövdedeki arşiv başlığı (H1) için editör H1'i. <title> Rank Math'te ayrı yönetilir. */
	public static function h1( $title ) {
		// <title> ve meta etiketleri wp_head içinde üretilir; orada dokunulmaz (blok temalar gövdeyi wp_head'den önce render eder).
		if ( is_admin() || is_feed() || doing_action( 'wp_head' ) || doing_filter( 'pre_get_document_title' ) || doing_filter( 'document_title_parts' ) || ! ( is_category() || is_tag() || is_tax() ) ) {
			return $title;
		}
		$q = get_queried_object();
		if ( $q instanceof WP_Term && EKA_Hubs::is_hub( $q ) ) {
			$h1 = (string) get_term_meta( $q->term_id, 'eka_h1', true );
			return $h1 ? $h1 : $title;
		}
		return $title;
	}
}
