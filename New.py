import copy
import math
import random
import numpy
import queue
import time

import Data

def intial_solution():
    route = []
    restrict = [0]*Data.number_of_trucks
    for i in range(Data.number_of_trucks):
        route.append([])
    r_d =[]
    for i in range(len(Data.release_date)):
        r_d.append([i, Data.release_date[i]])
    r_d = sorted(r_d,key = lambda r_d: r_d[1])
    r_d.pop(0)
    for i in range(Data.number_of_trucks):
        route[i].append(r_d[0][0])
#       crd.append(r_d[i][0])
        r_d.pop(0)
    for i in range(Data.number_of_trucks+1,Data.number_of_cities):
        index = -1
        min = 10000000
        ''' if crd.count(r_d[i]) != 0:
            r_d1 = copy.copy(Data.release_date)
            for p in range(crd.count(r_d[i])):
                r_d1.remove(r_d[i])
            next_customer_add = r_d1.index(r_d[i])
        else:
            next_customer_add = Data.release_date.index(r_d[i])'''
        next_customer_add = r_d[0][0]
        for j in range(Data.number_of_trucks):
            if Data.manhattan_move_matrix[route[j][len(route[j])-1]][next_customer_add] < min and i-restrict[j] > Data.number_of_trucks-1:
 #              min = truck_matrix[route[j][len(route[j])-1]][next_customer_add]
                index = j
        restrict[index] = i
        route[index].append(r_d[0][0])
        r_d.pop(0)
    route2 = []
    for i in route:
        receive_address = []
        for j in range(len(i)):
            a = j/len(i)
            add = random.uniform(a*0.5, a)
            receive_address.append(add)
        route2.append(receive_address)
    new_route1 = []
    new_route2 = []
    for i in range(Data.number_of_trucks):
        new_route1 +=  route[i] + [0]
        new_route2 += route2[i] +[0.0]
    new_route1.pop()
    new_route2.pop()
    solution = [new_route1, new_route2]
    return solution


def convert(solution):
    sol = []
    temp = []
    for i in range(len(solution[0])):
        if solution[0][i] != 0:
            temp.append([solution[0][i], solution[1][i]])
        else:
            sol.append(temp)
            temp = []
    sol.append(temp)
    for i in range(len(sol)):
        sol[i].insert(0,[0,0])
        for j in range(1, len(sol[i])):
            sol[i][j][1] = sol[i][int(sol[i][j][1] * (j+1))][0]
    result = copy.deepcopy(sol)
    for i in range(len(result)):
        for j in range(len(result[i])):
            result[i][j][1] = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            for k in range(1, len(sol[i])):
                if sol[i][k][1] == result[i][j][0]:
                    result[i][j][1].append(sol[i][k][0])
    return result

def max_release_date(point):
    if point == []: return 0
    array = []
    for i in range(len(point)):
        array.append(Data.release_date[point[i]])
    return max(array)

def sum_weight(package):
    sum = 0
    for i in range(len(package)):
        sum = sum + Data.city_demand[package[i]]
    return sum

def package_in_which_truck(solution, package):
    for i in range(len(solution)):
        for j in range(1, len(solution[i])):
            if solution[i][j][0] == package: return i

def sorted_by_release_date(package):
    array = []
    for i in range(len(package)):
        array.append([Data.release_date[package[i]], package[i]])
    sortt = sorted(array, key = lambda x:x[0])
    array = []
    for i in range(len(package)):
        array.append(sortt[i][1])
    return array

def find_drone_flight_route(truck_position):
    path = []
    current_point = 0
    while len(truck_position) != 0:
        next_point = 0
        current_len = pow(10, Data.number_of_cities)
        for i in range(len(truck_position)):
            if Data.euclid_flight_matrix[current_point][truck_position[i]] <= current_len:
                current_len = Data.euclid_flight_matrix[current_point][truck_position[i]]
                next_point = truck_position[i]
        current_point = next_point
        path.append(current_point)
        truck_position.remove(current_point)
    return path

