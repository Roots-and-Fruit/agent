<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Queue;

interface Factory
{
    /**
     * Resolve a queue connection instance.
     *
     * @param  string  $name
     * @return \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Queue\Queue
     */
    public function connection($name = null);
}
