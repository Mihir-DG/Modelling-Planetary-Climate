import csv
from matplotlib import pyplot as plt 
import numpy as np

dataArr = []
with open('output_runModel/equilibrium.csv', 'r') as equilibriumFile:
	csvRead = csv.reader(equilibriumFile)
	for row in csvRead:
		dataArr.append(row)

dataArr =  [ele for ele in dataArr if ele != []] 
lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf, airPressure_vertCoord = dataArr[0],dataArr[1],dataArr[2], dataArr[3], dataArr[4], dataArr[6]
airPressure_vertCoord = [round((float(ele)/1000),0) for ele in airPressure_vertCoord]
timeTaken = ''.join(dataArr[5])
print(airPressure_vertCoord[:28])

# Plotting flux divergence (h)
fig = plt.figure()
lwFluxNet = [float(i) for i in lwFluxNet]
plt.plot(lwFluxNet,airPressure_vertCoord)
plt.gca().invert_yaxis()
plt.xlabel("Net longwave radiative flux (Wm^-2)")
plt.ylabel("Pressure (kPa)")
plt.savefig("graphs/equilibrium_netFlux_vertical.png")

# Plotting upwelling longwave flux (p)
fig = plt.figure()
lwFluxUp = [float(i) for i in lwFluxUp]
plt.plot(lwFluxUp,airPressure_vertCoord)
plt.gca().invert_yaxis()
plt.xlabel("Upwelling longwave radiative flux (Wm^-2)")
plt.ylabel("Pressure (kPa)")
plt.savefig("graphs/equilibrium_upFlux_vertical.png")

# Plotting downwelling longwave flux (p)
fig = plt.figure()
lwFluxDown = [float(i) for i in lwFluxDown]
plt.xlabel("Downwelling longwave radiative flux (Wm^-2)")
plt.ylabel("Pressure (kPa)")
plt.gca().invert_yaxis()
plt.plot(lwFluxDown,airPressure_vertCoord)
plt.savefig("graphs/equilibrium_downFlux_vertical.png")

# Plotting heating rate (p)
fig = plt.figure()
heatRate = [float(i) for i in heatRate]
plt.xlabel("Longwave Heating Rate")
plt.ylabel("Pressure (kPa)")
plt.gca().invert_yaxis()
plt.plot(heatRate,airPressure_vertCoord)
plt.savefig("graphs/equilibrium_heatRate_vertical.png")

fig = plt.figure()
airTemperatureProf = [float(i) for i in airTemperatureProf]
plt.xlabel("Air Temperature (K)")
plt.ylabel("Pressure (kPa)")
plt.gca().invert_yaxis()
plt.plot(airTemperatureProf,airPressure_vertCoord[:28])
plt.savefig("graphs/equilibrium_airT_vertical.png")
