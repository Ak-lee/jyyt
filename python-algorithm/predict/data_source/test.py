import numpy as np

a = np.asarray([1, 2, 3, 4, 5])
b = np.asarray([[1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5], [1, 2, 3, 4, 5]])
a = a.reshape(-1, 1)
c = a * b
pass
