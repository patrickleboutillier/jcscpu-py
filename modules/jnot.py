
from hdl import *
from modules import jnand


class jnot:
    def __init__(self, wa, wb):
        jnand(wa, wa, wb)


if __name__ == "__main__":
    a, b = map(wire, ["a", "b"])
    x = jnot(a, b)
    
    t = test([a], [b])
    t.case([0], [1])
    t.case([1], [0])
