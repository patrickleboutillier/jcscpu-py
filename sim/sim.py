import sys

WIRES = {}
LABELS = {}
GATES = []
TESTS = {}


class sim:
    def __init__(self):
        for line in sys.stdin:
            args = line.rstrip().split()
            verb = args.pop(0)

            if verb == 'WIRE':
                id = int(args.pop(0))
                WIRES[id] = int(args[0])
                if len(args) > 1:
                    LABELS[args[1]] = id
            elif verb == 'NAND':
                [a, b, c] = args
                GATES.append({ 'k': 'NAND', 'a': int(a), 'b': int(b), 'c': int(c) })
            elif verb == 'TRI':
                [i, e, o] = args
                GATES.append({ 'k': 'TRI', 'i': int(i), 'e': int(e), 'o': int(o) })
            elif verb == 'TEST':
                id = int(args.pop(0))
                ins = {}
                outs = {}
                for i in args[0].rstrip().split(','):
                    [k, v] = i.split(':')
                    ins[k] = int(v)
                for o in args[1].rstrip().split(','):
                    [k, v] = o.split(':')
                    outs[k] = int(v)
                TESTS[id] = { 'ins': ins, 'outs': outs, 'label': ""}
                if len(args) > 2:
                    TESTS[id]['label'] = args[2]
        
        self.setval("GND", 0)
        self.setval("VCC", 1)
        self.setval("RESET", 1)     
        self.settle()
        self.setval("RESET", 0)       


    def setval(self, label, v):
        if label in LABELS:
            WIRES[LABELS[label]] = v
        else:
            sys.exit("No wire named '{}' was found!".format(label))


    def getval(self, label):
        if label in LABELS:
            return WIRES[LABELS[label]]
        else:
            sys.exit("No wire named '{}' was found!".format(label))


    def getbusval(self, label, len=8):
        bs = [ str(self.getval(label + "[" + str(i) + "]")) for i in range(len) ]
        return int("".join(bs), 2)


    def setbusval(self, label, v, len=8):
        f = "{0:0" + str(len) + "b}"
        vals = f.format(v)
        for i in range(len):
            self.setval(label + "[" + str(i) + "]", int(vals[i]))


    def settle(self):
        change = True
        iter = 0
        while change:
            iter =+ 1
            change = False
            for g in GATES:
                if g['k'] == 'NAND':
                    prev = WIRES[g['c']] 
                    cur = int(not (WIRES[g['a']] & WIRES[g['b']]))
                    if cur != prev:
                        WIRES[g['c']] = cur 
                        change = True         
                        # print("wire {}: {} -> {}".format(n['c'], prev, cur))
                elif g['k'] == 'TRI':
                    if WIRES[g['e']]:
                        prev = WIRES[g['o']] 
                        cur = WIRES[g['i']]
                        if cur != prev:
                            WIRES[g['o']] = cur 
                            change = True         

        return iter



import unittest

SIM = None


class test_sim(unittest.TestCase):

    def test_run_tests(self):
        for id in sorted(TESTS):
            t = TESTS[id]
            for wl in TESTS[id]['ins']:
                SIM.setval(wl, TESTS[id]['ins'][wl])
            SIM.settle()
            for wl in TESTS[id]['outs']:
                v = SIM.getval(wl)
                self.assertEqual(v, TESTS[id]['outs'][wl], "(" + wl + ") " + str(t))



from pprint import pprint
if __name__ == "__main__":
    SIM = sim()
    unittest.main()