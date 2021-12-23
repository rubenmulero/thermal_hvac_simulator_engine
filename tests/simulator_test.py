#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import numpy as np
import random
from tqdm import tqdm

from simulator.simulator import Simulator
from util.constants import YEAR

# Defining local variables to load exogenous data
PREV_WEATHER_DATA = 'weather_data_2018_minute.csv'
CURRENT_WEATHER_DATA = 'weather_data_2019_minute.csv'
ELECTRICITY_DATA = 'electricity_price_2019.csv'


class SimulatorTestCase(unittest.TestCase):
    """
    This class is intented to test the simulator process. To do so, the testing phase will be divided in two parts:

    1) test the public methods to ensure that the data returned by them is correct.
    2) perform a simulation process to check if the data returned by the simulation process is correct.

    """

    def setUp(self):
        """
        Configuring the needed class parameters to execute the different tests.

        :return:
        """
        self.simulator_engine = Simulator(CURRENT_WEATHER_DATA, PREV_WEATHER_DATA, ELECTRICITY_DATA)

    def tearDown(self):
        """
        Configuring the needed class parameters to end the test.

        :return:
        """
        pass

    def test_get_current_timestamp(self):
        """
        Test different timestamps to check if the provided timestamps are correct.

        :return:
        """
        res = False
        # Sanity check, reset simulation process
        data = self.simulator_engine.reset_simulator()
        zero_timestep = self.simulator_engine.get_timestep()        # should be 0
        data = self.simulator_engine.simulate_step(1, 50.0)
        first_timestep = self.simulator_engine.get_timestep()       # should be 1
        data2 = self.simulator_engine.simulate_step(1, 50.0)
        second_timestep = self.simulator_engine.get_timestep()      # should be 2
        data3 = self.simulator_engine.simulate_step(0, 50.0)
        third_timestep = self.simulator_engine.get_timestep()       # should be 3
        if zero_timestep == 0 and first_timestep == 1 and second_timestep == 2 and third_timestep == 3:
            # Timesteps are correct, the sequence has sense
            res = True
        self.assertEqual(True, res)

    def test_simulate_step(self):
        """
        Performs one step in the simulation process an ensure that data is returned.

        :return:
        """
        res = False
        data = self.simulator_engine.simulate_step(0, 50.0)
        if data.any() and isinstance(data, np.ndarray) and data.shape == (9,):
            # Is a valid numpy element with data attached to it.
            res = True
        self.assertEqual(True, res)

    def test_reset_simulator(self):
        """
        We are going to make a step to know that we are not in step and and then, perform a reset to know that
        the simulation process iw working as expected

        :return:
        """
        res = False
        data = self.simulator_engine.simulate_step(0, 50.0)
        if data.any() and isinstance(data, np.ndarray):
            # Simulation step succeeded.
            current_timestep = self.simulator_engine.get_timestep()
            if current_timestep and current_timestep > 0:
                # Seems a valid step in simulation. Making a step
                self.simulator_engine.reset_simulator()
                current_timestep = self.simulator_engine.get_timestep()
                t_s = self.simulator_engine.get_t_s()
                t_h = self.simulator_engine.get_t_h()
                t_i = self.simulator_engine.get_t_i()
                t_e = self.simulator_engine.get_t_e()
                t_a = self.simulator_engine.get_t_a()
                if current_timestep == 0 and t_s == t_h == t_i == t_e == 20.0:
                    # Simulation engine was reset successfully
                    res = True
        if not res:
            print("Error in test, the given data is: {data}".format(data=data))
            print("The current timestemp is: {timestep}".format(timestep=self.simulator_engine.get_timestep()))

        self.assertEqual(True, res)

    def test_complete_simulation(self):
        """
        Performs 1 year simulation process to:

        1º Check the results from the simulation
        2º Compares the results from the original inputs of the entire simulation, having the heater off

        # We are going to work with random values of 0/1 to interact with the simulation engine.

        :return:
        """
        res = False
        # Creating a first version of the simulation process. We are only some basic steps
        max_simulated_steps = self.simulator_engine._get_simulator_timesteps(YEAR)
        print("Total timesteps to simulate: {timesteps}".format(timesteps=max_simulated_steps))
        self.simulator_engine.reset_simulator()
        simulation_results = list()
        consumption_list = list()
        for i in tqdm(range(0, max_simulated_steps)):
            # On off simulation process.
            # Random pattern.
            action = random.randint(0, 1)
            data = self.simulator_engine.simulate_step(action, 50.0)
            # data = self.simulator_engine.simulate_step(action, 50.0)
            # Extracting data from the simulation result
            t_s, t_h, t_i, t_e = data[0]
            t_a = data[1]
            c_op = data[2]
            i_s = data[3]
            occupancy = data[6]
            next_occupancy = data[7]
            date = data[8]
            simulation_results.append([date, t_s, t_h, t_i, t_e, t_a, i_s, occupancy, next_occupancy, action, c_op])
            # Adding operational cost to the consumption list to track the total consumption
            if action:
                consumption_list.append(c_op)
        # Checking the current timestep and data. Just a Sanity check
        if max_simulated_steps == len(simulation_results):
            # Data has the same length, so it has sense
            print("Simulation finished, now saving results")
            np.savetxt("./simulation_results_from_test_code_h_random.csv", simulation_results, delimiter=",",
                       fmt=['%s', '%f', '%f', '%f', '%f', '%f', '%f', '%d', '%d', '%d', '%f'],
                       header='Date, T_s, T_h, T_i, T_e, T_a, I_s, Occupancy, Next_occupancy, Action, Operational_cost', comments='')
            # Giving information about the mean consumption
            consumption_data = np.asarray(consumption_list)
            consumption_mean = np.mean(consumption_data)
            consumption_max = np.max(consumption_data)
            consumption_min = np.min(consumption_data)
            print("The mean consumption was ", consumption_mean)
            print("The MAX consumption was ", consumption_max)
            print("The MIN consumption was ", consumption_min)
            res = True
        self.assertEqual(True, res)


if __name__ == '__main__':
    unittest.main()
