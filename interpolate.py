''''''

from sympy import N
from load import load_data
from fit_MCZ0 import power_series
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import scipy.integrate as integrate
import numpy as np  


effmass = load_data("Code/data/real-dimuon-4M.data")[6]


fig, ax = plt.subplots()
range = [110, 140]
n, bins, patches = ax.hist(effmass, bins = 500, range = range, density=False, alpha=0.3, label="Dimuon Data")

# cutting the data for the fit 
print(bins)
ll= np.argwhere(bins == 122.)[0][0]
ul = np.argwhere(bins == 128.)[0][0]
# ll = 160
# ul = 340
ax.axvspan(xmin = bins[ll], xmax = bins[ul], color="orange", alpha = 0.2, label=f"Gap area between {bins[ll]} and {bins[ul]}")

bins_gap = np.array(list(bins[:ll]) + list(bins[ul:]))
n_gap = np.array(list(n[:ll]) + list(n[ul:]))

popt_gap, pcov_gap = curve_fit(power_series, bins_gap[:-1], n_gap, maxfev = 10000, p0 = [5.32501, 2.13, 91.05])
a, k, x0 = popt_gap
a_err, k_err, x0_err = np.sqrt(np.diag(pcov_gap))
# ax.plot(bins_gap[:-1], n_gap)
ax.plot(bins, power_series(bins, *popt_gap), label=f"Power Fit Curve:\n $a={a:.5f} \pm {a_err:.3f}$ \n $k={k:.5f}\pm{k_err:.3f}$ \n $x_0 = {x0:.5f}\pm{x0_err:.3f}$" , color="forestgreen", marker = None)

# Calculating the area under the power series fit
print(bins[ll], bins[ul])
integral = integrate.quad(power_series, bins[ll], bins[ul], args=(a, k, x0))
print(f"integral = {integral[0]} +- {integral[1]}")  # has been checked with wolfram alpha and is correct

# Summing the bins in the range of the integral
n_gap_sum = sum(n[ll:ul])
print(n_gap_sum)
# print(n[ll:ul])

# sum of bins in the gap is much larger than the integral, likely error in theory

ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
ax.set_ylabel("Count")
ax.set_title("Real dimuon with fitted power law and gap")


ax.legend()
plt.show()