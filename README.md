# Modelling-Planetary-Climate
This project aims to explore methods of modelling large-scale Earth systems and interpreting the results through the lens of spectroscopy, radiative transfer and thermodynamics. It evaluates key planetary climate variables (eg. OLR, radiative surface temperatures, optical depth profiles) using a series of 1d and 0d modelling techniques.  A PDF report entitled, "Modelling__Planetary_Climate_FINAL.pdf", documenting and explaining our results can be found in the root directory of the repository. All problems in this repository have been completed under the guidance of [Ass. Prof. Joy Merwin Monteiro](https://joymonteiro.github.io) (IISER-Pune). Most of the graphs referenced in this README have not been stored on the repository, but can be found in the report mentioned earlier. All programs have been written in Python 3.7.2, using the libraries listed under the Modules section.

## Directory structure
1. **./zeroDims/**: Contains the code required to run a simple zero-dimensional model, primarily seeking to identify the surface's equilibrium radiating temperature for a given albedo level.

2. **./radiative_transferModel/**: Adds a vertical dimension to the 0d model i.e. considers atmospheric influence over a point-like projection of the surface. This model aims to evaluate:
    * The relationships between the atmosphere's optical thickness, absorptivity, and the planet's outgoing longwave radiative flux intensity,
    * The vertical profiles of longwave optical depth, heating rates, and flux divergence,
    * Their converse isothermal profiles. 
    * The effect of doubling aggregate atmospheric thickness on the system's outgoing longwave radiation. 


3. **./radiative_equilibriumModel/**: This is a dynamic model that attempts to bring the 1d system to equilibrium before evaluating the variables explored in the radiative tranfer model. It uses 4-hour increments to step the model forward through time. The choice between presenting variables as equilibrium profiles or historical profiles depended primarily upon its dimensional constraints- all results are presented as 1d line graphs for simplicity. The model specifically considers:
    * Equilibrium profiles of optical depth, heating rate, air temperature and flux divergence. 
    * Weekly changes in outgoing longwave radiative flux, surface temperature, net energy levels in the atmosphere, and the temperature gradient across the atmosphere-surface boundary. 
    * Stopping criteria via the minimization of a net energy level in the atmospheric column.
    * The effect of changing aggregate atmospheric thickness on the timespan required for the system to reach equilibrium. 

4. **./RCEModel/**: Similarly to (3), this is a dynamic model, but it utilizes both radiative and convective processes to bring the system to equilibrium (hence, a radiative-convective equilibrium model). Similar profiles as in (3) are generated to highlight the effect convection has on the radiative equilibrium system. The time increments are much shorter (1-hour) to account for the rapid variation in key variables post initialization as a result of convection resolving radiative instabilities. We generally see more accurate results (with regard to the Earth system) with the addition of the convective component. The model specifically considers:
   * Equilibrium profiles of optical depth, heating rate, air temperature and flux divergence.
   *  Weekly changes in outgoing longwave radiative flux, surface temperature, net energy levels in the atmosphere, and the temperature gradient across the atmosphere-surface boundary.
   *  Stopping criteria via the minimization of a net energy level in the atmospheric column.
   *  Potential temperature vertical profiles to identify regions of radiative instability, and thus, convective activity.
   *  Tropopause height (identified through upwelling longwave radiation and potential temperature vertical profiles).

### Making Your Own Profiles! ###
  * **0d Model**: Run *0dModel.py*. The other program in the directory (*snowball_ice-free_0dmodelling.py*) can be used to generate albedo latitudinal profiles through the snowball/ice-free modelling technique.
  * **Radiative Transfer Model**: Each program uses *setup.py* to run the model, but create different profiles using the model state as input. The current profiles that can be generated are air temperature, heating rate, and flux divergence (thermally-stratified + isothermal) profiles. We also have modalities that account for variations in optical depth with optical thickness the vertical distribution of the absorptivity coefficient, and variations of OLR with an exponentially-increasing optical thickness.
  * **Radiative Equilibrium Model**: Given that the model is dynamic, the execution process is more streamlined than the radiative transfer model. Execute *runModel.py* to update the CSV files (in *output_runModel/*) used as input to dedicated graphing programs. *equilibriumProfs.py* and *weeklyProfs.py* generate stable and historical profiles, respectively. Run these after the CSV update to obtain your results.
  * **Radiative-Convective Equilibrium Model**: Running this model will yield results not mentioned in the PDF outline, since they weren't distinct enough from their radiative equilibrium counterparts to provide new and relevant insights. Since we created additional graphs not mentioned in the PDF, we've added all of them to a folder (*./RCEModel/graphs/*). Since the computation load increases here, running the model was compiled into a single main file, *runMain.py* to keep the process simple. Executing this program will fill *./RCEModel/graphs/* with any and all relevant profiles.


## Modules Used ##
This section lists the Python3 libraries used directly for the development of the models in this repository- not the dependencies of the libraries themselves. 
* **CLiMT 0.16.23**: Provides components to set up a model state and create output tendencies and diagnostics.
* **numpy 1.19.5**: Used for the processing of multidimensional arrays.
* **Matplotlib 3.3.4**: Used to present results graphically.
* **datetime 3.9.4**: Handles time incrementation (timedelta) and monitors program runtime and the equilibrium time. 
* **metpy 1.0.1**: Provides important observed meteorological constants used to set up a relatively realistic model.
* **sympl 0.4.0**: Used for the Adams-Bashforth numerical integration technique that moves the model through time. It is also a primary dependency for CLiMT functioning, including the definition of the state dictionary and handling of component objects.
* **csv 3.9.5**: Used to pass output data to dedicated programs for graphing.
