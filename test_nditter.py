
import numpy as np
lis=[1,2]
a=np.array(lis)  #np.ndarray(list) 라고 하지 말자
print(a)

a=np.array([[1,2,3],[4,5,6]])

print(a)
for x in np.nditer(a):
    print(x)


