import climt
import matplotlib.pyplot as plt
import numpy as np
import metpy.calc as calc
from metpy.units import units

surface_temp = 300.
radiation_lw = climt.GrayLongwaveRadiation()
grid_state = climt.get_grid(p_toa_in_Pa=0.1)
state = climt.get_default_state([radiation_lw], grid_state=grid_state) 

state['surface_temperature'].values[:] = surface_temp
state['air_temperature'].values = calc.dry_lapse(state['air_pressure'], 
                                                 state['surface_temperature'] - 0.1)
max_tau = 15
linear = 0.1

optical_depth = climt.Frierson06LongwaveOpticalDepth(
        longwave_optical_depth_at_equator=max_tau,
        linear_optical_depth_parameter=linear)
state.update(optical_depth(state))  

opticalDepth_verticalCoord = list(np.array(state['longwave_optical_depth_on_interface_levels']).flatten())
airPressure_verticalCoord = np.array(state['air_pressure_on_interface_levels']).flatten()
airPressure_verticalCoord = [x/1000 for x in airPressure_verticalCoord]

def flux_maxTau():
  flux_list = []
  max_tau_list = np.arange(2, 400, 10)
  for max_tau in max_tau_list:
    optical_depth = climt.Frierson06LongwaveOpticalDepth(longwave_optical_depth_at_equator=max_tau,linear_optical_depth_parameter=linear)
    state.update(optical_depth(state))
    tend, diag = radiation_lw(state)
    flux = diag['upwelling_longwave_flux_in_air'] #- diag['downwelling_longwave_flux_in_air']
    flux_list.append(flux)
  return flux_list

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
    
def tauPressure_var_linear():
  depth_list = []
  ind_list = []
  lin_list = list(np.arange(0.2,1.6,0.4,dtype=list))
  lin_list = np.around(lin_list,2)
  for lin in lin_list:
    optical_depth = climt.Frierson06LongwaveOpticalDepth(longwave_optical_depth_at_equator=max_tau,linear_optical_depth_parameter=lin)
    state.update(optical_depth(state))
    depth_list.append(np.array(state['longwave_optical_depth_on_interface_levels']).flatten())
    ind_list.append(str(lin))
  y = list(np.array(state['air_pressure_on_interface_levels']).flatten())
  y2 = [x/1000 for x in y]
  for i in range(len(depth_list)):
    x = depth_list[i]
    l = ind_list[i]
    plt.xlabel("Longwave Optical Thickness ("+r'$\tau$'+")")
    plt.ylabel("Pressure (kPa)")
    plt.title("Variation of Longwave Optical Depth Profiles With Linear Value")
    plt.gca().invert_yaxis()
    plt.plot(x,y2,label = l)
    plt.legend()

def netFlux(maxTau, linear):
  optical_depth = climt.Frierson06LongwaveOpticalDepth(
        longwave_optical_depth_at_equator=max_tau,
        linear_optical_depth_parameter=linear)
  state.update(optical_depth(state))
  tend, diag = radiation_lw(state)
  upFlux = np.array(diag['upwelling_longwave_flux_in_air']).flatten()
  downFlux = np.array(diag['downwelling_longwave_flux_in_air']).flatten()
  net = upFlux - downFlux
  return net

def fluxTau():
  y = list(np.array(state['longwave_optical_depth_on_interface_levels']).flatten())
  x = netFlux(120,0.1)
  plt.xlabel("Net Flux (Wm^-2)")
  plt.ylabel("Optical Depth")
  plt.plot(x,y,label="upFlux")
  return 0

def fluxPressure():
  y = list(np.array(state['air_pressure_on_interface_levels']).flatten())
  y2 = [a/1000 for a in y]
  x = netFlux(120,0.1)
  plt.xlabel("Net Flux (Wm^-2)")
  plt.ylabel("Pressure (kPa)")
  plt.plot(x,y2,label="upFlux")
  plt.gca().invert_yaxis()
  
def heatingRate(maxTau, linear):
  tau = np.array(state['longwave_optical_depth_on_interface_levels']).flatten()
  net = netFlux(maxTau,linear)
  dNet = np.gradient(net)
  dp = np.gradient(p)
  return dNet[:28]/dtau

def create_isothermal_temperature_profile():
  newTemp = np.mean(np.array(state['air_temperature']).flatten()).round(1)
  state['air_temperature'].values[:] = newTemp
  state.update()
  net = netFlux(120,0.1)
  return list(net)

def iso_netFlux_opticalDepth():
  isoNet = create_isothermal_temperature_profile()
  plt.xlabel("Net Flux")
  plt.ylabel("Optical Depth")
  plt.plot(isoNet,opticalDepth_verticalCoord)