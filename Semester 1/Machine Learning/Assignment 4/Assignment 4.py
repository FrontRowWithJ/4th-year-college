

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow import keras
from tensorflow.keras import regularizers
from typing import Any
import time


def convolve(array: list[list[int]], kernel: list[list[int]]) -> list[list[int]]:
    """Convolves the k*k kernel to the n*n matrix and returns the result

    Args:
        array (list[list[int]]): n*n integer matrix
        kernel (list[list[int]]): k*k integer matrix

    Returns:
        list[list[int]]: (n - k + 1)*(n - k + 1) output array
    """

    size = len(array) - len(kernel) + 1
    # Initilaise the output matrix
    result = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        for j in range(size):
            tally = 0
            for k in range(len(kernel)):
                for l in range(len(kernel)):
                    tally += kernel[k][l] * array[i + k][j + l]
            result[i][j] = tally
    return result


def getChannels(filename: str) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    """ Takes the filename of an image and returns a 3-tuple containing the RGB values of the image represented as 2D arrays

    Args:
        filename (str): The file name of the image

    Returns:
        tuple[list[list[int]], list[list[int]], list[list[int]]]: tuple[0] = red, tuple[1] = blue and tuple[2] = green
    """
    image = Image.open(filename)
    rgb = np.array(image.convert("RGB"))
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]
    return (r, g, b)


def convolveChannel(kernel: list[list[int]], channel: list[list[int]]) -> None:
    output = convolve(channel, kernel)
    Image.fromarray(np.uint8(output)).show()


def addLayers0(model, num_classes: int, x_train, penalty: float):
    model.add(Conv2D(16, (3, 3), padding='same',
                     input_shape=x_train.shape[1:], activation='relu', ))
    model.add(Conv2D(16, (3, 3), strides=(2, 2),
              padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(Conv2D(32, (3, 3), strides=(2, 2),
              padding='same', activation='relu'))
    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax',
              kernel_regularizer=regularizers.l1(penalty)))


def addLayers1(model, num_classes: int, x_train, penalty: float):
    model.add(Conv2D(16, (3, 3), padding='same',
                     input_shape=x_train.shape[1:], activation='relu'))

    model.add(Conv2D(16, (3, 3), padding='same', activation='relu'))
    model.add(MaxPool2D())
    # add max pool layer

    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))

    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
    model.add(MaxPool2D())
    # add max pool layer

    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax',
              kernel_regularizer=regularizers.l1(penalty)))


def plotModel(history):
    plt.rc("font", size=18)
    plt.rcParams['figure.constrained_layout.use'] = True
    plt.subplot(211)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    plt.axhline(y=0.1, color="r", linestyle="-")

    plt.subplot(212)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'val'], loc='upper left')
    # acc = history.history["accuracy"]
    # val_acc = history.history["val_accuracy"]
    # result = [(a - b) / b for a, b in zip(acc, val_acc)]
    # plt.plot(result)
    # plt.axhline(y=0, color="r", linestyle="-")
    # plt.title("val accuracy and accuracy difference")
    # plt.ylabel("accuracy - val_accuracy")
    # plt.xlabel("epoch")
    # plt.legend(["acc vs val acc"], loc="upper left")
    plt.show()


def genTrainingData(n: int, cifar10Data) -> tuple[Any, Any, Any, Any]:
    num_classes = 10
    (x_train, y_train), (x_test, y_test) = cifar10Data
    x_train = x_train[1:n]
    y_train = y_train[1:n]
    # Scale images to the [0, 1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    return (x_train, x_test, y_train, y_test)


def printStats(model, data: tuple[Any, Any, Any, Any], t: float) -> None:
    x_train, x_test, y_train, y_test = data
    preds = model.predict(x_train)
    y_pred = np.argmax(preds, axis=1)
    y_train1 = np.argmax(y_train, axis=1)
    report_train = classification_report(y_train1, y_pred)
    matrix_train = confusion_matrix(y_train1, y_pred)

    preds = model.predict(x_test)
    y_pred = np.argmax(preds, axis=1)
    y_test1 = np.argmax(y_test, axis=1)
    report_test = classification_report(y_test1, y_pred)
    matrix_test = confusion_matrix(y_test1, y_pred)

    try:
        f = open("output.txt", "a")
        f.write(report_train + "\n")
        f.write(str(matrix_train) + "\n")
        f.write(report_test + "\n")
        f.write(str(matrix_test) + "\n")
        f.write("--- " + str(t) + " seconds ---\n\n")
        print(report_train)
        print(matrix_train)
        print(report_test)
        print(matrix_test)

    finally:
        f.close()


