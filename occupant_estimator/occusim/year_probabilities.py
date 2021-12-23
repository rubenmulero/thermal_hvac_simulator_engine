#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file creates the vector or probabilities alongside a complete year in order to be used later as the
input vector or Probabilities P(t) and P(t+1) in the J. Page formulas. The idea of this class it to pick up
the array of timeindex of a complete year, the proposed schedule with the hourly probabilities and the
monthly probabilities in order to create the probability vector for each hour in a year.

"""

import numpy as np


def get_yearly_vectors(date_range, days_in_schedule, schedule_array, monthly_multiplier,
                       normalize_first_daily_profile=False):
    """
    Creates a probability vector of each day of the year using the data loaded from the CSV file.

    It takes into account the different days of the year.

    :param date_range: The DatetimeIndex array created with pandas.
    :param days_in_schedule: An integer value with the days in schedule e.g. 3 if we have WEEKDAY, SATURDAY, SUNDAY.
    :param schedule_array: A numpy vector containing the probability of occupancy for each schedule and hour.
    :param monthly_multiplier: A vector containing the the monthly probability.
    :param normalize_first_daily_profile:  Normalise some variables if we take into account the water consumption.
    :return:
    """

    # transform into arrays
    # per weekday, saturday, sunday
    array_per_day = schedule_array.reshape(3, int(len(schedule_array) / days_in_schedule))
    array_week = array_per_day[0]
    array_sat = array_per_day[1]
    array_sun = array_per_day[2]

    if normalize_first_daily_profile:
        # for water consumption we need to normalize to the daily maximum
        # this is to account for typical units of water consumption in liters per person per day (lpd).

        if array_week.sum() != 0.0:
            norm_weekday_max = array_week.sum() ** -1
        else:
            norm_weekday_max = 0.0

        if array_sat.sum() != 0.0:
            norm_sat_max = array_sat.sum() ** -1
        else:
            norm_sat_max = 0.0

        if array_sun.sum() != 0.0:
            norm_sun_max = array_sun.sum() ** -1
        else:
            norm_sun_max = 0.0
    else:
        norm_weekday_max = 1.0
        norm_sat_max = 1.0
        norm_sun_max = 1.0

    yearly_array = [
        calc_hourly_value(date, array_week, array_sat, array_sun, norm_weekday_max, norm_sat_max, norm_sun_max,
                          monthly_multiplier) for date in date_range]

    return np.array(yearly_array)


def calc_hourly_value(date, array_week, array_sat, array_sun, norm_weekday_max, norm_sat_max, norm_sun_max,
                      monthly_multiplier):
    """
    For each hour inside a Year, this method calculates the probability of occupancy given a set of input values

    :param date: The current date range.
    :param array_week: A array of probabilities given by the csv file of weekdays.
    :param array_sat: A array of probabilities given by the csv file of saturdays.
    :param array_sun:  A array of probabilities given by the csv file of wsundays.
    :param norm_weekday_max: Normalised weekdays.
    :param norm_sat_max:  Normalised saturdays.
    :param norm_sun_max:  Normalised sundays.
    :param monthly_multiplier: a vector of 12 elements containing the monthly occupancy.
    :return:
    """

    month_year = monthly_multiplier[date.month - 1]
    hour_day = date.hour
    dayofweek = date.dayofweek
    if 0 <= dayofweek < 5:  # weekday
        return array_week[hour_day] * month_year * norm_weekday_max  # normalized dhw demand flow rates
    elif dayofweek is 5:  # saturday
        return array_sat[hour_day] * month_year * norm_sat_max  # normalized dhw demand flow rates
    else:  # sunday
        return array_sun[hour_day] * month_year * norm_sun_max  # normalized dhw demand flow rates
