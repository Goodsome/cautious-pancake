import numpy as np 
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression

array = [
    447, 76, 452, 758,
    515, 88, 521, 873,
    566, 96, 579, 970,
    618, 105, 642, 1075,
    724, 123, 770, 1290,
    794, 136, 853, 1430,
    856, 147, 937, 1571,
    914, 158, 1028, 1723,
    997, 173, 1144, 1916,
    1105, 191, 1268, 2124,
    1173, 203, 1477, 2475,
    1281, 224, 1662, 2785,
    1522, 266, 1975, 3309]

data = np.array(array).reshape(-1, 4)
i = data[:, 0].reshape(-1, 1)
s_1 = data[:, 1].reshape(-1, 1)
s_2 = data[:, 2].reshape(-1, 1) / 6
v = data[:, 3].reshape(-1, 1) / 7

model = LinearRegression()
model.fit(i, s_1)
print(model.coef_)
print(model.intercept_)
print(model.predict([[24]]))

i = 447
print(i * 0.09588 * 8 * 1.2)
print(i * 0.1836 * 7)
print(i * 0.47)
print(i * 2.03)
print(i * 0.9792)
print(i * 0.9792 * 1.1)