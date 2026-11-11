<?php
/**
 * WP-CLI: wp eka <komut>
 *
 * Tüm yazan komutlar varsayılan olarak KURU çalışır; değişiklik için --uygula gerekir.
 * Toplu eklemeler eka_log tablosuna yazılır ve `wp eka geri-al <parti>` ile geri alınır.
 */

defined( 'ABSPATH' ) || exit;

class EKA_CLI {

	/**
	 * Hub eşlemesini (motor/hub_esle.py çıktısı) bu siteye yükler.
	 *
	 * ## OPTIONS
	 * <dosya>
	 * : hublar.json
	 * --site=<site>
	 * : ev | dm | da
	 * [--uygula]
	 * : Seçeneği kaydet (yoksa yalnız özet).
	 *
	 * @subcommand hub-ice-aktar
	 */
	public function hub_ice_aktar( $args, $assoc ) {
		$all  = json_decode( file_get_contents( $args[0] ), true ); // phpcs:ignore
		$site = $assoc['site'];
		$map  = array();
		$miss = 0;
		foreach ( $all as $key => $h ) {
			if ( 0 !== strpos( $key, $site . ':' ) ) {
				continue;
			}
			$t = get_term( (int) $h['id'], $h['tax'] );
			if ( ! $t || is_wp_error( $t ) ) {
				$miss++;
				continue;
			}
			$map[ substr( $key, strlen( $site ) + 1 ) ] = array(
				'tax'   => $h['tax'],
				'id'    => (int) $h['id'],
				'kopya' => array_map( function ( $k ) { return array( $k['tax'], (int) $k['id'] ); }, isset( $h['kopya'] ) ? $h['kopya'] : array() ),
			);
		}
		WP_CLI::log( sprintf( '%d eşleme bulundu, %d terim bu sitede yok.', count( $map ), $miss ) );
		if ( empty( $assoc['uygula'] ) ) {
			WP_CLI::warning( 'Kuru çalışma: --uygula ile kaydedin.' );
			return;
		}
		update_option( 'eka_hublar', $map, false );
		foreach ( $map as $key => $h ) {
			$eid = substr( $key, strpos( $key, ':' ) + 1 );
			if ( ! get_term_meta( $h['id'], 'eka_varlik', true ) ) {
				update_term_meta( $h['id'], 'eka_varlik', $eid );
			}
		}
		WP_CLI::success( 'Hub eşlemesi kaydedildi.' );
	}

	/**
	 * Tek yazı için öneri.
	 *
	 * ## OPTIONS
	 * <post_id>
	 *
	 * @subcommand oner
	 */
	public function oner( $args ) {
		$p = get_post( (int) $args[0] );
		$s = EKA_Admin::suggestions( $p->ID, $p->post_title, $p->post_excerpt, $p->post_content );
		if ( ! empty( $s['uyari'] ) ) {
			WP_CLI::warning( $s['uyari'] );
		}
		$rows = array();
		foreach ( $s['oneriler'] as $o ) {
			$rows[] = array(
				'varlik' => $o['varlik'],
				'guven'  => $o['guven'],
				'arsiv'  => $o['arsiv'] ? $o['arsiv']['tax'] . ':' . $o['arsiv']['id'] . ' ' . $o['arsiv']['ad'] : '—',
				'bagli'  => $o['arsiv'] && $o['arsiv']['bagli'] ? 'evet' : '',
				'neden'  => $o['neden'],
			);
		}
		WP_CLI\Utils\format_items( 'table', $rows, array( 'varlik', 'guven', 'arsiv', 'bagli', 'neden' ) );
	}

