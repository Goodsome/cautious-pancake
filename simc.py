import json
import pandas as pd

from spells import spells, spells_name


class Equipment:
    def __init__(self, gear, primary=0, critical_strike=0, mastery=0, haste=0, versatility=0) -> None:
        super().__init__()
        self.gear = gear
        self.primary = primary
        self.critical_strike = critical_strike
        self.mastery = mastery
        self.haste = haste
        self.versatility = versatility
    

class Object:
    pass


class Classes(Object):
    def __init__(self, intellect=None, critical_strike=None, mastery=None, haste=None, versatility=None) -> None:
        super().__init__()
        self.name = 'shadow'
        self.intellect = intellect
        self.critical_strike = critical_strike
        self.mastery = mastery
        self.haste = haste
        self.versatility = versatility
    
    @property
    def spells(self):
        return {k: Spell(self, k, **v) for k, v in spells[self.name].items()}

    @property
    def cri(self):
        return self.critical_strike / 3500 + 0.05
    
    @property
    def mas(self):
        return self.mastery / 7000 + 0.04
    
    @property
    def has(self):
        return self.haste / 3300
    
    @property
    def ver(self):
        return self.versatility / 4000

    @property
    def sp(self):
        return self.intellect

    def equip(self, equipments: list):
        for e in equipments:
            self.primary += e.primary
            self.critical_strike += e.critical_strike
            self.mastery += e.mastery
            self.haste += e.haste
            self.versatility += e.versatility

    def attributes(self):
        print(f'intellect: {self.sp}, haste: {self.has:.2%}, critical strike: {self.cri:.2%}, mastery: {self.mas:.2%}, versatility: {self.ver:.2%}')
        

class Spell:
    def __init__(self, att, spell_id, cast_time, gcd, cd, damage=None, periodic_damage=None, interval=None, duration=None, give_power=None) -> None:
        self.att = att 

        self.spell_id = spell_id 
        self.cast_time = cast_time
        self.gcd = gcd
        self.cd = cd
        self.damage = damage
        self.periodic_damage = periodic_damage
        self.interval = interval
        self.duration = duration
        self.give_power = give_power
    
    @property
    def Damage(self):
        return self.att.sp * self.damage * (1+self.att.ver) * 1.2

    @property
    def Periodic_damage(self):
        return self.att.sp * self.periodic_damage * (1+self.att.ver) * 1.2

    @property
    def Interval(self):
        print(self.att.has)
        return self.interval * (1-self.att.has)

    def __repr__(self) -> str:
        return spells_name[self.spell_id] 


if __name__ == "__main__":
    x = Classes(intellect=1522, critical_strike=480, mastery=408, haste=827, versatility=100)
    print(x.attributes())
    print(x.spells[589].interval)
    print(x.spells[589].Interval)
    print(x.spells[589].duration)
    print(x.spells[589].Periodic_damage * 1.0983)
    print(x.spells[589].Periodic_damage * x.spells[589].duration / x.spells[589].Interval)