import json
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow.keras as keras

"""
Module that sets up neural network settings and processes dataset
This is based on video series: https://www.youtube.com/watch?v=CA0PQS1Rj_4&list=PL-wATfeyAMNpCRQkKgtOZU_ykXc63oyzp
by Valerio Velardo
"""

DATA_PATH = "data.json"
SAVED_MODEL_PATH = "model.h5"  # keras format
LEARNING_RATE = 0.0001  # adam optimizer
EPOCHS = 40
BATCH_SIZE = 32  # Samples for network backpropagation at a time
NUMBERS_KEYWORDS = 6


def load_dataset(data_path):
    with open(data_path, "r") as fp:
        data = json.load(fp)
    # inputs
    x = np.array(data["MFCCs"])
    # output
    y = np.array(data["labels"])
    return x, y


def get_data_splits(data_path, test_size=0.1, test_validation=0.1):
    # 10% of dataset used for testing
    # 9% of dataset used for validating
    # load dataset
    x, y = load_dataset(data_path)

    # create train/test splits
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)
    # create train/validation
    x_train, x_validation, y_train, y_validation = train_test_split(x_train, y_train,
                                                                    test_size=test_validation)
    # x_train, x_validation, y_train, y_validation - 2D arrays
    #  (#segments, #MFCC) ->
    # convert input from 2D to 3D arrays
    x_train = x_train[..., np.newaxis]
    x_validation = x_validation[..., np.newaxis]
    x_test = x_test[..., np.newaxis]

    return x_train, x_validation, x_test, y_train, y_validation, y_test


def build_model(input_shape, learning_rate, error="sparse_categorical_crossentropy"):
    # build network
    model = keras.Sequential()
    # conv layer 1
    model.add(keras.layers.Conv2D(64, (3, 3), activation="relu",
                                  input_shape=input_shape,
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    # prepare mean output and deviation
    model.add(keras.layers.BatchNormalization())
    # downsample output from layer
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    # conv layer 2
    model.add(keras.layers.Conv2D(32, (3, 3), activation="relu",
                                  input_shape=input_shape,
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((3, 3), strides=(2, 2), padding="same"))

    # conv layer 3
    model.add(keras.layers.Conv2D(32, (2, 2), activation="relu",
                                  input_shape=input_shape,
                                  kernel_regularizer=keras.regularizers.l2(0.001)))
    model.add(keras.layers.BatchNormalization())
    model.add(keras.layers.MaxPool2D((2, 2), strides=(2, 2), padding="same"))

    # flatten output and feed it into a dense layer
    model.add(keras.layers.Flatten())
    model.add(keras.layers.Dense(64, activation="relu"))
    # overfitting
    model.add(keras.layers.Dropout(0.3))
    # softmax classifier
    # outputs array of numbers of predicitions, sum equals to 1
    model.add(keras.layers.Dense(NUMBERS_KEYWORDS, activation="softmax"))
    # compile model
    optimiser = keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimiser, loss=error, metrics=["accuracy"])

    # print model overview
    model.summary()
    return model


def main():
    # load/validate/test model

    x_train, x_validation, x_test, y_train, y_validation, y_test = get_data_splits(DATA_PATH)

    # build CNN model that takes 3D input; segments/coefficient/1
    # 3D array; (#segments, #MFCC, depth of greyscale image=1)
    input_shape = (x_train.shape[1], x_train.shape[2], x_train.shape[3])
    model = build_model(input_shape, LEARNING_RATE)
    # train
    # x - input, y - output, #epochs - how many times CNN views dataset
    model.fit(x_train, y_train, epochs=EPOCHS, validation_data=(x_validation, y_validation))

    # evaluate
    test_error, test_accuracy = model.evaluate(x_test, y_test)
    print(f"Test error: {test_error}, test accuracy: {test_accuracy}")

    # save
    model.save(SAVED_MODEL_PATH)


if __name__ == "__main__":
    main()
