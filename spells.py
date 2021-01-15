import pandas as pd

columns = 'cast_time, gcd, cd, damage, periodic_damage, interval, duration, give_power'.split(',')
spells = pd.DataFrame(columns=columns)
spells.index.name = 'spells_id'
spells.loc[589] = [0, 1.5, 0, 0.1292, 0.09588, 2, 16, 4]
