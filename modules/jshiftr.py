from hdl import *
from modules import jbuf


class jshiftr:
    def __init__(self, bis, wci, bos, wco):
        jbuf(wci, bos[0]) 
        for j in range(1, 8):
            jbuf(bis[j-1], bos[j])
        jbuf(bis[7], wco)


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    wci, wco = wire("wci"), wire("wco")
    jshiftr(bis, wci, bos, wco)

    t = test(bis + [wci], bos + [wco])
    t.case([0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 0, 1, 0, 1, 0, 1])
    t.case([0, 1, 0, 1, 0, 1, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1])
    t.case([1, 0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0])
    t.case([1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 1, 0, 1, 0, 1, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 1])