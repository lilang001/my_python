__author__ = 'Administrator'
class Dict(dict):

    def __init__(self, **kw):
        return 100

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value
