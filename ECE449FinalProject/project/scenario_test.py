# -*- coding: utf-8 -*-
# Copyright © 2022 Thales. All Rights Reserved.
# NOTICE: This file is subject to the license agreement defined in file 'LICENSE', which is part of
# this source code package.

import time
import random
import numpy as np
import EasyGA as ga

from logger import Logger

from EasyGA import GA
from EasyGA.parent import Parent
from EasyGA.survivor import Survivor

from kesslergame import Scenario
from kesslergame import KesslerGame
from kesslergame import GraphicsType
from kesslergame import KesslerController
from kesslergame import TrainerEnvironment

# from test_controller import TestController
from GAController import GAController
from ro_controller import ROController
from graphics_both import GraphicsBoth
from fuzzy_controller import FuzzyController
from scott_dick_controller import ScottDickController

global counter

counter = 1

scenario = Scenario(time_limit=60,
                   name="Scenario",
                #    num_asteroids=10,
                   map_size=(1000, 800),
                   stop_if_no_ammo=False,
                   ammo_limit_multiplier=0,
                   ship_states=[
                       {'position': (500, 400), 'angle': 90, 'lives': 3, 'team': 1},
                    #    {'position': (400, 600), 'angle': 90, 'lives': 3, 'team': 2},
                       ],
                   asteroid_states=[
                       {'position': (600, 500), 'angle': 45,'size': 3, 'speed': -75},
                       {'position': (600, 300), 'angle': 135,'size': 3, 'speed': 75},
                       {'position': (400, 500), 'angle': -45,'size': 3, 'speed': 75},
                       {'position': (400, 300), 'angle': 45,'size': 3, 'speed': 75},
                       {'position': (500, 100), 'size': 1, 'speed': 0},
                # #        {'position': (400, 100), 'size': 1, 'speed': 0},
                       ],
                )

game_settings = {"perf_tracker": True,
                 "graphics_obj": None,
                 "realtime_multiplier": 1,
                 "graphics_type": GraphicsType.Tkinter,
                 }

# game = KesslerGame(settings=game_settings)  # Use this to visualize the game scenario
game = TrainerEnvironment(settings=game_settings)  # Use this for max-speed, no-graphics simulation

def generate_chromosomes() -> list[list[float]]:
    """
    Generate a list containing different randomly generated sets
    of chromosomes for the different antecedents and consequent universes.

    Returns:
        list[list[float]]: List of chromosome sets.
    """
    
    ship_speed_range = (0, 240)
    asteroid_distance_range = (0, 1280)
    asteroid_direction = (0, 180)
    ship_turn_rate_range = (0, 180)
    ship_thrust_range = (0, 480)
    
    chromosomes = [
        [random.uniform(*ship_speed_range), random.uniform(*ship_speed_range)],
        [random.uniform(*asteroid_distance_range), 
         random.uniform(*asteroid_distance_range), 
         random.uniform(*asteroid_distance_range), 
         random.uniform(*asteroid_distance_range), 
         random.uniform(*asteroid_distance_range)],
        [random.uniform(*asteroid_direction), random.uniform(*asteroid_direction)],
        [random.uniform(*ship_turn_rate_range), 
         random.uniform(*ship_turn_rate_range), 
         random.uniform(*ship_turn_rate_range)],
        [random.uniform(*ship_thrust_range), random.uniform(*ship_thrust_range)],
    ]
    
    for chromosome in chromosomes:
        chromosome.sort()
    
    return chromosomes

def fitness(chromosomes) -> float:
    """
    Fitness function used by the genetic algorithm to maximize asteroid hits and accuracy.

    Args:
        chromosomes (list): Randomly generated chromosomes

    Returns:
        tuple[float, float, float]: Product of average asteroid hits and average accuracy.
    """
    
    global counter
    
    hits = []
    fired = []
    deaths = []
    accuracies = []
    
    for i in range(5):
        ga_controller = GAController(chromosomes)
        scores = game.run(scenario=scenario, controllers=[ ga_controller ])[0].teams[0]
        
        hits.append(scores.asteroids_hit)
        fired.append(scores.shots_fired)
        deaths.append(scores.deaths)
        accuracies.append(scores.accuracy)
        
    mean_hits = np.mean(hits)
    mean_fired = np.mean(fired)
    mean_deaths = np.mean(deaths)
    mean_accuracy = np.mean(accuracies)
    
    Logger.log.info(f'Chromosome set #{counter}:')
    Logger.log.info(chromosomes)
    Logger.log.info(f'Hits: {mean_hits}, Accuracy: {mean_accuracy}, Frames: {ga_controller.eval_frames}')
    
    print(f'Run #{counter}')
    print(f'Average hits        : {mean_hits:.4f} hits')
    print(f'Average deaths      : {mean_deaths:.4f} deaths')
    print(f'Average accuracy    : {mean_accuracy * 100:.4f} %')
    print(f'Average shots fired : {mean_fired:.4f} shots')
    print(f'Frames survived     : {ga_controller.eval_frames} frames\n')
    
    counter += 1
    
    return mean_hits

def evaluate_ga() -> list[float]:
    """
    Evaluates the best chromosome sets using a genetic algorithm.

    Returns:
        list[float]: List of the predicted most optimal chromosome sets after evolution.
    """
    
    ga = GA()
    ga.population_size = 5
    ga.generation_goal = 50
    ga.chromosome_length = 5
    ga.target_fitness_type = 'max'
    ga.fitness_function_impl = fitness
    ga.parent_selection_impl = Parent.Rank.stochastic_geometric
    ga.gene_impl = lambda: generate_chromosomes()
    ga.evolve()
    
    return ga.population[0]

if __name__ == "__main__":
    population = evaluate_ga()
    
    print(f'Best fitness: {population.fitness}')
    print("Best Chromosomes:")
    for chromosome in population:
        print(f'\n{chromosome}\n')

    # pre = time.perf_counter()
    # score, perf_data = game.run(scenario=scenario, controllers = [ROController()])

    # print('Scenario eval time: '+str(time.perf_counter()-pre))
    # print(score.stop_reason)
    # print('Asteroids hit: ' + str([team.asteroids_hit for team in score.teams]))
    # print('Deaths: ' + str([team.deaths for team in score.teams]))
    # print('Accuracy: ' + str([team.accuracy for team in score.teams]))
    # print('Mean eval time: ' + str([team.mean_eval_time for team in score.teams]))
    # print('Evaluated frames: ' + str([controller.eval_frames for controller in score.final_controllers]))
