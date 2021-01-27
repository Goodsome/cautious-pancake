from utils import *
from config import *


class Quest:
    def __init__(self, QuestId) -> None:
        self.quest_id = QuestId
        self.npc = quest_info[self.quest_id]['npc']

    def accept_quest(self):
        interactive(self.npc)

    def abandon_quest(self):
        type_macro(f'abandon {self.quest_id}')

    def distance(self):
        type_macro(f'dump C_QuestLog.GetDistanceSqToQuest({self.quest_id})')
        

if __name__ == '__main__': 
    run(['alt', 'tab'], interval=0)
    q = Quest('59929')
    # q.accept_quest()
    # q.abandon_quest()
    q.distance()
        