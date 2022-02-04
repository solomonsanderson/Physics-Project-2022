# import numpy as np
import matplotlib.pyplot as plt

# f = open('higgs.data', 'r')
f = open(r"Code\data\real-dimuon-400k.data", 'r')
# with open('real-dimuon-small.data', 'r') as f:

effmass = []
counter=0
for line in f:
    line = line.strip()
    try:
        columns = [float(s) for s in line.split()]
        effmass.append(columns[6])

#        print(("effective mass", effmass)[counter<3])
        counter+=1
    except: continue
f.close()
plt.hist(effmass, bins = 100, range = [40,140])
plt.title('Effective mass plot for $\mu^{+} \mu^{-}$')
plt.xlabel('Effective $\mu^{+} \mu^{-}$ mass (GeV/c$^{2}$)')
plt.ylabel('No. of Events / 1 GeV/c$^{2}$')
plt.savefig('effmass.pdf')
plt.show()
#plt.hist2d(ximass, v0mass, bins = 100)
#plt.show()
