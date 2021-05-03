import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *

state, airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def create_isothermal_temperature_profile():
  newTemp = np.mean(np.array(state['air_temperature']).flatten()).round(1)
  state['air_temperature'].values[:] = newTemp
  state.update()
  net = netFlux()
  return list(net)