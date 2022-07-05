# Generates a .csv files with all parameters changing.

import numpy as np
import csv
from parameters import main

# Set this to 3 or 4 (since runs^4 is the total number of runs)
runs = 7

pars = np.array(main())

m22 = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100,200,300,400,500,600,700,800,900,1000])
k =np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3,4,5,6,7,8,9,10])

mult = []
for i in range(m22.size):
    for j in range(k.size):
        mult.append([m22[i],1,1,k[j]])

print("Creating a spreadsheet with %d total runs..."%len(mult))

with open("input_data.csv","w",newline="") as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n",doublequote=False)
    for val in mult:
        value = np.array(val*pars)
        for i in range(value.size):
            value[i] = float("%.5e"%(value[i]))
        writer.writerow(value)

