from hdl import *
from modules import jxor, jand, jor


class jadd:
    def __init__(self, wa, wb, wci, wc, wco):
        wi, wcoa, wcob = wire(), wire(), wire()
        jxor(wa, wb, wi)
        jxor(wi, wci, wc)
        jand(wci, wi, wcoa)
        jand(wa, wb, wcob)
        jor(wcoa, wcob, wco)


if __name__ == "__main__":
    wa, wb, wci, wc, wco = map(wire, ["wa", "wb", "wci", "wc", "wco"])
    jadd(wa, wb, wci, wc, wco)
    
    t = test([wa, wb, wci], [wc, wco])
    t.case([0, 0, 0], [0, 0])
    t.case([0, 1, 0], [1, 0])
    t.case([1, 0, 0], [1, 0])
    t.case([1, 1, 0], [0, 1])
    t.case([0, 0, 1], [1, 0])
    t.case([0, 1, 1], [0, 1])
    t.case([1, 0, 1], [0, 1])
    t.case([1, 1, 1], [1, 1])