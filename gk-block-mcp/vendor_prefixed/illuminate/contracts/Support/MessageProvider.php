<?php

namespace GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Support;

interface MessageProvider
{
    /**
     * Get the messages for the instance.
     *
     * @return \GravityKit\BlockMCP\Foundation\ThirdParty\Illuminate\Contracts\Support\MessageBag
     */
    public function getMessageBag();
}