def init_solution(solution):
    solution = convert(solution)
    #Declare
    drone_package = []
    truck_time = [0]*Data.number_of_trucks
    truck_position = []
    temp = []
    for i in range(len(solution)):
        for j in range(0, len(solution[i])):
            temp.append(solution[i][j][0])
        temp.append(0)
        truck_position.append(temp)
        temp = []

    truck_current_point = [0]*Data.number_of_trucks
    drone_queue = queue.PriorityQueue()
    for i in range(0, Data.number_of_drones):
        drone_queue.put((0, "Drone %i" % i))
    compare = [0]* Data.number_of_trucks

    #Decode

    #Truck move from depot
    for i in range(Data.number_of_trucks):
        '''print("Truck", i, "move from", truck_position[i][truck_current_point[i]], "to", truck_position[i][truck_current_point[i] + 1])'''
        truck_time[i] = max_release_date(solution[i][truck_position[i][truck_current_point[i]]][1]) + \
                                Data.manhattan_move_matrix[truck_position[i][truck_current_point[i]]][truck_position[i][truck_current_point[i] + 1]]
        solution[i][truck_current_point[i]][1] = []
        truck_current_point[i] = truck_current_point[i] + 1
    #Truck and drone move
    while True:
        number = 0
        for i in range(Data.number_of_trucks):
            if truck_position[i][truck_current_point[i]] == 0:
                number = number + 1
        if number == Data.number_of_trucks: break
        for i in range(Data.number_of_trucks):
            while solution[i][truck_current_point[i]][1] == []:
                if truck_position[i][truck_current_point[i]] == 0: break

                '''print("Truck", i, "move from", truck_position[i][truck_current_point[i]], "to", truck_position[i][truck_current_point[i] + 1])'''
                truck_time[i] = truck_time[i] + Data.manhattan_move_matrix[truck_position[i][truck_current_point[i]]][truck_position[i][truck_current_point[i] + 1]]

                if truck_position[i][truck_current_point[i] + 1] != 0:
                    truck_current_point[i] = truck_current_point[i] + 1
                else:
                    truck_current_point[i] = 0
                    break
            if truck_position[i][truck_current_point[i]] == 0: compare[i] = 999999
            else:
                temp = []
                size = 0
                fake = sorted_by_release_date(solution[i][truck_current_point[i]][1])
                for j in range(len(fake)):
                    size = size + Data.city_demand[fake[j]]
                    if size <= Data.drone_capacity:
                        temp.append(fake[j])
                compare[i] = max(max_release_date(temp),
                             truck_time[i] - Data.euclid_flight_matrix[0, truck_position[i][truck_current_point[i]]])
        number = 0
        for i in range(Data.number_of_trucks):
            if truck_position[i][truck_current_point[i]] == 0:
                number = number + 1
        if number == Data.number_of_trucks: break
        index = 0
        best = compare[index]
        for i in range(Data.number_of_trucks):
            if compare[i] <= best:
                index = i
                best = compare[index]
        drone = drone_queue.get()
        start = max(drone[0], best)
        temp = []
        size = 0
        fake = sorted_by_release_date(solution[index][truck_current_point[index]][1])
        for j in range(len(fake)):
            size = size + Data.city_demand[fake[j]]
            if size <= Data.drone_capacity:
                temp.append(fake[j])
        '''print(drone[1], "flight from 0 to", truck_position[index][truck_current_point[index]], "bring package", temp)'''
        drone_package.append(temp)
        for j in range(len(temp)):
            solution[index][truck_current_point[index]][1].remove(temp[j])
        drone_queue.put((start + 2*Data.euclid_flight_matrix[truck_position[index][truck_current_point[index]]][0], drone[1]))
        '''print(drone[1], "flight from", truck_position[index][truck_current_point[index]], "to 0")'''
        num = 0
        while solution[index][truck_current_point[index]][1] == []:
            if truck_position[index][truck_current_point[index]] == 0: break
            '''print("Truck", index, "move from", truck_position[index][truck_current_point[index]], "to", truck_position[index][truck_current_point[index] + 1])'''
            if num == 0:
                truck_time[index] = max(truck_time[index], start) + \
                                    Data.euclid_flight_matrix[truck_position[index][truck_current_point[index]]][0] +\
                                    Data.manhattan_move_matrix[truck_position[index][truck_current_point[index]]][truck_position[index][truck_current_point[index] + 1]]
            else:
                truck_time[index] = truck_time[index] + \
                                    Data.euclid_flight_matrix[truck_position[index][truck_current_point[index]]][0] + \
                                    Data.manhattan_move_matrix[truck_position[index][truck_current_point[index]]][truck_position[index][truck_current_point[index] + 1]]
            if truck_position[index][truck_current_point[index] + 1] != 0:
                truck_current_point[index] = truck_current_point[index] + 1
            else:
                truck_current_point[index] = 0
                break
            num = num + 1
    return max(truck_time), drone_package

def fitness(solution, drone_order):
    drone_package = copy.copy(drone_order)
    solution = convert(solution)
    #Declare
    truck_time = [0] * Data.number_of_trucks
    truck_position = []
    temp = []
    for i in range(len(solution)):
        for j in range(0, len(solution[i])):
            temp.append(solution[i][j][0])
        temp.append(0)
        truck_position.append(temp)
        temp = []
