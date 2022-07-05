import os
import numpy as np
import pandas as pd
import re

# This file takes the results from each individual run's csv and conglomerates them into a new csv called "converged_results.csv"

def get_df(file,dir,output,img):

    df = pd.DataFrame(columns=("m22","m33","m23","k","min","max","file"))

    with open(dir,"r") as f:
        all = f.readlines()
        last = all[-1]
        last = last.replace("\n","")
        vals = np.array(last.split(",")[1:]).astype(float)
        max = round(vals[0],5)
        min = round(vals[1],5)
        m22r = float(re.sub("_m33_.*","",re.sub("FeCrCo_m22_","",file)))
        m33r = float(re.sub("_m23_.*","",re.sub("FeCrCo_m22_.*_m33_","",file)))
        m23r = float(re.sub("_k_.*","",re.sub("FeCrCo_m22_.*_m33_.*_m23_","",file)))
        kr = float(re.sub("_c.*","",re.sub("FeCrCo_m22_.*_m33_.*_m23_.*_k_","",file)))

        m22 = float('%.5e'%m22r)
        m33 = float('%.5e'%m33r)
        m23 = float('%.5e'%m23r)
        k = float('%.5e'%kr)

        df = pd.DataFrame({"m22":[m22], "m33":[m33], "m23":[m23], "k":[k], "min":[min], "max":[max], "file":[img]})
        if os.path.exists(os.path.join(output,"converged_results.csv")):
            df.to_csv(os.path.join(output,"converged_results.csv"), index = False, mode = 'a', header = False)
        else:
            df.to_csv(os.path.join(output,"converged_results.csv"), index = False)

