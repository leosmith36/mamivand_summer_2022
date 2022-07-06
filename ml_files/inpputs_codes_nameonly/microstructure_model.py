# %% [markdown]
# # Machine Learning Model for M22 and Kappa

# %% [markdown]
# ### Import necessary packages

# %%
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
import os
import cv2
import shutil
import matplotlib.pyplot as plt
import tensorflow as tf
import re
print(tf.config.list_physical_devices('GPU'))

# %% [markdown]
# ### Keras packages

# %%
from keras.models import Model
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import BatchNormalization
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Activation
from keras.layers import Dropout
from keras.layers import Input
from keras.layers import concatenate
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.utils import get_custom_objects
from keras.backend import sigmoid

# %% [markdown]
# ### Set file paths for input and output data

# %%
# Where the images and data come from
input = os.path.join("..","..","data")
# input = os.path.join('data')
# input = "C:\\Users\\leomo\\Documents\\Boise\\mamivand\\data"
image_dir = os.path.join(input, "spinodal_images", "crop_images")
# Where output csv files will go
output = "results"

# Remove the output if it is already there
if os.path.exists(output):
    shutil.rmtree(output)
os.mkdir(output)

# %% [markdown]
# ### Read the csv with numerical results

# %%
print("Reading data...")
# data = pd.read_csv(os.path.join(input,"results","spinodal_results.csv"))
data = pd.DataFrame()

# %% [markdown]
# ### Get the images, and resize and rescale them

# %%
print("Reading images...")
# size_ = 64
image_paths = os.listdir(image_dir)
images = []
m22_list = []
k_list = []
for image_path in image_paths:
    total_path = os.path.join(input, "spinodal_images", "crop_images", image_path)
    # image = cv2.imread(total_path, cv2.IMREAD_GRAYSCALE)
    image = cv2.imread(total_path)
    
    image = np.array(tf.image.rgb_to_grayscale(image))
    thresh, imageb = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    image = cv2.resize(image, (size_,size_))
    image = np.array(image, dtype = float)
    image = np.expand_dims(image, 2)
    image = image / 255.0
    images.append(image)
    

    image_vert = np.array(tf.image.flip_up_down(image))
    images.append(image_vert)

    image_hor = np.array(tf.image.flip_left_right(image))
    images.append(image_hor)

    image_inv = np.array(tf.image.flip_left_right(image_vert))
    images.append(image_inv)

    imageb = cv2.resize(imageb, (size_,size_))
    imageb = np.array(imageb, dtype = float)
    imageb = np.expand_dims(imageb, 2)
    imageb = imageb / 255.0
    images.append(imageb)

    imageb_vert = np.array(tf.image.flip_up_down(imageb))
    images.append(imageb_vert)

    imageb_hor = np.array(tf.image.flip_left_right(imageb))
    images.append(imageb_hor)

    imageb_inv = np.array(tf.image.flip_left_right(imageb_vert))
    images.append(imageb_inv)

    m22r = float(re.sub("_m33_.*","",re.sub("FeCrCo_m22_","",image_path[:-4])))
    m33r = float(re.sub("_m23_.*","",re.sub("FeCrCo_m22_.*_m33_","",image_path[:-4])))
    m23r = float(re.sub("_k_.*","",re.sub("FeCrCo_m22_.*_m33_.*_m23_","",image_path[:-4])))
    kr = float(re.sub("_c.*","",re.sub("FeCrCo_m22_.*_m33_.*_m23_.*_k_","",image_path[:-4])))

    m22 = float('%.5e'%m22r)
    m33 = float('%.5e'%m33r)
    m23 = float('%.5e'%m23r)
    k = float('%.5e'%kr)

    m22_list.append(m22)
    k_list.append(k)

data["m22"] = np.array(m22_list, dtype = float)
data["k"] = np.array(k_list, dtype = float)
    
images = np.array(images)


# %% [markdown]
# ### Split the data into 0.7/0.3 training/test

# %%
print("Splitting data...")
data2 = pd.DataFrame(np.repeat(data.values, 8, axis = 0))
data2.columns = data.columns
trainX, testX, trainX_images, testX_images = train_test_split(data2, images, test_size = 0.3, random_state = 10)

# %% [markdown]
# ### Saves unprocessed training and test data to CSV files

# %%
trainX.to_csv(os.path.join(output,"trainX.csv"), index = False)
testX.to_csv(os.path.join(output,"testX.csv"), index = False)

# %% [markdown]
# ### Rescale the training and test M22 and Kappa values to be between 0 and 1

# %%
maxY = trainX[["m22", "k"]].max()
trainY = np.array(trainX[["m22", "k"]] / maxY, dtype = float)
testY = np.array(testX[["m22", "k"]] / maxY, dtype = float)

