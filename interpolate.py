'''Comparison of the real data in a gap surrounding the mass of the Higgs against the expected mass from the background'''


from sympy import N
from load import load_data
from fit_MCZ0 import power_series
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.stats import chisquare
import scipy.integrate as integrate
import numpy as np  

from matplotlib import cbook
from mpl_toolkits.axes_grid1.inset_locator import inset_axes 
from mpl_toolkits.axes_grid1.inset_locator import mark_inset

effmass = load_data("Code/data/real-dimuon-29M.data")[6]


fig, ax = plt.subplots()
ranges = [110, 140]
n, bins, patches = ax.hist(effmass, bins = 500, range = ranges, density=False, alpha=0.3, label="Dimuon Data")

# cutting the data for the fit 
print(bins)
ll = np.argwhere(bins == 122)[0][0]
ul = np.argwhere(bins == 128)[0][0]
ax.axvspan(xmin = bins[ll], xmax = bins[ul], color="orange", alpha = 0.2, label=f"Gap area between {bins[ll]} and {bins[ul]}")

bins_gap = np.array(list(bins[:ll]) + list(bins[ul:]))
n_gap = np.array(list(n[:ll]) + list(n[ul:]))



popt_gap, pcov_gap = curve_fit(power_series, bins_gap[:-1], n_gap, maxfev = 10000, p0 = [5.32501, 2.13, 91.05])
a, k, x0 = popt_gap
a_err, k_err, x0_err = np.sqrt(np.diag(pcov_gap))
dof = len(bins) - 1
print(dof)
chisq_test_stats = chisquare(n, power_series(bins, *popt_gap)[:-1])
chisqu = (chisq_test_stats[0]) / (len(bins) - 1)
print(chisqu)
ax.plot(bins, power_series(bins, *popt_gap), label=f"Power Fit Curve:\n $a={a:.5f} \pm {a_err:.3f}$ \n $k={k:.5f}\pm{k_err:.3f}$ \n $x_0 = {x0:.5f}\pm{x0_err:.3f}$ \n $\chi^2$ = {chisq_test_stats[0]:.3f}\np-value = {chisq_test_stats[1]:.3f}" , color="forestgreen", marker = None)

# Calculating the area under the power series fit
integral = integrate.quad(power_series, bins[ll], bins[ul], args=(a, k, x0))
bin_width = (ranges[1] - ranges[0])/500
integral_adjusted = integral[0]/bin_width
err_adjusted = integral[1]/bin_width
print(f"integral = {integral_adjusted} +- {err_adjusted}")

n_gap_sum = sum(n[ll:ul])
bw = (ranges[1] - ranges[0])/len(bins)

print(f"Count in gap = {n_gap_sum}")

textstr = f"Integral = {integral_adjusted:.5f} +- {err_adjusted:.3f} \n Count in gap = {n_gap_sum:.5f}$\pm${np.sqrt(n_gap_sum):.3f}"
props = dict(boxstyle='round', facecolor='White', alpha=1)
ax.text(0.10, 0.95, textstr, transform=ax.transAxes, fontsize=11, verticalalignment='top', bbox=props)

ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
ax.set_ylabel("Count")
ax.set_title("Real dimuon with fitted power law and gap")


# Code to show the extra point beyond the gap interval.
# When set to true this adds an inset figure and red markers to the data
extra_bin = True

if extra_bin == True:
    ax.plot(bins[ll:ul+1]+bw/2, n[ll:ul+1], linestyle = "None", marker = "o", mfc="red", mec="black")
    axins = inset_axes(ax, loc=1,width="30%", height="40%") # zoom = 2
    axins.plot(bins[ll:ul+1]+bw/2, n[ll:ul+1], linestyle = "None", marker = "o", mfc="red", mec="black", ms=5)
    axins.hist(effmass, bins = 500, range = ranges, density=False, alpha=0.3, color="#1f77b4")
    axins.axvspan(xmin = bins[ll], xmax = bins[ul], color="orange", alpha = 0.2, label=f"Gap area between {bins[ll]} and {bins[ul]}")
    axins.set_xlim(127.7, 128.3)
    axins.set_ylim(6*72.5,13*72.5)
    plt.xticks(visible=False)
    plt.yticks(visible=False)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    plt.draw()

# ax.legend()
plt.show()