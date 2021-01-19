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
    def __init__(self) -> None:
        self.health = 1e8


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

    def cast(self, spell_id):
        print(self.spells[spell_id])
        

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
        self.dot_count = 0
    
    @property
    def Damage(self):
        return self.att.sp * self.damage * (1+self.att.ver) * 1.2

    @property
    def Periodic_damage(self):
        return self.att.sp * self.periodic_damage * (1+self.att.ver) * 1.2

    @property
    def Interval(self):
        return self.interval / (1+self.att.has)

    def __repr__(self) -> str:
        return spells_name[self.spell_id] 


class Dot:
    def __init__(self, spells):
        self.periodic_damage = spells.periodic_damage
        self.interval = spells.interval
        self.duration = spells.duration

class Simc:
    def __init__(self, player) -> None:
        self.t = 0
        self.dt = 1e-2
        self.player = player
        self.damage = 0
        self.dot_pool = []
    
    def start_simc(self, total_time):
        for t in range(int(total_time / self.dt)):
            if self.t == 0:
                self.damage += self.player.spells[589].Damage
                self.dot_pool.append(self.player.spells[589])
            self.get_dot_damage()
            self.t += self.dt
    
    def cal_dps(self):
        print(f'dps: {self.damage / self.t}')
    
    def get_dot_damage(self):
        for dot in self.dot_pool:
            dot.dot_count += self.dt
            dot.duration -= self.dt
            if dot.dot_count >= dot.Interval:
                self.damage += dot.Periodic_damage
                dot.dot_count = 0
            if dot.duration <= 0:
                self.dot_pool.remove(dot)


if __name__ == "__main__":
    x = Classes(intellect=1522, critical_strike=480, mastery=408, haste=827, versatility=100)
    x.attributes()
    s = Simc(x)
    s.start_simc(10)
    s.cal_dps()
