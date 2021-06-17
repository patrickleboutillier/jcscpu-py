from hdl import *
from modules import jnand, jnot


class jor:
    def __init__(self, wa, wb, wc):
        wic = wire()
        wid = wire()
        jnot(wa, wic)
        jnot(wb, wid)
        jnand(wic, wid, wc)


if __name__ == "__main__":
    a, b, c = map(wire, ["a", "b", "c"])
    x = jor(a, b, c)
    
    t = test([a, b], [c])
    t.case([0, 0], [0])
    t.case([0, 1], [1])
    t.case([1, 0], [1])
    t.case([1, 1], [1])
