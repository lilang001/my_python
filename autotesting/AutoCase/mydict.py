__author__ = 'Administrator'
# _*_ #coding:utf-8 _*_
class Dict(dict):
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


if __name__ == "__main__":
    s = Dict(k=1, a=3, s=4)
    print s
