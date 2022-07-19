# Generates a .csv files with all parameters changing.

import numpy as np
import csv
from parameters import main

pars = np.array(main())

m22 = np.geomspace(0.5,1000,25)
k = np.geomspace(0.2,10,25)
mult = []
for i in range(len(m22)):
    for j in range(len(k)):
        mult.append([m22[i],1,1,k[j]])

print("Creating a spreadsheet with %d total runs..."%len(mult))

with open("input_data.csv","w",newline="") as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n",doublequote=False)
    for val in mult:
        value = np.array(val*pars)
        for i in range(value.size):
            value[i] = float("%.5e"%(value[i]))
        writer.writerow(value)
    # writer.writerow(pars * np.array(mult))
