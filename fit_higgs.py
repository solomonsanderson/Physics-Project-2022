'''
Code for fitting a Voigt curve to Monte Carlo Higgs data 
'''


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import chisquare
from scipy.special import wofz
from scipy.special import voigt_profile
from load import load_data


path = r"Code\data\higgs.data"
effmass = load_data(path)[6]
fig, ax = plt.subplots()
n, bins, patches = ax.hist(effmass, bins = 200, range = [40,140], density=False, alpha=0.3, label="Histogram of MC Higgs")


def V(x, alpha, gamma, x0, N):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.
    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return N * np.real(wofz((x + x0 + 1j*gamma)/sigma/np.sqrt(2))) / sigma /np.sqrt(2*np.pi)


bins = bins[:-1]
popt, pcov = curve_fit(V, bins, n, maxfev=50000, p0=[2.5, 1.12, 125, 6000])
alpha, gamma, x0, N = popt
chisq_test_stats = chisquare(n, V(bins, *popt))

alpha_err, gamma_err, x0_err, N_err = np.sqrt(np.diag(pcov))
ax.plot(bins, V(bins, alpha, gamma, x0, N), label=f"Voigt Fit Curve:\n $\\alpha={alpha:.5f}\pm{alpha_err:.3f}$ \n $\\gamma={gamma:.5f}\pm{gamma_err:.3f}$ \n $x_0 = {-x0:.5f}\pm{x0_err:.3f}$ \n N = {N:.5}$\pm${N_err:.3f}", color="hotpink")

ax.set_xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
ax.set_ylabel("Count")
ax.set_title("Histogram of MC Higgs data with Voigt Curve")
ax.legend()
plt.show()