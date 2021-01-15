from functools import reduce
import tensorflow as tf
from typing import Tuple
import pyautogui
import numpy as np

from utils import *

class Env:
    def __init__(self) -> None:
        self.action_space = {0: 'w', 1: 'a', 2: 's', 3: 'd'}
        self.model = tf.keras.models.load_model('model/tmp_model.h5')

    def reset(self):
        state = np.array(get_screenshot('state'))
        return state

    def step(self, action):
        action = self.action_space[action]
        pyautogui.keyDown(action)
        pyautogui.sleep(0.5)
        pyautogui.keyUp(action)
        state = np.array(get_screenshot('state'))

        distance = self.get_distance()
        reward = -distance
        done = False if distance > 5 else True

        return state, reward, done, None
    
    def get_distance(self):
        type_macro('test')
        n1 = get_screenshot('n1', 26, 1036, 35, 1050)
        n2 = get_screenshot('n2', 35, 1036, 44, 1050)
        n1 = preprocess_image(n1)
        n2 = preprocess_image(n2)
        data = tf.concat([n1, n2], axis=0)
        distance = np.argmax(self.model.predict(data), axis=1)
        distance = reduce(lambda x, y: 10 * x + y, distance)

        return distance


class Target_Env:

    def __init__(self) -> None:
        self.action_space = 2

    def reset(self):
        pyautogui.press('esc')
        state = np.array(get_screenshot('state'))

        return state

    def step(self, action):
        pyautogui.click(action)
        state = np.array(get_screenshot('state'))


if __name__ == "__main__":
    pyautogui.hotkey('alt', 'tab')
    pyautogui.sleep(0.5)
    env = Target_Env()
    env.reset()
    action = [400, 500]
    env.step(action)