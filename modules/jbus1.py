from hdl import *
from modules import jor, jnot, jand


class jenabler:
    def __init__(self, bis, wbit1, bos):
        wnbit1 = wire()
        jnot(wbit1, wnbit1)
  
        for j in range(8):
            if j < 7:
                jand(bis[j], wnbit1, bos[j])
            else:
                jor(bis[j], wbit1, bos[j]) 


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    wbit1 = wire("wbit1")
    jenabler(bis, wbit1, bos)

    t = test(bis + [wbit1], bos)
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 1, 0, 0, 0, 0, 1] + [0], [1, 0, 1, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [1], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 0, 0, 0, 0, 1] + [1], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 0, 0, 1, 0, 0] + [1], [0, 0, 0, 0, 0, 0, 0, 1])
