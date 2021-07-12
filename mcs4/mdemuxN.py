from hdl import *
from modules import jandN, jorN, jnot


class mdemuxN:
    # len(bis) must be equal to 2**len(bctrl)
    def __init__(self, i, bctrl, bos):
        n = len(bctrl)
        n2 = len(bos)
        wmap = [[wire(), wire()] for _ in range(n)]
  
        # Create our wire map
        for j in range(n-1, -1, -1):
            jnot(bctrl[j], wmap[j][0])
            wmap[j][1] = bctrl[j] 
    
        for j in range(n2-1, -1, -1):
            wos = bus(n) 
            for k in range(n-1, -1, -1):
                bit = (j >> (n-1-k)) & 1 
                wos[k] = wmap[k][bit] 
            jandN(wos + [i], bos[n2-1-j]) 


if __name__ == "__main__":
    bos2 = bus(2, "bos2")
    bctrl2 = bus(1, "bctrl2")
    i = wire("i")
    mdemuxN(i, bctrl2, bos2)
    t = test([i] + bctrl2, bos2)
    t.case([0] + [0], [0, 0])
    t.case([0] + [1], [0, 0])
    t.case([1] + [0], [0, 1])
    t.case([1] + [1], [1, 0])
