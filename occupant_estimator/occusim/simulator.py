"""
Main class of the module. This is used by the system to execute the different parts of this module.


"""

import numpy as np
from tqdm import tqdm

from . import year_probabilities
from . import utils
from . import statistics


def simulate_occupancy(profile, n_occupants, year, monthly_multiplier):
    """
    This method executes the simulation process. It receives different values in order to use the algorithm developed
    by Page, J., Robinson, D., Morel, N., & Scartezzini, J. L. (2008) in order to estimate the occupant presence.

    The method obtains the probability distribution of users in a building, the total number of occupants,
    the year to be simulated and the probability of people presence of each hour in the simulated year.


    Please, check Test Folder in order to understand the input values.


    -----------------------

    :param profile: A python dict containing the probability or presence given different hours and days of the week in
    [0,1] interval.
    :type profile: Python dictionary.
    :param n_occupants: An estimation of building occupants in integer.
    :type n_occupants: An integer value.
    :param year: An integer values containing the year to be simulated.
    :type year: An integer value.
    :param monthly_multiplier: A numpy array with size 12 which contains the monthly probability of presence in values
    [0,1]
    :type monthly_multiplier: Numpy array.
    :return:An array containing the number or persons per hour of the year.
    :rtype: Numpy array
    """
    hours_in_year = utils.get_hours_in_year(year)
    final_schedule = np.zeros(hours_in_year)  # list of zeros to fill later
    date_range = utils.get_dates_from_year(year)
    days_in_schedule = len(profile)  # type of days, actually supported: 'WEEKDAY', 'SATURDAY', 'SUNDAY'
    # yearly_array -> array of probabilities for each hour of the year
    array = utils.join_distributions(profile)
    yearly_array = year_probabilities.get_yearly_vectors(date_range, days_in_schedule, array, monthly_multiplier)
    for occupant in tqdm(range(n_occupants)):  # Current occupant number is not needed. But can be used in another context.
        final_schedule += statistics.calc_individual_occupant_schedule(yearly_array)

    return final_schedule
