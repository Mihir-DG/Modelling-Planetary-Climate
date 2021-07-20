# EQUILIBRIUM PROFILES
import numpy as np
import csv
from matplotlib import pyplot as plt

def eqProfs(state):
	#Compiling CSV data into independent variables
	dataArr = []
	with open('output_runModel/equilibrium.csv', 'r') as equilibriumFile:
		csvRead = csv.reader(equilibriumFile)
		for row in csvRead:
			dataArr.append(row)
	dataArr =  [ele for ele in dataArr if ele != []] 
	lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = dataArr[0],dataArr[1],dataArr[2], dataArr[3], dataArr[4]
	timeTaken = ''.join(dataArr[5])

	airPressure_vCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
	airPressure_vCoord = [round((float(ele)/1000),0) for ele in airPressure_vCoord]
	
	# Plotting Schwarzchild deltas.
	fig = plt.figure()
	lwFluxNet = [float(i) for i in lwFluxNet]
	plt.plot(lwFluxNet,airPressure_vCoord)
	plt.gca().invert_yaxis()
	plt.xlabel("Net longwave radiative flux (Wm^-2)")
	plt.ylabel("Pressure (kPa)")
	plt.savefig("graphs/equilibrium_netFlux_vertical.png")
	
	# Plotting upwelling longwave flux (p)
	fig = plt.figure()
	lwFluxUp = [float(i) for i in lwFluxUp]
	plt.gca().invert_yaxis()
	plt.plot(lwFluxUp, airPressure_vCoord)
	plt.xlabel("Upwelling longwave radiative flux (Wm^-2)")
	plt.ylabel("Pressure (kPa)")
	plt.savefig("graphs/equilibrium_upFlux_vertical.png")

	# Plotting downwelling longwave flux (p)
	fig = plt.figure()
	lwFluxDown = [float(i) for i in lwFluxDown]
	plt.xlabel("Downwelling longwave radiative flux (Wm^-2)")
	plt.ylabel("Pressure (kPa)")
	plt.gca().invert_yaxis()
	plt.plot(lwFluxDown,airPressure_vCoord)
	plt.savefig("graphs/equilibrium_downFlux_vertical.png")

	# Plotting heating rate (p)
	fig = plt.figure()
	heatRate = [float(i) for i in heatRate]
	plt.xlabel("Longwave Heating Rate")
	plt.ylabel("Pressure (kPa)")
	plt.gca().invert_yaxis()
	plt.plot(heatRate,airPressure_vCoord)
	plt.savefig("graphs/equilibrium_heatRate_vertical.png")

	fig = plt.figure()
	airTemperatureProf = [float(i) for i in airTemperatureProf]
	plt.xlabel("Air Temperature (K)")
	plt.ylabel("Pressure (kPa)")
	plt.gca().invert_yaxis()
	plt.plot(airTemperatureProf,airPressure_vCoord[:28])
	plt.savefig("graphs//equilibrium_airT_vertical.png")

	return 0.