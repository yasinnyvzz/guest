<?php
/**
 * Hub (konu arşivi) terim meta alanları ve kalite kapısı.
 *
 * Bir terim (kategori ya da etiket) "hub" olarak işaretlenince arşiv sayfasına editoryal modüller eklenir.
 * Meta anahtarları:
 *   eka_hub        1 = hub
 *   eka_varlik     sözlükteki varlık kimliği (ör. kaan)
 *   eka_h1         arşiv H1'i (boşsa terim adı)
 *   eka_intro      editoryal tanıtım (HTML, ilk sayfada gösterilir)
 *   eka_featured   öne çıkan yazı kimlikleri (virgülle)
 *   eka_related    ilgili arşivler: "category:58,post_tag:116" (boşsa sözlükten türetilir)
 *   eka_index      auto | index | noindex  (auto: kalite kapısına göre)
 * SEO başlığı ve meta açıklaması Rank Math'in kendi terim alanlarında tutulur (rank_math_title, rank_math_description).
 */

defined( 'ABSPATH' ) || exit;

class EKA_Hubs {

	const MIN_POSTS       = 5;   // indeks için asgari yazı
	const MIN_INTRO_WORDS = 40;  // indeks için asgari özgün tanıtım
	const FRESH_DAYS      = 365; // son yazı bundan eskiyse "bayat"

	public static function init() {
		foreach ( array( 'category', 'post_tag' ) as $tax ) {
			add_action( "{$tax}_edit_form_fields", array( __CLASS__, 'fields' ), 20, 2 );
			add_action( "edited_{$tax}", array( __CLASS__, 'save' ), 10, 2 );
		}
		add_action( 'set_object_terms', array( __CLASS__, 'touch' ), 10, 4 );
	}

	public static function is_hub( $term ) {
		$term = get_term( $term );
		return $term && ! is_wp_error( $term ) && '1' === (string) get_term_meta( $term->term_id, 'eka_hub', true );
	}

	/** Yeni yazı arşive girdiğinde "son güncelleme" zamanını tazeler (sayfa yüklenmesinde sorgu yapmamak için). */
	public static function touch( $object_id, $terms, $tt_ids, $taxonomy ) {
		if ( ! in_array( $taxonomy, array( 'category', 'post_tag' ), true ) || 'publish' !== get_post_status( $object_id ) ) {
			return;
		}
		foreach ( (array) $tt_ids as $tt ) {
			$t = get_term_by( 'term_taxonomy_id', (int) $tt, $taxonomy );
			if ( $t && self::is_hub( $t ) ) {
				update_term_meta( $t->term_id, 'eka_updated', current_time( 'mysql', true ) );
			}
		}
	}

	/** Arşivin son yazı tarihi (GMT). Önbellekli meta, yoksa tek ucuz sorgu. */
	public static function last_updated( $term ) {
		$v = get_term_meta( $term->term_id, 'eka_updated', true );
		if ( $v ) {
			return $v;
		}
		$q = get_posts(
			array(
				'post_type'        => 'post',
				'posts_per_page'   => 1,
				'fields'           => 'ids',
				'no_found_rows'    => true,
				'suppress_filters' => false,
				'tax_query'        => array( array( 'taxonomy' => $term->taxonomy, 'terms' => $term->term_id ) ), // phpcs:ignore WordPress.DB.SlowDBQuery
			)
		);
		if ( ! $q ) {
			return '';
		}
		$d = get_post_field( 'post_date_gmt', $q[0] );
		update_term_meta( $term->term_id, 'eka_updated', $d );
		return $d;
	}

