'''
Code for fitting a voigt or power law curve to simulated data 
'''


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from scipy.special import wofz
from scipy.special import voigt_profile
from scipy.stats import chisquare
from load import load_data


def power_series(x, a, k, x0):
    y = a * (x + x0)**(-k)
    return y 

def V(x, alpha, gamma, x0, N):
    """
    Return the Voigt line shape at x with Lorentzian component HWHM gamma
    and Gaussian component HWHM alpha.

    """
    sigma = alpha / np.sqrt(2 * np.log(2))

    return N * np.real(wofz((x - x0 + 1j*gamma)/sigma/np.sqrt(2))) / sigma /np.sqrt(2*np.pi)

if __name__ == "__main__":
    path = r"Code\data\MC-Z0.data"
    effmass = load_data(path)[6]
    fig, ax = plt.subplots()


    n, bins, patches = ax.hist(effmass, bins = 200, range = [40,140], density=False, alpha=0.3, label="Histogram of MC-Z0")

    bins = bins[:-1]
    popt, pcov = curve_fit(V, bins, n,  p0=[1.35105, 2.20259, 90.25890, 2], maxfev = 7000)
    chisq_test_stats_voigt = chisquare(n, V(bins, *popt))
    # print(chisq_test_stats_voigt)
    chisqu = (chisq_test_stats_voigt[0]) / (len(bins) - 1)
    print(chisqu)
    # popt, pcov = curve_fit(V, bins, n, maxfev = 7000)
    alpha, gamma, x0, N = popt
    alpha_err, gamma_err, x0_err, N_err = np.sqrt(np.diag(pcov))
    ax.plot(bins + 0.5, V(bins, alpha, gamma, x0, N), label=f"Voigt Fit Curve:\n $\\alpha={alpha:.5f} \pm {alpha_err:.3f}$ \n $\\gamma={gamma:.5f} \pm {gamma_err:.3f}$ \n $x_0 = {x0:.5f} \pm {x0_err:.3f}$ \n $\chi^2$ = {chisq_test_stats_voigt[0]:.3f}\np-value = {chisq_test_stats_voigt[1]:.3f}", color="hotpink")
    ax.set_xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
    ax.set_ylabel("Number")
    ax.set_title("Histogram of MC-Z0 data with Power Curve")

    bins = bins[111:]
    n = n[111:]

    popt_power, pcov_power = curve_fit(power_series, bins, n, maxfev = 1000000)
    chisq_test_stats_power = chisquare(n, power_series(bins, *popt_power))
    chisqu = (chisq_test_stats_power[0]) / (len(bins) - 1)
    print(chisqu)
    a, k, x0 = popt_power[0], popt_power[1], popt_power[2]
    a_err, k_err, x0_err = np.sqrt(np.diag(pcov_power))
    ax.plot(bins+0.5, power_series(bins, a, k, x0),label=f"Power Fit Curve:\n $a={a:.5f} \pm {a_err:.3f}$ \n $k={k:.5f}\pm{k_err:.3f}$ \n $x_0 = {x0:.5f}\pm{x0_err:.3f}$ \n $\chi^2$ = {chisq_test_stats_power[0]:.3f}\np-value = {chisq_test_stats_power[1]:.3f}" , color="forestgreen", marker = None)


    ax.legend()
    plt.show()  