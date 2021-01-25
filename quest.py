from utils import *
from config import *


class Quest:
    def __init__(self, QuestId) -> None:
        self.quest_id = QuestId
        self.npc = quest_info[self.quest_id]['npc']

    def accept_quest(self):
        interactive(self.npc)

    def abandon_quest(self):
        add_abandon = f'run C_QuestLog.SetAbandonQuest({self.quest_id})'
        type_macro(add_abandon)
        type_macro('run C_QuestLog.SetAbandonQuest()')
        type_macro('run C_QuestLog.AbandonQuest()')
        


if __name__ == '__main__': 
    run(['alt', 'tab'], interval=0)
    q = Quest('59929')
    q.abandon_quest()
        