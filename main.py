import Data
import New
import random
import Neighbors

global LOOP
global tabu_tenure
global best_sol
global best_fitness

tabu_tenure = 5
LOOP = 3

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


'''
hehe=intial_solution()
tabu_structure =[]
for i in range(Data.number_of_trucks):
    arr=[-5]*Data.number_of_cities
best_solution = hehe;
best_fitness = 


for i in range(LOOP):








print(New.fitness_function(hehe))'''

def Tabu_search_for_CVRP():
    global Tabu_Structure
    Tabu_Structure = []
    for i in range(Data.number_of_cities):
        row = [tabu_tenure * (-1)] * Data.number_of_cities
        Tabu_Structure.append(row)
    current_sol = intial_solution()
    current_fitness = New.fitness_function(current_sol)
    best_sol = current_sol
    best_fitness = current_fitness
    for i in range(LOOP):
        print(i)
        current_neighbourhood = Neighbors.one_move(current_sol)
        index = -1;
        min = 100000000
        for j in range(len(current_neighbourhood)):
            cfnode = current_neighbourhood[j][3]
            if cfnode < best_fitness:
                min = cfnode
                index = j
                best_fitness = cfnode
                best_sol = current_neighbourhood[j][2]

            elif (cfnode < min and Tabu_Structure[current_neighbourhood[j][1]][current_neighbourhood[j][0]] + tabu_tenure <= i):

                min = cfnode
                index = j
        current_sol = current_neighbourhood[index][2]
        Tabu_Structure[current_neighbourhood[index][1]][current_neighbourhood[index][0]] = i
    return best_fitness

hehe = intial_solution()
print(New.fitness_function(hehe))
print(Tabu_search_for_CVRP())
