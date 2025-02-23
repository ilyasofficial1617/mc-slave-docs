# Joined Event
A joined event allows for some args of an event to be mutated or for the event to be cancelled. As of 1.9.0, this is handled per-script for events that support joining. A joined event will use a watchdog in order to keep your script from freezing the game. For more info, do `!watchdog` or `!threading`.

## Joined To Main Error
If you are getting an error that a function is not supported because you are "joined to main," the solution is to do `context.releaseLock()` - which will finalize changes to these Joined scripts. This is because the function you are calling requires Minecraft to continue running in order to process. If you are in a `JsMacros.on` function, this is the second argument (it's also in the return value for `JsMacros.waitForEvent`).

## Script setting
The script can be set to join or fork by using the `:script_join:` or `:script_fork:` tags. With the default settings, the script will fork.


## Join: `:script_join:`
The script will be joined and the event can be mutated/cancelled before the client processes it.

## Fork: `:script_fork:`
The script will fork; while the event may still be mutated, it is not recommended as the client won't receive the changed result as the script runs in parallel to the client processing the event.

## Old Behavior
Prior to 1.9.0, this was a bit inconsistent. You could determine if an event was joined if it either had a name starting with "Joined" or had a non-final field, and the script doesn't have a choice to not be joined at trigger-time.