from evdev import InputDevice, list_devices, categorize, ecodes
from selectors import DefaultSelector, EVENT_READ
from threading import Thread
from mapping import *

subscriber = []

def in_key_mapping(key:int, key_map):
    for i in key_map.keys():
        if i == key:
            return True
    return False

def main():
    selector = DefaultSelector()
    devices = [InputDevice(fn) for fn in list_devices()]
    for device in devices:
        print(device.fn, device.name, device.phys)
        for name in key_mapping.keys():
            if name in device.name:
                dev = InputDevice(device.fn)
                dev.grab()
                selector.register(dev, EVENT_READ)

    while True:
        for key, mask in selector.select():
            device = key.fileobj
            key_map = get_key_mapping(device.name)
            for event in device.read():
                if event.type == ecodes.EV_KEY and key_map != None:
                    cat = categorize(event)
                    print("[!]event"+str(event.code))
                    if cat.keystate == 1 and in_key_mapping(event.code, key_map):
                        for m in subscriber:
                            print("Event geschmissen")
                            Thread(target=m, args=(key_map[event.code], key.fd)).start()

def get_key_mapping(name):
    for mapping, ident in enumerate(key_mapping):
        if ident in name:
            return key_mapping[ident]
    return None


def subscribe(method):
    """This method should get a method like this method(button : int, by: int) if this not the case, your method will not be added"""
    global subscriber
    subscriber.append(method)


def unsubscribe(method):
    global subscriber
    subscriber.remove(method)

main()
