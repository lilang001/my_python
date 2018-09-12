__author__ = 'Administrator'
from collections import Iterable
from collections import Iterator
# list[]
# tuple()
# dict{}
# set{}
R0 = isinstance([], Iterable)
R1 = isinstance([], Iterator)
print(R1, R0)
