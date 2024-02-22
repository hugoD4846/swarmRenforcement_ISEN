import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 7200, 7200)
plop = [[0]*10]*10
plop[0][0] = 1
plop[0][1] = 1
print(np.std(plop))
y = list(map(lambda x : 2 * np.std([x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,0,0,0,0,0,0,0,0,0,0,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x,x]), x))
plt.plot(y)
plt.show()