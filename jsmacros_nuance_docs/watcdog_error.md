# Watchdog Error
The watchdog error is there to prevent you from creating a script that locks Minecraft in a state where you'd have to Alt+F4 it. It prevents scripts from running on the "main" thread for over 500 ms (changeable in the config 😉).

These events run on the main thread as changes to the event contents affect the game:
- **SendMessage**
- **RecvMessage**
- **JoinedTick**
- **SignEdit**
- **ClickSlot**
- **DropSlot**

Someone let me know if I forgot one.

## Other ways to be on the main thread
Method wrappers passed into functions in the Hud library are sometimes run on the main thread (such as `Screen#setOnInit`).  
`Client#runOnMainThread` and some of the other functions that include a "callback" argument.

## Prevention
In order to release your event from the main thread, you can use `context.releaseLock()` (second argument if in `JsMacros.on`).

To prevent method wrappers from being on the main thread, use `JavaWrapper#methodToJavaAsync`, assuming they're not required to return anything. It is also not recommended to have async `Screen#setOnInit` functions. You may have to adjust the way your code is structured to fix this.

### (JS/JEP) Starving Joined JsMacros.on Events
Due to threading limitations on JavaScript (and JEP), it is possible to starve event listeners. The solution to this is to call `JavaWrapper.deferCurrentTask()` occasionally on threads that are long-lasting. (Do note that it is technically possible to starve during a `Client.waitTick()`, and the solution is to not sync to client ticks as of 1.7.0; I am working on fixing this though...)