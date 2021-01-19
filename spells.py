import pandas as pd

spells_name = {
    589: 'Shadow Word: Pain',
    34914: 'Vampiric Touch'
}
spells = {}
columns = 'cast_time, gcd, cd, damage, periodic_damage, interval, duration, give_power'.split(', ')
shadow_spells = pd.DataFrame(columns=columns)
shadow_spells.index.name = 'spells_id'
shadow_spells.loc[589] = [0, 1.5, 0, 0.1292, 0.09588, 2, 16, 4]
shadow_spells.loc[34914] = [1.5, 1.5, 0, 0, 0.1836, 3, 21, 5]

spells['shadow'] = shadow_spells.to_dict(orient='index')