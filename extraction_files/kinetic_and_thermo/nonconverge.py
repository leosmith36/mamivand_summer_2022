import pandas as pd
import re
import os

# This script conglomerates all of the diverged simulations into their own csv file

def get_fails(iname,output):
    m22r = float(re.sub("_m33_.*","",re.sub("FeCrCo_m22_","",iname)))
    m33r = float(re.sub("_m23_.*","",re.sub("FeCrCo_m22_.*_m33_","",iname)))
    m23r = float(re.sub("_k_.*","",re.sub("FeCrCo_m22_.*_m33_.*_m23_","",iname)))
    kr = float(re.sub(".i","",re.sub("FeCrCo_m22_.*_m33_.*_m23_.*_k_","",iname)))

    m22 = float('%.5e'%m22r)
    m33 = float('%.5e'%m33r)
    m23 = float('%.5e'%m23r)
    k = float('%.5e'%kr)

    df = pd.DataFrame({
        "m22":[m22], "m33":[m33], "m23":[m23], "k":[k], "file":[iname]
    })

    if os.path.exists(os.path.join(output,"diverged_results.csv")):
        df.to_csv(os.path.join(output,"diverged_results.csv"), index = False, mode = 'a', header = False)
    else:
        df.to_csv(os.path.join(output,"diverged_results.csv"), index = False)