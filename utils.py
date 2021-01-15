from matplotlib.pyplot import axis
import numpy as np
import pyautogui
import tensorflow as tf

from config import config


def type_macro(macro_name):
    pyautogui.press('/')
    pyautogui.sleep(0.2)
    pyautogui.write(macro_name)
    pyautogui.sleep(0.2)
    pyautogui.press('enter')
    pyautogui.sleep(0.2)


def get_screenshot(name, get_pos=False):
    if get_pos:
        input()
        x1, y1 = pyautogui.position()
        input()
        x2, y2 = pyautogui.position()
        im = pyautogui.screenshot(f'images/{name}.png', region=(x1, y1, x2-x1, y2-y1))
    else:
        im = pyautogui.screenshot(f'images/{name}.png')

    return im


def preprocess_image(image):
    # image = tf.image.decode_image(image)
    image = np.array(image)
    image = tf.image.resize(image, [64, 64])
    image /=  255.0

    return tf.expand_dims(image, axis=0)


def load_and_preprocess_image(path):
    image = tf.io.read_file(path)
    return preprocess_image(image)


if __name__ == "__main__":
    name = 'player_coordinate'
    pyautogui.hotkey('alt', 'tab')
    pyautogui.sleep(1)
    type_macro('test')
    pyautogui.sleep(2)

