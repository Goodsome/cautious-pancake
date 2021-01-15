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
        self.classes = 'shadow preist'
        self.intellect = intellect
        self.critical_strike = critical_strike
        self.mastery = mastery
        self.haste = haste
        self.versatility = versatility
    
    @property
    def Critical_strike(self):
        return self.critical_strike / 3500 + 0.05
    
    @property
    def Mastery(self):
        return self.mastery / 7000 + 0.04
    
    @property
    def Haste(self):
        return self.haste / 3300
    
    @property
    def Versatility(self):
        return self.versatility / 4000

    @property
    def Spells_power(self):
        return self.intellect

    def equip(self, equipments: list):
        for e in equipments:
            self.primary += e.primary
            self.critical_strike += e.critical_strike
            self.mastery += e.mastery
            self.haste += e.haste
            self.versatility += e.versatility

    def attributes(self):
        print(f'intellect: {self.Spells_power}, haste: {self.Haste:.2%}, critical strike: {self.Critical_strike:.2%}, mastery: {self.Mastery:.2%}, versatility: {self.Versatility:.2%}')
        

class Spells(Classes):
    def __init__(self, spells_id, cast_time, gcd, cd, damage=None, periodic_damage=None, interval=None, duration=None, give_power=None) -> None:
        super().__init__(intellect=1464)
        self.spells_id = spells_id 
        self.cast_time = cast_time
        self.gcd = gcd
        self.cd = cd
        self.damage = damage
        self.periodic_damage= periodic_damage
        self.interval = interval
        self.duration = duration
        self.give_power = give_power
    
    @property
    def Damage(self):
        return self.Spells_power * self.damage

    @property
    def Periodic_damage(self):
        return self.Spells_power * self.periodic_damage


if __name__ == "__main__":
    x = Classes(intellect=1464, critical_strike=517, mastery=335, haste=847, versatility=155)
    x.attributes()
    shadow = Spells(spells_id=589, cast_time=0, gcd=1.5, cd=0, damage=0.1292, periodic_damage=0.09588, interval=2, duration=16, give_power=4)
    print(shadow.Damage)
    print(shadow.Periodic_damage * 8)
    print(254 / shadow.Damage)

