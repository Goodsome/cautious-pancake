from sys import path
import pyautogui

def alt_tab():
    pyautogui.hotkey('alt', 'tab')
    pyautogui.sleep(1)

def test_1():
    alt_tab()
    for i in range(10000):
        pyautogui.keyDown('d')
        # pyautogui.sleep(0.1)
        pyautogui.keyUp('d')
        pyautogui.keyDown('a')
        # pyautogui.sleep(0.1)
        pyautogui.keyUp('a')
        pyautogui.rightClick()

def test_2():
    alt_tab()
    for i in range(10):
        pyautogui.press(['a', 'd'])
        # pyautogui.rightClick()

if __name__ == "__main__":
    test_1()

