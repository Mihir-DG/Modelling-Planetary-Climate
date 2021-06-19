from sympl import (
    AdamsBashforth, PlotFunctionMonitor)
from climt import (
    Frierson06LongwaveOpticalDepth, GrayLongwaveRadiation,
    SimplePhysics, DryConvectiveAdjustment, SlabSurface,
    get_default_state)
import climt
import datetime
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
	maxTau = 8
	planetary_albedo = 0.29
	cleaningUp()
	state, timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf = runningModel(maxTau, planetary_albedo)
	output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT,
		lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf)
	eqProfs(state)
	evolvingProfs(state)
	potentialTemperature_verticalProfile(state)

if __name__ == "__main__":
	main()