	/**
	 * Mevcut yazıları sınıflandırır. Varsayılan: KURU (rapor üretir, yazmaz).
	 *
	 * ## OPTIONS
	 * [--dil=<dil>]
	 * : Yalnız bu Polylang dili.
	 * [--varlik=<liste>]
	 * : Yalnız bu varlıklar (virgülle).
	 * [--guven=<seviye>]
	 * : yuksek (varsayılan) | orta — uygulanacak asgari güven.
	 * [--sayfa-boyu=<n>]
	 * : Parti başına yazı (varsayılan 200).
	 * [--limit=<n>]
	 * : En çok bu kadar yazı.
	 * [--rapor=<csv>]
	 * : Rapor dosyası.
	 * [--uygula]
	 * : Terimleri gerçekten ekle (geri alınabilir parti açılır).
	 *
	 * @subcommand siniflandir
	 */
	public function siniflandir( $args, $assoc ) {
		$apply  = ! empty( $assoc['uygula'] );
		$min    = isset( $assoc['guven'] ) && 'orta' === $assoc['guven'] ? 2 : 3;
		$sira   = array( 'yuksek' => 3, 'orta' => 2, 'dusuk' => 1 );
		$only   = isset( $assoc['varlik'] ) ? array_filter( explode( ',', $assoc['varlik'] ) ) : array();
		$size   = isset( $assoc['sayfa-boyu'] ) ? max( 10, (int) $assoc['sayfa-boyu'] ) : 200;
		$limit  = isset( $assoc['limit'] ) ? (int) $assoc['limit'] : 0;
		$batch  = $apply ? 'eka-' . gmdate( 'Ymd-His' ) . '-' . wp_generate_password( 4, false ) : '';
		$report = isset( $assoc['rapor'] ) ? fopen( $assoc['rapor'], 'w' ) : null; // phpcs:ignore
		if ( $report ) {
			fputcsv( $report, array( 'yazi_id', 'dil', 'baslik', 'varlik', 'guven', 'arsiv', 'durum', 'neden' ) );
		}
		$stats = array( 'yazi' => 0, 'eklenecek' => 0, 'eklendi' => 0, 'zaten_bagli' => 0, 'editor_onayi' => 0, 'hub_yok' => 0, 'dil_yok' => 0 );
		if ( $apply ) {
			wp_defer_term_counting( true );
		}
		$page = 1;
		do {
			$q = array(
				'post_type'        => 'post',
				'post_status'      => 'publish',
				'posts_per_page'   => $size,
				'paged'            => $page,
				'orderby'          => 'ID',
				'order'            => 'DESC',
				'fields'           => 'ids',
				'suppress_filters' => true,
				'lang'             => isset( $assoc['dil'] ) ? $assoc['dil'] : '',
			);
			$ids = get_posts( $q );
			foreach ( $ids as $pid ) {
				if ( $limit && $stats['yazi'] >= $limit ) {
					break 2;
				}
				$stats['yazi']++;
				$p = get_post( $pid );
				$s = EKA_Admin::suggestions( $pid, $p->post_title, $p->post_excerpt, $p->post_content );
				if ( null === $s['lang'] ) {
					$stats['dil_yok']++;
					continue;
				}
				$add = array(); // tax => [term_id => entity]
				foreach ( $s['oneriler'] as $o ) {
					if ( $only && ! in_array( $o['varlik'], $only, true ) ) {
						continue;
					}
					if ( 'dusuk' === $o['guven'] ) {
						continue;
					}
					if ( ! $o['arsiv'] ) {
						$durum = 'hub_yok';
					} elseif ( $o['arsiv']['bagli'] ) {
						$durum = 'zaten_bagli';
					} elseif ( $sira[ $o['guven'] ] >= $min ) {
						$durum = 'eklenecek';
						$add[ $o['arsiv']['tax'] ][ $o['arsiv']['id'] ] = array( $o['varlik'], $o['guven'] );
					} else {
						$durum = 'editor_onayi';
					}
					$stats[ $durum ]++;
					if ( $report ) {
						fputcsv( $report, array( $pid, $s['lang'], $p->post_title, $o['varlik'], $o['guven'], $o['arsiv'] ? $o['arsiv']['tax'] . ':' . $o['arsiv']['id'] : '', $durum, $o['neden'] ) );
					}
				}
				if ( $apply && $add ) {
					$stats['eklendi'] += $this->apply_terms( $pid, $add, $batch );
				}
			}
			$page++;
			if ( function_exists( 'wp_cache_flush_runtime' ) ) {
				wp_cache_flush_runtime();
			}
		} while ( count( $ids ) === $size );
		if ( $apply ) {
			wp_defer_term_counting( false );
		}
		if ( $report ) {
			fclose( $report ); // phpcs:ignore
		}
		WP_CLI\Utils\format_items( 'table', array( $stats ), array_keys( $stats ) );
		if ( $apply ) {
			WP_CLI::success( "Parti: {$batch}  (geri almak için: wp eka geri-al {$batch})" );
		} else {
			WP_CLI::warning( 'KURU çalışma: hiçbir yazı değiştirilmedi. Uygulamak için --uygula.' );
		}
	}

