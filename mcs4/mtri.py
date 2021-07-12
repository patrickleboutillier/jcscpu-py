from hdl import *
from modules import jnand, jnot


class mtri:
    def __init__(self, i, e, o):
        tri(i, e, o)


if __name__ == "__main__":
    i, e, o = map(wire, ["i", "e", "o"])
    mtri(i, e, o)
    
    t = test([i, e], [o])
    t.case([0, 0], [0])
    t.case([0, 1], [0])
    t.case([1, 0], [0])
    t.case([1, 1], [1])
