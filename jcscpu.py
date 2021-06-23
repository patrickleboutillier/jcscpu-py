from sim.sim import *


MAR = 0 
RAM = [ 0 for _ in range(256) ]
RAM[0] = 0b00100000
RAM[1] = 0b00010100
RAM[2] = 0b00100001
RAM[3] = 0b00010110
RAM[4] = 0b10000001
RAM[5] = 0b01100001

SIM = sim()

tick = -1

def advance_clk():
    global tick
    tick += 1 
    if tick == 4:
        tick = 0
        print("")

    clk, clkd, clke, clks = 0, 0, 0, 0
    if tick == 0:
        clk = 1 ; clkd = 0 ; clke = 1 ; clks = 0
    elif tick == 1:
        clk = 1 ; clkd = 1 ; clke = 1 ; clks = 1
    elif tick == 2:
        clk = 0 ; clkd = 1 ; clke = 1 ; clks = 0
    else:
        clk = 0 ; clkd = 0 ; clke = 0 ; clks = 0

    SIM.setval("clk", clk)       
    SIM.setval("clkd", clkd)
    #SIM.setval("clke", clke)       
    #SIM.setval("clks", clks)


step = 0 
def advance_step():
    global step 
    if tick == 0:
        step += 1
        if step == 7:
            step = 1 
        steps = [0, 0, 0, 0, 0, 0, 0]
        steps[step-1] = 1 
        for i in range(6):
            SIM.setval("stp_bus[" + str(i) + "]", steps[i])


def handle_RAM():
    global MAR, RAM
    if SIM.getval("ram_mar_s"):
        MAR = SIM.getbusval("bus")
    if SIM.getval("ram_s"):
        RAM[MAR] = SIM.getbusval("bus")        
    if SIM.getval("ram_e"):
        SIM.setbusval("ram_bus", RAM[MAR])
    else:
        SIM.setbusval("ram_bus", 0)



while True:
    advance_clk()
    # advance_step()

    SIM.settle() 
    handle_RAM()
    SIM.settle() 

    if SIM.getval("halt"):
        exit(0) 
    
    print("clk:{}, clkd:{}, clke:{}, clks:{}, ir_s:{}, rst_ir_s:{}".format(SIM.getval("clk"), SIM.getval("clkd"), 
        SIM.getval("clke"), SIM.getval("clks"), SIM.getval("ir_s"), SIM.getval("rst_ir_s")), end='')
    print(", step:{0:06b}".format(SIM.getbusval("stp_bus", 6)), end='')
    print(", bus:{0:08b}, ir_bus:{1:08b}".format(SIM.getbusval("bus"), SIM.getbusval("ir_bus")))


  #print("  ram_mar_s:")
  #print(getval(WIRE_ram_mar_s))
  #print(", ram_s:")
  #print(getval(WIRE_ram_s))
  #print(", ram_e:")
  #println(getval(WIRE_ram_e))