# %% [markdown]
# ### Rescale the Fe min and max data to be between 0 and 1

# %%
# vars = ["min", "max"]
# mms = MinMaxScaler()

# trainX = np.array(mms.fit_transform(trainX[vars]), dtype = float)
# testX = np.array(mms.transform(testX[vars]), dtype = float)

# %% [markdown]
# ### Creates the multi-layered perceptron which accepts Fe min/max data

# %%
# mlp = Sequential([
#     Dense(8, input_dim = trainX.shape[1], activation = "relu"),
#     Dense(4, activation = "relu")
# ])

# %%
def swish(x, beta = 1):
    return (x * sigmoid(beta * x))
get_custom_objects().update({'swish': Activation(swish)})

# %% [markdown]
# ### Creates the CNN which accepts the images

# %%
filters = (f1_, f2_, f3_)

input_shape = (size_,size_,1)
input = Input(shape = input_shape)

for i, size in enumerate(filters):
    if i == 0:
            x = input

    x = Conv2D(size, (3,3), padding = "same", activation = "relu")(x)
    x = BatchNormalization(axis = -1)(x)
    x = MaxPooling2D(pool_size = (2,2))(x)

x = Flatten()(x)
x = Dense(256, activation = "relu")(x)
x = BatchNormalization()(x)
x = Dropout(0.5)(x)
x = Dense(64, activation = "relu")(x)

cnn = Model(input, x)

# %% [markdown]
# ### Hyperparameters

# %%
learning_rate = lr_
epochs = ep_
batch_size = bs_
decay = lr_ / dc_

# %% [markdown]
# ### Combines the MLP and CNN into one network and compiles the model

# %%
# combined_input = concatenate([mlp.output, cnn.output])
x = Dense(16, activation = "relu")(cnn.output)
x = Dense(8, activation = "relu")(x)
x = Dense(2, activation = "linear")(x)
model = Model(inputs = cnn.input, outputs = x)
opt = Adam(learning_rate = learning_rate, decay = decay)
model.compile(loss = "mean_absolute_percentage_error", optimizer = opt)


# %% [markdown]
# ### Trains the model on the input data

# %%
print("Training model...")
# es = EarlyStopping(monitor = "val_loss", min_delta = 1, patience = 50, verbose = 1, mode = "min")
result = model.fit(
    x = trainX_images,
    y = trainY,
    validation_data = (testX_images, testY),
    epochs = epochs,
    batch_size = batch_size,
    verbose = 2
    # callbacks = [es]
)

# %% [markdown]
# ### Makes predictions based on the test data

# %%
print("Making predictions...")
predictions = model.predict(testX_images, verbose = 2)

# %% [markdown]
# ### Saves the predictions for later analysis

# %%
m22_pred = predictions.transpose()[0]
k_pred = predictions.transpose()[1]
m22_act = np.array(testY).transpose()[0]
k_act = np.array(testY).transpose()[1]

compare_m22 = {
    "Actual" : m22_act,
    "Predicted" : m22_pred
}

compare_k = {
    "Actual" : k_act,
    "Predicted" : k_pred
}

data_m22 = pd.DataFrame(compare_m22)
data_k = pd.DataFrame(compare_k)

data_m22.to_csv(os.path.join(output,"results_m22.csv"), index = False)
data_k.to_csv(os.path.join(output,"results_k.csv"), index = False)


# %% [markdown]
# ### Compiles statistics into a CSV file

# %%
m22_perc_diff = (np.abs(m22_act - m22_pred)/m22_act)*100.0
k_perc_diff = (np.abs(k_act - k_pred)/k_act)*100.0

m22_mean = np.mean(m22_perc_diff)
k_mean = np.mean(k_perc_diff)
m22_stdev = np.std(m22_perc_diff)
k_stdev = np.std(k_perc_diff)
m22_r2 = r2_score(m22_act,m22_pred)
k_r2 = r2_score(k_act,k_pred)
m22_mse = mean_squared_error(m22_act,m22_pred)
k_mse = mean_squared_error(k_act,k_pred)

stats_dict = {
    "Parameter":["m22","k"],
    "Mean Percent Difference":[m22_mean,k_mean],
    "Standard Deviation of Percent Difference":[m22_stdev,k_stdev],
    "R-Squared":[m22_r2,k_r2],
    "Mean Squared Error":[m22_mse,k_mse]
}

stats = pd.DataFrame(stats_dict)
stats.to_csv(os.path.join(output,"statistics.csv"), index = False)

# %% [markdown]
# ### Saves the model and its data for later analysis

# %%
model.save(os.path.join(output,"saved_model"))

history = pd.DataFrame(result.history)
history.to_csv(os.path.join(output,"history.csv"), index = False)


