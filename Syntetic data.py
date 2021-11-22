import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import padasip as pa
import random
import csv

syntdata = []
for i in range(0,196):
    n = random.randint(0,3)
    syntdata.append(n)
np.savetxt("Syntetická data.csv",syntdata,delimiter=",")

SYNTDATA = open("Syntetická data.csv","r")
sdp =(np.genfromtxt(SYNTDATA, delimiter=",", skip_header=0))

SDP1 = np.insert(sdp,[20],[8])
SDP2 = np.insert(SDP1,[60],[8])
SDP3 = np.insert(SDP2,[100],[8])
SDP4 = np.insert(SDP3,[140],[8])
#print(SDP4.shape)
#print(SDP4)
np.savetxt("Syntetická data_C.csv",SDP4,delimiter=",")


