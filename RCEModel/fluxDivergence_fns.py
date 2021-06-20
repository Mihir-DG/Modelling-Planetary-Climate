import numpy as np
import climt

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