<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

use GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Auth\Access\Gate as GateContract;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Auth\Access\Gate
 */
class Gate extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return GateContract::class;
    }
}
