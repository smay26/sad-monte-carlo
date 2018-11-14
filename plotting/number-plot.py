#!/usr/bin/python3

import yaml, sys
import numpy as np
import matplotlib.pyplot as plt
 
def latex_float(x):
    exp = np.log10(x*1.0)
    if abs(exp) > 2:
        x /= 10.0**exp
        if ('%g' % x) == '1':
            return r'10^{%.0f}' % (exp)
        return r'%g\times 10^{%.0f}' % (x, exp)
    else:
        return '%g' % x

allcolors = list(reversed(['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple',
                           'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']))

my_histogram = {}
current_histogram = {}
my_entropy = {}
current_free_energy = {}
current_total_energy = {}
my_temperature = {}
my_time = {}
my_color = {}
max_iter = 0
my_gamma = {}
my_gamma_t = {}
Smin = None
fnames = sys.argv[1:]
for fname in fnames:
    print(fname)
    with open(fname) as f:
        yaml_data = f.read()
    data = yaml.load(yaml_data)
    current_histogram[fname] = np.array(data['bins']['histogram'])
    current_free_energy[fname] = np.array(data['bins']['lnw'])
    current_total_energy[fname] = np.array(data['bins']['total_energy'])
    my_color[fname] = allcolors.pop()
    my_time[fname] = np.array(data['movies']['time'])
    if len(my_time[fname]) > max_iter:
        max_iter = len(my_time[fname])
    my_temperature[fname] = data['T']
    my_entropy[fname] = np.array(data['movies']['lnw'])
    my_histogram[fname] = np.array(data['movies']['histogram'])
    my_gamma[fname] = np.array(data['movies']['gamma'], dtype=float)
    my_gamma_t[fname] = np.array(data['movies']['gamma_time'])
    if 'Sad' in data['method']:
        minT = data['method']['Sad']['min_T']
    if Smin is None:
        Sbest = my_entropy[fname][-1,:]
        Smin = Sbest[Sbest!=0].min() - Sbest.max()

plt.figure('gamma')
for fname in fnames:
        plt.loglog(my_gamma_t[fname], my_gamma[fname], color=my_color[fname], label=fname)
        print(my_gamma[fname])
plt.legend(loc='best')
plt.xlabel('$t$')
plt.ylabel(r'$\gamma$')
# plt.ylim(1e-12, 1.1)

plt.figure('histograms')
for fname in fnames:
        plt.plot(current_histogram[fname], 
                   color=my_color[fname], label=fname)
        print(my_histogram[fname])
plt.legend(loc='best')

plt.figure('excess free energy')
for fname in fnames:
        plt.plot(current_free_energy[fname], 
                   color=my_color[fname], label=fname)
        
plt.legend(loc='best')

plt.figure('excess internal energy')
for fname in fnames:
        plt.plot(current_total_energy[fname]/current_histogram[fname], 
                   color=my_color[fname], label=fname)
        
plt.legend(loc='best')

plt.figure('excess entropy')
for fname in fnames:
        U = current_total_energy[fname]/current_histogram[fname]
        F = current_free_energy[fname]
        T = my_temperature[fname]
        S = (U-F)/T
        S = S-S[0]
        plt.plot(S,
                   color=my_color[fname], label=fname)

plt.figure('excess entropy/N')
for fname in fnames:
        U = current_total_energy[fname]/current_histogram[fname]
        F = current_free_energy[fname]
        T = my_temperature[fname]
        S = (U-F)/T
        S = S-S[0]
        SN = np.arange(0, len(S), 1) 
        plt.plot(S/SN,
                   color=my_color[fname], label=fname)

        
plt.legend(loc='best')

plt.figure('excess internal energy/N')
for fname in fnames:
        U = current_total_energy[fname]/current_histogram[fname]
        UN = np.arange(0, len(U), 1) 
        plt.plot(U/UN,
                   color=my_color[fname], label=fname)

        
plt.legend(loc='best')
plt.show()