from hdl import *
from modules import jnand, jnot


class jxor:
    def __init__(self, wa, wb, wc):
        wic, wid, wie, wif = wire(), wire(), wire(), wire()
        jnot(wa, wic)
        jnot(wb, wid)
        jnand(wic, wb, wie)
        jnand(wa, wid, wif)
        jnand(wie, wif, wc)


if __name__ == "__main__":
    a, b, c = map(wire, ["a", "b", "c"])
    x = jxor(a, b, c)
    
    t = test([a, b], [c])
    t.case([0, 0], [0])
    t.case([0, 1], [1])
    t.case([1, 0], [1])
    t.case([1, 1], [0])
