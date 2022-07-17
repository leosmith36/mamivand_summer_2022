# Generates a .csv files with all parameters changing.

import numpy as np
import csv
from parameters import main

pars = np.array(main())

mult = [[1,1,1,1],[10,1,1,1],[100,1,1,1],[1,1,1,0.2],[1,1,1,0.4]]

print("Creating a spreadsheet with %d total runs..."%len(mult))

with open("input_data.csv","w",newline="") as f:
    writer = csv.writer(f,delimiter=",",lineterminator="\n",doublequote=False)
    for val in mult:
        value = np.array(val*pars)
        for i in range(value.size):
            value[i] = float("%.5e"%(value[i]))
        writer.writerow(value)
    # writer.writerow(pars * np.array(mult))
