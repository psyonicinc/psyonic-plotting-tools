import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0,3,1000);
theta = t*-10;
theta_wrapped = np.mod(theta+ np.pi, 2*np.pi) - np.pi 

plt.plot(t, theta)
plt.plot(t, theta_wrapped)
plt.show()