#    print(truck_position)
    truck_current_point = [0] * Data.number_of_trucks
    drone_queue = queue.PriorityQueue()
    for i in range(0, Data.number_of_drones):
        drone_queue.put((0, "Drone %i" % i))
    compare = [0] * Data.number_of_trucks
    #Decode

    #Truck move form depot
    for i in range(Data.number_of_trucks):
        '''print("Truck", i, "move from", truck_position[i][truck_current_point[i]], "to", truck_position[i][truck_current_point[i] + 1])'''
        truck_time[i] = max_release_date(solution[i][truck_position[i][truck_current_point[i]]][1]) + \
                                Data.manhattan_move_matrix[truck_position[i][truck_current_point[i]]][truck_position[i][truck_current_point[i] + 1]]
        solution[i][truck_current_point[i]][1] = []
        truck_current_point[i] = truck_current_point[i] + 1
    '''print("from depot:", truck_time)'''
    #Truck and drone move
    while True:
        for i in range(Data.number_of_trucks):
            while solution[i][truck_current_point[i]][1] == []:
                if truck_position[i][truck_current_point[i]] == 0: break

                '''print("Truck", i, "move from", truck_position[i][truck_current_point[i]], "to", truck_position[i][truck_current_point[i] + 1])'''
                truck_time[i] = truck_time[i] + Data.manhattan_move_matrix[truck_position[i][truck_current_point[i]]][
                    truck_position[i][truck_current_point[i] + 1]]

                if truck_position[i][truck_current_point[i] + 1] != 0:
                    truck_current_point[i] = truck_current_point[i] + 1
                else:
                    truck_current_point[i] = 0
                    break
        number = 0
        for i in range(Data.number_of_trucks):
            if truck_position[i][truck_current_point[i]] == 0:
                number = number + 1
        if number == Data.number_of_trucks: break
        drone_pack = drone_package[0]
        position = []
        for i in range(len(drone_pack)):
            if (package_in_which_truck(solution, drone_pack[i]) in position) == False:
                position.append(package_in_which_truck(solution, drone_pack[i]))
        position = find_drone_flight_route(position)
        drone_package.pop(0)
        drone = drone_queue.get()
        start = max(drone[0], max_release_date(drone_pack))
        for i in range(len(position)):
            deliver = []
            for j in range(len(drone_pack)):
                if package_in_which_truck(solution, drone_pack[j]) == position[i]:
                    deliver.append(drone_pack[j])
            if i == 0:
                '''print(drone[1], "flight from 0 to", truck_position[position[i]][truck_current_point[position[i]]],
                  "bring package", drone_pack, "deliver", deliver)'''
                start = start + Data.euclid_flight_matrix[0][truck_position[position[i]][truck_current_point[position[i]]]]
            else:
                '''print(drone[1], "flight from", truck_position[position[i-1]][truck_current_point[position[i-1]]],
                      "to", truck_position[position[i]][truck_current_point[position[i]]],
                      "bring package", drone_pack, "deliver", deliver)'''
                start = start + Data.euclid_flight_matrix[truck_position[position[i-1]][truck_current_point[position[i-1]]]][truck_position[position[i]][truck_current_point[position[i]]]]
            for j in range(len(deliver)):
                for k in range(Data.number_of_trucks):
                    for l in range(truck_current_point[k], len(solution[k])):
                        if deliver[j] in solution[k][l][1]:
                            solution[k][l][1].remove(deliver[j])
                            break
            num = 0
            while solution[position[i]][truck_current_point[position[i]]][1] == []:
                if truck_position[position[i]][truck_current_point[position[i]]] == 0: break
                '''print("Truck", position[i], "move from", truck_position[position[i]][truck_current_point[position[i]]],
                      "to", truck_position[position[i]][truck_current_point[position[i]] + 1])'''
                if num == 0:
                    truck_time[position[i]] = max(truck_time[position[i]], start) + \
                                              Data.manhattan_move_matrix[
                                                  truck_position[position[i]][truck_current_point[position[i]]]][
                                                  truck_position[position[i]][truck_current_point[position[i]] + 1]]
                else:
                    truck_time[position[i]] = truck_time[position[i]] + \
                                              Data.manhattan_move_matrix[
                                                  truck_position[position[i]][truck_current_point[position[i]]]][
                                                  truck_position[position[i]][truck_current_point[position[i]] + 1]]
                num = num + 1
                if truck_position[position[i]][truck_current_point[position[i]] + 1] != 0:
                    truck_current_point[position[i]] = truck_current_point[position[i]] + 1
                else:
                    truck_current_point[position[i]] = 0
                    break
        end = start + Data.euclid_flight_matrix[truck_position[position[-1]][truck_current_point[position[-1]]]][0]
        drone_queue.put((end, drone[1]))
        '''print(drone[1], "flight from", truck_position[position[-1]][truck_current_point[position[-1]]], "to 0")
        print("nah",truck_time)'''
    return (truck_time)

