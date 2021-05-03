import sympl
from matplotlib import pyplot as plt
import numpy as np
import climt
from datetime import timedelta

radiation1 = climt.GrayLongwaveRadiation()
grid = climt.get_grid(nx=None,ny=None,nz=0)
timeStep = timedelta(hours=1)

state = climt.get_default_state([radiation1],grid_state=grid)
time_stepper = sympl.AdamsBashforth([radiation1])

out = []
out.append(state['surface_temperature'])

for step in range(10):
  diagnostics, new_state = time_stepper(state, timeStep)
  state.update(diagnostics)
  state.update(new_state)
  state['time'] += timeStep
  out.append(state['surface_temperature'])

# Albedo vs emissivity
upFlux = diagnostics['upwelling_longwave_flux_in_air'][0][0]
x = np.linspace(0,1,100)
y = 1-((4*upFlux)/1376.6)*x
plt.ylabel('Albedo')
plt.xlabel('Epsilon (Emissivity)')
plt.plot(x,y)
plt.savefig("epsilonValbedo.png")

# Temperature vs emissivity
phi = 5.68*10**-8
x = np.linspace(0,1,100)
t = (1376*(1-0.33)/(4 * phi * x))**0.25
plt.xlabel("Epsilon (Emissivity)")
plt.ylabel("Temperature (K)")
plt.plot(x,t)

#Temperature vs albedo
phi = 5.68*10**-8
x = np.linspace(0,1,100)
t = ((1376*(1-x))/(4*phi*0.5244))**0.25
plt.xlabel("Albedo")
plt.ylabel("Temperature (K)")
plt.plot(x,t)
