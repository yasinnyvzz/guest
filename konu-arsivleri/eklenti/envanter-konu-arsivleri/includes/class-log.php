<?php
/**
 * Toplu işlem günlüğü (geri alma için). Her ekleme bir satırdır; geri alma yalnız o partinin eklediklerini kaldırır.
 */

defined( 'ABSPATH' ) || exit;

class EKA_Log {

	const DB_VERSION = '1';

	public static function table() {
		global $wpdb;
		return $wpdb->prefix . 'eka_log';
	}

	public static function install() {
		global $wpdb;
		require_once ABSPATH . 'wp-admin/includes/upgrade.php';
		$t = self::table();
		dbDelta(
			"CREATE TABLE {$t} (
				id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
				batch VARCHAR(40) NOT NULL,
				post_id BIGINT UNSIGNED NOT NULL,
				taxonomy VARCHAR(32) NOT NULL,
				term_id BIGINT UNSIGNED NOT NULL,
				action VARCHAR(16) NOT NULL,
				entity VARCHAR(64) NOT NULL DEFAULT '',
				confidence VARCHAR(8) NOT NULL DEFAULT '',
				created DATETIME NOT NULL,
				PRIMARY KEY  (id),
				KEY batch (batch),
				KEY post_term (post_id, term_id)
			) {$wpdb->get_charset_collate()};"
		);
		update_option( 'eka_db_version', self::DB_VERSION, false );
	}

	public static function maybe_upgrade() {
		if ( get_option( 'eka_db_version' ) !== self::DB_VERSION ) {
			self::install();
		}
	}

	public static function add( $batch, $post_id, $taxonomy, $term_id, $action, $entity = '', $confidence = '' ) {
		global $wpdb;
		$wpdb->insert( // phpcs:ignore WordPress.DB.DirectDatabaseQuery
			self::table(),
			array(
				'batch'      => $batch,
				'post_id'    => $post_id,
				'taxonomy'   => $taxonomy,
				'term_id'    => $term_id,
				'action'     => $action,
				'entity'     => $entity,
				'confidence' => $confidence,
				'created'    => current_time( 'mysql', true ),
			)
		);
	}

	public static function batch_rows( $batch ) {
		global $wpdb;
		return $wpdb->get_results( $wpdb->prepare( 'SELECT * FROM ' . self::table() . ' WHERE batch = %s AND action IN (%s, %s) ORDER BY id DESC', $batch, 'add', 'add_sync' ) ); // phpcs:ignore
	}

	public static function batches() {
		global $wpdb;
		return $wpdb->get_results( 'SELECT batch, MIN(created) AS baslangic, SUM(action IN (\'add\',\'add_sync\')) AS ekleme, SUM(action = \'remove\') AS geri_alinan FROM ' . self::table() . ' GROUP BY batch ORDER BY baslangic DESC' ); // phpcs:ignore
	}
}
