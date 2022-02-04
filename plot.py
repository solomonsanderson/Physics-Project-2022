'''
Program to plot data files
'''

from email import header
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd


filename = r"Code\data\MC-Z0.data"

data = pd.read_csv(filename, delim_whitespace = True , header=None)
print(data)
effmass = data[6]
plt.hist(effmass, bins = 100, range = [40,140])
plt.title('Invariant mass plot for $\mu^{+} \mu^{-}$')
plt.xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 1 GeV/c$^{2}$')
plt.savefig('effmass.pdf')
plt.show()