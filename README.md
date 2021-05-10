## Modelling-Planetary-Climate
This project aims to explore methods of modelling large-scale Earth system and interpreting the results through the lens of spectroscopy, radiative transfer and thermodynamics. It evaluates key planetary climate variables (eg. OLR, radiative surface temperatures, optical depth profiles) using a series of 1d and 0d modelling techniques.  A PDF report entitled, "Modelling Planetary Climate", documenting and explaining our results is currently being created, and will be uploaded to the root directory of the repository upon completion. As of now, these exercises remain incomplete- the report is being written concurrently with the problems being attempted. All problems in this repository have been completed under the guidance of [Dr. Joy Merwin Monteiro](https://joymonteiro.github.io) (IISER-Pune), using his EC2213 lectures. All programs have been written in Python 3.6.8, using the libraries listed under the Modules section.

## Directory structure
1. **zeroDims**: Contains the code required to run a simple zero-dimensional model, primarily seeking to identify the surface's equilibrium radiating temperature for a given albedo level.

2. **1dmodels/radiative_transferModel**: Adds a vertical dimension to the 0d model i.e. considers atmospheric influence over a point-like projection of the surface. This model aims to evaluate:
    * The relationships between the atmosphere's optical thickness, absorptivity, and the planet's outgoing longwave radiative flux intensity,
    * The vertical profiles of longwave optical depth, heating rates, and flux divergence,
    * Their converse isothermal profiles. 
    * The effect of doubling aggregate atmospheric thickness on the system's outgoing longwave radiation. 


3. **1dmodels/radiative_equilibriumModel**: This is a dynamic model that attempts to bring the 1d system to equilibrium before evaluating the variables explored in the radiative tranfer model. It uses 4-hour increments to step the model forth through time. The system monitors the net energy level in the atmospheric column as a marker for equilibrium to terminate the program. The choice between presenting variables as equilibrium profiles or historical profiles depended upon its dimensional constraints- all results are presented as 1d line graphs for simplicity. The model specifically considers:
    * Equilibrium profiles of optical depth, heating rate, air temperature and flux divergence. 
    * Weekly changes in outgoing longwave radiative flux, surface temperature, net energy levels in the atmosphere, and the temperature gradient across the atmosphere-surface boundary. 
    * The effect of changing aggregate atmospheric thickness on the length of time required for the system to reach equilibrium. 

## Modules Used ##
This section lists the Python3 libraries used directly for the development of the models in this repository- not the dependencies of the libraries themselves. 
* **CLiMT**: Provides components to set up a model state and create output tendencies and diagnostics.
* **Numpy**: Used for the processing of multidimensional arrays.
* **Matplotlib**: Used to present results graphically.
* **Datetime**: Handles time incrementation (timedelta) and monitors program runtime and the equilibrium time. 
* **Metpy**: Provides important observed meteorological constants used to set up a relatively realistic model.
* **Sympl**: Used for the Adams-Bashforth numerical integration technique used to move the model through time. It is also a primary dependency for CLiMT functioning.
