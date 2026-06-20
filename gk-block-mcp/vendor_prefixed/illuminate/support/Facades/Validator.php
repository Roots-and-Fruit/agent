<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Validation\Factory
 */
class Validator extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return 'validator';
    }
}
