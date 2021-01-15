import pyautogui


if __name__ == "__main__":
    for i in range(10):
        print(i)
        pyautogui.sleep(1)

    pyautogui.screenshot('images/tmp.png')