import pandas as pd
import os
import numpy as np
import shutil
from PIL import Image
import pathlib

# Finds all of the runs that produced spinodal decomposition, and creates a new csv file and image folder for these runs
# Also crops the images

def filter_images(wd):
    df = pd.read_csv(os.path.join(wd,"results","converged_results.csv"))

    df["difference"] = df["max"] - df["min"]
    df["label"] = np.where(df["difference"] <= 0.05, 0, 1)

    spinodal = (df.loc[(df["label"] == 1)]).reset_index(drop = True)

    spinodal['m22'] = spinodal['m22'].map(lambda x : "%.5e" %x)
    spinodal['m33'] = spinodal['m33'].map(lambda x : "%.5e" %x)
    spinodal['m23'] = spinodal['m23'].map(lambda x : "%.5e" %x)
    spinodal['k'] = spinodal['k'].map(lambda x : "%.5e" %x)
    spinodal['difference'] = spinodal['difference'].map(lambda x : "%.5f" %x)

    m22 = spinodal["m22"]
    m33 = spinodal["m33"]
    m23 = spinodal["m23"]
    k = spinodal["k"]
    file = spinodal["file"]
    
    spinodal.to_csv(os.path.join(wd,"results","spinodal_results.csv"), index = False)

    images = os.path.join(wd,"images")
    image_names = spinodal["file"]

    output = os.path.join(wd,"spinodal_images")
    if not os.path.exists(output):
        os.mkdir(output)

    for f in os.listdir(images):
        for i in range(len(image_names)):

            if f == image_names[i]:
                source = os.path.join(images,f)
                dest = os.path.join(output,f)
                shutil.copyfile(source,dest)
            
    new_width = 380
    new_height = 380
    new_images = os.listdir(output)
    for image in new_images:
        if not os.path.isfile(os.path.join(output,image)):
            new_images.remove(image)
    crop_images = os.path.join(output,"crop_images")
    if not os.path.exists(crop_images):
        os.mkdir(crop_images)
    else:
        shutil.rmtree(crop_images)
        os.mkdir(crop_images)

    for i in new_images:
        filepath = os.path.join(output,i)
        cd = os.getcwd()

        tmp = shutil.copy(filepath,cd)
        
        img = Image.open(tmp)

        width, height = img.size

        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        img = img.crop((left,top,right,bottom))

        img.save(tmp)
        shutil.move(tmp,crop_images)


if __name__=="__main__":
    filter()