#!/usr/bin/env python3

import threading
from moveForward import *
from moveBackward import *
from ballCage import *
from moveRight import *
from moveLeft import *
from moveStop import *
import time

print("start")
t1 = threading.Thread(target=move_forward, args=[50])
t2 = threading.Thread(target=move_stop, args=[50])

t1.start()
t2.start()

t1.join()
t2.join()
