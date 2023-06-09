import numpy as np

from multiprocessing import Array

# Attach to the existing shared memory block

existing_shm = Array('i', [i for i in range(6)])
# Note that a.shape is (6,) and a.dtype is np.int64 in this example

c = np.ndarray(6, dtype=np.int64, buffer=bytes(existing_shm[:]))

print(c)