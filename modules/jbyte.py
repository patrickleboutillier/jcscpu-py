from hdl import *
from modules import jmem, jor


class jbyte:
    def __init__(self, bis, ws, bos):
        for j in range(len(bis)):
            jmem(bis[j], ws, bos[j])


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    ws, wsr = wire("ws"), wire("wsr")
    jor(ws, wire.RESET, wsr)
    x = jbyte(bis, wsr, bos)

    t = test(bis + [ws], bos)
    # Output is undefined until 's' has been set once! 
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0])
    t.case([1, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 0])
    t.case([0, 0, 0, 0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 1, 0, 0, 0])
    t.case([0, 0, 0, 0, 1, 0, 0, 0, 1], [0, 0, 0, 0, 1, 0, 0, 0])
    t.case([0, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0, 0, 0])
    t.case([0, 0, 0, 0, 1, 1, 1, 1, 0], [0, 0, 0, 0, 1, 0, 0, 0]) 
    t.case([0, 0, 0, 0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 1, 1, 1])
