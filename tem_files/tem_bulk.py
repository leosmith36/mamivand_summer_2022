import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from keras import models
import cv2
from sklearn.preprocessing import MinMaxScaler
from keras.applications import imagenet_utils
import re
import copy
from silence_tensorflow import silence_tensorflow
silence_tensorflow()
import tensorflow as tf
import shutil

results = os.listdir()
tem = "tem_stuff2"
image_names = os.listdir(os.path.join(tem,"images"))
image_names.sort(key = lambda x : int(re.sub("\.png", "", x)))

def process_images(path, shape):
    images = []
    names = []
    output = os.path.join(path,"processed_images")

    for image_name in image_names:
        total_path = os.path.join(tem,"images",image_name)

        image = cv2.imread(total_path)
        image = np.array(tf.image.rgb_to_grayscale(image))
        thresh, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        
        image = np.array(image)
        # image = 255 - image
        image = cv2.medianBlur(image, 3)

        # image = np.array(tf.bitwise.invert(image))
        

        imagef = image.flatten()
        total = imagef.shape[0]
        count = np.count_nonzero(imagef)
        frac = 1 - (count / total)
        if frac < 0.5:
            if not os.path.exists(output):
                os.mkdir(output)
            cv2.imwrite(os.path.join(output,image_name), image)
            if shape > 500:
                image = cv2.resize(image, (128,128))
                image = np.expand_dims(image, 0)
                image = imagenet_utils.preprocess_input(image)
                
            else:
                image = cv2.resize(image, (shape,shape))
                image = np.expand_dims(image, 2)
                image = np.array(image,dtype = float) / 255.0
        
            
            images.append(image)
            names.append(image_name)

    images = np.array(images)
    if shape > 500:
        images = np.vstack(images)
    return images,names

def make_predictions(path):
    preds_df = pd.DataFrame()
    if os.path.isdir(path) and path != tem:
        output = os.path.join(path,"predictions.csv")
       
        model = models.load_model(os.path.join(path,"saved_model"))
        images,names = process_images(path, model.input_shape[1])

        # data = pd.DataFrame({"min" : [0.11], "max" : [0.57]})
        # mms = MinMaxScaler()
        train = pd.read_csv(os.path.join(path,"trainX.csv"))
        # cols = ["min","max"]
        # trainX = np.array(mms.fit_transform(train[cols]))
        # scaled = np.array(mms.transform(data[cols]))

        # scaled2 = np.repeat(scaled, images.shape[0], axis = 0)
        preds = model.predict(images)

        maxY = train[["m22", "k"]].max()
        preds2 = np.transpose(preds)
        m22 = maxY["m22"] * preds2[0]
        k = maxY["k"] * preds2[1]

        m22_mean = m22.mean()
        k_mean = k.mean()

        m22_stdev = m22.std(dtype = np.float64)
        k_stdev = k.std()

        m22_list = np.append(m22, m22_mean)
        k_list = np.append(k, k_mean)

        m22_list = np.append(m22_list, m22_stdev)
        k_list = np.append(k_list, k_stdev)

        img_list = names.copy()
        img_list.append("average")
        img_list.append("st_dev")

        preds_df = pd.DataFrame({"image": img_list, "m22" : m22_list, "k" : k_list})
        preds_df.to_csv(output, index = False)
    return preds_df

        # cols = {}
        # cols["names"] = []
        # for name in names:
        #     cols[name] = []
        # cols["average"] = []
        # cols["st_dev"] = []

        # predictions_m22 = copy.deepcopy(cols)
        # predictions_k = copy.deepcopy(cols)

        # for i in range(len(names) + 3):
        #     if i == 0:
        #         predictions_m22["names"].append(path)
        #     elif i < (len(names) + 1):
        #         predictions_m22[names[i - 1]].append(m22_list[i - 1])
        #     elif i == (len(names) + 1):
        #         predictions_m22["average"].append(m22_list[-2])
        #     else:
        #         predictions_m22["st_dev"].append(m22_list[-1])
        
        # for i in range(len(names) + 3):
        #     if i == 0:
        #         predictions_k["names"].append(path)
        #     elif i < (len(names) + 1):
        #         predictions_k[names[i - 1]].append(k_list[i - 1])
        #     elif i == (len(names) + 1):
        #         predictions_k["average"].append(k_list[-2])
        #     else:
        #         predictions_k["st_dev"].append(k_list[-1])
    


def main():
    m22_preds = pd.DataFrame()
    k_preds = pd.DataFrame()
    for result in results:
        
        preds = make_predictions(result)
        if preds.empty:
            continue
        m22_preds["image"] = preds["image"]
        k_preds["image"] = preds["image"]

        m22_preds[result] = preds["m22"]
        k_preds[result] = preds["k"]
    m22_preds.to_csv("m22_predictions.csv", index = False)
    k_preds.to_csv("k_predictions.csv", index = False)


if __name__ == "__main__":
    main()


