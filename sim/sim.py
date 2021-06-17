import sys

WIRES = {}
LABELS = {}
NANDS = {}
TESTS = {}


class sim:
    def __init__(self):
        for line in sys.stdin:
            args = line.rstrip().split()
            verb = args.pop(0)
            id = int(args.pop(0))

            if verb == 'WIRE':
                WIRES[id] = int(args[0])
                if len(args) > 1:
                    LABELS[args[1]] = id
            elif verb == 'NAND':
                [a, b, c] = args
                NANDS[id] = { 'a': int(a), 'b': int(b), 'c': int(c) } 
            elif verb == 'TEST':
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


    def settle(self):
        change = True
        iter = 0
        while change:
            iter =+ 1
            change = False
            for id in sorted(NANDS):
                n = NANDS[id]
                prev = WIRES[n['c']] 
                cur = int(not (WIRES[n['a']] & WIRES[n['b']]))
                if cur != prev:
                    WIRES[n['c']] = cur 
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



#sub setbusval {
#	my $label = shift ;
#	my $val = shift ;
#	my $len = shift || 8 ;

#    my @vals = split('', sprintf("%0${len}b", $val)) ;
#    map { setval("${label}[$_]", $vals[$_]) } (0 .. ($len-1)) ;
#}


#sub getbusval {
#	my $label = shift ;
#	my $len = shift || 8 ;
#
#	my @bus = map { getval("${label}[$_]") } (0 .. ($len-1)) ;
#	return oct("0b" . join('', @bus)) ;	
#}

from pprint import pprint
if __name__ == "__main__":
    SIM = sim()
    unittest.main()