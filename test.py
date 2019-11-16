import itertools

ar = [i for i in range(1000)]
all = itertools.permutations(ar,2)

import sys

print(sys.getsizeof(all))
print(sys.getsizeof(list(all)))
