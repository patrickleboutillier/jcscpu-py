

NANDS = []


class nand:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        NANDS.append(self)


def dump_nands():
    print("""

struct nand {
\tunsigned int a, b, c ;    
}

    """)
    print("PROGMEM const word NANDS[] = {")
    cnt = 0
    for n in NANDS:
        # print('NAND {} {} {}'.format(n._a._id, n._b._id, n._c._id))
        print('\t{}, {}, {},'.format(n._a._id, n._b._id, n._c._id))
        cnt += 3
    print("}} ;\n\n\n#define NANDS_SIZE\t{}".format(cnt))
