'''Fitting the sum of the power law and crystal ball functions '''


from crystalball import crystal_ball_vec, crystal_ball_vec_self
from fit_MCZ0 import power_series
from load import load_data
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import numpy as np  
from scipy.stats import chisquare



higgs_effmass = load_data(r"Code\data\higgs.data")
scale = len(higgs_effmass) / 240.816

effmass = load_data(r"Code\data\real-dimuon-29M.data")[6]

fig, ax = plt.subplots()
n, bins, patches = ax.hist(effmass, bins = 500, range = [110,140], density=False, alpha=0.3, label="Dimuon Data")

def power_crystal_sum(x, a, k, x0, N):
    # pow_fixed = [5.32501, 2.13846, -91.0539]
    alpha = 1.35733
    sigma = 2.62439
    x_bar = 124.381
    n = 2.58513
    f = power_series(x, a, k, x0) + crystal_ball_vec_self(x, alpha, n, x_bar, sigma, N)
    return f


sum_popt, sum_pcov = curve_fit(power_crystal_sum, bins[:-1], n, p0 = [244884.29, 2.61, -89.18, 1], maxfev=10000)
a, k, x0, N = sum_popt
a_perr, k_perr, x0_perr, N_perr = np.sqrt(np.diag(sum_pcov))
chisq_test_stats = chisquare(n, power_crystal_sum(bins, *sum_popt)[:-1])
label = f"Fitted Crystal Ball/ Power Law Function \n a = {a:.3f}$\pm${a_perr:.3f}\n k = {k:.5f}$\pm${k_perr:.3f} \n $x_0$ = {x0:.5f}$\pm${x0_perr:.3f} \n N = {N:.3f}$\pm${N_perr:.3f}\n $\chi^2$ = {chisq_test_stats[0]:.3f}\np-value = {chisq_test_stats[1]:.3f}"
ax.plot(bins, power_crystal_sum(bins, *sum_popt), label = label)
print(sum_popt)

ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
ax.set_ylabel("Count")
ax.set_title("Summed Crystal Ball & Power Law Fit to Dimuon Data")

# Calculating a scaling factor, for finding the upper limit on the number of higgs
var_higgs_0 = ((len(higgs_effmass) / 240.816) ** 2) * ( (N_perr)**2)

var_higgs_1 = (((-len(higgs_effmass) * N) / (240.816 ** 2)) **2) * (1.24**2)

sigma_higgs_no = np.sqrt(var_higgs_0 + var_higgs_1)


higgs_no = N * len(higgs_effmass) / 240.816
higgs_upper = higgs_no + 2 * sigma_higgs_no
print(higgs_upper)
ax.legend()
plt.show()