def trainModel(modelName: str, use_saved_model: bool, data: tuple[Any, Any, Any, Any], penalty: float) -> tuple[Any, Any]:
    NUM_CLASSES = 10
    BATCH_SIZE = 128
    EPOCHS = 20

    x_train, _, y_train, _ = data
    if use_saved_model:
        model = keras.models.load_model(modelName)
        history = model.fit(x_train, y_train, batch_size=BATCH_SIZE,
                            epochs=EPOCHS, validation_split=0.1)
        return (history, model)

    model = keras.Sequential()
    addLayers0(model, NUM_CLASSES, x_train, penalty)
    model.compile(loss="categorical_crossentropy",
                  optimizer='adam', metrics=["accuracy"])
    model.summary()
    history = model.fit(x_train, y_train, batch_size=BATCH_SIZE,
                        epochs=EPOCHS, validation_split=0.1)
    return (history, model)


def trainModels(ns: list[int], penalties: list[float], cifar10Data) -> None:
    histories = []
    models = []
    datasets = []
    times = []
    for n, penalty in zip(ns, penalties):
        dataset = genTrainingData(n, cifar10Data)
        datasets.append(dataset)
        modelName = "cifar-" + str(n) + ".model"
        start = time.time()
        history, model = trainModel(modelName, False, dataset, penalty)
        times.append(time.time() - start)
        model.save(modelName)
        histories.append(history)
        models.append(model)

    f = open("output.txt", "w")
    f.write("")
    f.close()
    for model, history, dataset, t in zip(models, histories, datasets, times):
        plotModel(history)
        printStats(model, dataset, t)
        print("--- %s seconds ---" % t)


def maxIndex(l: list):
    return max(range(len(l)), key=l.__getitem__)


def mode(l: list[int]) -> int:
    res = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for n in l:
        res[n] += 1
    return maxIndex(res)


def useBaselineModel(data: tuple[Any, Any, Any, Any]) -> None:
    _, _, y_train, y_test = data
    y_train1 = np.argmax(y_train, axis=1)
    y_test1 = np.argmax(y_test, axis=1)

    train_mode = mode(y_train1)
    test_mode = mode(y_test1)

    baseline_train_preds = np.array([train_mode for _ in y_train1])
    baseline_test_preds = np.array([test_mode for _ in y_test1])

    baseline_class_report_train = classification_report(
        y_train1, baseline_train_preds, zero_division=0)
    baseline_class_report_test = classification_report(
        y_test1, baseline_test_preds, zero_division=0)

    print(baseline_class_report_test)
    print(baseline_class_report_train)


def main() -> None:
    ORIGINAL_PENALTY = 0.0001
    RED, GREEN, BLUE = [0, 1, 2]
    kernel1 = [[-1, -1, -1],
               [-1, 8, -1],
               [-1, -1, -1]]
    kernel2 = [[0, -1, 0],
               [-1, 8, -1],
               [0, -1, 0]]
    
    CIFAR_10_DATA = keras.datasets.cifar10.load_data()
    channels = getChannels("hexagon.png")
    convolveChannel(kernel1, channels[GREEN])
    convolveChannel(kernel2, channels[GREEN])
    
    useBaselineModel(genTrainingData(5000, CIFAR_10_DATA))
    ns = [5000, 10000, 20000, 40000]
    penalties = [0.0001, 0.0001, 0.0001, 0.0001]
    trainModels(ns, penalties, CIFAR_10_DATA)

    penalties = [10, 5, 1, 0, 0.1, 0.001, 0.0001, 0.00001]
    ns = [5000 for _ in penalties]
    trainModels(ns, penalties, CIFAR_10_DATA)
    trainModels([5000], [ORIGINAL_PENALTY], CIFAR_10_DATA)
    
if __name__ == "__main__":
    main()
