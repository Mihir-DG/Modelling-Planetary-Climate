import climt
import sympl
from sympl import AdamsBashforth
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
import datetime
import csv
#Importing setup functions for profile development.
from setupMain import surf_airBdry_tempDiff, radiating_pressure, net_energy_level_in_column, netFlux, heatingRate

#Runs model to equilibrium ~ 260 days.
# Uses net energy in atm. column as stopping criteria.

def runningModel():
	#Setting up system components in disequilbrium.
	diagnostic = climt.Frierson06LongwaveOpticalDepth(linear_optical_depth_parameter=0.1)
	radiation = climt.GrayLongwaveRadiation(tendencies_in_diagnostics=True)
	surface = climt.SlabSurface()
	albedo = 0.3
	time_stepper = AdamsBashforth([radiation,surface])
	timestep = datetime.timedelta(hours = 4)
	state = climt.get_default_state([radiation, diagnostic, surface])
	sw_flux = 200
	state['downwelling_shortwave_flux_in_air'][:] = sw_flux
	state['ocean_mixed_layer_thickness'][:] = 1.
	state['air_temperature'][:] = 200. #Arbitrary init value
	diff_acceptable = 5.
	time = datetime.datetime(2020,1,1,0,0,0) # In months (Add 1/168 for each timedelta jump)
	stop = False
	radPres = radiating_pressure(state,diff_acceptable)
	radHt = radPres[1]
	#Creates list for assorted 0d output vars.
	netEn = [(net_energy_level_in_column(state,diff_acceptable))[0]]
	bdry_tempDiff = [surf_airBdry_tempDiff(state)]
	olrs = [(np.array(state['upwelling_longwave_flux_in_air']).flatten())[radHt]]
	surfT = [(np.array(state['surface_temperature']).flatten())[0]]
	counter = 0
	#Loop to increment time
	while stop == False:
		#Updating state
		state.update(diagnostic(state))
		diagnostics, state = time_stepper(state,timestep)
		state.update(diagnostics)
		#Updating appropriate quantities every month
		if counter % 42 == 0:
			netEn.append((net_energy_level_in_column(state,diff_acceptable))[0])
			bdry_tempDiff.append(surf_airBdry_tempDiff(state))
			olrs.append((np.array(state['upwelling_longwave_flux_in_air']).flatten())[radHt])
			surfT.append((np.array(state['surface_temperature']).flatten())[0])
		# Checks breakout condition and increments time + counter.
		counter += 1
		time = time + timestep
		if abs(net_energy_level_in_column(state,diff_acceptable)[0]) < 0.5:
			stop = True
	#Calculating output quantities.
	timeTaken = time - datetime.datetime(2020,1,1,0,0,0)
	lwFluxNet, lwFluxUp, lwFluxDown = netFlux(state)
	heatRate = heatingRate(state)
	airTemperatureProf = (np.array(state['air_temperature'])).flatten()
	return timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf

def output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf):
	with open('output_runModel/weekly_results.csv', mode='w') as weeklyCSV:
		weeklyWriter = csv.writer(weeklyCSV)
		weeklyWriter.writerow(olrs)
		weeklyWriter.writerow((np.array(bdry_tempDiff)).flatten())
		weeklyWriter.writerow(surfT)
		weeklyWriter.writerow(netEn)
	with open('output_runModel/equilibrium.csv', mode='w') as equilibriumCSV:
		equilibriumWriter = csv.writer(equilibriumCSV)
		equilibriumWriter.writerow(lwFluxNet)
		equilibriumWriter.writerow(lwFluxUp)
		equilibriumWriter.writerow(lwFluxDown)
		equilibriumWriter.writerow(heatRate)
		equilibriumWriter.writerow(airTemperatureProf)
		equilibriumWriter.writerow(str(timeTaken))
	return 0.

# runningModel() calls first 3 fns; does not need to be called in main() for runningModel()	
def main():
	 timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = runningModel()
	 output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf)

if __name__ == '__main__':
	main()
# NOTE: DIFF ACCEPTABLE SET TO 5.

"""
Required outs from runningModel():
	1) olr - historical
	2) bdry_tempDiff - historical
	3) net Energy level in atm. - historical
	4) surface temp. - historical
	5) upFlux - eq.
	6) downFlux - eq.
	7) netFlux - eq.
	8) heating rate - eq.
	9) air temp (p) - eq.
	10) opticalDepth (p) - eq. --> MAYBE!!
	11) equilibrium time
"""