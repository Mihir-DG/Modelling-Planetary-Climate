import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units

def setup():
  surface_temp = 300.
  radiation_lw = climt.GrayLongwaveRadiation()
  grid_state = climt.get_grid(p_toa_in_Pa=0.1)
  state = climt.get_default_state([radiation_lw], grid_state=grid_state)  
  state['surface_temperature'].values[:] = surface_temp
  state['air_temperature'].values = calc.dry_lapse(state['air_pressure'], state['surface_temperature'] - 0.1)
  max_tau = 15 #tauInfinity
  linear = 0.1
  optical_depth = climt.Frierson06LongwaveOpticalDepth(longwave_optical_depth_at_equator=max_tau, linear_optical_depth_parameter=linear)
  state.update(optical_depth(state))  
  opticalDepth_verticalCoord = list(np.array(state['longwave_optical_depth_on_interface_levels']).flatten())
  airPressure_verticalCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
  airPressure_verticalCoord = [x/1000 for x in airPressure_verticalCoord]
  return airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear