from hdl import *
from modules import jandN, jnot


class jdecoderN:
    # len(bos) must be equal to 2**len(bis)
    def __init__(self, bis, bos):
        n = len(bis)
        n2 = len(bos)
        wmap = [[wire(), wire()] for _ in range(n)]
  
        # Create our wire map
        for j in range(n-1, -1, -1):
            jnot(bis[j], wmap[j][0])
            wmap[j][1] = bis[j] 
    
        for j in range(n2-1, -1, -1):
            wos = bus(n) 
            for k in range(n-1, -1, -1):
                bit = (j >> (n-1-k)) & 1 
                wos[k] = wmap[k][bit] 
            jandN(wos, bos[n2-1-j]) 


if __name__ == "__main__":
    bis2 = bus(2, "bis2")
    bos2 = bus(4, "bos2")
    jdecoderN(bis2, bos2)
    t = test(bis2, bos2)
    t.case([0, 0], [0, 0, 0, 1])
    t.case([0, 1], [0, 0, 1, 0])
    t.case([1, 0], [0, 1, 0, 0])
    t.case([1, 1], [1, 0, 0, 0])    

    bis3 = bus(3, "bis3")
    bos3 = bus(8, "bos3")
    jdecoderN(bis3, bos3)
    t = test(bis3, bos3)
    t.case([0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0])   
    t.case([1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0])
    t.case([1, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0])
    t.case([1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0])  

    bis4 = bus(4, "bis4")
    bos4 = bus(16, "bos4")
    jdecoderN(bis4, bos4)
    t = test(bis4, bos4)
    t.case([0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0])   
    t.case([0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0])
    t.case([0, 1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0])
    t.case([0, 1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0])
    t.case([0, 1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])  
    t.case([1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 1, 0], [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 1, 1], [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])   
    t.case([1, 1, 0, 0], [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 0, 1], [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 1, 0], [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 1, 1], [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])  