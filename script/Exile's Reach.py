import sys

import pyautogui
sys.path.append('..')

from utils import run, run_macro
from macro import *


def start():
    run([960, 900])
    run(['shift', 'p'])
    run([277, 722])
    run([90, 250])
    run([490, 250])
    run([90, 320])
    run([90, 390])
    run([290, 390])
    run([90, 460])
    run([490, 570])
    run([415, 653])
    run([290, 250])
    run([490, 390])
    run('esc')


def skip():
    run('esc')

class Quest:
    def __init__(self, npc, target=None) -> None:
        self.npc = npc
        self.target = target
    
    def interactive(self, target):
        run_macro(f'/tar {target}')
        run('`')
    
    def exec(self):
        run_macro(f'/tar {self.target}')
        run('`')
    
    def battle(self):
        for i in range(2):
            run('z', interval=1.5)

    def turn_arount(self, interval=1):
        pyautogui.keyDown('right')
        pyautogui.sleep(interval)
        pyautogui.keyUp('right')
    
    def run(self):
        # self.interactive(self.npc)
        # pyautogui.sleep(10)
        self.interactive(self.target)
        self.battle()
        run(['shift', 'tab'])
        run('`')
        # pyautogui.sleep(5)
        # self.interactive(self.npc)


if __name__ == "__main__":
    run(['alt', 'tab'], interval=0)
    # start()
    # q0 = Quest('Warlord', 'Combat')
    # q0.run()
    # q1 = Quest('Grunt', 'Grunt')
    # q1.run()
    # q2 = Quest('Grunt', 'Warlord')
    # q2.interactive(q2.npc)
    # q2.sleep(5)
    # q2.turn_arount(interval=0.8)
    # q2.interactive(q2.target)
    
    q3 = Quest('warlord', 'murloc')
    q3.run()

    