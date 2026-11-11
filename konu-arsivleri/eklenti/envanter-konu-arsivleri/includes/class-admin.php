<?php
/**
 * Editör: "Akıllı Arşiv Önerileri" kutusu.
 * Öneriler başlık + özet + gövdeden üretilir; editör onaylamadan hiçbir terim eklenmez.
 * Onaylanan terimler editörün kendi terim seçimine eklenir ve yazıyla birlikte kaydedilir
 * (Gutenberg'de core/editor deposu, klasik editörde kategori kutuları / etiket alanı).
 */

defined( 'ABSPATH' ) || exit;

class EKA_Admin {

	public static function init() {
		add_action( 'add_meta_boxes', array( __CLASS__, 'box' ) );
		add_action( 'admin_enqueue_scripts', array( __CLASS__, 'assets' ) );
		add_action( 'rest_api_init', array( __CLASS__, 'routes' ) );
		add_action( 'save_post_post', array( __CLASS__, 'cache' ), 30, 2 );
	}

	public static function box() {
		add_meta_box( 'eka-oneriler', __( 'Akıllı Arşiv Önerileri', 'envanter-konu-arsivleri' ), array( __CLASS__, 'render' ), 'post', 'side', 'default' );
	}

	public static function render( $post ) {
		echo '<div id="eka-box" data-post="' . (int) $post->ID . '"><p class="description">'
			. esc_html__( 'Başlık ve metne göre ilgili şirket, ürün, ülke ve konu arşivleri. Yalnız gerçekten ilgili olanları onaylayın.', 'envanter-konu-arsivleri' )
			. '</p><p><button type="button" class="button" id="eka-analiz">' . esc_html__( 'Önerileri getir', 'envanter-konu-arsivleri' ) . '</button></p><div id="eka-sonuc"></div></div>';
	}

	public static function assets( $hook ) {
		if ( ! in_array( $hook, array( 'post.php', 'post-new.php' ), true ) || 'post' !== get_current_screen()->post_type ) {
			return;
		}
		wp_enqueue_script( 'eka-editor', EKA_URL . 'assets/editor.js', array( 'wp-api-fetch' ), EKA_VERSION, true );
		wp_enqueue_style( 'eka-editor', EKA_URL . 'assets/editor.css', array(), EKA_VERSION );
	}

	public static function routes() {
		register_rest_route(
			'eka/v1',
			'/oner',
			array(
				'methods'             => 'POST',
				'permission_callback' => function ( $r ) {
					return current_user_can( 'edit_post', (int) $r['post_id'] );
				},
				'callback'            => array( __CLASS__, 'rest_oner' ),
				'args'                => array(
					'post_id' => array( 'required' => true, 'type' => 'integer' ),
					'title'   => array( 'type' => 'string', 'default' => '' ),
					'excerpt' => array( 'type' => 'string', 'default' => '' ),
					'content' => array( 'type' => 'string', 'default' => '' ),
				),
			)
		);
	}

	/** Metni sade metne indirger (eşleştirme gövdesi). */
	public static function plain( $html ) {
		$html = preg_replace( '#<(script|style|figure|figcaption)[^>]*>.*?</\1>#is', ' ', (string) $html );
		$html = preg_replace( '/<!--.*?-->/s', ' ', $html );
		return trim( preg_replace( '/\s+/u', ' ', html_entity_decode( wp_strip_all_tags( $html ), ENT_QUOTES | ENT_HTML5, 'UTF-8' ) ) );
	}

	/**
	 * Öneri listesi + her önerinin hedef arşivi.
	 * @return array{lang:string|null, oneriler:array}
	 */
	public static function suggestions( $post_id, $title, $excerpt, $content ) {
		$lang = EKA_Dictionary::post_lang( $post_id );
		if ( ! $lang ) {
			return array( 'lang' => null, 'oneriler' => array(), 'uyari' => 'Yazının Polylang dili atanmamış; önce dil atanmalı.' );
		}
		list( $guclu, $zayif ) = EKA_Matcher::instance()->oner( wp_strip_all_tags( $title ), self::plain( $excerpt ), self::plain( $content ) );
		$cur = array();
		foreach ( array( 'category', 'post_tag' ) as $tax ) {
			foreach ( (array) wp_get_post_terms( $post_id, $tax, array( 'fields' => 'ids' ) ) as $id ) {
				$cur[ $tax . ':' . $id ] = true;
			}
		}
		$out = array();
		foreach ( array_merge( $guclu, $zayif ) as $o ) {
			$h    = EKA_Dictionary::hub_for( $lang, $o['id'] );
			$term = $h ? get_term( (int) $h['id'], $h['tax'] ) : null;
			$row  = array(
				'varlik' => $o['id'],
				'ad'     => EKA_Dictionary::label( $o['id'], $lang ),
				'tip'    => EKA_Matcher::instance()->tip( $o['id'] ),
				'guven'  => $o['guven'],
				'neden'  => $o['kaynak'] . sprintf( ' (başlık %d, giriş %d, gövde %d)', $o['T'], $o['L'], $o['B'] ),
				'arsiv'  => null,
			);
			if ( $term && ! is_wp_error( $term ) ) {
				$row['arsiv'] = array(
					'tax'    => $term->taxonomy,
					'id'     => $term->term_id,
					'ad'     => $term->name,
					'link'   => get_term_link( $term ),
					'bagli'  => isset( $cur[ $term->taxonomy . ':' . $term->term_id ] ),
				);
			}
			$out[] = $row;
		}
		return array( 'lang' => $lang, 'oneriler' => $out );
	}

	public static function rest_oner( WP_REST_Request $r ) {
		return rest_ensure_response( self::suggestions( (int) $r['post_id'], (string) $r['title'], (string) $r['excerpt'], (string) $r['content'] ) );
	}

	/** Kayıtta önerileri önbelleğe alır (editör kuyruğu ve raporlar için; sayfa yüklenmesinde analiz yapılmaz). */
	public static function cache( $post_id, $post ) {
		if ( wp_is_post_revision( $post_id ) || wp_is_post_autosave( $post_id ) || 'auto-draft' === $post->post_status ) {
			return;
		}
		$s = self::suggestions( $post_id, $post->post_title, $post->post_excerpt, $post->post_content );
		update_post_meta( $post_id, '_eka_oneriler', wp_slash( wp_json_encode( $s, JSON_UNESCAPED_UNICODE ) ) );
	}
}
