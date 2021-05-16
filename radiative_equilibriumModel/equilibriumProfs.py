import csv
from matplotlib import pyplot as plt 
import numpy as np

dataArr = []
with open('output_runModel/equilibrium.csv', 'r') as equilibriumFile:
	csvRead = csv.reader(equilibriumFile)
	for row in csvRead:
		dataArr.append(row)

dataArr =  [ele for ele in dataArr if ele != []] 
lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = dataArr[0],dataArr[1],dataArr[2], dataArr[3], dataArr[4]
timeTaken = ''.join(dataArr[5])

# Plotting flux divergence (h)
fig = plt.figure()
lwFluxNet = [float(i) for i in lwFluxNet]
plt.plot(lwFluxNet,range(29))
plt.xlabel("Net longwave radiative flux (Wm^-2)")
plt.ylabel("Altitude (Interface Levels)")
plt.savefig("../../../graphs_modelling/1dradiative-eq/equilibrium_netFlux_vertical.png")

# Plotting upwelling longwave flux (p)
fig = plt.figure()
lwFluxUp = [float(i) for i in lwFluxUp]
plt.plot(lwFluxUp,range(29))
plt.xlabel("Upwelling longwave radiative flux (Wm^-2)")
plt.ylabel("Altitude (Interface Levels)")
plt.savefig("../../../graphs_modelling/1dradiative-eq/equilibrium_upFlux_vertical.png")

# Plotting downwelling longwave flux (p)
fig = plt.figure()
lwFluxDown = [float(i) for i in lwFluxDown]
plt.xlabel("Downwelling longwave radiative flux (Wm^-2)")
plt.ylabel("Altitude (Interface Levels)")
plt.plot(lwFluxDown,range(29))
plt.savefig("../../../graphs_modelling/1dradiative-eq/equilibrium_downFlux_vertical.png")

# Plotting heating rate (p)
fig = plt.figure()
heatRate = [float(i) for i in heatRate]
plt.xlabel("Longwave Heating Rate")
plt.ylabel("Altitude (Interface Levels)")
plt.plot(heatRate,range(29))
plt.savefig("../../../graphs_modelling/1dradiative-eq/equilibrium_heatRate_vertical.png")

fig = plt.figure()
airTemperatureProf = [float(i) for i in airTemperatureProf]
plt.xlabel("Air Temperature (K)")
plt.ylabel("Altitude (Interface Levels)")
plt.plot(airTemperatureProf,range(28))
plt.savefig("../../../graphs_modelling/1dradiative-eq/equilibrium_airT_vertical.png")
