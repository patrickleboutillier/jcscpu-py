

NANDS = []


class nand:
    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        NANDS.append(self)


def dump_nands():
    for n in NANDS:
        print('NAND {} {} {}'.format(n._a._id, n._b._id, n._c._id))
