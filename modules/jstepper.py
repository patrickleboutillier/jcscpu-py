from hdl import *
from modules import jmem0, jor, jnot, jand, jbuf


class jstepper:
    def __init__(self, reset, clk, bos):
        wrst, bos6 = wire(), wire()

        # Loop around to wrst
        jbuf(bos6, wrst)

        wnrm1, wnco1, wmsn, wmsnn = wire(), wire(), wire(), wire()
        jnot(wrst, wnrm1)
        jnot(clk, wnco1)
        jor(wrst, wnco1, wmsn)
        # assign #1 wmsn = wrst | wnco1
        jor(wrst, clk, wmsnn)

        # M1
        wn12b, wm112 = wire(), wire()
        jor(wrst, wn12b, bos[0])
        jmem0(reset, wnrm1, wmsn, wm112)

        # M12
        wn12a = wire()
        jnot(wn12a, wn12b)
        jmem0(reset, wm112, wmsnn, wn12a)

        # M2
        wn23b, wm223 = wire(), wire()
        jand(wn12a, wn23b, bos[1])
        jmem0(reset, wn12a, wmsn, wm223)

        # M23
        wn23a = wire()
        jnot(wn23a, wn23b)
        jmem0(reset, wm223, wmsnn, wn23a)

        # M3
        wn34b, wm334 = wire(), wire()
        jand(wn23a, wn34b, bos[2])
        jmem0(reset, wn23a, wmsn, wm334)

        # M34
        wn34a = wire()
        jnot(wn34a, wn34b)
        jmem0(reset, wm334, wmsnn, wn34a)

        # M4
        wn45b, wm445 = wire(), wire()
        jand(wn34a, wn45b, bos[3])
        jmem0(reset, wn34a, wmsn, wm445)

        # M45
        wn45a = wire()
        jnot(wn45a, wn45b)
        jmem0(reset, wm445, wmsnn, wn45a)

        # M5
        wn56b, wm556 = wire(), wire()
        jand(wn45a, wn56b, bos[4])
        jmem0(reset, wn45a, wmsn, wm556)

        # M56
        wn56a = wire()
        jnot(wn56a, wn56b)
        jmem0(reset, wm556, wmsnn, wn56a)

        # M6
        wn67b, wm667 = wire(), wire()
        jand(wn56a, wn67b, bos[5])
        jmem0(reset, wn56a, wmsn, wm667)

        # M67
        jnot(bos6, wn67b)
        jmem0(reset, wm667, wmsnn, bos6)


if __name__ == "__main__":
    clk = wire("clk")
    bos = bus(6, "bos")
    jstepper(wire.RESET, clk, bos)

    t = test([clk], bos)
    t.case([1], [1, 0, 0, 0, 0, 0])
    t.case([1], [1, 0, 0, 0, 0, 0])
    t.case([0], [1, 0, 0, 0, 0, 0])
    t.case([0], [1, 0, 0, 0, 0, 0])
    t.case([1], [0, 1, 0, 0, 0, 0])
    t.case([1], [0, 1, 0, 0, 0, 0])
    t.case([0], [0, 1, 0, 0, 0, 0])
    t.case([0], [0, 1, 0, 0, 0, 0])
    t.case([1], [0, 0, 1, 0, 0, 0])
    t.case([1], [0, 0, 1, 0, 0, 0])
    t.case([0], [0, 0, 1, 0, 0, 0])
    t.case([0], [0, 0, 1, 0, 0, 0])
    t.case([1], [0, 0, 0, 1, 0, 0])
    t.case([1], [0, 0, 0, 1, 0, 0])
    t.case([0], [0, 0, 0, 1, 0, 0])
    t.case([0], [0, 0, 0, 1, 0, 0])
    t.case([1], [0, 0, 0, 0, 1, 0])
    t.case([1], [0, 0, 0, 0, 1, 0])
    t.case([0], [0, 0, 0, 0, 1, 0])
    t.case([0], [0, 0, 0, 0, 1, 0])
    t.case([1], [0, 0, 0, 0, 0, 1])
    t.case([1], [0, 0, 0, 0, 0, 1])
    t.case([0], [0, 0, 0, 0, 0, 1])
    t.case([0], [0, 0, 0, 0, 0, 1]) 
    t.case([1], [1, 0, 0, 0, 0, 0])
    t.case([1], [1, 0, 0, 0, 0, 0])
    t.case([0], [1, 0, 0, 0, 0, 0])
    t.case([0], [1, 0, 0, 0, 0, 0]) 