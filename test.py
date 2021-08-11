import pandas as pd
import numpy as np
import matplotlib as plt
import padasip as pa

hodnoty = open("Bankrot.csv", "r")
data = {
    "data": hodnoty
}
array = np.array(pd.DataFrame(data))
print(array.shape)
A = []
B = []
array = []
for i in range(0, 6819,1):
    array.append(i)

for j in range(0, 6819, 1):
    j_int=(j/6)
    if j_int.is_integer():
        A.insert(0, array[j])
    else:
        B.insert(0, array[j:j+6])
print(A)
print(B)

arrayA = np.asarray(A)
arrayB = np.asarray(B)

BT = arrayB.T
n = (BT.shape)
print(arrayA.shape)
print(BT.shape)


f = pa.filters.FilterNLMS(n[1], mu=0.1, eps=1, w="zeros")
y, e, w = f.run(arrayA, BT)