def split(solution, drone_package, index):
    split_array = []
    temp = []
    for i in range(len(drone_package[index]) - 1):
        temp = copy.copy(drone_package)
        temp.insert(index + 1, drone_package[index][:i+1])
        temp.insert(index + 2, drone_package[index][i+1:])
        temp.pop(index)
        split_array.append(temp)
    variable = fitness(solution, drone_package)
    first_value = max(variable)
    current_sum = 0
    for j in range(Data.number_of_trucks):
        current_sum = current_sum + variable[j]
    value = first_value
    init = drone_package
    current = drone_package
    for i in range(len(split_array)):
        cp = fitness(solution, split_array[i])
        summ = 0
        for j in range(Data.number_of_trucks):
            summ = summ + cp[j]
        if (value > max(cp)) or ((value >= max(cp)) and (summ < current_sum)):
            value = max(cp)
            current = split_array[i]
            current_sum = summ
    a = True
    if current != init: a = False
    return current, value, a

def change(solution, drone_package, index):
    change_array = []
    temp = []
    length = len(drone_package[index])
    for i in range(length):
        temp = copy.deepcopy(drone_package)
        size = sum_weight(drone_package[index + 1])
        for j in range(length - i - 1, length):
            if size + Data.city_demand[drone_package[index][j]] > Data.drone_capacity: break
            temp[index+1].append(drone_package[index][j])
            temp[index].remove(drone_package[index][j])
        if temp[index] == []: temp.pop(index)
        change_array.append(temp)
    variable = fitness(solution, drone_package)
    first_value = max(variable)
    current_sum = 0
    for j in range(Data.number_of_trucks):
        current_sum = current_sum + variable[j]
    value = first_value
    init = drone_package
    current = drone_package
    for i in range(len(change_array)):
        cp = fitness(solution, change_array[i])
        summ = 0
        for j in range(Data.number_of_trucks):
            summ = summ + cp[j]
        if (value > max(cp)) or ((value >= max(cp)) and (summ < current_sum)):
            value = max(cp)
            current = change_array[i]
            current_sum = summ
    a = True
    if current != init : a = False
    return current, value, a

def fitness_function(solution):
    drone_package = init_solution(solution)[1]
#    print(solution[0])
    value = fitness(solution, drone_package)
    test_split = 1
    test_change = 1
    num = 0
    while test_split != 0 or test_change != 0:
        num = num + 1
        for i in range(len(drone_package)):
            temp = split(solution, drone_package, i)
            if temp[2] == False:
                drone_package = temp[0]
                value = [temp[1]]
                break
            if i == len(drone_package) - 1:
                test_split = 0
        for i in range(len(drone_package) - 1):
            temp = change(solution, drone_package, i)
            if temp[2] == False:
                drone_package = temp[0]
                value = [temp[1]]
                break
            if i == len(drone_package) - 2:
                test_change = 0

    return max(value)

#Run run
'''truck_route = [1,3,5,6,7,0,2,4,8,0,9,10]
drone_route = [0.4,0.5,0.8,0.75,0.15,0.9,0.3,0.25,0.65,0.7,0.13,0.45]
#hehe = [truck_route, drone_route]
#print(intial_solution())
hehe = intial_solution()


truck_route = [1,2,0,5,3,4,7,6,0,10,8,9]
drone_route = [0.1,0.2,0.15,0.14,0.2,0.3,0.45,0.5,0.6,0.1,0.2,0.8]

truck_route=[20,1,27,11,16,21,5,7,22,14,2,4,29,0,6,23,10,26,3,13,15,9,18,19,30,28,12,17,24,8,0,25]
drone_route=[0.8,0.45,0.2,0.6,0.9,0.1,0.4,0.6,0.85,0.9,0.15,0.65,0.7,0.05,0.075,0.8,0.8,0.3,0.22,0.4,0.1,0.4,0.85,0.2,0.1,0.45,0.9,0.15,0.2,0.6,0.85,0.44]
hehe = [truck_route, drone_route]
print("convert", convert(hehe))
start_time = time.time()
for i in range(1):
    print("init is:", init_solution(hehe))
    print("fitness is:", fitness(hehe, init_solution(hehe)[1]))
    print("fitness is:", fitness_function(hehe))
end_time = time.time()
timeee = end_time - start_time
print("Time is: ", timeee)
print("Fitness is: ", fitness_function(hehe))'''
#print(convert(hehe))