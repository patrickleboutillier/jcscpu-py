from hdl import *
from modules import jbuf


class jshiftr:
    def __init__(self, bis, wci, bos, wco):
        jbuf(bis[0], wco) 
        for j in range(1, 8):
            jbuf(bis[j], bos[j-1])
        jbuf(wci, bos[7])


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    wci, wco = wire("wci"), wire("wco")
    jshiftr(bis, wci, bos, wco)

    t = test(bis + [wci], bos + [wco])
    t.case([0, 1, 0, 1, 0, 1, 0, 1, 0], [1, 0, 1, 0, 1, 0, 1, 0, 0])
    t.case([0, 1, 0, 1, 0, 1, 0, 1, 1], [1, 0, 1, 0, 1, 0, 1, 1, 0])
    t.case([1, 0, 1, 0, 1, 0, 1, 0, 0], [0, 1, 0, 1, 0, 1, 0, 0, 1])
    t.case([1, 0, 1, 0, 1, 0, 1, 0, 1], [0, 1, 0, 1, 0, 1, 0, 1, 1])
