from hdl import *
from modules import jxor, jand, jnot, jor, jandN


class jcmp:
    def __init__(self, wa, wb, weqi, wali, wc, weqo, walo):
        w23, w45 = wire(), wire()
        jxor(wa, wb, wc)
        jnot(wc, w23) 
        jand(weqi, w23, weqo)
        jandN([weqi, wa, wc], w45)
        jor(wali, w45, walo) 


if __name__ == "__main__":
    wa, wb, weqi, wali, wc, weqo, walo = map(wire, ["wa", "wb", "weqi", "wali", "wc", "weqo", "walo"])
    jcmp(wa, wb, weqi, wali, wc, weqo, walo)
    
    t = test([wa, wb, weqi, wali], [wc, weqo, walo])
    t.case([0, 0, 0, 0], [0, 0, 0])
    t.case([0, 1, 0, 0], [1, 0, 0])
    t.case([1, 0, 0, 0], [1, 0, 0])
    t.case([1, 1, 0, 0], [0, 0, 0])
    t.case([0, 0, 1, 0], [0, 1, 0])
    t.case([0, 1, 1, 0], [1, 0, 0])
    t.case([1, 0, 1, 0], [1, 0, 1])
    t.case([1, 1, 1, 0], [0, 1, 0])
    t.case([0, 0, 0, 1], [0, 0, 1])
    t.case([0, 1, 0, 1], [1, 0, 1])
    t.case([1, 0, 0, 1], [1, 0, 1])
    t.case([1, 1, 0, 1], [0, 0, 1])
    # impossible... 
    t.case([0, 0, 1, 1], [0, 1, 1])
    t.case([0, 1, 1, 1], [1, 0, 1])
    t.case([1, 0, 1, 1], [1, 0, 1])
    t.case([1, 1, 1, 1], [0, 1, 1])
