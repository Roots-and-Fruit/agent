<?php

namespace GravityKit\BlockMCP\Foundation\CLI\Commands;

use GravityKit\BlockMCP\Foundation\CLI\AbstractCommand;
use GravityKit\BlockMCP\Foundation\Core as GravityKitFoundation;
use WP_CLI;

/**
 * Manage GravityKit products and licenses.
 */
class Root extends AbstractCommand {
	/**
	 * Display GravityKit Foundation version.
	 *
	 * @since      1.2.0
	 *
	 * @subcommand version
	 *
	 * @return void
	 */
	public function version() {
		$foundation_information = GravityKitFoundation::get_instance()->get_foundation_information();

		WP_CLI::line( $foundation_information['loaded_by_message'] );
	}
}
