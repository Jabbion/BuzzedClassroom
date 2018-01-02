from evdev import *
import _thread
devices = [InputDevice(fn) for fn in list_devices()]
devs = []
for device in devices:
    print(device.fn, device.name, device.phys)
    if device.name == "VR-PARK":
        devs.append(device)
def test(dev,a):
    try:
        print(dev)

        for event in dev.read_loop():
            if event.type == ecodes.EV_KEY:
                print(dev, )
    except Exception as e:
        print(e)
for dev in devs:
    print(dev)
    _thread.start_new_thread( test, (dev, "a",  ) )
