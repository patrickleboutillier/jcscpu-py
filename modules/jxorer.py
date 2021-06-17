from hdl import *
from modules import jcmp


class jxorer:
    def __init__(self, bas, bbs, bcs, weqo, walo):
        teqo, talo = bus(8), bus(8)
        jcmp(bas[0], bbs[0], wire.VCC, wire.GND, bcs[0], teqo[0], talo[0])
        for j in range(1, 7):
            jcmp(bas[j], bbs[j], teqo[j-1], talo[j-1], bcs[j], teqo[j], talo[j])
        jcmp(bas[7], bbs[7], teqo[6], talo[6], bcs[7], weqo, walo) 


if __name__ == "__main__":
    bas = bus(8, "bas")
    bbs = bus(8, "bbs")
    bcs = bus(8, "bcs")
    weqo, walo = wire("weqo"), wire("walo")
    jxorer(bas, bbs, bcs, weqo, walo)

    t = test(bas + bbs, bcs + [weqo, walo])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0] + [1, 0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0] + [1, 0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0] + [1, 0])
    t.case([1, 1, 1, 1, 1, 1, 1, 1] + [0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1] + [0, 1])
    t.case([0, 1, 0, 0, 0, 0, 0, 1] + [1, 0, 1, 0, 1, 0, 1, 1], [1, 1, 1, 0, 1, 0, 1, 0] + [0, 0])