	/** Terimleri ekler; birincil kategoriyi korur; Polylang eşitlemesiyle çevirilere geçen terimleri de günlüğe yazar. */
	private function apply_terms( $pid, $add, $batch ) {
		$n            = 0;
		$translations = function_exists( 'pll_get_post_translations' ) ? array_diff( array_values( pll_get_post_translations( $pid ) ), array( $pid ) ) : array();
		foreach ( $add as $tax => $terms ) {
			$before = array();
			foreach ( $translations as $tid ) {
				$before[ $tid ] = wp_get_object_terms( $tid, $tax, array( 'fields' => 'ids' ) );
			}
			if ( 'category' === $tax && defined( 'RANK_MATH_VERSION' ) && ! get_post_meta( $pid, 'rank_math_primary_category', true ) ) {
				$cur = wp_get_object_terms( $pid, 'category', array( 'fields' => 'ids', 'orderby' => 'term_order' ) );
				if ( $cur ) {
					// Görünen ana kategori ve breadcrumb değişmesin.
					update_post_meta( $pid, 'rank_math_primary_category', (int) $cur[0] );
					EKA_Log::add( $batch, $pid, 'rank_math_primary_category', (int) $cur[0], 'meta_set' );
				}
			}
			$ids = array_map( 'intval', array_keys( $terms ) );
			$r   = wp_set_object_terms( $pid, $ids, $tax, true );
			if ( is_wp_error( $r ) ) {
				WP_CLI::warning( "#{$pid}: " . $r->get_error_message() );
				continue;
			}
			foreach ( $terms as $term_id => $info ) {
				EKA_Log::add( $batch, $pid, $tax, (int) $term_id, 'add', $info[0], $info[1] );
				$n++;
			}
			foreach ( $translations as $tid ) {
				$after = wp_get_object_terms( $tid, $tax, array( 'fields' => 'ids' ) );
				foreach ( array_diff( $after, $before[ $tid ] ) as $new ) {
					EKA_Log::add( $batch, $tid, $tax, (int) $new, 'add_sync' );
				}
			}
		}
		return $n;
	}

	/**
	 * Bir partinin eklediği terimleri kaldırır (yalnız o partinin ekledikleri).
	 *
	 * ## OPTIONS
	 * <parti>
	 * [--uygula]
	 *
	 * @subcommand geri-al
	 */
	public function geri_al( $args, $assoc ) {
		$rows = EKA_Log::batch_rows( $args[0] );
		if ( ! $rows ) {
			WP_CLI::error( 'Parti bulunamadı.' );
		}
		WP_CLI::log( count( $rows ) . ' ekleme geri alınacak.' );
		if ( empty( $assoc['uygula'] ) ) {
			WP_CLI::warning( 'KURU çalışma: --uygula ile geri alın.' );
			return;
		}
		wp_defer_term_counting( true );
		foreach ( $rows as $r ) {
			wp_remove_object_terms( (int) $r->post_id, (int) $r->term_id, $r->taxonomy );
			EKA_Log::add( $args[0], (int) $r->post_id, $r->taxonomy, (int) $r->term_id, 'remove' );
		}
		global $wpdb;
		$metas = $wpdb->get_results( $wpdb->prepare( 'SELECT post_id, term_id FROM ' . EKA_Log::table() . ' WHERE batch = %s AND action = %s', $args[0], 'meta_set' ) ); // phpcs:ignore
		foreach ( $metas as $m ) {
			if ( (int) get_post_meta( $m->post_id, 'rank_math_primary_category', true ) === (int) $m->term_id ) {
				delete_post_meta( $m->post_id, 'rank_math_primary_category' );
			}
		}
		wp_defer_term_counting( false );
		WP_CLI::success( 'Geri alındı.' );
	}

