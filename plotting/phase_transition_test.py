import numpy as np
import matplotlib.pyplot as plt


row = 10
col = 10
N_sites = 10

pressure = np.zeros((row, col))
T = np.zeros((row, col))
s_excess = np.zeros((row, col))
chem_pot = np.zeros((row, col))
N = np.zeros((row, col))
energy_data = np.zeros((row, col))
E = np.zeros((row, col))
for i in np.arange(0,col,1):
    for j in np.arange(0,row,1):
        T[i][j] = 2
        s_excess[i][j] = 3
        chem_pot[i][j] = 4
        N[i][j] = 5
        energy_data[i][j] = 6
        E = 7

print((2 * 3 + 4*5 - 6)/10**2)

for i in np.arange(0,col,1):
    for j in np.arange(0,row,1):
        pressure[i][j] = (T[i][j] * s_excess[i][j] + chem_pot[i][j] * N[i][j] - energy_data[i][j])/N_sites**2
        #pressure[i][j] = 1

    print(pressure)

    plt.figure('pressure')
    plt.clf()
    #pressure = T(ds/dv)U,N
    plt.pcolor(N,E,pressure,)
    plt.xlabel('$N$')
    plt.ylabel('$E$')
    plt.colorbar()
    plt.pause(1)