# People Occupant Estimation

This is an implementation of the People Occupant prediction based on the paper of J. Page

_Page, J., Robinson, D., Morel, N., & Scartezzini, J. L. (2008). A generalised stochastic model for the 
simulation of occupant presence. Energy and buildings, 40(2), 83-98._

The code is implemented by the people behind the project __City Energy Analyst__.

Credits to:
[City Energy Analyst](https://zenodo.org/record/1487867)


## Requirements

* Python 3
* Common Data Scientist libraries:
    * Pandas
    * Numpy
    * Tqmd
    
To install dependencies, please use pip:

``` pip install -r requirements.txt```

## How to use

The occupant simulation program has been modularized to be easily used in other programs. 
The module needs user to define data in an specified way. Actually the day types are limited to 'WEEKDAY', 'SATURDAY' 
and 'SUNDAY' so it is mandatory to use the module as follows:

```python
import occusim
n_occupants = 10  # maximum number of occupants
year = 2020  # year to make the simulation
# define the hourly probabilities of presence per occupant
profile = {
    'WEEKDAY': [1, 1, 1, 1, 1, 1, 1, 0.9, 0.8, 0.8, 0.8, 0.75, 0.5, 0.65, 0.7, 0.67, 0.78, 0.85, 0.9, 0.95, 1, 1, 1, 1],
    'SATURDAY': [1, 1, 1, 1, 1, 1, 1, 0.9, 0.8, 0.8, 0.8, 0.75, 0.5, 0.65, 0.7, 0.67, 0.78, 0.85, 0.9, 0.95, 1, 1, 1, 1],
    'SUNDAY': [1, 1, 1, 1, 1, 1, 1, 0.9, 0.8, 0.8, 0.8, 0.75, 0.5, 0.65, 0.7, 0.67, 0.78, 0.85, 0.9, 0.95, 1, 1, 1, 1],
}
# define the general month probability estimation (e.g. factory occupancy probabilities are not the same in March and August)
monthly_multiplier = [0.8, 0.6, 0.9, 0.6, 0.8, 1.0, 0.0, 0.6, 1.0, 0.6, 0.9, 0.6]  
# execute the simulation 
simulation = occusim.simulator.simulate_occupancy(profile, n_occupants, year, monthly_multiplier, )
```
 
## Data sources and ground truth.

There are different webpages to extract data to test this system, for example:

* This [link](https://openei.org/datasets/dataset/one-year-behavior-environment-data-for-medium-office) contains some
data of one year of occupant behaviour for a medium us office.