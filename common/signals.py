#! python

"""this module handles all the signals"""

import datetime
import logging
import signal
import sys

__author__ = "Isha Geurtsen"
__date__ = datetime.datetime(2019, 6, 3)

_SIGNAL_HANDLERS = []
_CALLBACKS = []

def register_signal_handler(handler):
    """register a function to be called on receiving a signal.
    If the function returns true, the signal is considered resolved

    handler should be a function that takes a signal number and a stackframe
    """
    _SIGNAL_HANDLERS.append(handler)

def register_signal_callback(callback):
    """register a function to be called on shutdown after receiving an unhandled signal

    callback should be a function that takes no parameters
    """
    _CALLBACKS.append(callback)

def __handle_signal(signal_num, stack_frame):
    """internal method, called when a signal is received.
    when the signal remains unhandled, calls __stop"""
    logging.critical("received signal %s", signal.Signals(signal_num).name)
    for signal_handler in _SIGNAL_HANDLERS:
        if signal_handler(signal_num, stack_frame):
            return
    __stop(signal_num)

def __stop(signal_num):
    "internal method, called when a signal remains unhandled. "
    for callback in _CALLBACKS:
        callback()
    exit(signal_num)

signal.signal(signal.SIGINT, __handle_signal)
signal.signal(signal.SIGTERM, __handle_signal)

if sys.platform != "win32":
    signal.signal(signal.SIGQUIT, __handle_signal)  #pylint: disable=no-member
