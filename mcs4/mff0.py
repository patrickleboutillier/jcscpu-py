from hdl import *
from modules import jnot, jmem0


# A D-style flip-flop. Value changes when "s" goes from 1 to 0.


class mff0:
    def __init__(self, reset, i, s, o):
        ns, q = wire(), wire()
        jnot(s, ns)
        jmem0(reset, i, s, q)
        jmem0(reset, q, ns, o)


if __name__ == "__main__":
    i, s, o = map(wire, ["i", "s", "o"])
    x = mff0(wire.RESET, i, s, o)

    t = test([i, s], [o])
    t.case([0, 0], [0])
    t.case([0, 1], [0])
    t.case([1, 1], [0])
    t.case([1, 0], [1])
    t.case([0, 0], [1])
    t.case([0, 1], [1])
    t.case([0, 0], [0])
    t.case([1, 0], [0])