"""
AI_Project
Algorithm.py

@author: Santosh Kumar Nunna (sn7916@rit.edu)
@author: Mouna Reddy Kallu (mk9014@rit.edu)
@author: Gautham Gadipudi (gg7148@rit.edu)

This class is the main class where the key algorithm lies. We call the line of functions which perform the necessary
set of operations producing new population, performing mutation, crossover and different operation on the given city
list to return the best route for the travelling salesman.
"""
import random
import operator
from City import City
from Fitness import Fitness
import pandas as pd
import numpy as np


def router(city_list):
    """
    This function generated a random route map from the given list of cities. The length of route depends on the length
    of the cities list.
    :param city_list: City list
    :return: list of cities in random order
    """
    pop_list = random.sample(city_list, len(city_list))
    return pop_list


def start_population(population_size, cities):
    """
    This function generates the population from the list of cities. The number of population depends on the
    population size given. Each population is nothing but a list of cities which randomly selected in different orders
    for each iteration.
    :param population_size: Number of population to be generated
    :param cities: List of cities
    :return: List of population
    """
    population = list()
    for pop in range(population_size):
        population.append(router(cities))
    return population


def route_fitness(population):
    """
    This function returns the sorted dictionary of cities over the fitness function.
    :param population: Population generated
    :return: Record or dictionary of cities sorted on fitness value
    """
    fitness_record = dict()
    for pop in range(len(population)):
        fitness_record[pop] = Fitness(population[pop]).fitness_evaluator()
    return sorted(fitness_record.items(), key=operator.itemgetter(1), reverse=True)


def population_selector(population, selection_size):
    """
    This function selects the best members of the given population. This selection happens based on the fitness and
    cumulative sum of the distance to fitness. The number of shortlisted members depends on the selection size.
    :param population: Population input
    :param selection_size: Number of elite squad to be selected from the given population
    :return: list of selected population.
    """
    selected_population = list()
    data_frame = pd.DataFrame(np.array(population), columns=['Index', 'Fitness'])
    data_frame['cumulative_sum'] = data_frame.Fitness.cumsum()
    data_frame['cumulative_per'] = 100*data_frame.cumulative_sum/data_frame.Fitness.sum()

    for size in range(selection_size):
        selected_population.append(population[size][0])

    for size in range(len(population) - selection_size):
        pick = random.random() * 100
        for i in range(len(population)):
            if pick <= data_frame.iat[i, 3]:
                selected_population.append(population[i][0])
                break
    return selected_population


def mating_selector(population, selected_population):
    """
    This function selects the population of the best fit population and the given population to make a crossover or
    mating to produce the next generation of population.
    :param population: Population
    :param selected_population: Selected population or the elite squad
    :return: list of population from which the mating pairs are selected
    """
    mating_population = list()
    for pop in range(len(selected_population)):
        index = selected_population[pop]
        mating_population.append(population[index])
    return mating_population


def breeder(parent1, parent2):
    """
    This function performs the breeding process between to two population units and produces a new offspring.
    :param parent1: Population 1 or parent 1
    :param parent2: Population 2 or parent 2
    :return: newly created population or child
    """
    child, part1, part2 = list(), list(), list()

    gene1 = int(random.random() * len(parent1))
    gene2 = int(random.random() * len(parent1))

    start_gene = min(gene1, gene2)
    end_gene = max(gene1, gene2)

    for gene in range(start_gene, end_gene):
        part1.append(parent1[gene])

    part2 = [item for item in parent2 if item not in part1]

    child = part1 + part2
    return child


def children_creator(mating_population, selection_size):
    """
    The function uses the mating population and creates the list of new population or next generation or the child
    population.
    :param mating_population: Mating population
    :param selection_size: Selection size or the count of elite squad
    :return: list of child population
    """
    children = list()
    diff = len(mating_population) - selection_size
    pool = random.sample(mating_population, len(mating_population))

    for size in range(selection_size):
        children.append(mating_population[size])

    for le in range(diff):
        child = breeder(pool[le], pool[len(mating_population)-le-1])
        children.append(child)
    return children


def population_mutator(population, mutation_rate):
    """
    This function creates the new population based on the mutation rate.
    :param population: Population or current generation
    :param mutation_rate: mutation rate, or production rate of new population
    :return: new generation or new population
    """
    new_population = list()
    for i in range(len(population)):
        mutate_index = mutator(population[i], mutation_rate)
        new_population.append(mutate_index)
    return new_population


def mutator(single, mutation_rate):
    """
    This function is used to mutate the population based on the mutation rate given. Mutation in general means altering
    the population by either removing a part of it or swapping parts of it.
    :param single: population element or a single route of the population list
    :param mutation_rate: mutation rate
    :return: mutated single or population
    """
    for ind in range(len(single)):
        if random.random() < mutation_rate:
            swap_ind = int(random.random()*len(single))

            first = single[ind]
            second = single[swap_ind]

            single[ind] = second
            single[swap_ind] = first
    return single


def next_generation(current_population, elite_size, mutation_rate):
    """
    This function generates the next generation of population. Here we will first select the best members of the given
    population based on the fitness function. The count of best members depends on the value of elite size. A set of
    combinations are performed between these selected population. The process of mutation also happens based on the
    given mutation rate.
    :param current_population: Current population from which a new generation is created
    :param elite_size: elite count of population from the given set
    :param mutation_rate: mutation rate of population
    :return: next generation population list
    """
    fit_population = route_fitness(current_population)
    selected_population = population_selector(fit_population, elite_size)
    mating_population = mating_selector(current_population, selected_population)
    children = children_creator(mating_population, elite_size)
    next_population = population_mutator(children, mutation_rate)
    return next_population


def tsp_by_ga(city_list, population_size=50, elite_size=10, mutation_rate=0.03, generations=20):
    """
    The alpha function, which runs all the show. This function generates the population, formulates the next
    generation, calculates the fitness and returns the best route at the end.
    :param city_list: Cities list for which the best route needs to be found
    :param population_size: Population size
    :param elite_size: Fit members size (The count of members to be picked from the population based on the fitness
    :param mutation_rate: mutation rate to generate the next gen population
    :param generations: number of generations
    :return:
    """
    population = start_population(population_size, city_list)
    print("Initial distance calculated: " + str(1/route_fitness(population)[0][1]))

    for gen in range(generations):
        population = next_generation(population, elite_size, mutation_rate)

    print("Final distance calculated: " + str(1 / route_fitness(population)[0][1]))
    best_route_index = route_fitness(population)[0][0]
    best_route = population[best_route_index]

    return best_route


if __name__ == '__main__':
    my_cities = list()
    for counter in range(10):
        my_cities.append(City(int(random.random() * 200), int(random.random() * 200)))
    print(tsp_by_ga(my_cities, 100, 20, 0.01, 50))
