<?php
/**
 * FluentSnippets body for rootsandfruit.com AI crawler robots.txt rules.
 *
 * Deploy: FluentSnippets → Add snippet (PHP, run everywhere) OR
 *   rootsandfruit/snippets-create + snippets-activate (admin Application Password).
 *
 * Policy: block model-training crawlers; allow retrieval/citation bots.
 * @see https://specification.website/spec/agent-readiness/robots-for-ai-crawlers/
 *
 * Copy from the line after this block comment — omit the opening <?php tag.
 */

add_action(
	'wp_abilities_api_init',
	static function (): void {
		rf_register_agent_abilities(
			array(
				array(
					'slug'        => 'ai-crawler-robots-policy',
					'label'       => 'AI crawler robots policy',
					'description' => 'Documents named AI crawler allow/disallow rules on robots.txt.',
					'handler'     => 'rf_handler_ai_crawler_robots_policy',
					'permission'  => 'read',
					'readonly'    => true,
				),
			)
		);
	}
);

/**
 * @param array<string, mixed> $input
 * @return array<string, mixed>
 */
function rf_handler_ai_crawler_robots_policy( array $input = array() ): array {
	return array(
		'policy'              => 'training-disallow-retrieval-allow',
		'training_disallow'   => array(
			'GPTBot',
			'Google-Extended',
			'Applebot-Extended',
			'ClaudeBot',
			'anthropic-ai',
			'CCBot',
			'Bytespider',
		),
		'retrieval_allow'     => array(
			'OAI-SearchBot',
			'ChatGPT-User',
			'PerplexityBot',
		),
		'reference'           => 'https://specification.website/spec/agent-readiness/robots-for-ai-crawlers/',
		'llms_txt'            => home_url( '/llms.txt' ),
	);
}

add_filter(
	'robots_txt',
	static function ( string $output, bool $public ): string {
		if ( ! $public ) {
			return $output;
		}

		$rules = <<<'TXT'

# AI crawlers — explicit policy (https://rootsandfruit.com/llms.txt)
User-agent: GPTBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: PerplexityBot
Allow: /
TXT;

		return rtrim( $output ) . "\n" . $rules . "\n";
	},
	100,
	2
);
