from hdl import *
from modules import jdecoderN, busE, jand
import modules.jregister as jregister

class jRAM:
    def __init__(self, bas, wsa, bis, ws, we, bos):
        busd = bus() ;	
        jregister.jregister(bas, wsa, wire.VCC, busd) 
  
        wxs, wys = bus(16), bus(16) 
        jdecoderN(busd[0:4], wxs)
        jdecoderN(busd[4:8], wys)
  
        bosE = busE(bos, 256)
        for x in range(16):
            for y in range(16):
                wxo, wso, weo = wire(), wire(), wire()
                jand(wxs[x], wys[y], wxo) 
                jand(wxo, ws, wso)
                jand(wxo, we, weo)
                jregister.jregister(bis, wso, weo, bosE.new_bus()) 


if __name__ == "__main__":
    bas, bis, bos = [ bus(8, l) for l in ["bas", "bis", "bos"]]
    wsa, ws, we = [ wire(l) for l in ["wsa", "ws", "we"]]
    jRAM(bas, wsa, bis, ws, we, bos)
    
    t = test(bas + [wsa] + bis + [ws, we], bos)
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 0, 0, 0, 0, 0, 0] + [0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 0, 0, 0, 0, 1, 0] + [1, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [0, 0, 0, 0, 0, 0, 1, 0])
