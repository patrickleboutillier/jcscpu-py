
from hdl import *
from modules import jand


class jbuf:
    def __init__(self, wa, wb):
        jand(wa, wa, wb)


if __name__ == "__main__":
    a, b = map(wire, ["a", "b"])
    x = jbuf(a, b)
    
    t = test([a], [b])
    t.case([0], [0])
    t.case([1], [1])
