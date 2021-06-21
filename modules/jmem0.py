from hdl import *
from modules import jmem, jor, jnot, jand


class jmem0:
    def __init__(self, reset, wi, ws, wo):
        wsr, wnr, wir = wire(), wire(), wire()
        jor(reset, ws, wsr)
        jnot(reset, wnr)
        jand(wnr, wi, wir)
        jmem(wir, wsr, wo)


if __name__ == "__main__":
    wi, ws, wo = map(wire, ["wi", "ws", "wo"])
    x = jmem0(wire.RESET, wi, ws, wo)

    t = test([wi, ws], [wo])
    t.case([0, 0], [0])
    t.case([0, 1], [0])
    t.case([1, 1], [1])
    t.case([1, 0], [1])
    t.case([0, 0], [1])
    t.case([0, 1], [0])
    t.case([0, 0], [0])
    t.case([1, 0], [0])

