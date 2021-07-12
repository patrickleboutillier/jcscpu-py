from hdl import *
from modules import jxor, jnot, jbuf, jand, jor
from mcs4 import mff0, mmuxN


# The Stack Pointer. It goes up or down (according to up_down) when s goes from 1 to 0.


class mSP:
    def __init__(self, reset, s, up_down, os):
        nup_down = wire()
        ips, ops = bus(2), bus(2)
        jnot(up_down, nup_down)
        x, nx = wire(), wire()
        jxor(ips[0], ips[1], x)
        jnot(x, nx)
        a1, a2 = wire(), wire()
        jand(nup_down, x, a1)
        jand(up_down, nx, a2)
        jor(a1, a2, ops[0])
        jnot(ips[1], ops[1])

        mff0(reset, ops[0], s, ips[0])
        mff0(reset, ops[1], s, ips[1])

        x, nops0 = wire(), wire()
        jand(s, up_down, x)
        jnot(ops[0], nops0)
        mmuxN([nops0, ops[0]], [x], os[0])
        jbuf(ops[1], os[1])



if __name__ == "__main__":
    s, up_down = wire("s"), wire("up_down")
    os = bus(2, "os")
    mSP(wire.RESET, s, up_down, os)

    t = test([s, up_down], os)
    t.case([0, 0], [0, 1])
    t.case([1, 0], [0, 1])
    t.case([0, 0], [1, 0])
    t.case([0, 0], [1, 0])
    t.case([1, 0], [1, 0])
    t.case([0, 0], [1, 1])
    t.case([0, 0], [1, 1])
    t.case([1, 0], [1, 1])
    t.case([0, 0], [0, 0])

    t.case([0, 0], [0, 0])
    t.case([1, 1], [0, 0])
    t.case([0, 0], [1, 1])

    t.case([0, 0], [1, 1])
    t.case([1, 1], [1, 1])
    t.case([0, 0], [1, 0])

    t.case([0, 0], [1, 0])
    t.case([1, 1], [1, 0])
    t.case([0, 0], [0, 1])

    t.case([0, 0], [0, 1])
    t.case([1, 0], [0, 1])
    t.case([0, 0], [1, 0])
