import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import padasip as pa

hodnoty = []
for i in range(0,500,1):
    hodnoty.append(i)
np.savetxt("hodnoty.csv", hodnoty, delimiter=",")

hodnoty = open("hodnoty.csv", "r")
data = {
    "data": hodnoty
}
array = np.genfromtxt("hodnoty.csv", delimiter = ",")

s = array
t = []
j = []
k = []

for i in range(1,500,1):
    k = np.append(k,s[i])
for i in range(0,499,1):
    j = np.append(j,1)
for i in range(0,499,1):
    t =np.append(t,s[i])
l = np.asarray([t,j])
f = np.asarray([k])
x = l.T
d = f.T
d[250] = d[250] * 1.5
print(x)
print(d)

f = pa.filters.FilterGNGD(n=2, mu=0.7, w="zeros")
y, e, w = f.run(d, x)
plt.plot(e)
print(w[:])
plt.figure(5)
plt.plot(w)
plt.show()

