#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file implements the statistical calculations given by Page et al. (2008).

"""

import random
import numpy as np


def calc_individual_occupant_schedule(deterministic_schedule):
    """
    Calculates the stochastic occupancy pattern for an individual based on Page et al. (2008). The so-called parameter
    of mobility mu is assumed to be a uniformly-distributed random float between 0 and 0.5 based on the range of values
    presented in the aforementioned paper.

    :param deterministic_schedule: deterministic schedule of occupancy provided in the user inputs
    :type deterministic_schedule: array(float)

    :return pattern: yearly occupancy pattern for a given occupant in a given occupancy type
    :rtype pattern: list[int]
    """

    # get a random mobility parameter mu between 0 and 0.5
    mu = random.uniform(0, 0.5)
    # assign initial state by comparing a random number to the deterministic schedule's probability of occupant presence at t = 0
    if random.random() <= deterministic_schedule[0]:
        state = 1
    else:
        state = 0

    # start list of occupancy states throughout the year
    pattern = [state]

    # calculate probability of presence for each hour of the year
    for i in range(len(deterministic_schedule[:-1])):
        # get probability of presence at t and t+1 from archetypal schedule
        p_0 = deterministic_schedule[i]
        p_1 = deterministic_schedule[i + 1]
        # calculate probability of transition from absence to presence (T01) and from presence to presence (T11)
        T01, T11 = calculate_transition_probabilities(mu, p_0, p_1)

        if state == 1:
            next = get_random_presence(T11)
        else:
            next = get_random_presence(T01)

        pattern.append(next)
        state = next

    return np.array(pattern)


def calculate_transition_probabilities(mu, P0, P1):
    """
    Calculates the transition probabilities at a given time step as defined by Page et al. (2008). These are the
    probability of arriving (T01) and the probability of staying in (T11) given the parameter of mobility mu, the
    probability of the present state (P0), and the probability of the next state t+1 (P1).

    :param mu: parameter of mobility
    :type mu: float
    :param P0: probability of presence at the current time step t
    :type P0: float
    :param P1: probability of presence at the next time step t+1
    :type P1: float

    :return T01: probability of transition from absence to presence at current time step
    :rtype T01: float
    :return T11: probability of transition from presence to presence at current time step
    :rtype T11: float
    """

    # Calculate mobility factor fraction from Page et al. equation 5
    m = (mu - 1) / (mu + 1)

    # Calculate transition probability of arriving and transition probability of staying
    T01 = (m) * P0 + P1
    if P0 != 0:
        T11 = ((P0 - 1) / P0) * (m * P0 + P1) + P1 / P0
    else:
        T11 = 0

    # For some instances of mu the probabilities are bigger than 1, so the min function is used in the return statement.
    return min(1, T01), min(1, T11)


def get_random_presence(p):
    """
    Get the current occupant state (presence=1 or absence=0) at the current time step given a probability p.

    :param p: A probability (e.g. T01, T11)
    :type p: float

    Returns the randomly-chosen state (0 or 1).
    """

    # Calculate probability of presence
    P1 = int(p * 100)
    # Calculate probability of absence
    P0 = 100 - P1

    # Create population of possible values and choose one value
    weighted_choices = [(1, P1), (0, P0)]
    population = [val for val, cnt in weighted_choices for i in range(cnt)]

    return random.choice(population)
