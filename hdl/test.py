

TESTS = {}


class test:
    _cnt = 0

    def __init__(self, ils, ols, label=""):
        self._ils = ils
        self._ols = ols


    def case(self, ivs, ovs, label=""):
        TESTS[test._cnt] = {'id': test._cnt, 'ins': dict(zip(self._ils, ivs)), 'outs': dict(zip(self._ols, ovs)), 'label': label}
        test._cnt += 1

def dump_tests():
    for i in sorted(TESTS):
        t = TESTS[i]
        ins = ",".join([str(w._label) + ":" + str(v) for w, v in t['ins'].items()])
        outs = ",".join([str(w._label) + ":" + str(v) for w, v in t['outs'].items()])
        print('TEST {} {} {} {}'.format(t['id'], ins, outs, t['label']))

