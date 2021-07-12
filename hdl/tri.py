

TRIS = []


class tri:
    def __init__(self, i, e, o):
        self._i = i
        self._e = e
        self._o = o
        TRIS.append(self)


def dump_tris():
    for n in TRIS:
        print('TRI {} {} {}'.format(n._i._id, n._e._id, n._o._id))
