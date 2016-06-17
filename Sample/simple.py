class P(object):    # <- super works only with new-class style
    def __init__(self, argp):
        self.pstr=argp

class C(P):
    def __init__(self, argp, argc):
        super(C, self).__init__(argp)
        self.cstr=argp