'''
Finding percentage of points contained in a range and the errors associated
with them. Dataframe at the end is created to tabulate errors and percentages
so that it can be sorted and compared.
'''


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import quad
from load import load_data
from matplotlib.patches import Rectangle


path = r"Code/data/higgs.data"

effmass = load_data(path)[6]
fig, ax = plt.subplots()


n, bins, patches = ax.hist(effmass, bins = 60, range = [80,140], alpha=0.3, label="MC Higgs")


def integrand(x):
    '''integrand for error_func'''

    integrand = (1/np.sqrt(np.pi)) * np.exp(-x**2)
    return integrand


def error_func(z):
    '''Error function used for calculating D in crystal ball function
    https://en.wikipedia.org/wiki/Error_function'''

    integral = quad(integrand, 0, z)
    return integral


def crystal_ball(x, alpha, n, x_bar, sigma, N):
    '''Crystal ball function: https://en.wikipedia.org/wiki/Crystal_Ball_function'''

    
    A = (n/np.abs(alpha))**n * np.exp(-(np.abs(alpha)**2) / 2)
    B = n / np.abs(alpha) - np.abs(alpha)


    def greater_minus_alpha(x):
        f = N * np.exp(-(x - x_bar)**2/(2 * sigma**2))
        return f


    def less_equal_minus_alpha(x):
        f = N * A * (B - (x - x_bar)/(sigma))**(-n)
        return f
    
    
    if (x - x_bar)/(sigma) > -alpha:
        f = greater_minus_alpha(x)
    elif ((x - x_bar)/sigma<=-alpha):
        f = less_equal_minus_alpha(x)

    return f


crystal_ball_vec = np.vectorize(crystal_ball)

def crystal_ball_vec_self(x,  alpha, n, x_bar, sigma, N):
    y = np.zeros(x.shape)
    for i in range(len(y)):
        y[i] = crystal_ball(x[i], alpha, n, x_bar, sigma, N)
    return y


popt_crystal, pcov_crystal = curve_fit(crystal_ball_vec, bins[:-1], n, maxfev = 10000, p0 = [1,2,125,1,1602])
alpha, n_crystal, x_bar, sigma, N = popt_crystal


lower_limit_range = range(80,122)
upper_limit_range = range(128,140)

limits_and_errors = []


for lower_limit in lower_limit_range:
    for upper_limit in upper_limit_range:
        lli = int(np.where(bins == lower_limit)[0])
        uli = int(np.where(bins == upper_limit)[0])
        no_in_range = np.sum(n[lli:uli+1])
        
        n_tot = len(effmass)

        # p is AKA Efficiency
        p = no_in_range/len(effmass)
        p_sigma = np.sqrt(n_tot * p * (1-p)) / n_tot
        
        row = [lli, uli, no_in_range, p, p_sigma]
        limits_and_errors.append(row)


lim_and_err_df = pd.DataFrame(limits_and_errors, columns=['lower','upper','no','p','p_err'])

ax.axvspan(lower_limit_range[0], upper_limit_range[0], 0, 4000, color='red', alpha=0.08)
ax.axvspan(lower_limit_range[-1], upper_limit_range[-1], 0, 4000, color='red', alpha=0.08)


ax.vlines(lower_limit_range[0], 0, 4000, linestyles='dashed')
ax.vlines(upper_limit_range[-1], 0, 4000, linestyles='dashed')


x_label_1 =  "$\\bar{x}$" + f"={x_bar:.6}"
x_label_2 =  f"Fitted Crystal Ball Function \n $\\alpha$ = {alpha:.6} \n n = {n_crystal:.6} \n $\\sigma$ = {sigma:.6} \n " + x_label_1
ax.plot(bins + 0.5, crystal_ball_vec_self(bins, *popt_crystal), label = x_label_2, color="hotpink")
ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
ax.set_ylabel("Count")
ax.set_title("Histogram of MC Higgs data with Crystal Ball Function")
ax.legend()
plt.show()
