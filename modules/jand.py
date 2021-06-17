from hdl import *
from modules import jnand, jnot


class jand:
    def __init__(self, a, b, c):
        w = wire()
        jnand(a, b, w)
        jnot(w, c)


if __name__ == "__main__":
    a, b, c = map(wire, ["a", "b", "c"])
    x = jand(a, b, c)
    
    t = test([a, b], [c])
    t.case([0, 0], [0])
    t.case([0, 1], [0])
    t.case([1, 0], [0])
    t.case([1, 1], [1])
