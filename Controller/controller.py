from evdev import InputDevice, list_devices, categorize, ecodes
from selectors import DefaultSelector, EVENT_READ

key_mapping = {
    115:"C",    # Up
    114:"D",    # Down
    272:"A",    # Right     # Okay
    1:"B"       # Left      # Back
                }
subscriber = []

def in_key_mapping(key:int):
    for i in key_mapping:
        if i == key:
            return True
    return False

def main():
    selector = DefaultSelector()
    devices = [InputDevice(fn) for fn in list_devices()]
    devs = []
    for device in devices:
        print(device.fn, device.name, device.phys)
        if device.name == "VR-PARK":
            dev = InputDevice(device.fn)
            dev.grab()
            selector.register(dev, EVENT_READ)

    while True:
        for key, mask in selector.select():
            print("[1]event" + str(key) + " "+ str(mask))
            device = key.fileobj
            for event in device.read():
                if event.type == ecodes.EV_KEY:
                    if categorize(event).keystate == 1 and not in_key_mapping(event.code):
                        for m in subscriber:
                            print("Event geschmießen")
                            m(event.code, key.fd)



def subscribe(method):
    """This method should get a method like this method(button : int, by: int) if this not the case, your method will not be added"""
    global subscriber
    subscriber.append(method)


def unsubscribe(method):
    global subscriber
    subscriber.remove(method)