	/**
	 * Partileri listeler.
	 *
	 * @subcommand partiler
	 */
	public function partiler() {
		WP_CLI\Utils\format_items( 'table', array_map( 'get_object_vars', EKA_Log::batches() ), array( 'batch', 'baslangic', 'ekleme', 'geri_alinan' ) );
	}

	/**
	 * Hub arşivlerinin kalite/indeks denetimi.
	 *
	 * ## OPTIONS
	 * [--format=<format>]
	 * : table | csv | json
	 *
	 * @subcommand denetle
	 */
	public function denetle( $args, $assoc ) {
		$rows = array();
		foreach ( EKA_Dictionary::hubs() as $key => $h ) {
			$t = get_term( (int) $h['id'], $h['tax'] );
			if ( ! $t || is_wp_error( $t ) ) {
				continue;
			}
			$q      = EKA_Hubs::quality( $t );
			$rows[] = array(
				'anahtar'  => $key,
				'terim'    => $t->taxonomy . ':' . $t->term_id . ' ' . $t->name,
				'url'      => get_term_link( $t ),
				'yazi'     => $t->count,
				'hub'      => EKA_Hubs::is_hub( $t ) ? 'evet' : '',
				'karar'    => $q['karar'],
				'nedenler' => implode( '; ', $q['nedenler'] ),
				'indeks'   => EKA_SEO::indexable( $t ) ? 'index' : 'noindex',
				'kopya'    => count( $h['kopya'] ),
			);
		}
		WP_CLI\Utils\format_items( isset( $assoc['format'] ) ? $assoc['format'] : 'table', $rows, array( 'anahtar', 'terim', 'yazi', 'hub', 'karar', 'indeks', 'kopya', 'nedenler', 'url' ) );
	}

	/**
	 * Bir varlığın arşivini hub olarak kurar: H1, tanıtım, ilgili arşivler ve (boşsa) Rank Math başlık/açıklama.
	 * Metinler seo_metinleri.json'dan gelir. Varsayılan KURU.
	 *
	 * ## OPTIONS
	 * <metin_dosyasi>
	 * --dil=<dil>
	 * [--varlik=<liste>]
	 * [--uygula]
	 *
	 * @subcommand hub-kur
	 */
	public function hub_kur( $args, $assoc ) {
		$texts = json_decode( file_get_contents( $args[0] ), true ); // phpcs:ignore
		$lang  = $assoc['dil'];
		$only  = isset( $assoc['varlik'] ) ? array_filter( explode( ',', $assoc['varlik'] ) ) : array();
		$rows  = array();
		foreach ( $texts as $key => $x ) {
			list( $site, $l, $eid ) = array_pad( explode( ':', $key ), 3, '' );
			if ( $l !== $lang || ( $only && ! in_array( $eid, $only, true ) ) ) {
				continue;
			}
			$h = EKA_Dictionary::hub_for( $lang, $eid );
			if ( ! $h ) {
				$rows[] = array( 'varlik' => $eid, 'terim' => '—', 'islem' => 'hub eşlemesi yok (yeni arşiv kararı gerekli)' );
				continue;
			}
			$tid  = (int) $h['id'];
			$todo = array( 'eka_hub' => '1', 'eka_varlik' => $eid, 'eka_h1' => $x['h1'], 'eka_intro' => $x['tanitim'] );
			$rm   = array();
			if ( ! get_term_meta( $tid, 'rank_math_title', true ) ) {
				$rm['rank_math_title'] = $x['seo_title'];
			}
			if ( ! get_term_meta( $tid, 'rank_math_description', true ) ) {
				$rm['rank_math_description'] = $x['meta_description'];
			}
			$rows[] = array( 'varlik' => $eid, 'terim' => $h['tax'] . ':' . $tid, 'islem' => 'hub + ' . implode( ',', array_keys( $rm ) ) );
			if ( ! empty( $assoc['uygula'] ) ) {
				foreach ( $todo + $rm as $k => $v ) {
					update_term_meta( $tid, $k, $v );
				}
			}
		}
		WP_CLI\Utils\format_items( 'table', $rows, array( 'varlik', 'terim', 'islem' ) );
		if ( empty( $assoc['uygula'] ) ) {
			WP_CLI::warning( 'KURU çalışma: --uygula ile yazın. Rank Math başlık/açıklaması doluysa ezilmez.' );
		}
	}
}
