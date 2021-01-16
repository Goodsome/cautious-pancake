import pyautogui

def press(interval, key='z'):
    pyautogui.sleep(interval)
    pyautogui.press(key)



if __name__ == "__main__":
    pyautogui.hotkey('alt', 'tab')
    
    press(2)
    press(1, '`')
    pyautogui.sleep(2)
    pyautogui.click(93, 264)
    intervals = {
        0: 3,
        1: 4.3,
        2: 1.25,
        3: 1.21,
        4: 1.12,
        5: 1.28,
        6: 1.6,
        7: 1.1,
        8: 1.1,
        9: 1.1,
        10: 1.1,
    }
    for k, i in intervals.items():
        press(i)
    press(1.1, key='x')
    inter = [1, 1.4, 1.3, 1.3, 1.1, 0.9, 0.9, 0.9, 1, 1, 1.1, 1.9, 1.1, 1.1]
    for i in inter:
        press(i)
    press(1.1, key='x')
    inter = [1.1, 1.1, 1.1]
    for i in inter:
        press(i)