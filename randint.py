
import numpy as np
import matplotlib.pyplot as plt
a=['a','b','c','d','e','f']
np.random.seed(42)
selection=[]
for i in range(10000):
    selection.append(a[np.random.randint(len(a))])

plt.hist(selection,6)
plt.show()

for _ in range(10):
    print(np.random.randint(3))
