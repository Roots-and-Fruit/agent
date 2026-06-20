<?php

/**
 * Wrapper for key internal GravityKit components (Settings, Licenses, Translations, etc.) and other utility classes.
 *
 * @package     GravityKit_Foundation
 * @author      GravityKit
 * @copyright   2024 GravityKit
 * @license     GPL-2.0+
 *
 * @wordpress-plugin
 *
 * Plugin Name:       GravityKit Foundation (Standalone)
 * Plugin URI:        https://www.gravitykit.com
 * Description:       Wrapper for key internal GravityKit components (Settings, Licenses, Translations, etc.) and other utility classes.
 * Version:           1.21.0
 * Author:            GravityKit
 * Author URI:        https://www.gravitykit.com
 * Text Domain:       gk-foundation
 * License:           GPL-2.0+
 * License URI:       http://www.gnu.org/licenses/gpl-2.0.txt
 */
if (!defined('WPINC')) {
    die;
}
require_once __DIR__ . '/src/preflight_check.php';
if (!\GravityKit\BlockMCP\Foundation\should_load(__FILE__)) {
    return;
}
require_once __DIR__ . '/vendor/autoload.php';
require_once __DIR__ . '/vendor_prefixed/autoload.php';
\GravityKit\BlockMCP\Foundation\Core::register(__FILE__);