from hdl import *
from modules import jand, jor


class jclock:
    def __init__(self, wclk, wclkd, wclke, wclks):
        jor(wclk, wclkd, wclke)
        jand(wclk, wclkd, wclks) 



if __name__ == "__main__":
    wclk, wclkd, wclke, wclks = map(wire, ["wclk", "wclkd", "wclke", "wclks"])
    jclock(wclk, wclkd, wclke, wclks)

    t = test([wclk, wclkd], [wclke, wclks])
    t.case([1, 0], [1, 0])
    t.case([1, 1], [1, 1])
    t.case([0, 1], [1, 0])
    t.case([0, 0], [0, 0])
 

