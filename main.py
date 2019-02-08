# DFS-Astar-Search
# @Author: AndyKang98
# Python 2.7

import copy
from heapq import heappop, heappush

class State:
    """ Each state represent cameras placed on the field
    
    Attributes:
        add_camera (void): add a new camera to the state with the score, level, camera lists updated
        invalid (boolean): check whether the new_camera has conflict with the current placed cameras in this state
        duplicate (boolean): check whether the updated camera lists will be the same solution in explored set
        goal_estimate (int): f(n) to estimate the "potential max score" for a status, used in A* Search
    """ 
    def __init__(self): 
        self.level = 0
        self.camera = set()
        self.score = 0
    
    def add_camera(self, parent_state, new_camera, ANIMALS):
        self.level = parent_state.level + 1
        self.score = parent_state.score
        self.camera = copy.copy(parent_state.camera)
        self.camera.add(new_camera)
        if new_camera in ANIMALS:
            self.score += 1                         

    def invalid(self, new_camera):
        for i in self.camera:
            if i[0] == new_camera[0] or i[1] == new_camera[1] or abs(i[0]-new_camera[0]) == abs(i[1]-new_camera[1]):
                return True
        return False
    
    def duplicate(self, new_camera, explored_set):
        if self.camera.union({new_camera}) in explored_set:
            return True
        
    def goal_estimate(self, C, A):
        return -(self.score + min(C-self.level, A-self.score))

class DFS:
    """ DFS Search method - depth first search all possible states and select the solution with max score
    
    Attributes:
        DFS (int): run DFS and return the max score
    """
    def __init__(self):
        self.max_score = 0
        self.explored_set = set()
 
    def DFS_vist(self, N, C, ANIMALS, parent_state):
        for i in range(N):
            for j in range(N):
                if parent_state.invalid((i,j)) or parent_state.duplicate((i,j), self.explored_set):
                    continue
                new_state = State()
                new_state.add_camera(parent_state, (i,j), ANIMALS)
                self.explored_set.add(frozenset(new_state.camera))

                if new_state.level >= C:
                    if new_state.score > self.max_score:
                        self.max_score = new_state.score
                    return

                self.DFS_vist(N, C, ANIMALS, new_state)
        return self.max_score


def AStar(N, C, A, ANIMALS, initial_state):
    """ A* Search method - explore next sates according to the "potntial", select the first best solution with
    Args:
        N - size of the field
        C - number of cameras
        A - number of animals
        ANIMALS - positions of animals
        initial_state - initial state
    Returs:
        max_score - the score of the first best solution
    """
    h = []
    heappush(h, (initial_state.goal_estimate(C, A), initial_state))
    explored_set = set()
    
    while True:
        if len(h)==0: return "Fail"
        parent_state = heappop(h)[1]
        if parent_state.level >= C:
            return parent_state.score
        
        for i in range(N):
            for j in range(N):
                if parent_state.invalid((i,j)) or parent_state.duplicate((i,j), explored_set):
                    continue
                new_state = State()
                new_state.add_camera(parent_state, (i,j), ANIMALS)
                heappush(h, (new_state.goal_estimate(C, A), new_state))
                explored_set.add(frozenset(new_state.camera))

                
def Read_input(filename):
    lines = open(filename + ".txt").read().splitlines()
    N = int(lines[0])
    C = int(lines[1])
    A = int(lines[2])
    SEARCH = lines[3]
    ANIMALS = set()
    for i in lines[4:]:
        ANIMALS.add(eval(i))
    return N, C, A, SEARCH, ANIMALS


def Write_output(max_score):
    output_file = open("output.txt","w")
    output_file.write(str(max_score))
    output_file.close()


if __name__ == "__main__":
    N, C, A, SEARCH, ANIMALS = Read_input("input")

    initial_state = State()
    max_score = 0

    if SEARCH == "dfs":
        max_score = DFS().DFS_vist(N, C, ANIMALS, initial_state)
    elif SEARCH == "astar":
        max_score = AStar(N, C, A, ANIMALS, initial_state)

    Write_output(max_score)