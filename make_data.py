from matplotlib.pyplot import imshow

from utils import load_and_preprocess_image


import numpy as np
import pyautogui
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import Sequential, layers
from tensorflow.python.keras.backend import backend 
from utils import get_screenshot

AUTOTUNE = tf.data.experimental.AUTOTUNE

def get_images():
    pyautogui.hotkey('alt', 'tab')
    pyautogui.sleep(1)
    for i in range(283, 1638):
        pyautogui.moveTo(i, 500)
        pyautogui.sleep(0.1)
        get_screenshot(f'{i}', 325, 988, 360, 1003)


def get_data(paths):
    images = [tf.expand_dims(load_and_preprocess_image(p), axis=0) for p in paths]
    images = tf.concat(images, axis=0)
    return images


def train_model(data):
    label = tf.range(10)

    model = Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=(64, 64, 3)),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(32, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(64, activation='relu'),
        layers.Dense(10)
    ])
    model.compile(
        optimizer='adam',
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=['accuracy'],
    )

    model.fit(x=data, y=label, epochs=50)
    tf.keras.models.save_model(model, 'model/tmp_model.h5')


def train():
    paths = [f'images/number/{i}.png' for i in range(10)]
    images = get_data(paths)
    train_model(images)

def test():
    paths = [f'images/number/{i}.png' for i in range(10)]
    image = load_and_preprocess_image(path=paths[4])
    model = tf.keras.models.load_model('model/tmp_model.h5')
    probability_model = tf.keras.Sequential([model, tf.keras.layers.Softmax()])
    prob = probability_model.predict(tf.expand_dims(image, axis=0))
    print(np.argmax(prob))
    plt.imshow(image)
    plt.show()


if __name__ == "__main__":
    test()
