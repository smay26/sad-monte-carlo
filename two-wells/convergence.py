#!/usr/bin/python3

import os
import numpy as np
import matplotlib.pyplot as plt
import system, compute
import glob

E = np.linspace(-system.h_small, 0, 10000)
E = 0.5*(E[1:] + E[:-1])
dE = E[1] - E[0]
hist = None

lowest_interesting_E = -1.07
highest_interesting_E = -0.5

indices_for_err = np.array([i for i in range(len(E)) if lowest_interesting_E <= E[i] <= highest_interesting_E])
E_for_err = E[indices_for_err]

def normalize_S(S):
    S = S - max(S)
    total = np.sum(np.exp(S)*dE)
    return S - np.log(total)

plt.figure('latest-entropy')

correct_S = normalize_S(system.S(E))

correct_S_for_err = correct_S[indices_for_err]
plt.plot(E, correct_S, ':', label='exact', linewidth=2)

markers= {'0.01+0.01':'D','0.01+0.001':'^','0.001+0.01':'o','0.001+0.001':'x'}
colors = {'z':'k','wl':'b','itwl':'g','sad':'tab:orange'}
dashes = {0: 'solid', 1:'dashed'}

paths = []
for fname in sorted(glob.glob('*'+system.system+'*.cbor')):
    if not ('no-barrier' in fname):
        if 'sad' in fname:
            if not( '0.01+0.001' in fname):
                paths.append(fname)
        elif 'wl' in fname or 'itwl' in fname:
            if '0.001+' in fname:
                paths.append(fname)
        else:
            paths.append(fname)

for fname in paths:
    print(fname)
    base = fname[:-5]
    method = base[:base.find('-')]

    energy_boundaries, mean_e, my_lnw, my_system, p_exc = compute.read_file(base)
    
    # Create a function for the entropy
    l_function, eee, sss = compute.linear_entropy(energy_boundaries, mean_e, my_lnw)
    plt.figure('latest-entropy')
    #plt.plot(E, normalize_S(l_function(E)), label=base)
    if method in {'wl','itwl','sad'}:
        precision = base[base.rfind('-') + 1:]
        plt.plot(E, normalize_S(l_function(E)), label=base, marker = markers[precision], color = colors[method], linestyle= dashes['no-barrier' in base], markevery=250)
    elif method == 'z':
        plt.plot(E, normalize_S(l_function(E)), label=base, color = colors[method], linestyle= dashes['no-barrier' in base])

    plt.figure('fraction-well')
    mean_which = np.loadtxt(f'{base}-which.dat')
    plt.plot(mean_e, mean_which, label=base)
    

    if os.path.exists(f'{base}-histogram.dat'):
        hist = np.loadtxt(f'{base}-histogram.dat')
        plt.figure('histogram')
        plt.plot(mean_e, hist, label=base)


    errors = []
    moves = []
    for frame_fname in sorted(glob.glob(f'{base}/*.cbor')):
        frame_base =frame_fname[:-5] 

        try:
            energy_boundaries, mean_e, my_lnw, my_system, p_exc = compute.read_file(frame_base)
            l_function, eee, sss = compute.linear_entropy(energy_boundaries, mean_e, my_lnw)

            moves.append(int(frame_fname[len(base)+1:-5]))
            err = np.max(np.abs(normalize_S(l_function(E))[indices_for_err] - correct_S_for_err))
            # print(f'err is {err} for {frame_base}')
            errors.append(err)
        except:
            pass

    plt.figure('convergence')
    if method in {'wl','itwl','sad'}:
        precision = base[base.rfind('-') + 1:]
        plt.loglog(moves, errors, label=base, marker = markers[precision], color = colors[method], linestyle= dashes['no-barrier' in base], markevery=2)
    elif method == 'z':
        plt.loglog(moves, errors, label=base, color = colors[method], linestyle= dashes['no-barrier' in base], linewidth = 3)

    #print(base[:base.find('-')]) #for debugging

plt.figure('latest-entropy')
plt.xlabel(r'$E$')
plt.ylabel(r'$S(E)$')
plt.legend()
plt.savefig(system.system+'.svg')

plt.figure('fraction-well')
plt.xlabel(r'E')
plt.ylabel(r'Proportion in Small Well')
plt.legend()
plt.savefig(system.system+'-which.svg')

if hist is not None:
    plt.figure('histogram')
    plt.xlabel(r'$E$')
    plt.ylabel(r'# of Visitors')
    plt.legend()
    plt.savefig(system.system+'-histogram.svg')

plt.figure('convergence')
plt.xlabel(r'# of Moves')
plt.ylabel(rf'max error in entropy between {lowest_interesting_E} and {highest_interesting_E}')
plt.ylim(1e-2, 1e2)
plt.legend()
plt.savefig(system.system+'-convergence.svg')

plt.show()