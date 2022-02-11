'''
Code for fitting a curve to simulated data 
'''


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import wofz
from scipy.special import voigt_profile


path = r"Code\data\real-dimuon-400k.data"

data = pd.read_csv(path, delim_whitespace = True , header=None)
effmass = data[6]
fig, ax = plt.subplots()


n, bins, patches = ax.hist(effmass, bins = 100, range = [40,140], density=True, alpha=0.3, label="Histogram of MC-Z0")

def V(x, alpha, gamma, x0):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.

    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz((x - x0 + 1j*gamma)/sigma/np.sqrt(2))) / sigma /np.sqrt(2*np.pi)

bins = bins[:-1]

popt, pcov = curve_fit(V, bins, n,  p0=[1.35105, 2.20259, 90.25890], maxfev = 7000)
alpha, gamma, x0 = popt[0], popt[1], popt[2]
ax.plot(bins + 0.5, V(bins, alpha, gamma, x0), label=f"Voigt Fit Curve:\n $\\alpha={alpha:.5f}$ \n $\\gamma={gamma:.5f}$ \n $x_0 = {x0:.5f}$", color="hotpink"    )
ax.set_xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
ax.set_ylabel("Number")
ax.set_title("Histogram of MC-Z0 data with Power Curve")

def power_series(x, a, k, x0):
    y = a * (x + x0)**(-k)
    return y 

bins = bins[54:]
n = n[54:]
print(len(n))
popt_power, pcov_power = curve_fit(power_series, bins, n, maxfev = 10000)
a, k, x0 = popt_power[0], popt_power[1], popt_power[2]
ax.plot(bins+0.5, power_series(bins, a, k, x0),label=f"Power Fit Curve:\n $a={a:.5f}$ \n $k={k:.5f}$ \n $x_0 = {x0:.5f}$" , color="forestgreen", marker = None)


ax.legend()
plt.show()