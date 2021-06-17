from hdl import *
from modules import jbyte, jenabler, jor


class jregister:
    def __init__(self, bis, ws, we, bos):
        rbus = bus()
        jbyte(bis, ws, rbus)
        jenabler(rbus, we, bos)


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    ws, we, wsr = wire("we"), wire("ws"), wire("wsr")
    jor(ws, wire.RESET, wsr) 
    jregister(bis, wsr, we, bos)

    t = test(bis + [ws, we], bos)
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 0, 0, 0, 0, 0, 0, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0])
