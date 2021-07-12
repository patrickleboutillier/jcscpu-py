from hdl import *
from modules import jbyte, jenabler
from mcs4 import mff0, mmuxN, mdemuxN, menatri


# The Address Buffer. The address buffer is 12 bits wide. 
# Each nibble can be set individually (using s_ph, s_pm and s_pl): 
# - From the data bus (if data_addr == 0) or 
# - From the address bus (if data_addr == 1)
# Each nibble can be enabled individually (using e_ph, e_pm and e_pl):
# - To the data bus (if data_addr == 0) or 
# - From the address bus ((if data_addr == 1))
#
# Note: Only one of s_ph, s_pm and s_pl should be set when data_addr == 0.


class mADDR_BUF:
    def __init__(self, data_in, addr_in, s_ph, s_pm, s_pl, data_addr, e_ph, e_pm, e_pl, data_out, addr_out):
        nibs_in, nibs_out = bus(12), bus(12)
        jbyte(nibs_in[0:4], s_ph, nibs_out[0:4])
        jbyte(nibs_in[4:8], s_pm, nibs_out[4:8])
        jbyte(nibs_in[8:12], s_pl, nibs_out[8:12])
        # Input
        for j in range(12):
            mmuxN([addr_in[j], data_in[j % 4]], [data_addr], nibs_in[j])
        # Output
        ena_out = bus(12)
        for j in range(12):
            mdemuxN(nibs_out[j], [data_addr], [addr_out[j], ena_out[j]])
        # Only one e_ signal should be used at a time since they all output to the same bus!
        menatri(ena_out[0:4], e_ph, data_out[0:4])
        menatri(ena_out[4:8], e_pm, data_out[0:4])
        menatri(ena_out[8:12], e_pl, data_out[0:4])


if __name__ == "__main__":
    data_in, data_out = bus(4, "data_in"), bus(4, "data_out")
    addr_in, addr_out = bus(12, "addr_in"), bus(12, "addr_out")
    s_ph, s_pm, s_pl, data_addr, e_ph, e_pm, e_pl = map(wire, ["s_ph", "s_pm", "s_pl", "data_addr", "e_ph", "e_pm", "e_pl"])

    mADDR_BUF(data_in, addr_in, s_ph, s_pm, s_pl, data_addr, e_ph, e_pm, e_pl, data_out, addr_out)

    t = test(data_in + addr_in + [s_ph, s_pm, s_pl, data_addr, e_ph, e_pm, e_pl], data_out, addr_out)
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [1, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 
    t.case([0, 1, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 1, 0, 0, 0, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 
    t.case([1, 1, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 1, 0, 0, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 1, 0, 0], [1, 0, 1, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 1, 0], [0, 1, 0, 1] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) 
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 1], [1, 1, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    # Clear data out
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [1, 0, 0, 0, 1, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])     
    t.case([0, 0, 0, 0] + [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1] + [1, 1, 1, 1, 0, 0, 0], [0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] + [0, 0, 0, 1, 1, 1, 1], [0, 0, 0, 0] + [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]) 