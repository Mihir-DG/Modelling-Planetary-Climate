#monitor = PlotFunctionMonitor(plot_function)
def runningModel():
  maxTau = 8.
  albedo = 0.3
  # Initialize components
  diagnostic = Frierson06LongwaveOpticalDepth(linear_optical_depth_parameter=.1, longwave_optical_depth_at_equator=maxTau)
  radiation = GrayLongwaveRadiation(tendencies_in_diagnostics=True)
  surface = SlabSurface()
  boundary_layer = SimplePhysics(
      use_external_surface_specific_humidity=True)
  dry_convection = DryConvectiveAdjustment()
  time_stepper = AdamsBashforth([radiation, surface])
  timestep = timedelta(hours=1)
  # Set up model state.
  state = get_default_state([radiation, diagnostic, surface,
                           boundary_layer, dry_convection])
  sw_flux = 200
  state['downwelling_shortwave_flux_in_air'][:] = sw_flux
  state['ocean_mixed_layer_thickness'][:] = 1.
  state['air_temperature'][:] = 250.
  diff_acceptable = 5.
  # Creates list for 0d historical profiles.
  netEn = [(net_energy_level_in_column(state,diff_acceptable))[0]]
  bdry_tempDiff = [surf_airBdry_tempDiff(state)]
  olrs = [(np.array(state['upwelling_longwave_flux_in_air']).flatten())[-1]]
  surfT = [(np.array(state['surface_temperature']).flatten())[0]]
  # Iteration
  startTime = datetime.datetime(2020,1,1,0,0,0)
  counter = 0.
  errorMargin = .5
  stop = False
  while stop == False:
    #Updating state
    state.update(diagnostic(state))
    diagnostics, state = time_stepper(state,timestep)
    state.update(diagnostics)
    #Updating appropriate quantities every month
    if counter % 168 == 0:
      netEn.append((net_energy_level_in_column(state,diff_acceptable))[0])
      bdry_tempDiff.append(surf_airBdry_tempDiff(state))
      olrs.append((np.array(state['upwelling_longwave_flux_in_air']).flatten())[-1])
      surfT.append((np.array(state['surface_temperature']).flatten())[0])
    # Checks breakout condition and increments time + counter.
    counter += 1
    startTime += timestep
    if abs(net_energy_level_in_column(state,diff_acceptable)[0]) < errorMargin:
      stop = True
    state['eastward_wind'][:] = 10.
	#Calculating output quantities.
  timeTaken = startTime - datetime.datetime(2020,1,1,0,0,0)
  lwFluxNet, lwFluxUp, lwFluxDown = netFlux(state)
  heatRate = heatingRate(state)
  airTemperatureProf = (np.array(state['air_temperature'])).flatten()
  return float(timeTaken.days), olrs, bdry_tempDiff, netEn, surfT, lwFluxNet, lwFluxUp, lwFluxDown, heatRate, airTemperatureProf