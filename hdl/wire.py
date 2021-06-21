

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
    for i in sorted(WIRES):
        w = WIRES[i]
        if not w._assigned:
            print('WIRE {} {} {}'.format(w._id, w._init, w._label))


wire.GND = wire("GND")
wire.VCC = wire("VCC", 1)
wire.RESET = wire("RESET", 1)
