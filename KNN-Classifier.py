import pandas as pd
import numpy as np
from sklearn import neighbors

df=pd.read_csv("post-operative.csv")

def mod_data(df):
    df.replace('mid', 2, inplace=True)
    df.replace('low', 1, inplace=True)
    df.replace('excellent', 4, inplace=True)
    df.replace('stable', 2, inplace=True)
    df.replace('high', 3, inplace=True)
    df.replace('mod-stable', 1, inplace=True)
    df.replace('good', 3, inplace=True)
    df.replace('unstable', 0, inplace=True)
    df.replace('fair', 2, inplace=True)
    df.replace('poor', 1, inplace=True)
    df.replace('A', 0, inplace=True)
    df.replace('S', 1, inplace=True)
    df.replace('I', 2, inplace=True)
mod_data(df)

veri = np.array(df)

x = veri[:, 0:8]
y = veri[:, 8:9]

K = 11

classifiers = neighbors.KNeighborsClassifier(K, weights='distance')
classifiers.fit(x, y.ravel())

dataClass = classifiers.predict([[2, 1, 5, 2, 2, 2, 0, 10]])
print('Prediction:', end='')

if dataClass == 0:
    print('A')
elif dataClass == 1:
    print('S')
else:
    print('I')
















