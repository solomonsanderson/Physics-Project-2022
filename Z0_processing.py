'''
Code to remove the Z0 monte carlo data from the dimuon mass data
'''

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 


dimuon = r"Code\data\real-dimuon-400k.data"
Z0 = r"Code\data\MC-Z0.data"

data_dm = pd.read_csv(dimuon, delim_whitespace = True , header=None)
effmass_dm = data_dm[6]

data_Z0 = pd.read_csv(Z0, delim_whitespace = True , header=None)
effmass_Z0 = data_Z0[6]

n_dm, bins_dm, patches_dm = plt.hist(effmass_dm, bins = 100, range = [40,140], density=True, alpha=0.3)
n_Z0, bins_Z0, patches_Z0 = plt.hist(effmass_Z0, bins = 100, range = [40,140], density=True, alpha=0.3)

plt.title('Invariant mass plot for $\mu^{+} \mu^{-}$')
plt.xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 1 GeV/c$^{2}$')


diff = n_dm - n_Z0

fig, ax = plt.subplots()

# ax.hist(diff, bins=100, density = True)
ax.bar(bins_dm[:-1], diff, width=1)
print(diff)

plt.show()