'''
Program to plot data files
'''

import matplotlib.pyplot as plt
from load import load_data


filename = r"Code\data\real-dimuon-4m.data"
effmass = load_data(filename)[6]
plt.hist(effmass, bins = 500, range = [40,140])
plt.title('Invariant mass plot for $\mu^{+} \mu^{-}$')
plt.xlabel('Invariant $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 1 GeV/c$^{2}$')
# plt.savefig('effmass.pdf')
plt.show()
