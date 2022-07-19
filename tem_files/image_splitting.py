import numpy as np
from PIL import Image
import os
import shutil

# This file automatically crops the TEM image across the given x and y ranges

if os.path.exists("cropped_images"):
    shutil.rmtree("cropped_images")
os.mkdir("cropped_images")

image = Image.open("tem_original.png")

step = 20

x_range = list(np.arange(5, 465, step))
y_range = list(np.arange(745, 1345, step))

for y in y_range:
    for x in x_range:
        if x > 395 and y > 1295:
            continue    
        else:
            box = (x, y, x + 105, y + 105)
            crop = image.crop(box)
            crop.save(os.path.join("cropped_images",f"cropped_image_{x}_{y}.png"))