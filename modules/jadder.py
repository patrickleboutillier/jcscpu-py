from hdl import *
from modules import jand, jadd


class jadder:
    def __init__(self, bas, bbs, wci, bcs, wco):
        tc = bus(7)
        jadd(bas[7], bbs[7], wci, bcs[7], tc[0]) 
        for j in range(1, 7):
            jadd(bas[7-j], bbs[7-j], tc[j-1], bcs[7-j], tc[j])
        jadd(bas[0], bbs[0], tc[6], bcs[0], wco) 


if __name__ == "__main__":
    bas = bus(8, "bas")
    bbs = bus(8, "bbs")
    bcs = bus(8, "bcs")
    wci, wco = wire("wci"), wire("wco")
    jadder(bas, bbs, wci, bcs, wco)

    t = test(bas + bbs + [wci], bcs + [wco])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] + [0], [0, 0, 0, 0, 0, 0, 0, 0] + [0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1] + [0], [1, 1, 1, 1, 1, 1, 1, 0] + [1])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0], [1, 1, 1, 1, 1, 1, 1, 1] + [0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [1], [0, 0, 0, 0, 0, 0, 0, 0] + [1])
    t.case([0, 0, 0, 1, 0, 1, 0, 0] + [0, 0, 0, 1, 0, 1, 1, 0] + [0], [0, 0, 1, 0, 1, 0, 1, 0] + [0])