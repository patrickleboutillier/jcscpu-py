from hdl import *

a = wire()
b = wire()
c = wire("c")
a.assign(wire.GND)

x = nand(a, b, c)