	/**
	 * Kalite kapısı. Yalnız yazı sayısına bakmaz: özgün tanıtım, tazelik, kopya terim ve açık niyet (varlık eşlemesi) aranır.
	 * @return array( 'karar' => INDEX|NOINDEX, 'nedenler' => string[] )
	 */
	public static function quality( $term ) {
		$term = get_term( $term );
		$why  = array();
		if ( ! self::is_hub( $term ) ) {
			return array( 'karar' => 'DEFAULT', 'nedenler' => array( 'hub değil: sitenin mevcut ayarı geçerli' ) );
		}
		$force = get_term_meta( $term->term_id, 'eka_index', true );
		if ( 'index' === $force || 'noindex' === $force ) {
			return array( 'karar' => strtoupper( $force ), 'nedenler' => array( 'editör kararı' ) );
		}
		if ( (int) $term->count < self::MIN_POSTS ) {
			$why[] = sprintf( 'yazı sayısı %d < %d', $term->count, self::MIN_POSTS );
		}
		$intro = wp_strip_all_tags( (string) get_term_meta( $term->term_id, 'eka_intro', true ) );
		$words = count( preg_split( '/\s+/u', trim( $intro ), -1, PREG_SPLIT_NO_EMPTY ) );
		if ( $words < self::MIN_INTRO_WORDS ) {
			$why[] = sprintf( 'özgün tanıtım %d kelime < %d', $words, self::MIN_INTRO_WORDS );
		}
		if ( ! EKA_Dictionary::entity_for_term( $term->taxonomy, $term->term_id ) ) {
			$why[] = 'varlık eşlemesi yok (arama niyeti tanımsız)';
		}
		$last = self::last_updated( $term );
		if ( $last && ( time() - strtotime( $last . ' UTC' ) ) > self::FRESH_DAYS * DAY_IN_SECONDS ) {
			$why[] = 'son yazı bir yıldan eski';
		}
		return array( 'karar' => $why ? 'NOINDEX' : 'INDEX', 'nedenler' => $why ? $why : array( 'kalite kapısı geçti' ) );
	}

	/** İlgili arşivler: editör listesi yoksa sözlükteki ilgili/üst ilişkilerden türetilir. @return WP_Term[] */
	public static function related_terms( $term, $limit = 8 ) {
		$out = array();
		$raw = (string) get_term_meta( $term->term_id, 'eka_related', true );
		if ( $raw ) {
			foreach ( array_filter( array_map( 'trim', explode( ',', $raw ) ) ) as $ref ) {
				list( $tax, $id ) = array_pad( explode( ':', $ref ), 2, '' );
				$t = get_term( (int) $id, $tax );
				if ( $t && ! is_wp_error( $t ) ) {
					$out[ $t->term_taxonomy_id ] = $t;
				}
			}
		} else {
			$eid = EKA_Dictionary::entity_for_term( $term->taxonomy, $term->term_id );
			$e   = $eid ? EKA_Dictionary::entity( $eid ) : null;
			if ( $e ) {
				$lang = EKA_Dictionary::term_lang( $term->term_id );
				$ids  = array_merge(
					isset( $e['ilgili'] ) ? $e['ilgili'] : array(),
					isset( $e['yapan'] ) ? $e['yapan'] : array(),
					isset( $e['ust'] ) ? $e['ust'] : array()
				);
				// Bu varlığı üreten/üstü olan diğer varlıklar (ör. TUSAŞ arşivinden KAAN'a).
				foreach ( EKA_Dictionary::data()['varliklar'] as $o ) {
					$up = array_merge( isset( $o['yapan'] ) ? $o['yapan'] : array(), isset( $o['ust'] ) ? $o['ust'] : array() );
					if ( in_array( $eid, $up, true ) ) {
						$ids[] = $o['id'];
					}
				}
				foreach ( array_unique( $ids ) as $rid ) {
					$h = EKA_Dictionary::hub_for( $lang, $rid );
					if ( ! $h ) {
						continue;
					}
					$t = get_term( (int) $h['id'], $h['tax'] );
					if ( $t && ! is_wp_error( $t ) && $t->count > 0 && $t->term_id !== $term->term_id ) {
						$out[ $t->term_taxonomy_id ] = $t;
					}
				}
			}
		}
		return array_slice( array_values( $out ), 0, $limit );
	}

