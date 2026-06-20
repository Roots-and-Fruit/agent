<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

use GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Testing\Fakes\BusFake;
use GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Bus\Dispatcher as BusDispatcherContract;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Bus\Dispatcher
 */
class Bus extends Facade
{
    /**
     * Replace the bound instance with a fake.
     *
     * @return void
     */
    public static function fake()
    {
        static::swap(new BusFake);
    }

    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return BusDispatcherContract::class;
    }
}
