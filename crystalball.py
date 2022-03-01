'''Plots higgs data and fits the crystal ball function'''


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import quad
from load import load_data


path = r"Code\data\higgs.data"

effmass = load_data(path)[6]
fig, ax = plt.subplots()


n, bins, patches = ax.hist(effmass, bins = 100, range = [40,140], density=True, alpha=0.3, label="MC Higgs")


def integrand(x):
    '''integrand for error_func'''

    integrand = (1/np.sqrt(np.pi)) * np.exp(-x**2)
    return integrand


def error_func(z):
    '''Error function used for calculating D in crystal ball function
    https://en.wikipedia.org/wiki/Error_function'''

    integral = quad(integrand, 0, z)
    return integral


def crystal_ball(x, alpha, n, x_bar, sigma):
    '''Crystal ball function: https://en.wikipedia.org/wiki/Crystal_Ball_function'''

    
    A = (n/np.abs(alpha))**n * np.exp(-(np.abs(alpha)**2) / 2)
    B = n / np.abs(alpha) - np.abs(alpha)
    C = (n/np.abs(alpha)) * (1/(n-1)) * np.exp(-(np.abs(alpha)**2)/2)
    D = np.sqrt(np.pi/2) * (1 + error_func(np.abs(alpha)/np.sqrt(2))[0])
    N = 1/(sigma*(C+D))

    # print(f'A:{A}, B:{B}, C:{C}, D:{D}, N:{N}')


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

def crystal_ball_vec_self(x,  alpha, n, x_bar, sigma):
    y = np.zeros(x.shape)
    for i in range(len(y)):
        y[i] = crystal_ball(x[i], alpha, n, x_bar, sigma)
    return y


popt_crystal, pcov_crystal = curve_fit(crystal_ball_vec, bins[:-1], n, maxfev = 800, p0 = [1,2,125,1])
alpha, n, x_bar, sigma = popt_crystal

x_label_1 =  "$\\bar{x}$" + f"={x_bar:.6}"
x_label_2 =  f"Fitted Crystal Ball Function \n $\\alpha$ = {alpha:.6} \n n = {n:.6} \n $\\sigma$ = {sigma:.6} \n " + x_label_1
ax.plot(bins + 0.5, crystal_ball_vec_self(bins, *popt_crystal), label = x_label_2, color="hotpink")
ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
ax.set_ylabel("Count")
ax.set_title("Histogram of MC Higgs data with Crystal Ball Function")
ax.legend()
plt.show()