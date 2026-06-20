<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

use GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Routing\ResponseFactory as ResponseFactoryContract;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Routing\ResponseFactory
 */
class Response extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return ResponseFactoryContract::class;
    }
}
