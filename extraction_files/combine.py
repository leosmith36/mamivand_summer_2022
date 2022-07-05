import shutil
import os
import pandas as pd
import numpy as np

dirs = os.listdir(os.getcwd())
image_paths = []
csv_paths = []
all_paths = []

if os.path.exists("data"):
    shutil.rmtree("data")

if os.path.exists('full_data'):
    shutil.rmtree("full_data")

csv_dest = os.path.join("data","results")
image_dest = os.path.join("data","spinodal_images","crop_images")
all_dest = "full_data"
os.makedirs(csv_dest)
os.makedirs(image_dest)
os.makedirs(all_dest)

for dir in dirs:
    if os.path.isdir(dir):
        if os.path.exists(os.path.join(dir,"microstructure_data")):
            image_paths.append(os.path.join(dir,"microstructure_data","spinodal_images","crop_images"))
            csv_paths.append(os.path.join(dir,"microstructure_data","results","spinodal_results.csv"))
            all_paths.append(os.path.join(dir,"microstructure_data","images"))

for image_path in image_paths:
    images = os.listdir(image_path)
    for image in images:
        shutil.copy(os.path.join(image_path, image), image_dest)

for all in all_paths:
    images = os.listdir(all)
    for image in images:
        shutil.copy(os.path.join(all, image), all_dest)

df = pd.concat((map(pd.read_csv, csv_paths)), ignore_index = True)
df["m22"] = df["m22"].map(lambda x : float("%.5e"%x))
df["k"] = df["k"].map(lambda x : float("%.5e"%x))
df.to_csv(os.path.join(csv_dest,"spinodal_results.csv"), index = False)


