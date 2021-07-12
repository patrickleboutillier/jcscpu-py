from hdl import *
from modules import jand, jbuf
from mcs4 import mtri


class menatri:
    def __init__(self, bis, we, bos):
        for j in range(len(bis)):
            mtri(bis[j], we, bos[j])


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    we = wire("we")
    menatri(bis, we, bos)

    t = test(bis + [we], bos)
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])  # Unchanged from previous value
    t.case([1, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])  # Unchanged from previous value
    t.case([1, 0, 0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])  # Unchanged from previous value
    t.case([1, 0, 0, 0, 1, 0, 0, 0, 1], [1, 0, 0, 0, 1, 0, 0, 0])
    t.case([1, 0, 0, 0, 0, 0, 0, 0, 1], [1, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1])  # Unchanged from previous value    