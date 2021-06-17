from hdl import *
from modules import jor, jbuf


class jorN:
    def __init__(self, bis, wo):
        n = len(bis)
        os = [wire()]
	
        jor(bis[0], bis[1], os[0])
        for j in range(n-2):
            os.append(wire())
            jor(os[j], bis[j+2], os[j+1])
        jbuf(os[n-2], wo)


if __name__ == "__main__":
    bis2 = bus(2, "bis2")
    c2 = wire("c2")
    jorN(bis2, c2)
    t = test(bis2, [c2])
    t.case([0, 0], [0])
    t.case([0, 1], [1])
    t.case([1, 0], [1])
    t.case([1, 1], [1])    

    bis3 = bus(3, "bis3")
    c3 = wire("c3")
    jorN(bis3, c3)
    t = test(bis3, [c3])
    t.case([0, 0, 0], [0])
    t.case([0, 0, 1], [1])
    t.case([0, 1, 0], [1])
    t.case([0, 1, 1], [1])    
    t.case([1, 0, 0], [1])
    t.case([1, 0, 1], [1])
    t.case([1, 1, 0], [1])
    t.case([1, 1, 1], [1])    

    bis4 = bus(4, "bis4")
    c4 = wire("c4")
    jorN(bis4, c4)
    t = test(bis4, [c4])
    t.case([0, 0, 0, 0], [0])
    t.case([0, 0, 0, 1], [1])
    t.case([0, 0, 1, 0], [1])
    t.case([0, 0, 1, 1], [1])    
    t.case([0, 1, 0, 0], [1])
    t.case([0, 1, 0, 1], [1])
    t.case([0, 1, 1, 0], [1])
    t.case([0, 1, 1, 1], [1])
    t.case([1, 0, 0, 0], [1])
    t.case([1, 0, 0, 1], [1])
    t.case([1, 0, 1, 0], [1])
    t.case([1, 0, 1, 1], [1])    
    t.case([1, 1, 0, 0], [1])
    t.case([1, 1, 0, 1], [1])
    t.case([1, 1, 1, 0], [1])
    t.case([1, 1, 1, 1], [1])         