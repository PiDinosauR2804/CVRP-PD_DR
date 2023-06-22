import copy
import random

global number_of_customer
#number_of_customer = 5
global drone_matrix
global truck_matrix
global release_date
global drone_capicity
global number_of_drone
global number_of_truck
global weight_customer

truck_matrix =[[1,3,4,6,7],[2,4,6,8,9],[3,4,7,9,8],[1,2,3,4,5],[4,7,9,2,1]]
number_of_customer = 4
number_of_truck = 3
number_of_drone = 2
release_date = [0,43,4,5,98]
drone_capicity = 10
weight_customer = [3,6,2,7,9]


def intial_solution():
    route = []
    crd = []
    restrict = [0]*number_of_truck
    for i in range(number_of_truck):
        route.append([])
    r_d = copy.copy(release_date)
    r_d.sort()
    for i in range(1,number_of_truck+1):
        route[i-1].append(release_date.index(r_d[i]))
        crd.append(r_d[i])
    for i in range(number_of_truck+1,number_of_customer+1):
        index = -1
        min = 10000000
        if crd.count(r_d[i]) != 0:
            r_d1 = copy.copy(release_date)
            for p in range(crd.count(r_d[i])):
                r_d1.remove(r_d[i])
            next_customer_add = r_d1.index(r_d[i])
        else:
            next_customer_add = release_date.index(r_d[i])
        for j in range(number_of_truck):
            if truck_matrix[route[j][len(route[j])-1]][next_customer_add] < min and i-restrict[j] > number_of_truck/2:
 #              min = truck_matrix[route[j][len(route[j])-1]][next_customer_add]
                index = j
        restrict[index] = i
        route[index].append(i)
        crd.append(r_d[i])
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
    for i in range(number_of_truck):
        new_route1 +=  route[i] + [0]
        new_route2 += route2[i] +[0.0]

    return new_route1,new_route2

def find_neighborhood(route1,route2):
    neighborhood = []
    for i in range(len(route1)):
        if route1[i] == 0: continue
        for j in range(i+1,len(route1)):
            if route1[j] == 0: continue
            offspring = []
            new_route = route1[:i]+route1[j:j+1]+route1[i+1:j]+route1[i:i+1]+route1[j+1:]
            offspring.append(route1[i])
            offspring.append(route1[j])
            offspring.append(new_route)
            offspring.append(fitness(new_route,route2))
            neighborhood.append(offspring)
    return neighborhood

def fitness(route1, route2):
    return 1

print(intial_solution())
a,b = intial_solution()

print(len(b))
print(b)
print(find_neighborhood(a, b))
print("Hello")













