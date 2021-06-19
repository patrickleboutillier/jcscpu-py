from hdl import *
from modules import jorN, jbuf


class jorE:
    def __init__(self, wo=wire(), max=6):
        self._out = wo
        self._wires = bus(max)
        self._orN = jorN(self._wires, wo)
        self._n = 0
	
    def out(self):
        return self._out

    def add_wire(self, w):
        jbuf(w, self._wires[self._n])
        self._n += 1 

    def assign(self, w):
        self.add_wire(w)


class busE:
    def __init__(self, bos, max=8):
        n = len(bos)
        self._buses = [ bus(n) for _ in range(max) ]
        for j in range(n):
            ore = jorE(bos[j], max)
            for k in range(max):
                ore.add_wire(self._buses[k][j])
        self._n = 0

    def add_bus(self, bis):
        for j in range(len(bis)):
           jbuf(bis[j], self._buses[self._n][j]) 
        self._n += 1 

    def new_bus(self, n=8, label=""):
        b = bus(n, label)
        self.add_bus(b)
        return b 


if __name__ == "__main__":
    wo = wire("wo")
    x = jorE(wo)
    bis = bus(4, "bis")
    x.add_wire(bis[0])
    x.add_wire(bis[1])
    # bis[2] and bis[3] not added to the eor

    t = test(bis, [wo])
    t.case([0, 0, 1, 0], [0])
    t.case([0, 1, 0, 0], [1])
    t.case([1, 0, 0, 0], [1])
    t.case([1, 1, 0, 0], [1])


    bos = bus(4, "bos")
    x = busE(bos)
    bis0 = bus(4, "bis0")
    bis1 = bus(4, "bis1")
    x.add_bus(bis0)
    x.add_bus(bis1)

    t = test(bis0 + bis1, bos)
    t.case([0, 0, 0, 0] + [0, 0, 0, 0], [0, 0, 0, 0])
    t.case([0, 0, 0, 1] + [0, 0, 0, 0], [0, 0, 0, 1])    
    t.case([1, 0, 0, 0] + [0, 0, 0, 1], [1, 0, 0, 1])  