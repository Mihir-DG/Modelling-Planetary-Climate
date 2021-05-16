import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *

state, airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def tauPressure_var_maxTau():
  depth_list = []
  ind_list = []
  max_tau_list = np.arange(0, 200, 40)
  for max_tau in max_tau_list:
    optical_depth = climt.Frierson06LongwaveOpticalDepth(longwave_optical_depth_at_equator=max_tau,linear_optical_depth_parameter=linear)
    state.update(optical_depth(state))
    depth_list.append(np.array(state['longwave_optical_depth_on_interface_levels']).flatten())
    ind_list.append(str(max_tau))
  y = list(np.array(state['air_pressure_on_interface_levels']).flatten())
  y2 = [x/1000 for x in y]
  for i in range(len(depth_list)):
    x = depth_list[i]
    l = ind_list[i]
    plt.xlabel("Longwave Optical Thickness ("+r'$\tau$'+")")
    plt.ylabel("Pressure (kPa)")
    plt.title("Variation of Longwave Optical Depth Profiles With " + r'$\tau_\infty$')
    plt.gca().invert_yaxis()
    plt.plot(x,y2,label = (r'$\tau_\infty$' + " = "+l))
    plt.legend()
 return 0