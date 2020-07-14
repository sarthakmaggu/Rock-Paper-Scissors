# -*- coding: utf-8 -*-
"""train.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14KLVDsbBbSFdR16Vg0-QC7J5ITEkY18T
"""

from google.colab import drive
drive.mount('/content/drive')

data_path = '/content/drive/My Drive/Rock-Paper-Scissors/data'

from keras.models import Sequential,load_model
from keras.layers import Dense,MaxPool2D,Dropout,Flatten,Conv2D,GlobalAveragePooling2D,Activation
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.optimizers import Adam
from keras.applications.densenet import DenseNet121
from keras.preprocessing.image import ImageDataGenerator 
import os
import cv2
import numpy as np
import pandas as pd
from sklearn.utils import shuffle

image = []
labels = []

shape_to_label = {'rock':np.array([1.,0.,0.,0.]),'paper':np.array([0.,1.,0.,0.]),'scissors':np.array([0.,0.,1.,0.]),'ok':np.array([0.,0.,0.,1.])}
arr_to_shape = {np.argmax(shape_to_label[x]):x for x in shape_to_label.keys()}

for dr in os.listdir(data_path):
  if dr not in ["rock", "paper", "scissors"]:
    continue
  label = shape_to_label[dr]
  for image_file in os.listdir(os.path.join(data_path,dr)):
    images = cv2.imread(data_path+ '/'+ dr +'/'+image_file)
    images = cv2.cvtColor(images, cv2.COLOR_BGR2RGB) 
    images = cv2.resize(images,(300,300)) 
    image.append([images,label])

np.random.shuffle(image)

image,label = zip(*image)

image = np.array(image)
label = np.array(label)

print(image.shape)
print(label.shape)

dense = DenseNet121(include_top=False, weights='imagenet', classes=3,input_shape=(300,300,3))
dense.trainable=True

def model(base):
    model = Sequential()
    model.add(base)
    model.add(MaxPool2D())
    model.add(Flatten())
    model.add(Dense(4,activation='softmax'))
    model.compile(optimizer=Adam(),loss='categorical_crossentropy',metrics=['acc'])
    return model

densenet = model(dense)

densenet.summary()

history = densenet.fit(
    x = image,
    y = label,
    batch_size = 16,
    epochs = 30,
    validation_split = 0.1
)

densenet.save("model.h5")