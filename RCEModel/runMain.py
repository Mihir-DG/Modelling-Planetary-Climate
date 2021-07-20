from sympl import (
    AdamsBashforth, PlotFunctionMonitor)
from climt import (
    Frierson06LongwaveOpticalDepth, GrayLongwaveRadiation,
    SimplePhysics, DryConvectiveAdjustment, SlabSurface,
    get_default_state)
import climt
import datetime
import math
import numpy as np
import sympl
from datetime import timedelta
import matplotlib.pyplot as plt
import metpy.calc as calc
import os
from metpy.units import units

# Importing functions from local pys.
from analyticFunctions import (
	surf_airBdry_tempDiff, radiating_pressure, cleaningUp)
from fluxDivergence_fns import netFlux, heatingRate
from stoppingCriteria_fn import net_energy_level_in_column
from modelTimestep import runningModel
from csv_writer import output_to_csv
from equilibriumProfiles import eqProfs
from evolutionVars import evolvingProfs
from potentialTemperatureProfiles import (
	potentialTemperature_verticalProfile)

def main():
	#maxTau = 2.8
	maxTau = 2.84
	planetary_albedo = 0.29
	cleaningUp()
	state, timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = runningModel(maxTau, planetary_albedo)
	output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT,
		lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf)
	eqProfs(state)
	evolvingProfs(state)
	potentialTemperature_verticalProfile(state)
	print(state['upwelling_longwave_flux_in_air'][-1])
	print(state['surface_temperature'])

	#output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT,
		#lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf)
	#eqProfs(state)
	#evolvingProfs(state)
	#potentialTemperature_verticalProfile(state)
	"""idealizedSurfT = 288.2
	idealizedOLR = 231.76
	RMS = []
	maxTau_ranges = np.linspace(0,6,20)
	for maxTau in maxTau_ranges:
		#planetary_albedo = 0.29
		#cleaningUp()
		state, timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = runningModel(maxTau, planetary_albedo)
		olr = np.array(state['upwelling_longwave_flux_in_air'][-1]).flatten()[0]
		surfT = np.array(state['surface_temperature']).flatten()[0]
		errorFunc = math.sqrt((idealizedOLR-olr)**2 + (idealizedSurfT-surfT)**2)
		print(errorFunc,maxT)
		RMS.append(errorFunc)
	plt.plot(RMS)
	plt.show()
	print(np.amin(RMS))"""

if __name__ == "__main__":
	main()


"""
maxTau = 2.84
	planetary_albedo = 0.29
	cleaningUp()
	state, timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = runningModel(maxTau, planetary_albedo)
	output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT,
		lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf)
	eqProfs(state)
	evolvingProfs(state)
	potentialTemperature_verticalProfile(state)
	"""