<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

use GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Broadcasting\Factory as BroadcastingFactoryContract;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Broadcasting\Factory
 */
class Broadcast extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return BroadcastingFactoryContract::class;
    }
}
