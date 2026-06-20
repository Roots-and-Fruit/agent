<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Filesystem;

interface Factory
{
    /**
     * Get a filesystem implementation.
     *
     * @param  string  $name
     * @return \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Filesystem\Filesystem
     */
    public function disk($name = null);
}
