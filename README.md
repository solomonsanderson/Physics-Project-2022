# Physics Project 2022
## [Solomon Sanderson](https://github.com/solomonsanderson) & [Samuel de Gorrequer Griffith](https://github.com/samdgg)
Collaborative project to find the Higgs Boson from muon muon decay in ATLAS data

## Data
### Data Structure 
Each line of the data file contains 7 columns:
1. Transverse momentum p<sub>T</sub> of the first muon
2. Azimuthal angle of the first muon 
3. The pseudo-rapidity of the first muon
4. Transverse moment p<sub>T</sub> of the second muon
5. Azimuthal angle of the second muon 
6. The pseudo-rapidity of the second muon
7. The effective mass of the dimuon system

### Data Files
* higgs.data: Monte-Carlo data for the Higgs Boson
* MC-Z0.data: Monte-Carlo data for the Z Boson
* real-dimuon-4M.data: Real data containing 4 million dimuon events from ATLAS at the CERN LHC
* real-dimuon-400k.data: Real data containing 400,000 dimuon events from ATLAS at the CERN LHC
* real-dimuon-small-1.data: Real data containing 1000 dimuon events from ATLAS at the CERN LHC

## Code
* load.py: loads data files and returns a pandas dataframe
* plot.py: plots the input data in a histogram
* crystalball.py: plots a histogram of input data and fits aa crystal ball function
* fit_higgs.py: plots a histogram of higgs.data and fits a voigt curve
* fit_MCZ0.py: plots a histogram of MC-Z0.data, fits a voigt curve and a power law curve
* angular_distance.py: 
* Z0_processing.py: Takes the ratio of the real dimuon data and the MC-Z0 data to remove the background from the Z0
