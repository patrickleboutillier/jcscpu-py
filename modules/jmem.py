from hdl import *
from modules import jnand, jor


class jmem:
    def __init__(self, wi, ws, wo):
        wa, wb, wc = wire(), wire(), wire()
        jnand(wi, ws, wa)
        jnand(wa, ws, wb)
        jnand(wa, wc, wo)
        jnand(wo, wb, wc)


if __name__ == "__main__":
    wi, ws, wo, wsr = map(wire, ["wi", "ws", "wo", ""])
    jor(wire.RESET, ws, wsr)
    x = jmem(wi, wsr, wo)

    t = test([wi, ws], [wo])
    # Output is undefined until 's' has been set once! 
    t.case([0, 0], [0])
    t.case([0, 1], [0])
    t.case([1, 1], [1])
    t.case([1, 0], [1])
    t.case([0, 0], [1])
    t.case([0, 1], [0])
    t.case([0, 0], [0])
    t.case([1, 0], [0])

