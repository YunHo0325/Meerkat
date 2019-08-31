from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import ImageDataGenerator
from keras.layers import Input, Conv2D, MaxPooling2D
from keras.layers import Dense, Flatten, Dropout
from keras.models import Sequential
from keras.models import load_model

train_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
	 '../../data/train',
        target_size=(256, 256),
        batch_size=3,
        class_mode='binary')

test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        '../../data/test',
        target_size=(256, 256),    
        batch_size=3,
        class_mode='binary')


from tensorflow.python.client import device_lib
print(device_lib.list_local_devices())


import keras.backend.tensorflow_backend as K


with K.tf.device('/gpu:0'):
	model = Sequential()
	model.add(Conv2D(filters=256, kernel_size=(3,3), padding="same", activation="relu", input_shape=(256, 256, 3)))
	model.add(MaxPooling2D((2, 2)))
	model.add(Dropout(0.1))
	model.add(Conv2D(filters=128, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPooling2D((2, 2)))
	model.add(Dropout(0.2))
	model.add(Conv2D(filters=64, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPooling2D((2, 2)))
	model.add(Dropout(0.3))
	model.add(Conv2D(filters=32, kernel_size=(3,3), padding="same", activation="relu"))
	model.add(MaxPooling2D((2, 2)))
	model.add(Dropout(0.4))

	model.add(Flatten())
	model.add(Dense(128, activation="relu"))
	model.add(Dropout(0.1))
	model.add(Dense(128, activation="relu"))
	model.add(Dropout(0.1))
	model.add(Dense(1, activation="sigmoid"))

model.compile(loss='binary_crossentropy', optimizer='Adamax', metrics=['accuracy'])
    
model.fit_generator(
        train_generator,
        steps_per_epoch=10,
        epochs=500
)

import numpy as np

print("-- Evaluate --")
scores = model.evaluate_generator(test_generator, steps=5)
print("%s: %.3f%%" % (model.metrics_names[1], scores[1] * 100))
print("%s: %.3f" % (model.metrics_names[0], scores[0]))

model.save('./model.h5')

