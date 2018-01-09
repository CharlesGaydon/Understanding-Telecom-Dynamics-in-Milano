import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

f = "Results/Results-Pregel-12-01.txt"
d = pd.read_csv(f, sep = ',', header=None, names = ["Id","Score"])
Map = np.zeros((100,100))
# print(d.head(5))
val = d["Score"].max()
print(val)

for i in range(d.shape[0]) :
    v = d.iloc[i].values
    j = int(v[0])%100
    i = int((int(v[0])-j)/100)

    Map[i,j] = float(v[1])
# Map = Map[15:-15, 20:-11]
Map[14,:] = val/2
Map[-14] = val/2
Map[:,19] = val/2
Map[:,-10] = val/2
plt.imshow(Map, cmap='hot', interpolation='nearest')
plt.show()