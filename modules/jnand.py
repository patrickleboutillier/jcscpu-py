from hdl import *


class jnand:
    def __init__(self, wa, wb, wc):
        nand(wa, wb, wc)

if __name__ == "__main__":
    a, b, c = map(wire, ["a", "b", "c"])
    jnand(a, b, c)
    
    t = test([a, b], [c])
    t.case([0, 0], [1])
    t.case([0, 1], [1])
    t.case([1, 0], [1])
    t.case([1, 1], [0])
