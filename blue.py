import logging
import sys
log = logging.getLogger()
log.setLevel(logging.DEBUG)
stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log.addHandler(stream)

import bluefang
bluetooth = bluefang.Bluefang()
bluetooth.register_profile("/omnihub/profile")
bluetooth.scan(5000)
device = bluetooth.connect("D0:03:4B:24:57:84")
