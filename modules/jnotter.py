from hdl import *
from modules import jnot


class jnotter:
    def __init__(self, bis, bos):
        for j in range(8):
            jnot(bis[j], bos[j])


if __name__ == "__main__":
    bis = bus(8, "bis")
    bos = bus(8, "bos")
    x = jnotter(bis, bos)

    t = test(bis, bos)
    t.case([0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1])
    t.case([1, 1, 1, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1])