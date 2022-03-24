'''
Code for fitting a curve to simulated data 
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
n, bins, patches = ax.hist(effmass, bins = 100, range = [40,140], density=True, alpha=0.3, label="Histogram of MC Higgs")


def V(x, alpha, gamma, x0):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.
    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return np.real(wofz((x + x0 + 1j*gamma)/sigma/np.sqrt(2))) / sigma /np.sqrt(2*np.pi)


bins = bins[:-1]
popt, pcov = curve_fit(V, bins, n)
alpha, gamma, x0 = popt
chisq_test_stats = chisquare(n, V(bins, *popt))

alpha_err, gamma_err, x0_err = np.sqrt(np.diag(pcov))
ax.plot(bins + 0.5, V(bins, alpha, gamma, x0), label=f"Voigt Fit Curve:\n $\\alpha={alpha:.5f}\pm{alpha_err:.3f}$ \n $\\gamma={gamma:.5f}\pm{gamma_err:.3f}$ \n $x_0 = {-x0:.5f}\pm{x0_err:.3f}$ \n $\chi^2$ = {chisq_test_stats[0]:.3f}\np-value = {chisq_test_stats[1]:.3f}", color="hotpink")
ax.set_xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
ax.set_ylabel("Number of Amount")
ax.set_title("Histogram of MC Higgs data with Voigt Curve")
ax.legend()
plt.show()