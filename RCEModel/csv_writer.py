import csv
import numpy as np

def output_to_csv(timeTaken, olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf):
	with open('output_runModel/weekly_results.csv', mode='w') as weeklyCSV:
		weeklyWriter = csv.writer(weeklyCSV)
		weeklyWriter.writerow(olrs)
		weeklyWriter.writerow((np.array(bdry_tempDiff)).flatten())
		weeklyWriter.writerow(surfT)
		weeklyWriter.writerow(netEn)
	
	with open('output_runModel/equilibrium.csv', mode='w') as equilibriumCSV:
		equilibriumWriter = csv.writer(equilibriumCSV)
		equilibriumWriter.writerow(lwFluxNet)
		equilibriumWriter.writerow(lwFluxUp)
		equilibriumWriter.writerow(lwFluxDown)
		equilibriumWriter.writerow(heatRate)
		equilibriumWriter.writerow(airTemperatureProf)
		equilibriumWriter.writerow(str(timeTaken))
	
	return 0.