import copy
import math
import random
import numpy
import heapq
import time
import itertools
import collections
file_path = "C101_3.dat"
number_of_trucks = 5
number_of_cities = 0
number_of_drones = 10
truck_speed = 0.3
drone_speed = 0.6
drone_capacity = 4
drone_runtime = 3
city_demand = []
release_date = []
unloading_time = 1/60
manhattan_move_matrix = []
euclid_flight_matrix = []
city = []
def read_data(path):
    global data
    global number_of_cities
    global euclid_flight_matrix
    global manhattan_move_matrix
    global city
    global release_date
    global city_demand
    f = open(path)
    data = f.readlines()
    number_of_cities = int(data[0].split()[1])
    manhattan_move_matrix = [0] * number_of_cities
    for i in range(number_of_cities):
        manhattan_move_matrix[i] = [0] * number_of_cities
    euclid_flight_matrix = [0] * number_of_cities
    for i in range(number_of_cities):
        euclid_flight_matrix[i] = [0] * number_of_cities
    city = []
    for i in range(5, 5 + number_of_cities):
        city.append([])
        line = data[i].split()
        for j in range(0, 2):
            city[i - 5].append(float(line[j]))
    for i in range(number_of_cities):
        for j in range(number_of_cities):
            euclid_flight_matrix[i][j] = euclid_distance(city[i], city[j]) / drone_speed
    euclid_flight_matrix = numpy.array(euclid_flight_matrix)
    for i in range(number_of_cities):
        for j in range(number_of_cities):
            manhattan_move_matrix[i][j] = manhattan_distance(city[i], city[j]) / truck_speed
    manhattan_move_matrix = numpy.array(manhattan_move_matrix)
    release_date = []
    for i in range(5, 5 + number_of_cities):
        release_date.append([])
        line = data[i].split()
        release_date[i - 5] = float(line[-1])
    city_demand = [0] * number_of_cities
    for i in range(1, number_of_cities):
        _ = random.random()
        if _ <= 0.5:
            city_demand[i] = 0.5
        else:
            city_demand[i] = random.uniform(0, 2.27)
    return data

random.seed(1)
def euclid_distance(city1, city2):
    return math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
def manhattan_distance(city1, city2):
    return abs(city1[0] - city2[0]) + abs(city1[1] - city2[1])
read_data(file_path)