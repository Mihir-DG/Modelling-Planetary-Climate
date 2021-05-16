import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *

state, airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def netFlux():
  radiation_lw = climt.GrayLongwaveRadiation()
  optical_depth = climt.Frierson06LongwaveOpticalDepth(
        longwave_optical_depth_at_equator=max_tau,
        linear_optical_depth_parameter=linear)
  state.update(optical_depth(state))
  tend, diag = radiation_lw(state)
  upFlux = np.array(diag['upwelling_longwave_flux_in_air']).flatten()
  downFlux = np.array(diag['downwelling_longwave_flux_in_air']).flatten()
  net = upFlux - downFlux
  return net
