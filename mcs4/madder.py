from hdl import *
from modules import jadd, jxor, jand, jnot


class madder:
    def __init__(self, bas, bbs, ci, ci_0, ci_notci, b_0, b_notb, bcs, co):
        # Calculate the effective ci after the controls signals are applied.
        not_ci_0, a, eci = wire(), wire(), wire()
        jnot(ci_0, not_ci_0)
        jand(not_ci_0, ci, a)
        jxor(a, ci_notci, eci)

        # Calculate the effective bbs after the controls signals are applied.
        ebbs = bus(4)
        not_b_0 = wire()
        jnot(b_0, not_b_0)
        for j in range(4):
            t = wire()
            jand(not_b_0, bbs[j], t)
            jxor(t, b_notb, ebbs[j])

        # Build the adder circuit
        tc = bus(3)
        jadd(bas[3], ebbs[3], eci, bcs[3], tc[0]) 
        for j in range(1, 3):
            jadd(bas[3-j], ebbs[3-j], tc[3-1], bcs[3-j], tc[j])
        jadd(bas[0], ebbs[0], tc[2], bcs[0], co)


if __name__ == "__main__":
    bas, bbs, bcs = bus(4, "bas"), bus(4, "bbs"), bus(4, "bcs")
    ci, ci_0, ci_notci = wire("ci"), wire("ci_0"), wire("ci_notci")
    b_0, b_notb = wire("b_0"), wire("b_notb")
    co = wire("co")
    madder(bas, bbs, ci, ci_0, ci_notci, b_0, b_notb, bcs, co)

    t = test(bas + bbs + [ci, ci_0, ci_notci, b_0, b_notb], bcs + [co])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0] + [0, 0, 0, 0], [0, 0, 0, 0] + [0])
