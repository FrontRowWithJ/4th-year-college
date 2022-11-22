
import matplotlib.pyplot as plt
import numpy as np
from keras.layers import Conv2D, Dense, Dropout, Flatten
from sklearn.metrics import classification_report, confusion_matrix
from tensorflow import keras
from tensorflow.keras import regularizers

plt.rc('font', size=18)
plt.rcParams['figure.constrained_layout.use'] = True

# Model / data parameters
num_classes = 10
input_shape = (32, 32, 3)

# the data, split between train and test sets
(x_train, y_train), (x_test, y_test) = keras.datasets.cifar10.load_data()

n = 5000
x_train = x_train[1:n]
y_train = y_train[1:n]


#x_test=x_test[1:500]; y_test=y_test[1:500]

# Scale images to the [0, 1] range
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

print("orig x_train shape:", x_train.shape)

# convert class vectors to binary class matrices
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

use_saved_model = False
if use_saved_model:
    model = keras.models.load_model("cifar.model")
else:
    model = keras.Sequential()
    model.add(Conv2D(16, (3, 3), padding='same',
              input_shape=x_train.shape[1:], activation='relu'))

    model.add(Conv2D(16, (3, 3), strides=(2, 2),
              padding='same', activation='relu'))

    model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))

    model.add(Conv2D(32, (3, 3), strides=(2, 2),
              padding='same', activation='relu'))

    model.add(Dropout(0.5))
    model.add(Flatten())
    model.add(Dense(num_classes, activation='softmax',
              kernel_regularizer=regularizers.l1(0.0001)))
    model.compile(loss="categorical_crossentropy",
                  optimizer='adam', metrics=["accuracy"])
    model.summary()

    batch_size = 128
    epochs = 20
    history = model.fit(x_train, y_train, batch_size=batch_size,
                        epochs=epochs, validation_split=0.1)
    model.save("cifar.model")
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

preds = model.predict(x_train)
y_pred = np.argmax(preds, axis=1)
y_train1 = np.argmax(y_train, axis=1)
print(classification_report(y_train1, y_pred))
print(confusion_matrix(y_train1, y_pred))


preds = model.predict(x_test)
y_pred = np.argmax(preds, axis=1)
y_test1 = np.argmax(y_test, axis=1)
print(classification_report(y_test1, y_pred))
print(confusion_matrix(y_test1, y_pred))

