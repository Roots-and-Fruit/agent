<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

/**
 * @see \Illuminate\Redis\RedisManager
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Redis\Factory
 */
class Redis extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return 'redis';
    }
}