	public static function fields( $term, $taxonomy ) {
		wp_nonce_field( 'eka_term', 'eka_term_nonce' );
		$m = function ( $k ) use ( $term ) {
			return (string) get_term_meta( $term->term_id, $k, true );
		};
		$q = self::quality( $term );
		?>
		<tr class="form-field"><th colspan="2"><h2><?php esc_html_e( 'Konu arşivi (hub)', 'envanter-konu-arsivleri' ); ?></h2></th></tr>
		<tr class="form-field">
			<th><label for="eka_hub">Hub</label></th>
			<td><label><input type="checkbox" id="eka_hub" name="eka_hub" value="1" <?php checked( '1', $m( 'eka_hub' ) ); ?>> Bu arşiv editoryal konu sayfasıdır</label>
			<p class="description">Kalite kapısı: <strong><?php echo esc_html( $q['karar'] ); ?></strong> — <?php echo esc_html( implode( '; ', $q['nedenler'] ) ); ?></p></td>
		</tr>
		<tr class="form-field"><th><label for="eka_varlik">Varlık kimliği</label></th>
			<td><input type="text" id="eka_varlik" name="eka_varlik" value="<?php echo esc_attr( $m( 'eka_varlik' ) ); ?>" placeholder="kaan"></td></tr>
		<tr class="form-field"><th><label for="eka_h1">H1</label></th>
			<td><input type="text" id="eka_h1" name="eka_h1" value="<?php echo esc_attr( $m( 'eka_h1' ) ); ?>" placeholder="KAAN Haberleri"></td></tr>
		<tr class="form-field"><th><label for="eka_intro">Tanıtım</label></th>
			<td><textarea id="eka_intro" name="eka_intro" rows="6"><?php echo esc_textarea( $m( 'eka_intro' ) ); ?></textarea>
			<p class="description">Özgün editoryal metin. Şablonla çoğaltılmış metin indeks kapısından geçmez (en az <?php echo (int) self::MIN_INTRO_WORDS; ?> kelime).</p></td></tr>
		<tr class="form-field"><th><label for="eka_featured">Öne çıkan yazılar</label></th>
			<td><input type="text" id="eka_featured" name="eka_featured" value="<?php echo esc_attr( $m( 'eka_featured' ) ); ?>" placeholder="84593,84210"></td></tr>
		<tr class="form-field"><th><label for="eka_related">İlgili arşivler</label></th>
			<td><input type="text" id="eka_related" name="eka_related" value="<?php echo esc_attr( $m( 'eka_related' ) ); ?>" placeholder="category:332,post_tag:116">
			<p class="description">Boş bırakılırsa sözlükteki ilişkilerden türetilir.</p></td></tr>
		<tr class="form-field"><th><label for="eka_index">İndeksleme</label></th>
			<td><select id="eka_index" name="eka_index">
				<?php foreach ( array( 'auto' => 'Kalite kapısına göre', 'index' => 'index (editör)', 'noindex' => 'noindex (editör)' ) as $k => $l ) : ?>
					<option value="<?php echo esc_attr( $k ); ?>" <?php selected( $k, $m( 'eka_index' ) ? $m( 'eka_index' ) : 'auto' ); ?>><?php echo esc_html( $l ); ?></option>
				<?php endforeach; ?>
			</select></td></tr>
		<?php
	}

	public static function save( $term_id ) {
		if ( ! isset( $_POST['eka_term_nonce'] ) || ! wp_verify_nonce( sanitize_key( $_POST['eka_term_nonce'] ), 'eka_term' ) || ! current_user_can( 'manage_categories' ) ) {
			return;
		}
		update_term_meta( $term_id, 'eka_hub', empty( $_POST['eka_hub'] ) ? '0' : '1' );
		foreach ( array( 'eka_varlik' => 'sanitize_key', 'eka_h1' => 'sanitize_text_field', 'eka_featured' => 'sanitize_text_field', 'eka_related' => 'sanitize_text_field', 'eka_index' => 'sanitize_key' ) as $k => $fn ) {
			if ( isset( $_POST[ $k ] ) ) {
				update_term_meta( $term_id, $k, call_user_func( $fn, wp_unslash( $_POST[ $k ] ) ) );
			}
		}
		if ( isset( $_POST['eka_intro'] ) ) {
			update_term_meta( $term_id, 'eka_intro', wp_kses_post( wp_unslash( $_POST['eka_intro'] ) ) );
		}
	}
}
