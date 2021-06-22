from hdl import *
from modules import jand, jor, busE, jmem
import modules.jclock as jclock, modules.jstepper as jstepper, modules.jregister as jregister, modules.jbus1 as jbus1
import modules.jALU as jALU, modules.jCU as jCU, modules.jRAM as jRAM


class jCORE:
    def __init__(self, reset, clk, clkd, clke, clks, stp_bus,
        busi, buso, ram_mar_s, ram_s, ram_e,
        io_s, io_e, io_io, io_da, halt):
    
        core_busE = busE(buso) 
  
        r0_s, r0_e, r1_s, r1_e, r2_s, r2_e, r3_s, r3_e = map(wire, 
            ["r0_s", "r0_e", "r1_s", "r1_e", "r2_s", "r2_e", "r3_s", "r3_e"])
        rst_r0_s, rst_r1_s, rst_r2_s, rst_r3_s = wire(), wire(), wire(), wire()
        jor(reset, r0_s, rst_r0_s)
        jregister.jregister(busi, rst_r0_s, r0_e, core_busE.new_bus())
        jor(reset, r1_s, rst_r1_s)
        jregister.jregister(busi, rst_r1_s, r1_e, core_busE.new_bus())
        jor(reset, r2_s, rst_r2_s)
        jregister.jregister(busi, rst_r2_s, r2_e, core_busE.new_bus())
        jor(reset, r3_s, rst_r3_s)
        jregister.jregister(busi, rst_r3_s, r3_e, core_busE.new_bus())

        tmp_s, bus1, rst_tmp_s = wire(), wire(), wire()
        tmp_bus, bus1_bus = bus(), bus()
        jor(reset, tmp_s, rst_tmp_s)
        jregister.jregister(busi, rst_tmp_s, wire.VCC, tmp_bus)
        jbus1.jbus1(tmp_bus, bus1, bus1_bus)

        alu_op, alu_bus = bus(3), bus()
        alu_ci, alu_co, alu_eqo, alu_alo, alu_z = wire(), wire(), wire(), wire(), wire()
        jALU.jALU(busi, bus1_bus, alu_ci, alu_op, alu_bus, alu_co, alu_eqo, alu_alo, alu_z)

        flags_s, rst_flags_s = wire(), wire()
        flags_in = [alu_co, alu_alo, alu_eqo, alu_z, wire.GND, wire.GND, wire.GND, wire.GND]
        flags_bus = bus()
        jor(reset, flags_s, rst_flags_s)
        jregister.jregister(flags_in, rst_flags_s, wire.VCC, flags_bus)
        
        acc_s, acc_e, rst_acc_s = wire(), wire(), wire()
        jor(reset, acc_s, rst_acc_s)
        jregister.jregister(alu_bus, rst_acc_s, acc_e, core_busE.new_bus())

        alu_ena_ci, wco = wire(), wire()
        jmem(flags_bus[0], rst_tmp_s, wco)
        jand(wco, alu_ena_ci, alu_ci)

        iar_s, iar_e, ir_s, rst_iar_s, rst_ir_s = wire(), wire(), wire(), wire(), wire()
        ir_bus = bus(8)
        jor(reset, iar_s, rst_iar_s)
        jregister.jregister(busi, rst_iar_s, iar_e, core_busE.new_bus())
        jor(reset, ir_s, rst_ir_s)
        jregister.jregister(busi, rst_ir_s, wire.VCC, ir_bus)


        jCU.jCU(
            clke, clks, stp_bus,
            flags_bus[0:4],
            ir_bus,
            alu_op,
            alu_ena_ci, flags_s, tmp_s,
            bus1, acc_s, acc_e,
            r0_s, r0_e, r1_s, r1_e, r2_s, r2_e, r3_s, r3_e,
            ram_mar_s, ram_s, ram_e,
            iar_s, iar_e, ir_s, halt,
            io_s, io_e, io_da, io_io	
            )    
		

