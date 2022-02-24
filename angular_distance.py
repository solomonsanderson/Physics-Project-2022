# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 16:39:55 2022

@author: sam-j
"""

'''
COMPARE DELTA R CODE
'''

import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt 


dimuon = "C:/Users/sam-j/Documents/uob/y2/sem2/project/real-dimuon-400k.data"
Z0 = "C:/Users/sam-j/Documents/uob/y2/sem2/project/MC-Z0.data"

data_dm = pd.read_csv(dimuon, delim_whitespace = True , header=None)
data_Z0 = pd.read_csv(Z0, delim_whitespace = True , header=None)


eta_1_dm, eta_2_dm = data_dm[2], data_dm[5]
phi_1_dm, phi_2_dm = data_dm[1], data_dm[4]

eta_1_Z0, eta_2_Z0 = data_Z0[2], data_Z0[5]
phi_1_Z0, phi_2_Z0 = data_Z0[1], data_Z0[4]

delta_r_dm = np.sqrt( np.square(eta_1_dm - eta_2_dm) + np.square(phi_1_dm - phi_2_dm) )
delta_r_Z0 = np.sqrt( np.square(eta_1_Z0 - eta_2_Z0) + np.square(phi_1_Z0 - phi_2_Z0) )


# =============================================================================
# # Histogram
# =============================================================================
plt.figure(figsize=[9,9])

n_dm, bins_dm, patches_dm = plt.hist(delta_r_dm, bins=100, density=True, alpha=0.5, label='Real Dimuon Decay Data')
n_Z0, bins_Z0, patches_Z0 = plt.hist(delta_r_Z0, bins=100, density=True, alpha=0.5, label='Simulated Z0 Decays')

plt.title('Simulated and real Data Angular distance Histogram')
plt.xlabel('Angular separation')
plt.ylabel('Count (normalised)')


plt.legend()

plt.show()



# =============================================================================
# # Line graph
# =============================================================================
plt.figure(figsize=[9,9])

plt.plot(bins_dm[:-1], n_dm, label='Real Dimuon Decay Data')
plt.plot(bins_Z0[:-1], n_Z0, label='Simulated Z0 Decays')

plt.title('Simulated and real Data Angular distance Trendlines')
plt.xlabel('Angular separation')
plt.ylabel('Count (normalised)')

plt.legend()
plt.show()




# =============================================================================
# # Polar
# =============================================================================
plt.figure(figsize=[9,9])

plt.polar(bins_dm[:-1], n_dm, label='Real Dimuon Decay Data')
plt.polar(bins_Z0[:-1], n_Z0, label='Simulated Z0 Decays')

plt.title('Simulated and real Data Angular distance Trendlines')
plt.xlabel('Angular separation')
plt.ylabel('Count (normalised)')

plt.legend()
plt.show()



