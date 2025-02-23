# JsMacros Threading Model (JS/JEP)

JavaScript and JEP are "single threaded" languages. This means I had to do a bit of work to get them to actually run on more than one thread; they are still single threaded, but the thread is imaginary. As in, you can change which thread it's bound to (JS supported this; I had to hack JEP to make it work. Please let me know if that broke something).

## Actual Threading Model

As for their actual threading model now, they use a priority FIFO non-preemptive queue.

### What Does That Mean?

The priority part means that your threads can be assigned a priority which can determine what order they run in; FIFO means that they are run in the order inserted into the queue when they are the same priority. Non-preemptive means that threads can't interrupt each other (too much work to implement, and would probably lead to race conditions).

## Creating a New Thread

When Java calls your `JavaWrapped` function, it can do this on any thread, and that'll add it to the queue. You can tell it the priority as an argument in your wrapping functions. You can also create a new thread manually using `JavaWrapper.methodToJavaAsync(priority, functionToCall).run()`, as "Async" creates and does things on a new thread. Due to the threading model, this won't run immediately though...

## Getting the Next Thread to Run

You can defer the current thread in favor of the next one in the queue using `JavaWrapper.deferCurrentTask()` or one of the various "sleep" methods (`Client.waitTick`, `Time.sleep`, `JsMacros.waitForEvent`, I'm probably forgetting at least one more). These will insert the thread back at the end of the current priority's FIFO queue. In the case of the "sleep" methods, this happens after they have finished waiting. With `deferCurrentTask`, it accepts an argument to lower/raise its priority by adding the number you provide to its current priority. I'd suggest you keep priorities within 0-10, with 10 being the highest priority, but I didn't enforce any limits...