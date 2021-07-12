from hdl import *
from modules import jxor, jand, jnot
from mcs4 import mff0


class mcarry:
    def __init__(self, reset, ci, ci_0, ci_notci, s, co):
        # Build the ALU circuit
        not_ci_0, a, i = wire(), wire(), wire()
        jnot(ci_0, not_ci_0)
        jand(not_ci_0, ci, a)
        jxor(a, ci_notci, i)
        mff0(reset, i, s, co)


if __name__ == "__main__":
    ci, ci_0, ci_notci = wire("ci"), wire("ci_0"), wire("ci_notci")
    s, co = wire("s"), wire("co")
    mcarry(wire.RESET, ci, ci_0, ci_notci, s, co)

    t = test([ci, ci_0, ci_notci, s], [co])
    t.case([0, 0, 0, 0], [0])
    t.case([1, 0, 0, 0], [0])
    t.case([1, 0, 0, 1], [0])
    t.case([1, 0, 0, 0], [1])
    t.case([0, 0, 0, 0], [1])
    t.case([0, 0, 0, 1], [1])
    t.case([0, 0, 0, 0], [0])
    t.case([0, 0, 1, 1], [0])
    t.case([0, 0, 1, 0], [1])
    t.case([0, 1, 0, 1], [1])
    t.case([0, 1, 0, 0], [0])
    t.case([0, 1, 1, 1], [0])
    t.case([0, 1, 1, 0], [1])
    t.case([1, 0, 0, 1], [1])
    t.case([1, 0, 0, 0], [1])
    t.case([1, 0, 1, 1], [1])
    t.case([1, 0, 1, 0], [0])
    t.case([1, 1, 0, 1], [0])
    t.case([1, 1, 0, 0], [0])
    t.case([1, 1, 1, 1], [0])
    t.case([1, 1, 1, 0], [1])