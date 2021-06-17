from hdl import *
from modules import jor


class jorer:
    def __init__(self, bas, bbs, bcs):
        for j in range(8):
            jor(bas[j], bbs[j], bcs[j])


if __name__ == "__main__":
    bas = bus(8, "bas")
    bbs = bus(8, "bbs")
    bcs = bus(8, "bcs")
    x = jorer(bas, bbs, bcs)

    t = test(bas + bbs, bcs)
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1])
    t.case([0, 1, 0, 0, 0, 0, 0, 0] + [1, 0, 1, 0, 1, 0, 1, 0], [1, 1, 1, 0, 1, 0, 1, 0])
