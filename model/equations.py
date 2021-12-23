#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contain the proposed model equations, here, we are going to call to the rest of the elements in order
to obtain the current values at timestep T.

The model is based on the validated model from Peder Bacher.

"Identifying suitable models for the heat dynamics of buildings"
DOI: https://doi.org/10.1016/j.enbuild.2011.02.005


Equations parameters (Defined as constants)
--------------------------------

Ris = Resistance between the interior and the sensor.
Cs = Capacity of the sensor.
Rih = Resistance between the heaters and the interior.
Ch = Capacity of the electrical heaters.
Rie = Resistance between from the interior and the building envelope.
Ce = Capacity of the building envelope.
Rea = Resistance between the building envelope and the ambient.
Aw = Effective window area of the building.
Ae = Effective area in which the solar radiation enters the building envelope

---------------------------------

Decimals are rounded in six digits to have <0.01º corrections each hour.

    Sensivity = 0.01ºC/hour
    timesteps_per_hour = 3600
    1 timestep = 1 second

    Sensivity / timesteps_per_hour = 2.777778e-06 (Six decimals)

---------------------------------

@author: Rubén Mulero
"""

from util.constants import COMFORT_TEMP, M_BAND, R_VENT
from util.logger import LoggingClass
from util.exception import TemperatureValidationError

logger = LoggingClass('simulator_engine').get_logger()


def is_comfort(p_t_s):
    """
    This method calculates if the current temperature is inside the comfort values given the current Temperature
    setpoint.

    :param p_t_s: supplied temperature taken from the model
    :return: True if comfort, False otherwise.
    """
    min_comfort = (COMFORT_TEMP - M_BAND) / 2
    max_comfort = (COMFORT_TEMP + M_BAND) / 2
    return True if min_comfort < p_t_s < max_comfort else False


##############################
##
# Main model equations
##
##############################

def calculate_t_s(p_delta_t, p_c_s, p_r_is, p_t_i_1, p_t_s_1):
    """
    This method calculates the sensor temperature (T_s) at timestep (t).

    :param p_delta_t: The time difference in seconds. (Time difference in seconds in a timestep)
    :param p_c_s: Capacity of the sensor
    :param p_r_is: Resistance between the interior and the sensor
    :param p_t_i_1: Previous temperature of the interior at timestep (t-1)
    :param p_t_s_1: Previous temperature of the sensor value at timestep (t-1)

    :return: Sensors temperature at timestemp (t) given by the T_s variable.
    """

    timestep = p_delta_t / (3600 * p_c_s)
    thermald_difference = (p_t_i_1 - p_t_s_1) / p_r_is
    t_i = p_t_s_1 + (timestep * thermald_difference)
    return t_i


def calculate_t_h(p_delta_t, p_c_h, p_r_ih, p_q_h, p_t_i_1, p_t_h_1):
    """
    This method calculates the temperature of the heaters

    :param p_delta_t: The time difference in seconds (Time difference in seconds in a timestep)
    :param p_c_h: Capacity of the electrical heaters.
    :param p_r_ih: Resistance between the heaters and the interior.
    :param p_q_h: Hydrophobic coefficient value at timestemp (t)
    :param p_t_i_1: Previous temperature of the interior at timestep (t-1)
    :param p_t_h_1: Previous temperature of the heater at timestep (t-1)

    :return: Heater temperature at timestemp (t) given by T_h variable
    """

    timestep = p_delta_t / (3600 * p_c_h)
    thermald_difference = (p_t_i_1 - p_t_h_1) / p_r_ih
    t_h = p_t_h_1 + (timestep * thermald_difference) + (timestep * p_q_h)
    return t_h


def calculate_t_i(p_delta_t, p_c_i, p_r_is, p_r_ih, p_r_ie, p_q_ig, p_t_s_1, p_t_i_1, p_t_h_1, p_t_e_1,
                  p_aw, p_i_s, p_r_vent):
    """
    This method calculates the temperature of the interior (Indoor temperature).


    Additional notes
    ------------------

    The setpoint temperature should be between 20 and 50 degrees.



    :param p_delta_t: The time difference in seconds (Time difference in seconds in a timestep)
    :param p_c_i: Capacity of the interior
    :param p_r_is: Resistance between the interior and the sensor
    :param p_r_ih: Resistance between the heaters and interior
    :param p_r_ie: Resistance between from the interior and the building envelope
    :param p_q_ig: Internal gain coefficient
    :param p_t_s_1: Previous temperature of the sensor at timestep (t-1)
    :param p_t_i_1: Previous temperature of the interior at timestep (t-1)
    :param p_t_h_1: Previous temperature of the heater at timestep (t-1)
    :param p_t_e_1: Previous temperature of the enveloping at timestep (t-1)
    :param p_aw: Effective window area.
    :param p_i_s: Solar radiation from horizontal plane.
    :param p_r_vent: Ventilation resistance if ventilation is active

    :return: Interior temperature at timestep (t) given by T_i variable
    """

    timestep = p_delta_t / (3600 * p_c_i)
    thermal_difference_s = (p_t_s_1 - p_t_i_1) / p_r_is
    thermal_difference_h = (p_t_h_1 - p_t_i_1) / p_r_ih
    thermal_difference_e = (p_t_e_1 - p_t_i_1) / p_r_ie
    radiation_coefficient = p_aw * p_i_s
    # Adding timesteps
    thermal_variation_s = timestep * thermal_difference_s
    thermal_variation_h = timestep * thermal_difference_h
    thermal_variation_e = timestep * thermal_difference_e
    internal_gain_variation = timestep * p_q_ig
    radiation_variation = timestep * radiation_coefficient
    ventilation_variation = timestep * p_r_vent
    t_i = p_t_i_1 + thermal_variation_s + thermal_variation_h + thermal_variation_e + \
        internal_gain_variation + radiation_variation + ventilation_variation
    return t_i


def calculate_t_e(p_delta_t, p_c_e, p_r_ie, p_r_ea, p_t_i_1, p_t_a_1, p_t_e_1, p_a_e, p_i_s):
    """
    This method calculates the temperature of enveloping.


    Additional notes
    -----------------

    The envelope temperature can not be grather than 50 Cº thus:

    T_e < 50CCº Always.

    If for some reason, the obtained temperatures are greater, then something is not correct.



    :param p_delta_t: The time difference in seconds (Time difference in seconds in a timestep)
    :param p_c_e: Capacity of the building envelope
    :param p_r_ie: Resistance between from the interior and the building envelope
    :param p_r_ea:  Resistance between the building envelope and the ambient.
    :param p_t_i_1: Previous temperature of the interior at timestep (t-1)
    :param p_t_a_1: Previous temperature of ambient at timestep (t-1) (Outdoor temperature)
    :param p_t_e_1: Previous temperature of enveloping at timestep (t-1)
    :param p_a_e: Effective are in which the solar radiation enters to the building envelope
    :param p_i_s: Solar radiation from horizontal plane

    :return: Envelope temperature at timestep (t) given vy T_e variable
    """
    timestep = p_delta_t / (3600 * p_c_e)
    thermal_difference_i = (p_t_i_1 - p_t_e_1) / p_r_ie
    thermal_difference_a = (p_t_a_1 - p_t_e_1) / p_r_ea
    ambient_radiation = p_a_e * p_i_s
    # Adding timesteps
    thermal_variation_i = timestep * thermal_difference_i
    thermal_variation_a = timestep * thermal_difference_a
    ambient_radiation_variation = timestep * ambient_radiation
    t_e = p_t_e_1 + thermal_variation_i + thermal_variation_a + ambient_radiation_variation
    # Sanity check
    if t_e > 50:
        print("It is impossible tha T_e is greater than 50ºC")
        print("The value of T_e is {t_e}".format(t_e=t_e))
        logger.error("Error calculating T_e. Obtained value is greater than 50ºC")
        raise Exception
    return t_e
