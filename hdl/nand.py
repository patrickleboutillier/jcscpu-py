

NANDS = {}


class nand:
    _cnt = 0

    def __init__(self, a, b, c):
        self._a = a
        self._b = b
        self._c = c
        self._id = nand._cnt
        nand._cnt += 1
        NANDS[self._id] = self


def dump_nands():
    for i in sorted(NANDS):
        n = NANDS[i]
        print('NAND {} {} {} {}'.format(n._id, n._a._id, n._b._id, n._c._id))
