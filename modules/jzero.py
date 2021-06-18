from hdl import *
from modules import jorN, jnot


class jzero:
    def __init__(self, bis, wz):
  	    wi = wire()
  	    jorN(bis, wi)
  	    jnot(wi, wz)


if __name__ == "__main__":
    bis = bus(8, "bis")
    wz = wire("wz")
    jzero(bis, wz)

    t = test(bis, [wz])
    t.case([0, 0, 0, 0, 0, 0, 0, 0], [1])
    t.case([0, 0, 0, 0, 0, 0, 1, 0], [0])
