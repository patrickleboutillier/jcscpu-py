from hdl import *
from modules import jdecoderN, jorE, jand, jor, jnot, jandN, jorN, jbuf


class jCU:
    def __init__(self, clke, clks, stp_bus, flags_bus, ir_bus, 
        alu_op, alu_ena_ci, flags_s, tmp_s, bus_bit1, acc_s, acc_e, 
        r0_s, r0_e, r1_s, r1_e, r2_s, r2_e, r3_s, r3_e, 
        ram_mar_s, ram_s, ram_e, iar_s, iar_e, ir_s,
        halt, io_s, io_e, io_io, io_da):

        inst_bus = bus(8, "inst_bus")

        # ALL ENABLES
        iar_ena_wor, ram_ena_wor, acc_ena_wor, bus_bit1_wor = jorE(), jorE(), jorE(), jorE(bus_bit1)
        jand(clke, iar_ena_wor.out(), iar_e)
        jand(clke, ram_ena_wor.out(), ram_e)
        jand(clke, acc_ena_wor.out(), acc_e)
   
        # ALL SETS
        ir_set_wor, ram_mar_set_wor, iar_set_wor, acc_set_wor = jorE(), jorE(), jorE(), jorE()
        ram_set_wor, tmp_set_wor, flags_set_wor = jorE(), jorE(), jorE()
        jand(clks, ir_set_wor.out(), ir_s)
        jand(clks, ram_mar_set_wor.out(), ram_mar_s)
        jand(clks, iar_set_wor.out(), iar_s)
        jand(clks, acc_set_wor.out(), acc_s)
        jand(clks, ram_set_wor.out(), ram_s)
        jand(clks, tmp_set_wor.out(), tmp_s)
        jand(clks, flags_set_wor.out(), flags_s)

        # Hook up the circuit used to process the first 3 steps of each cycle (see page 108 in book), i.e
        # - Load IAR to MAR and increment IAR in AC
        # - Load the instruction from RAM into IR
        # - Increment the IAR from ACC
        bus_bit1_wor.assign(stp_bus[0])
        iar_ena_wor.assign(stp_bus[0])
        ram_mar_set_wor.assign(stp_bus[0]) 
        acc_set_wor.assign(stp_bus[0]) 
        ram_ena_wor.assign(stp_bus[1])
        ir_set_wor.assign(stp_bus[1]) 
        acc_ena_wor.assign(stp_bus[2]) 
        iar_set_wor.assign(stp_bus[2]) 

        # Then, we set up the parts that are required to actually implement instructions, i.e.
        # - Connect the decoders for the enable and set operations on R0-R3
        rega_e, regb_e, regb_s = wire(), wire(), wire()
        rega_ena_wor, regb_ena_wor, regb_set_wor = jorE(rega_e), jorE(regb_e), jorE(regb_s)
            
        # s side
        sdeco = bus(4)
        jandN([clks, regb_s, sdeco[3]], r0_s)
        jandN([clks, regb_s, sdeco[2]], r1_s)
        jandN([clks, regb_s, sdeco[1]], r2_s)
        jandN([clks, regb_s, sdeco[0]], r3_s)
        jdecoderN([ir_bus[6], ir_bus[7]], sdeco) 

        # e side
        edecoa, edecob = bus(4), bus(4)
        r0_wora, r0_worb = wire(), wire()
        jor(r0_wora, r0_worb, r0_e) 
        jandN([clke, rega_e, edecoa[3]], r0_wora) 
        jandN([clke, regb_e, edecob[3]], r0_worb) 
        r1_wora, r1_worb  = wire(), wire()
        jor(r1_wora, r1_worb, r1_e) 
        jandN([clke, rega_e, edecoa[2]], r1_wora) 
        jandN([clke, regb_e, edecob[2]], r1_worb) 
        r2_wora, r2_worb  = wire(), wire()
        jor(r2_wora, r2_worb, r2_e) 
        jandN([clke, rega_e, edecoa[1]], r2_wora) 
        jandN([clke, regb_e, edecob[1]], r2_worb) 
        r3_wora, r3_worb  = wire(), wire()
        jor(r3_wora, r3_worb, r3_e) 
        jandN([clke, rega_e, edecoa[0]], r3_wora) 
        jandN([clke, regb_e, edecob[0]], r3_worb) 

        jdecoderN([ir_bus[4], ir_bus[5]], edecoa)
        jdecoderN([ir_bus[6], ir_bus[7]], edecob)
            
        # Finally, install the instruction decoder
        notalu = wire()
        jnot(ir_bus[0], notalu)
        idecbus = bus(8)
        jdecoderN(ir_bus[1:4], idecbus)
        for j in range(8):
            jand(notalu, idecbus[7-j], inst_bus[j])
            
        
        # Now, setting up instruction circuits involves:
        # - Hook up to the proper wire of INST.bus
        # - Wire up the logical circuit and attach it to proper step wires
        # - Use the "elastic" OR gates (xxx.eor) to enable and set

        # ALU INSTRUCTIONS
        aa1 = wire()
        jand(stp_bus[3], ir_bus[0], aa1) 
        regb_ena_wor.assign(aa1)
        tmp_set_wor.assign(aa1)

        aa2 = wire()
        jand(stp_bus[4], ir_bus[0], aa2)
        rega_ena_wor.assign(aa2)
        jbuf(aa2, alu_ena_ci)
        acc_set_wor.assign(aa2)
        flags_set_wor.assign(aa2)

        wnotcmp, aa3 = wire(), wire()
        jandN([stp_bus[5], ir_bus[0], wnotcmp], aa3)
        acc_ena_wor.assign(aa3) 
        regb_set_wor.assign(aa3)

        # Operation selector
        walu = wire()
        jnot(walu, wnotcmp)
        jandN([ir_bus[1], ir_bus[2], ir_bus[3]], walu)
        jandN([stp_bus[4], ir_bus[0], ir_bus[1]], alu_op[0])
        jandN([stp_bus[4], ir_bus[0], ir_bus[2]], alu_op[1])
        jandN([stp_bus[4], ir_bus[0], ir_bus[3]], alu_op[2]) 

        # LOAD AND STORE INSTRUCTIONS
        l1 = wire()
        jand(stp_bus[3], inst_bus[0], l1)
        rega_ena_wor.assign(l1)
        ram_mar_set_wor.assign(l1)

        l2 = wire()
        jand(stp_bus[4], inst_bus[0], l2)
        regb_set_wor.assign(l2)

        s1 = wire()
        jand(stp_bus[3], inst_bus[1], s1)
        rega_ena_wor.assign(s1)
        ram_mar_set_wor.assign(s1)

        s2 = wire()
        jand(stp_bus[4], inst_bus[1], s2)
        regb_ena_wor.assign(s2)
        ram_set_wor.assign(s2)  

        # DATA INSTRUCTIONS
        d1 = wire()
        jand(stp_bus[3], inst_bus[2], d1)
        bus_bit1_wor.assign(d1)
        iar_ena_wor.assign(d1)
        ram_mar_set_wor.assign(d1)
        acc_set_wor.assign(d1)

        d2 = wire()
        jand(stp_bus[4], inst_bus[2], d2)
        ram_ena_wor.assign(d2)
        regb_set_wor.assign(d2)

        d3 = wire()
        jand(stp_bus[5], inst_bus[2], d3)
        acc_ena_wor.assign(d3) 
        iar_set_wor.assign(d3)  

        # CLF INSTRUCTIONS
        clbreg = [ ir_bus[4], ir_bus[5], ir_bus[6], ir_bus[7] ]
        clbinst = bus(16)
        jdecoderN(clbreg, clbinst)

        # CLF, 01100000
        cl1 = wire()
        jandN([inst_bus[6], stp_bus[3], clbinst[15]], cl1)
        bus_bit1_wor.assign(cl1)
        flags_set_wor.assign(cl1)

        # HALT, 01100001
        jandN([inst_bus[6], stp_bus[5], clbinst[14]], halt)
                
        # IO INSTRUCTIONS
        io1 = wire()
        jandN([stp_bus[3], inst_bus[7], ir_bus[4]], io1)
        regb_ena_wor.assign(io1)

        ion4, io2 = wire(), wire()
        jnot(ir_bus[4], ion4)
        jandN([stp_bus[4], inst_bus[7], ion4], io2)
        regb_set_wor.assign(io2)

        jand(clks, io1, io_s)
        jand(clke, io2, io_e)
        jbuf(ir_bus[4], io_io)
        jbuf(ir_bus[5], io_da)

        # JUMP INSTRUCTIONS
        # JUMPR
        jr1 = wire()
        jand(stp_bus[3], inst_bus[3], jr1)
        regb_ena_wor.assign(jr1)
        iar_set_wor.assign(jr1)

        # JUMP
        j1, j2 = wire(), wire()
        jand(stp_bus[3], inst_bus[4], j1)
        iar_ena_wor.assign(j1)
        ram_mar_set_wor.assign(j1)
        jand(stp_bus[4], inst_bus[4], j2)
        ram_ena_wor.assign(j2)
        iar_set_wor.assign(j2)

        # JUMPIF
        ji1 = wire()
        jand(stp_bus[3], inst_bus[5], ji1)
        bus_bit1_wor.assign(ji1)
        iar_ena_wor.assign(ji1)
        ram_mar_set_wor.assign(ji1)
        acc_set_wor.assign(ji1)
        ji2 = wire()
        jand(stp_bus[4], inst_bus[5], ji2)
        acc_ena_wor.assign(ji2) 
        iar_set_wor.assign(ji2)

        ji3, jflago = wire(), wire()
        jandN([stp_bus[5], inst_bus[5], jflago], ji3)
        ram_ena_wor.assign(ji3)
        iar_set_wor.assign(ji3)

        jfbus = bus(4)
        jand(flags_bus[0], ir_bus[4], jfbus[0])
        jand(flags_bus[1], ir_bus[5], jfbus[1])
        jand(flags_bus[2], ir_bus[6], jfbus[2])
        jand(flags_bus[3], ir_bus[7], jfbus[3])
        jorN(jfbus, jflago)       
		

if __name__ == "__main__":
    null = wire("null")
