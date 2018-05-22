#!/usr/bin/env python3

import pyscreenshot as ImageGrab
from time import time

last_time = time()
while(True):
    print(time() - last_time)
    last_time = time()
    im = ImageGrab.grab()
im.save('screenshot.png')
#im.show()
