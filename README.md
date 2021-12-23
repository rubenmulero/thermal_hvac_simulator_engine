# Thermal Simulator Engine

The thermal simulation engine consist on a programming code with the aim of making a direct integration of engineered 
thermal formulas to allow researchers build their custom models to train control-oriented algorithms. 

A variation of the thermal model proposed by Peder Batcher et al. from the Denmark Technical University (DTU) 
is presented as a testing tool to show the benefits of using this simulation engine. 

## Requirements

To run this simulator you need the following requirements:

* A [Python 3](https://www.python.org/) interpreter (tested with Python 3.8)
* A GNU/Linux based Operating system (tested on Arch Linux).
* Minor knowledge about how to use PIP, the standard package manager for Python.


## Acknowledgements

I would like to thank you the following persons/services to allow this to make happen:

* [DTU Climate Station](http://climatestationdata.byg.dtu.dk), Department of Civil Engineering, Technical University of Denmark.
* [NordPool](https://www.nordpoolgroup.com/) electricity provider
* Peder Batcher.
* Jessen Page.
* People behind [City Energy Analyst](https://zenodo.org/record/1487867) program.


## Questions?

If you have some questions you can visit my [personal page](www.rubenmulero.com) or send me an [email](me@rubenmulero.com).

_______

Data weather provided by DTU Climate Station, Department of Civil Engineering, Technical University of Denmark, http://climatestationdata.byg.dtu.dk

Radiator model provided by: Hydronic heating systems - the effect of design on system sensitivity. PhD, Department of Building Services Engineering,
Chalmers University of Technology (2002)

Electricity prices data provided by [NordPool](https://www.nordpoolgroup.com/).

Occupant estimation algorithm by Page, J., Robinson, D., Morel, N., & Scartezzini, J. L. (2008). A generalised stochastic model for the simulation of occupant presence. Energy and buildings, 40(2), 83-98.

Data sources and ground truth following this  [link](https://openei.org/datasets/dataset/one-year-behavior-environment-data-for-medium-office) contains some
data of one year of occupant behaviour for a medium us office (used in the simulation engine).