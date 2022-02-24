from scipy.stats import crystalball
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

path = r"Code\data\higgs.data"

data = pd.read_csv(path, delim_whitespace = True , header=None)
effmass = data[6]
fig, ax = plt.subplots()


n, bins, patches = ax.hist(effmass, bins = 100, range = [40,140], density=True, alpha=0.3, label="Histogram of MC Higgs")

def crystal_ball(x, beta, m, N, x0):
    A = (m/np.abs(beta))**m * np.exp(-beta**2/2)
    B = m / (np.abs(beta) - np.abs(beta))
    if x > -beta:
        f = N * np.exp(-(x+x0)**2 / 2)
    elif x <= -beta:
        f = N * A * (B - (x+x0))**(-m)
    return f



# def crystal_ball(x, alpha, n, x_bar, sigma, x0):

# fit = crystalball.fit(bins)
# print(fit)
# a = crystalball.pdf(*fit)



popt_crystal, pcov_crystal = curve_fit(crystal_ball, bins[:-1], n, maxfev = 10000)
print(popt_crystal)
# ax.plot(bins, a)
plt.show()