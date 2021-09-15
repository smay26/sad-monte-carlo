#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
import system, compute
import glob

def C(T, S):#T is a temperature and S is an entropy function
    E = np.linspace(-system.h_small, 0, 5000)
    E = 0.5*(E[1:] + E[:-1])
    dE = E[1] - E[0]

    def normalize_S(S):
        S = S - max(S)
        total = np.sum(np.exp(S)*dE)
        return S - np.log(total)

    S = normalize_S(S(E))

    S_minus_E = S-E/T
    M = np.max(S_minus_E)

    Z = np.sum(np.exp(S_minus_E-M))*dE

    avg_E = np.sum(np.exp(S_minus_E-M) * E) * dE / Z

    avg_E_squared = np.sum(np.exp(S_minus_E-M) * E**2) * dE / Z

    return (avg_E_squared - avg_E**2 ) / T**2

#Testing
if __name__ == "__main__":
    
    t_low = np.linspace(0.001,0.002,50)
    t_peak = np.linspace(0.002,0.009,150)
    t_high = np.linspace(0.009,0.1,50)
    try:
        c_low = np.loadtxt('cv_low_saved.txt')
    except:
        c_low = np.array([C(T,system.S) for T in t_low])
        np.savetxt('cv_low_saved.txt', c_low)

    try:
        c_peak = np.loadtxt('cv_peak_saved.txt')
    except:
        c_peak = np.array([C(T,system.S) for T in t_peak])
        np.savetxt('cv_peak_saved.txt', c_peak)

    try:
        c_high= np.loadtxt('cv_high_saved.txt')
    except:
        c_high = np.array([C(T,system.S) for T in t_high])
        np.savetxt('cv_high_saved.txt', c_high)

    c_peak = np.array([C(T,system.S) for T in t_peak])

    fig, ax = plt.subplots(figsize=[5, 4])

    ax.plot(np.concatenate((t_low,t_peak,t_high)), np.concatenate((c_low,c_peak,c_high)))

    # inset axes....
    axins = ax.inset_axes( 0.75 *  np.array([1, 1, 0.47/0.5, 0.47/0.5]))#[0.005, 0.012, 25, 140])
    axins.plot(t_peak,c_peak)
    # sub region of the original image
    x1, x2, y1, y2 = 0.002, 0.009, 25, 140
    axins.set_xlim(x1, x2)
    axins.set_ylim(y1, y2)
    axins.set_xticklabels('')
    axins.set_yticklabels('')

    ax.indicate_inset_zoom(axins, edgecolor="black")

    plt.show()







