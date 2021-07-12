import atexit

from .wire import *
from .nand import *
from .tri import *
from .test import *

atexit.register(dump_tests)
atexit.register(dump_tris)
atexit.register(dump_nands)
atexit.register(dump_wires)