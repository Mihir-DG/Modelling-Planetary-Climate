import numpy as np
from matplotlib import pyplot as plt

def get_temp_profile(eqTemp, eqPoleGradient, lats):
  return eqTemp - eqPoleGradient*(np.sin(lats)**2)

def get_weighted_average(quantity, lats):
  return np.average(quantity, weights = np.cos(latitudes))

albedo_ocean = 0.2
albedo_ice = 0.5
Ti = 250
To = 300
delta = 25
tBorder = 274
latitudes = np.linspace(-np.pi/2, np.pi/2, 180)
def get_average_albedo(eqTemp, eqPoleGradient):
  albedoList = []
  tempProfile = get_temp_profile(eqTemp, eqPoleGradient, latitudes)
  for latTemp in tempProfile:
    if latTemp < tBorder:
      albedo = albedo_ice
    else:
      albedo = albedo_ocean
    albedoList.append(albedo)
  return (get_weighted_average(tempProfile,latitudes),get_weighted_average(albedoList,latitudes))

#Looks at average albedo for mean temperatures 220K-320K

avgTemps = []
avgAlbedo = []
for i in range(220,320):
  avgTemps.append(get_average_albedo(i,delta)[0])
  avgAlbedo.append(get_average_albedo(i,delta)[1])

out = []
for i in range(220,320):
  out.append(albedo_ice - (albedo_ice - albedo_ocean)*((float(i)-Ti)/(Ti-To))**2)
plt.plot(out)