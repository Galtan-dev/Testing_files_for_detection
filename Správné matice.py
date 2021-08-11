import pandas as pd
import numpy as np
import matplotlib as plt
import padasip as pa

hodnoty = open("Bankrot.csv", "r")
data = {
    "data": hodnoty
}
array = np.array(pd.DataFrame(data))

d = []
x = []

for idx, sample in enumerate(array[6:20]):
    d.append(sample)
    x.append(array[idx - 6:idx - 1])
print(np.asarray(d).shape)
print(np.asarray(x).shape)
print(x)