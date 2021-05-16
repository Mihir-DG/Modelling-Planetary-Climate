import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *

state, airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def OLR(maxTau):
  optical_depth = climt.Frierson06LongwaveOpticalDepth(
        longwave_optical_depth_at_equator=maxTau,
        linear_optical_depth_parameter=linear)
  state.update(optical_depth(state))
  opticalDepth_verticalCoord = np.array(state['longwave_optical_depth_on_interface_levels'])
  radiation_lw = climt.GrayLongwaveRadiation()
  tend, diag = radiation_lw(state)
  upFlux = np.array(diag['upwelling_longwave_flux_in_air']).flatten()
  olr_sum = 0
  sb_const = 5.67e-08
  surfTemp = (np.array(state['surface_temperature']).flatten())[0]
  surfBlackbody = sb_const * (surfTemp**4)
  olr_sum += surfBlackbody * math.exp(-maxTau)
  for i in range(29):
    olr_sum += upFlux[i] * math.exp(opticalDepth_verticalCoord[i]-maxTau)
  return olr_sum
