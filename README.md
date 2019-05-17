# Internal Communication - Python

This document is WIP!

## FAQ
### When running a `main.py`, I get `No module named 'Client'`
Set the `PYTHONPATH` environment variable to the root directory of `r2d2-python-build`.
Use the entire path; things like `~` won't work!

### When running `main.py` i get `ConnectionRefusedError: No connection could be made because the target
machine actively refused it`
Ensure that the bus manager is running in the background. Start the manager with `python manager/manager.py`

## Introduction
### What makes a module?
A basic module consists of two files:
 - `main.py`, containing the `main()` function (which is symbolic in Python).
 - `module/mod.py`, the file containing the actual module.
 
 
### `main.py` 
A basic `main.py` file generally looks like this:
```python
from time import sleep
from sys import platform
import signal

from client.comm import Comm
from modules.template.module.mod import Module

should_stop = False


def main():
    print("Starting application...\n")
    module = Module(Comm())
    print("Module created...")

    while not should_stop:
        module.process()
        sleep(0.05)

    module.stop()


def stop(signal, frame):
    global should_stop
    should_stop = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)

if __name__ == "__main__":
    main()

```

Let's break that down:

`should_stop` is the global stop flag the program loop checks.


`main()` is the (symbolic) main function, containing the actual meat of the program. It instantiates the `Module` class and starts processing.

As you can see here, the `Module` class is instantiated with a `Comm` instance passed to the constructor:
```python
module = Module(Comm())
```
This works in the same fashion as the C++ internal communication module.

The following loop is important:
```python
while not should_stop:
    module.process()
    sleep(0.05)
```

Just like the C++ internal communication module, a `process` function is present on the module that processes all outstanding work.
The `sleep(0.05)` call is important. If we don't place that here, we'll occupy an entire CPU core for nothing.
 
If your module allows for a longer sleep, **please** increase this value! The longer the sleep is, the more room you'll leave for other modules on the host system.
Increasing this value too much will cause you to miss frames however, so please test.

Then there is the signal machinery:
```python
def stop(signal, frame):
    global should_stop
    should_stop = True


signal.signal(signal.SIGINT, stop)
signal.signal(signal.SIGTERM, stop)

if platform != "win32":
    signal.signal(signal.SIGQUIT, stop)
```
   
This will allow the module to correctly handle a shutdown request. This is also for your convenience; without this a `Ctrl+C` won't work correctly.

Lastly, this checks whether the current file is the starting point for the interpreter:
```python
if __name__ == "__main__":
    main() 
```
 


### `module/mod.py`
A basic `mod.py` looks like this (in this case, for the LED module):
```python
from client.comm import BaseComm
from common.frame_enum import FrameType


class Module:
    def __init__(self, comm: BaseComm):
        self.comm = comm
        self.comm.listen_for([FrameType.ACTIVITY_LED_STATE])

    def process(self):
        while self.comm.has_data():
            frame = self.comm.get_data()

            if frame.request:
                continue

            values = frame.get_data()

            if values[0]:
                print("The LED is ON")
            else:
                print("The LED is OFF")

    def stop(self):
        self.comm.stop()
```

Let's break that down:

In the constructor, a `comm` instance of type `BaseComm` is received. `BaseComm` is an interface that every communication module has to inherit from.
Then, the module specifies what frame types it wants to receive using `listen_for(...)`:
```python
self.comm.listen_for([FrameType.ACTIVITY_LED_STATE])
```

If you want to receive **all** frames, you can specify `FrameType.ALL`.

The process function works on all data that is not yet processed. Please note: if you don't process data often enough, you might miss some frames.
It is dependent on the module if this is a problem or not.

The following idiom is important:
```python
while self.comm.has_data():
    frame = self.comm.get_data()
``` 

It is important that you first check whether there is data available at all; calling `get_data()` when there is no data available will cause an exception.

#### Getting data from the frame
One major difference from the C++ internal communication module, is that there is an extra step to get the data out of a frame:
```python
 # Get the frame from the comm module
frame = self.comm.get_data()

# Extract the data out of the frame,
# the result will be a tuple
data = frame.get_data()

# We only process answers
if frame.request:
    continue

# Create the frame that will be send
# to the led module
state = FrameActivityLedState()

# Set the data.
state.set_data(data[0])

# Send it off!
self.comm.send(state)
```

The `get_data()` function deserializes data in the frame to a format Python can understand. All properties will be returned in a tuple.
In the example above, `data = frame.get_data()` returns a `(bool)`. 
Similarly, the `set_data(...)` function serializes the data into the frame.

The `set_data(...)` requires all properties to be set at once. 

### Where are the frametypes defined?
A script is used to parse the frame types from the C++ internal communication bus. To add your own frame type, create a PR there and it will be available here a bit later.

## About the system
### Requirements
Currently, the system requires port 5000 to be free upon manager startup. Modules will try to connect to this port.
This might be configurable in the future.

### Multiplatform
The system supports Linux and Windows. While Python itself is multiplatform, quite a bit of differences exist when, for example, using network sockets. It is expected of modules that they are also compatible with Linux and Windows.

### Local development
The `manager` can be started in the background and modules can connect to it, provided the port is free on manager start.

## Process based 

### Overview
This high level image should give an overview of how the system works. The squares represent the start of the process, the cyclic arrows represent threads.

[![Pythonbus-1.png](https://i.postimg.cc/tCb8F6MX/Pythonbus-1.png)](https://postimg.cc/kDjjm2CZ)

### Modules and processes
Every module should run in its owm process. Once created, the `Comm` class can be used to connect to the manager process that should be already running.
In practice, this means your module is started by simply doing `python3 module/main.py` while the manager is running in the background. **Make sure you manually start the manager**

### Processes vs threads (in Python)
In Python, there is something called the Global Interpreter Lock, or GIL.
This system regulates access to the Python interpreter; the interpreter can only do one thing at a time.
A consequence of this is that a CPU-bound thread can actually occupy the interpreter fully, defeating one of the advantages of multithreading.

The way around this in Python (and in this library) is using multiple processes. Communication works by interprocess communication and synchronization.
This system has a big advantage: modules (and the manager) are completely unrelated from each other. If a module were to crash, other modules are not affected.

A downside is that interprocess communication is tricky and can be quite slow (relatively) due to synchronization.
 

## Components
### Manager
`manager.py` in the `manager` folder is a file that should be started in a separate process. Start the manager with `python manager/manager.py`
When actually deployed, this file should run in the background as a service.
Modules can dynamically connect or disconnect from the manager application at will, providing a lot of flexibility.

### Module
Each module runs in its owm process, i.e. it is started separately with `python3 filename.py`.
This means every module will provide their owm `main.py`.
