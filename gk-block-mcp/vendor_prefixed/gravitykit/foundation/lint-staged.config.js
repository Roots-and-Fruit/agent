module.exports = {
	'**/*.php': [
		// PHPCS accepts file paths - lint-staged passes them automatically
		'composer code:sniff',
		// PHPStan needs full project context for stubs - ignore file list
		() => 'composer code:analyze',
	],
	'{UI/Settings,UI/Licenses,UI/BackgroundJobs}/**/*.{json,js,cjs,svelte}': [
		'node lint-staged-ui.js',
	],
};
