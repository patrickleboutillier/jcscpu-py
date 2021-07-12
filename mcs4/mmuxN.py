from hdl import *
from modules import jandN, jorN, jnot


class mmuxN:
    # len(bis) must be equal to 2**len(bctrl)
    def __init__(self, bis, bctrl, o):
        n = len(bctrl)
        n2 = len(bis)
        wmap = [[wire(), wire()] for _ in range(n)]
  
        # Create our wire map
        for j in range(n-1, -1, -1):
            jnot(bctrl[j], wmap[j][0])
            wmap[j][1] = bctrl[j] 
    
        bos = bus(n2)
        for j in range(n2-1, -1, -1):
            wos = bus(n) 
            for k in range(n-1, -1, -1):
                bit = (j >> (n-1-k)) & 1 
                wos[k] = wmap[k][bit] 
            jandN(wos + [bis[n2-1-j]], bos[n2-1-j]) 
        
        jorN(bos, o)


if __name__ == "__main__":
    bis2 = bus(2, "bis2")
    bctrl2 = bus(1, "bctrl2")
    o = wire("o")
    mmuxN(bis2, bctrl2, o)
    t = test(bis2 + bctrl2, [o])
    t.case([0, 0] + [0], [0])
    t.case([0, 0] + [1], [0])
    t.case([0, 1] + [0], [1])
    t.case([0, 1] + [1], [0])
    t.case([1, 0] + [0], [0])
    t.case([1, 0] + [1], [1])
    t.case([1, 1] + [0], [1])
    t.case([1, 1] + [1], [1])