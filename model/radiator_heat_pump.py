#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This class merges the previous version in which the radiator coefficients and the heat pump formulas where
separated in two different classes.

The radiator formulas are used to calculate the Coefficient of Performance (COP) and the Power Electricity (P_el) to
be used later to calculate the Operational Cost (C_op).

-----------------------------------------------------------

The exposed hear pump formula, is based on the following paper:

https://doi.org/10.1016/j.enbuild.2015.11.014

The exposed radiator formulas are based in the following work:

Hydroponic heating systems - the effect of design on system sensitivity.
PhD, Department of Building Services Engineering, Chalmers University of Technology (2002)

"""

import os

from util.logger import LoggingClass
from util.constants import N, K_RAD
from util.exception import TemperatureValidationError
from util.constants import Q_HP_MIN, Q_HP_MAX, Q_HP_BOOST


logger = LoggingClass('simulator_engine').get_logger()
file_name = os.path.basename(__file__)


def _calculate_qh(p_act_hp, p_t_sup, p_t_i_1):
    """
    By given the current actuation of the heat pump, the needed supply temperature of the building and the
    indoor temperature. This method calculates the coefficient of a water Hydroponic heating radiator.

    In our model, this represent the calculation of the Q_h value.

    -----------------------
    Coefficients:

    n = 1,33
    K_rad = 9000/((50-20)^n)	12

    Inputs:

    ACThp = The current actuation of the heat pump (should be 0 or 1).
    T_sup = Supplied temperature to the building (by the heat pump).
    T_i = Previous Indoor temperature (Temperature of the interior).

    Output

    Q_h = ACT_HP * K_rad * (T_supply (i) - T_out(i-1))^n

    WHERE:

    i --> Current timestep
    i-1 ---> Previous timestep

    Notes:

    The T_supply is the water temperature, in general it should be a constant value. If for some reason, the T_out
    temperature is greater, the formula will fail. It is impossible that The interior temperature could be grater than
    the supplied one because the building envelope dissipates the heat.


    :param p_act_hp: The current actuation of the heat pump. Should be 0 or 1.
    :param p_t_sup: The  temperature supplied to the building of the current timestep (t)
    :param p_t_i_1: The indoor temperature of the building at previous timestep (t-1)
    :return: The Hydrophobic coefficient Q_h value needed by other parts of the simulation engine.
    """

    if isinstance(p_t_sup, float) and isinstance(p_t_i_1, float) and p_act_hp in [0, 1]:
        # The T_i could not be greater than T_sup, if so, an error will raise.
        # Raise an error if this is happening because it can be deleted.
        if p_t_sup < p_t_i_1:
            print("It is impossible tha T_i is greater than T_sup")
            print("The value of T_sup is {t_sup} \n The value of T_i is {t_i}".format(t_sup=p_t_sup, t_i=p_t_i_1))
            raise TemperatureValidationError("The interior temperature is greater than supplied one", [p_t_sup, p_t_i_1])
        temperature_diff = (p_t_sup - p_t_i_1) ** N
        q_h = p_act_hp * K_RAD * temperature_diff
    else:
        logger.error(
            file_name + f"The given input values are not in correct format: T_s={p_t_sup} type: {type(p_t_sup)}"
                        f"; T_i_1= {p_t_i_1} type: {type(p_t_i_1)}; ACT_HP={p_act_hp} type: {type(p_act_hp)}.")
        raise Exception("The given input temperature values are not float. Something wrong happened. Check logs")
    return q_h


def calculate_cop(p_act_hp, p_t_sup, p_t_i_1, p_t_a):
    """
    Giving the needed supply temperature to the building (t_sup) and the current outdoor temperature (t_out) this method
    calculates the current COP of the heat pump.

    This formula is calculated in a specific timestamp. So, the developer should decide which is the best time window
    to consider in each timestamp.

    We are using a simple decay formula with no specific parameters of a heat pump model. The method calculates the
    temperature decay taking into account a fixed temperature drop.

    The COP should be always >1. If for some reason, the calculated value is 0 or bellow, something was wrong in this
    method or in the model itself.

    :param p_act_hp: The current actuation of the heat pump. Should be 0 or 1.
    :param p_t_sup: The  temperature supplied to the building of the current timestep (t)
    :param p_t_i_1: The indoor temperature of the building at previous timestep (t-1)
    :param p_t_a: The outdoor temperature at the current step (t). (Ambient temperature)

    :return: The coefficient of a water Hydroponic heating radiator (q_h).
             The Power electricity of the heat pump (p_el).
    """
    if p_act_hp in [0, 1] and isinstance(p_t_sup, float) and isinstance(p_t_i_1, float) and isinstance(p_t_a, float):
        t_sup_effect = p_t_sup
        q_h = _calculate_qh(p_act_hp, t_sup_effect, p_t_i_1)
        if q_h >= Q_HP_BOOST:
            q_h = Q_HP_BOOST
            t_sup_effect = ((q_h / K_RAD) ** (1 / N)) + p_t_i_1
        elif q_h <= Q_HP_MIN:
            q_h = 0.
        q_h_hp = min(q_h, Q_HP_MAX)
        q_h_boost = q_h - q_h_hp
        # Calculating the COP based on the activation requirement
        cop = 2.6 + (0.0465 * p_t_a) - (0.0187 * t_sup_effect)
        p_el = (q_h_hp / cop) + q_h_boost
    else:
        logger.error(
            file_name + f"The given input values are not in correct format: T_s={p_t_sup} type: {type(p_t_sup)}; "
                        f"T_a={p_t_a} type: {type(p_t_a)}; T_i_1= {p_t_i_1} type: {type(p_t_i_1)}; "
                        f"ACT_HP={p_act_hp} type: {type(p_act_hp)}.")
        raise Exception("The given input temperature values are not float. Something wrong happened. Check logs")

    return q_h, p_el
