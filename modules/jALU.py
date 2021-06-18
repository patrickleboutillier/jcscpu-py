from hdl import *
from modules import jenabler, jdecoderN, busE, jorN, jand
import modules.jxorer as jxorer, modules.jorer as jorer, modules.jandder as jandder, modules.jnotter as jnotter
import modules.jzero as jzero, modules.jshiftr as jshiftr, modules.jshiftl as jshiftl, modules.jadder as jadder


class jALU:
    def __init__(self, bas, bbs, wci, bops, bcs, wco, weqo, walo, wz):
        # Build the ALU circuit
        bdec = bus()
        jdecoderN(bops, bdec) 
  
        bcsE = busE(bcs, 7)
        bxor, bor, band, bnot, bshl, bshr, badd = bus(), bus(), bus(), bus(), bus(), bus(), bus()
        jxorer.jxorer(bas, bbs, bxor, weqo, walo) 
        jenabler(bxor, bdec[1], bcsE.new_bus())

        jorer.jorer(bas, bbs, bor)
        jenabler(bor, bdec[2], bcsE.new_bus()) 
  
        jandder.jandder(bas, bbs, band)
        jenabler(band, bdec[3], bcsE.new_bus())
  
        jnotter.jnotter(bas, bnot)
        jenabler(bnot, bdec[4], bcsE.new_bus())
  
        wcotmp = bus(3) 
        jorN(wcotmp, wco)
  
        woshl = wire()
        jshiftl.jshiftl(bas, wci, bshl, woshl) 
        jand(woshl, bdec[5], wcotmp[0])
        jenabler(bshl, bdec[5], bcsE.new_bus())
    
        woshr = wire()
        jshiftr.jshiftr(bas, wci, bshr, woshr)
        jand(woshr, bdec[6], wcotmp[1])
        jenabler(bshr, bdec[6], bcsE.new_bus())
    
        aco = wire()
        jadder.jadder(bas, bbs, wci, badd, aco)
        jand(aco, bdec[7], wcotmp[2])
        jenabler(badd, bdec[7], bcsE.new_bus())
    
        jzero.jzero(bcs, wz)


if __name__ == "__main__":
    bas, bbs, bcs = [ bus(8, l) for l in ["bas", "bbs", "bcs"]]
    bops = bus(3, "bops")
    wci, wco, weqo, walo, wz = wire("wci"), wire("wco"), wire("weqo"), wire("walo"), wire("wz")
    x = jALU(bas, bbs, wci, bops, bcs, wco, weqo, walo, wz)

    t = test(bas + bbs + [wci] + bops, bcs + [wco, weqo, walo, wz])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0] + [0, 1, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0] + [1, 0, 1, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 1, 0], [0, 0, 0, 0, 0, 0, 1, 0] + [0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [0, 1, 1], [1, 1, 1, 1, 1, 1, 1, 0] + [0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 1, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [1, 0, 1], [0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [1, 1, 0], [0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0] + [0] + [1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 1, 1])
    t.case([0, 0, 0, 0, 0, 1, 0, 1] + [0, 0, 0, 0, 1, 0, 0, 1] + [0] + [1, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 1])