if __name__ == "__main__":
    BUS = busE(bus(8, "bus"))

    clk, clkd, clke, clks = map(wire, ["clk", "clkd", "clke", "clks"])
    #jclock.jclock(clk, clkd, clke, clks)
    stp_bus = bus(6, "stp_bus")
    #jstepper.jstepper(wire.RESET, clk, stp_bus)

    ram_mar_s, ram_s, ram_e = map(wire, ["ram_mar_s", "ram_s", "ram_e"]) 
    halt, io_s, io_e, io_da, io_io = map(wire, ["halt", "io_s", "io_e", "io_da", "io_io"])

    ram_mar_s_out, ram_s_out, ram_e_out = wire(), wire(), wire()
    ram_mar_s_t, ram_s_t, ram_e_t = map(wire, ["ram_mar_s_t", "ram_s_t", "ram_e_t"]) 
    jor(ram_mar_s, ram_mar_s_t, ram_mar_s_out)
    jor(ram_s, ram_s_t, ram_s_out)
    jor(ram_e, ram_e_t, ram_e_out)
    jRAM.jRAM(BUS.out(), ram_mar_s_out, BUS.out(), ram_s_out, ram_e_out, BUS.new_bus())

    jCORE(
        wire.RESET,
        clk, clkd, clke, clks, stp_bus,
        BUS.out(), BUS.new_bus(),
        ram_mar_s, ram_s, ram_e,
        io_s, io_e, io_da, io_io,
        halt
        )

    # We must place our program in RAM
    rbus = BUS.new_bus(8, "rbus")
    t = test(rbus + [ram_mar_s_t, ram_s_t], [wire.GND])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [1, 0], [0])
    t.case([0, 0, 1, 0, 0, 0, 0, 0] + [0, 1], [0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [1, 0], [0])
    t.case([0, 0, 0, 1, 0, 1, 0, 0] + [0, 1], [0])
    t.case([0, 0, 0, 0, 0, 0, 1, 0] + [1, 0], [0])
    t.case([0, 0, 1, 0, 0, 0, 0, 1] + [0, 1], [0])
    t.case([0, 0, 0, 0, 0, 0, 1, 1] + [1, 0], [0])
    t.case([0, 0, 0, 1, 0, 1, 1, 0] + [0, 1], [0])
    t.case([0, 0, 0, 0, 0, 1, 0, 0] + [1, 0], [0])
    t.case([1, 0, 0, 0, 0, 0, 0, 1] + [0, 1], [0])
    # Clear bus...
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0], [0])

    # Check that stuff is well written in RAM
    t = test(rbus + [ram_mar_s_t, ram_e_t], BUS.out())
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [1, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [0, 0, 1, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 1] + [1, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 1, 0] + [1, 0], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [0, 0, 1, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0, 0, 0, 1, 1] + [1, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([0, 0, 0, 0, 0, 1, 0, 0] + [1, 0], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 1], [1, 0, 0, 0, 0, 0, 0, 1])
    # Clear bus...
    t.case([0, 0, 0, 0, 0, 0, 0, 0] + [0, 0], [0, 0, 0, 0, 0, 0, 0, 0])


    t = test([clk, clkd, clke, clks] + stp_bus, BUS.out())
    # INST 0 
    ### STEP 1 
    t.case([1, 0, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([1, 1, 1, 1] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 1, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 2 
    t.case([1, 0, 1, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0])
    t.case([1, 1, 1, 1] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0])
    t.case([0, 1, 1, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 0])
    t.case([0, 0, 0, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 3 
    t.case([1, 0, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 1] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 1, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 4 
    t.case([1, 0, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 1] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 1, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 5 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 6 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    # INST 1 
    ### STEP 1 
    t.case([1, 0, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([1, 1, 1, 1] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 1, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 0])
    t.case([0, 0, 0, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 2 
    t.case([1, 0, 1, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 1] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1])
    t.case([0, 1, 1, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 3 
    t.case([1, 0, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([1, 1, 1, 1] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([0, 1, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([0, 0, 0, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 4 
    t.case([1, 0, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([1, 1, 1, 1] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([0, 1, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 1, 1])
    t.case([0, 0, 0, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 5 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 6 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])
    # INST 2 
    ### STEP 1 
    t.case([1, 0, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([1, 1, 1, 1] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 1, 1, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 0])
    t.case([0, 0, 0, 0] + [1, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 2 
    t.case([1, 0, 1, 0] + [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1])
    t.case([1, 1, 1, 1] + [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 1, 1, 0] + [0, 1, 0, 0, 0, 0], [1, 0, 0, 0, 0, 0, 0, 1])
    t.case([0, 0, 0, 0] + [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 3 
    t.case([1, 0, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1])
    t.case([1, 1, 1, 1] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1])
    t.case([0, 1, 1, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 1, 0, 1])
    t.case([0, 0, 0, 0] + [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 4 
    t.case([1, 0, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 1, 0, 1, 1, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 5 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 1, 0, 1, 0, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0, 0])
    ### STEP 6 
    t.case([1, 0, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0])
    t.case([1, 1, 1, 1] + [0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0])
    t.case([0, 1, 1, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 1, 0, 1, 0, 1, 0])
    t.case([0, 0, 0, 0] + [0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0])