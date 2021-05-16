import climt
import matplotlib.pyplot as plt
import numpy as np
import math
import metpy.calc as calc
from metpy.units import units
from setup import *
from olr import *

state, airPressure_verticalCoord, opticalDepth_verticalCoord, max_tau, linear = setup()

def exp_tauDoubled_onOLR(tauInit,tauFin):
  tauList = []
  olrSum_list = []
  tauList.append(tauInit)
  while tauList[-1] < tauFin:
    tauList.append(tauList[-1]*2)
  for i in tauList:
    olrSum_list.append(OLR(i))
  return olrSum_list,tauList

olrSums, taus = exp_tauDoubled_onOLR(0.05,100)[0],exp_tauDoubled_onOLR(0.05,100)[1]
olrDiffs = []
for i in range(1,len(olrSums)):
  olrDiffs.append(olrSums[i]-olrSums[i-1])

plt.plot(olrDiffs)
