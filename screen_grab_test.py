#!/usr/bin/env python3

# mss documentation:
# https://python-mss.readthedocs.io/examples.html

import mss
import mss.tools
from time import time

with mss.mss() as sct:
    monitor = {"top": 160, "left": 160, "width": 200, "height": 200}
    output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)

    last_time = time()
    while True:
        sct_img = sct.grab(monitor)
        new_time = time()
        print(new_time - last_time)
        last_time = time()
    print(sct_img.__dict__)
    print(len(sct_img.raw)/4)

    mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)
    print(output)

#from mss import mss
#
#with mss() as sct:
#    sct.shot()
