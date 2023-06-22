import random

import Data
import New

def two_swap(truck_route):
    neighbors = []

    for i in range(len(truck_route)):
        for j in range(i+1, len(truck_route)):
            if truck_route[i]==0 or truck_route[j]==0: continue
            arr=[]
            tmp_state=truck_route[:i]+truck_route[j:j+1]+truck_route[i+1:j]+truck_route[i:i+1]+truck_route[j+1:]
            arr.append(truck_route[i])
            arr.append(truck_route[j])
            arr.append(tmp_state)
            neighbors.append(arr)

    return neighbors

def one_move(solution):
    neighbors = []

    for i in range(len(solution[0])):
        for j in range (i+1, len(solution[0])):
            if solution[0][i]==0 or solution[0][j]==0: continue
            arr=[]
            tmp_state = solution[0][:i]+solution[0][j:j+1]+solution[0][i+1:j]+solution[0][i:i+1]+solution[0][j+1:]
            tmp_state1 = solution[1][:i]+solution[0][j:j+1]+solution[1][i+1:j]+solution[1][i:i+1]+solution[1][j+1:]
            tmp_state1[i] = random.uniform(0, 1)
            tmp_state1[j] = random.uniform(0, 1)
            new_solution = [tmp_state,tmp_state1]
            arr.append(solution[0][i])
            arr.append(solution[0][j])
            arr.append(new_solution)
            arr.append(New.fitness_function(new_solution))
            neighbors.append(arr)

    return neighbors

def two_opt_move(truck_route):
    neighbors = []

    for i in range(len(truck_route)):
        for j in range (i+1, len(truck_route)):
            if truck_route[i]==0 or truck_route[j]==0 or truck_route[i+1]==0 or truck_route[j+1]==0 or truck_route[i+1]==truck_route[j]: continue
            arr=[]
            tmp_state=truck_route[:i]+truck_route[j+1:j+2]+truck_route[i:i+1]+truck_route[i+2:j]+truck_route[i+1:i+2]+truck_route[j:j+1]+truck_route[j+2:]
            arr.append(truck_route[i])
            arr.append(truck_route[i+1])
            arr.append(truck_route[j])
            arr.append(truck_route[j+1])
            arr.append(tmp_state)
            neighbors.append(arr)

    return neighbors
    

truck_route=[1,2,4,7,10,0,5,6,3,0,8,9,0]
#print(two_opt_move(truck_route))