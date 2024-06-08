from typing import TypeVar, Callable

from PyP100.PyP100 import Device

T = TypeVar('T', bound=Device)
R = TypeVar('R')


def execute_device_method(device: T, function: Callable[[T], R]) -> R:
    try:
        return function(device)
    except:
        device.handshake()
        device.login()

    return function(device)
