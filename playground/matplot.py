import matplotlib.pyplot as plt
import numpy as np


x = np.linspace(0, 10, 50)
y1 = x*x

plt.figure()
plt.xlabel('X')
plt.ylabel('Y')

# plt.plot(x, y1, label='hello')
plt.plot(np.array([1, 2, 4, 24]), np.array([2, 3, 4, 2]), label='world')
plt.scatter(np.array([1, 2, 4, 24]), np.array([2, 3, 4, 2]), label='world')

plt.legend(loc='upper left')
plt.show()