from hdl import *
import modules.jadder as jadder


class mADDR_INCR:
    def __init__(self, addr_in, addr_out):
        one = bus(11) + [wire.VCC]
        null = wire()
        jadder.jadder(addr_in, one, wire.GND, addr_out, null)
 


if __name__ == "__main__":
    addr_in, addr_out = bus(12, "addr_in"), bus(12, "addr_out")
    mADDR_INCR(addr_in, addr_out)

    t = test(addr_in, addr_out)
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0])
    # Wrap around
    t.case([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 