import re


WIRES = {}


class wire:
    _cnt = 0

    def __init__(self, label="", init=0):
        self._assigned = False
        self._init = init
        self._label = label
        self._id = wire._cnt
        wire._cnt += 1
        WIRES[self._id] = self


def bus(n=8, label=""):
    ret = []
    for i in range(n):
        wlab = label
        if wlab != "":
            wlab = wlab + "[" + str(i) + "]"
        ret.append(wire(wlab))
    return ret


def dump_wires():
    print("""
#include <Arduino.h>


byte WIRES[512] = {} ;

""")
    for i in sorted(WIRES):
        w = WIRES[i]
        if not w._assigned:
            if w._label != "":
                label = re.sub(r'\[(\d+)\]', r'_\1', w._label)
                print('#define {}\t{}'.format(label, w._id))
    
    print("""

void hdl_wire_init(){""")
    for i in sorted(WIRES):
        w = WIRES[i]
        if not w._assigned:
            if w._init != 0:
                print('\tbitSet(WIRES[{0} / 8], {0} % 8]) ;'.format(w._id))
    print("}")


wire.GND = wire("GND")
wire.VCC = wire("VCC", 1)
wire.RESET = wire("RESET", 1)
