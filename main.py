import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

from cstr import cstr
from disturbances import disturbances

# time horizon
T = 60
nsteps = 1000
t = np.linspace(0, T, nsteps)

# initial states
x = np.ones((len(t), 2))
x[0] = [0.87725294608097, 324.475443431599]  # steady state

# control trajectory
u = [300 for i in range(int(nsteps/4))] + \
    [298 for i in range(int(nsteps/2))] + \
    [302 for i in range(int(nsteps/4))]

# disturbances
# d = np.c_[
#     np.array(
#         [1 for i in range(int(nsteps/3))] + \
#         [1.2 for i in range(int(nsteps/3))] + \
#         [1.1 for i in range(int(nsteps/3) + 1)]
#     ).reshape(-1, 1),
#     np.array(
#         [350 for i in range(int(nsteps/2))] + \
#         [340 for i in range(int(nsteps/2))]
#     ).reshape(-1, 1)
# ]
disturbance_space = {"low": np.array([0.9, 340]), "high": np.array([1.1, 360])}
d = disturbances(nsteps, disturbance_space)

# simulate
for i in range(nsteps - 1):
    ts = [t[i], t[i + 1]]
    x[i + 1] = odeint(cstr, x[i], ts, args=(u[i], d[i]))[-1]

    if x[i + 1][1] < 370:
        u[i + 1] = 310
    else:
        u[i + 1] = 290
    
# plot disturbances
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
ax1.plot(t, d[:, 0], label='Caf')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Concentration (mol/m$^3$)')
ax1.legend()
ax2.plot(t, d[:, 1], label='Tf')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Temperature ($^\circ$C)')
ax2.legend()
f.suptitle('Disturbances')
plt.tight_layout()

# plot controls
plt.figure(figsize=(4, 3))
plt.plot(t, u, label='Tc')
plt.xlabel('Time (min)')
plt.ylabel('Temperature ($^\circ$C)')
plt.title('Control')
plt.legend()
plt.tight_layout()

# plot states
f, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3))
ax1.plot(t, x[:, 0], label='Ca')
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Concentration (mol/m$^3$)')
ax1.legend()
ax2.plot(t, x[:, 1], label='T')
ax2.set_xlabel('Time (min)')
ax2.set_ylabel('Temperature ($^\circ$C)')
ax2.legend()
f.suptitle('States')
plt.tight_layout()
