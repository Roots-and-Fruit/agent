<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Support\Facades;

/**
 * @see \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Filesystem\Filesystem
 */
class File extends Facade
{
    /**
     * Get the registered name of the component.
     *
     * @return string
     */
    protected static function getFacadeAccessor()
    {
        return 'files';
    }
}
