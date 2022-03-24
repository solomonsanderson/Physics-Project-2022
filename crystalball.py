'''Plots higgs data and fits the crystal ball function'''


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.integrate import quad
from sympy import N
from load import load_data
from scipy.stats import crystalball, chisquare


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
    # C = (n/np.abs(alpha)) * (1/(n-1)) * np.exp(-(np.abs(alpha)**2)/2)
    # D = np.sqrt(np.pi/2) * (1 + error_func(np.abs(alpha)/np.sqrt(2))[0])
    # N = 1/(sigma*(C+D))
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

def crystal_ball_vec_self(x,  alpha, n, x_bar, sigma, N):
    y = np.zeros(x.shape)
    for i in range(len(y)):
        y[i] = crystal_ball(x[i], alpha, n, x_bar, sigma, N)
    return y


if __name__ == "__main__":
    path = r"Code\data\higgs.data"
    effmass = load_data(path)[6]
    fig, ax = plt.subplots() 
    
    
    n, bins, patches = ax.hist(effmass, bins = 500, range = [110,140], density=False, alpha=0.3, label="MC Higgs")
    p0 = [1,1.2,124,1, 10000]
    popt_crystal, pcov_crystal = curve_fit(crystal_ball_vec, bins[:-1], n, p0, maxfev = 10000,)
    chisq_test_stats = chisquare(n, crystal_ball_vec(bins, *popt_crystal)[:-1])
    alpha, n, x_bar, sigma, N = popt_crystal
    perr = np.sqrt(np.diag(pcov_crystal))
    x_label_1 =  "$\\bar{x}$" + f"={x_bar:.6}$\pm${perr[2]:.3}"
    x_label_2 =  f"Fitted Crystal Ball Function \n $\\alpha$ = {alpha:.6}$\pm${perr[0]:.3} \n n = {n:.6}$\pm${perr[1]:.3} \n $\\sigma$ = {sigma:.6}$\pm${perr[3]:.3} \n N = {N:.6}$\pm${perr[4]:.3} \n " + x_label_1 + "\n $\chi^2$ = {chisq_test_stats[0]:.3f}\np-value = {chisq_test_stats[1]:.3f}"
    ax.plot(bins, crystal_ball_vec_self(bins-0.2 , *popt_crystal), label = x_label_2, color="hotpink")
    ax.set_xlabel("Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)")
    ax.set_ylabel("Count")
    ax.set_title("Histogram of MC Higgs data with Crystal Ball Function")

    ax.legend()
    plt.show()