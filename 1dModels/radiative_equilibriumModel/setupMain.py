import climt
import sympl
from sympl import AdamsBashforth
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
import datetime

#Ex 1: Difference b/w surface temperature and first model level.
def surf_airBdry_tempDiff(state):
  return (state['surface_temperature'] - state['air_temperature'])[0][0][0]

#Ex 2: Define and write an algorithm to find the radiating height in a model.
# Def: The pressure after which the atmos is relatively transparent to IR radiation.
# Input: Acceptable difference between flux from radiative height and last interface level. 
def radiating_pressure(state,diff_acceptable):
	upFlux = np.array(state['upwelling_longwave_flux_in_air']).flatten()
	int_level = 0
	for i in range(1,29):
		if abs(upFlux[i]-upFlux[i-1]) < diff_acceptable:
			int_level = i
			break
		else:
			int_level = 29
	return (np.array(state['air_pressure_on_interface_levels']).flatten())[int_level],int_level

def net_energy_level_in_column(state,diff_acceptable):
	radPres = radiating_pressure(state,diff_acceptable)
	radHt = radPres[1]
	sb_const = 5.67e-08
	lw_up_ntat_OUT = (np.array(state['upwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_up_surf_IN = sb_const * (((np.array(state['surface_temperature']).flatten())[0])**4)
	lw_down_ntat_IN = (np.array(state['downwelling_longwave_flux_in_air']).flatten())[radHt]
	lw_down_surf_OUT = (np.array(state['downwelling_longwave_flux_in_air']).flatten())[0]
	otherSurfFluxes_IN = (np.array(state['surface_upward_latent_heat_flux'] + state['surface_upward_sensible_heat_flux']).flatten())[0]
	sw_up_ntat_OUT = (np.array(state['upwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_up_surf_IN = (np.array(state['upwelling_shortwave_flux_in_air']).flatten())[0]
	sw_down_ntat_IN = (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[radHt]
	sw_down_surf_OUT = (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[0]
	#sw_up_surf_reflected_IN = albedo * (np.array(state['downwelling_shortwave_flux_in_air']).flatten())[0]
	fluxesIn = [lw_up_surf_IN,lw_down_ntat_IN,otherSurfFluxes_IN,sw_up_surf_IN,sw_down_ntat_IN]#,sw_up_surf_reflected_IN]
	fluxesOut = [lw_up_ntat_OUT,lw_down_surf_OUT,sw_up_ntat_OUT,sw_down_surf_OUT]
	netEn = sum(fluxesIn) - sum(fluxesOut)
	return netEn,fluxesIn,fluxesOut

def netFlux(state):
	radiation_lw = climt.GrayLongwaveRadiation(tendencies_in_diagnostics=True)
	tend, diag = radiation_lw(state)
	upFlux = np.array(diag['upwelling_longwave_flux_in_air']).flatten()
	downFlux = np.array(diag['downwelling_longwave_flux_in_air']).flatten()
	net = upFlux - downFlux
	return net,upFlux,downFlux

def heatingRate(state):
  tau = np.array(state['longwave_optical_depth_on_interface_levels']).flatten()
  airPressure_verticalCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
  net = (netFlux(state))[0]
  dNet = np.gradient(net)
  dNet = np.array(dNet).flatten()
  dtau = np.gradient(tau)
  dp = np.gradient(airPressure_verticalCoord)
  return np.array(dNet/dp)

