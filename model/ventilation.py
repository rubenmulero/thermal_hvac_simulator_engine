#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains the equations to calculate the building ventilation. This should be plugged in the current
formulas in order to add more realism to the entire model.

The ventilation parameters are extracted direcly from:

ASHRAE 62.1.2013. Table 6.2.2.1. Office

------------------------
Input parameters

the activation or deactivation of the ventilation process in a fixed time range

Output parameters

The values of the ventilation process.


@author: Rubén Mulero
"""

import os
from util.logger import LoggingClass
from util.constants import V, CP, DENS, R_VENT


logger = LoggingClass('simulator_engine').get_logger()
file_name = os.path.basename(__file__)


def calculate_ventilation_power(p_t_a_1, p_t_i_1, p_act_vent):
    """
    Calculates the power of the ventilation based on the thermal difference between external and internal temperature.

    Some defined constants are used to calculate the ventilation:

    CP in kJ/kgK
    Dens in kG/K

    delta value is the thermal difference between outdoor and indoor temperatures.


    :param p_t_a_1 outdoor temperature at time t-1
    :param p_t_i_1 indoor temperature at time t-1
    :param p_act_vent ventilation activation status

    :return: P_vent which has the current power ventilation
    """
    delta = p_t_a_1 - p_t_i_1
    p_vent = V * CP * DENS * delta * p_act_vent
    return p_vent


def calculate_ventilation_resistance_variance(p_t_a_1, p_t_i_1, p_act_vent):
    """
    By knowing if the current ventilation process is activated, this method calculate the ventilation resistance
    based on the variation of the current external and internal temperature.

    :param p_t_a_1:
    :param p_t_i_1:
    :param p_act_vent: ventilation activation status

    :return: Ventilation resistance variance with the temperature difference
    """
    if p_act_vent:
        delta = p_t_a_1 - p_t_i_1
        ventilation_resistance = delta / R_VENT
    else:
        ventilation_resistance = 0

    return ventilation_resistance
