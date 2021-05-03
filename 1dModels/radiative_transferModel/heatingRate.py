import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *

airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def heatingRate():
  tau = np.array(state['longwave_optical_depth_on_interface_levels']).flatten()
  net = netFlux()
  dNet = np.gradient(net)
  dtau = np.gradient(tau)
  dp = np.gradient(airPressure_verticalCoord)
  return dNet/dp

"""
plt.plot(heatingRate(),airPressure_verticalCoord)
plt.gca().invert_yaxis()
plt.xlabel("Heating Rate")
plt.ylabel("Pressure (kPa)")
"""