from hdl import *
from modules import jand, jadd


class jadder:
    def __init__(self, bas, bbs, wci, bcs, wco):
        lb = len(bas) - 1
        tc = bus(lb)
        jadd(bas[lb], bbs[lb], wci, bcs[lb], tc[0]) 
        for j in range(1, lb):
            jadd(bas[lb-j], bbs[lb-j], tc[j-1], bcs[lb-j], tc[j])
        jadd(bas[0], bbs[0], tc[lb-1], bcs[0], wco) 


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