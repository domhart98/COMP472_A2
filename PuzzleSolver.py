import copy
import heapq
import os
from dataclasses import dataclass, field
import time
from datetime import datetime
from queue import PriorityQueue, Queue
from threading import Timer

#Class representing a node
class Node():

    def __lt__(self, other):
        return self.path_cost < other.path_cost

    def state(self):
        return self.state

    #return solution path
    def path(self):
        node, p = self, []
        while node:
            p.append(node)
            node = node.parent
        return list(reversed(p))

    #determine possible actions based on location of the hole(0)
    def actions(self,state):

        global possible_actions
        possible_actions = {"up": 1, "down": 1, "left": 1, "right": 1, "left_wrap": 2, "right_wrap": 2, "wrap_diag": 3,
                            "left_up_diag": 3, "left_down_diag": 3, "right_up_diag": 3, "right_down_diag": 3}

        if self.state.index(0) == 0:
            possible_actions.pop("left")
            possible_actions.pop("left_wrap")
            possible_actions.pop("left_down_diag")
            possible_actions.pop("left_up_diag")
            possible_actions.pop("right_up_diag")
        elif self.state.index(0) == 4:
            possible_actions.pop("left")
            possible_actions.pop("left_wrap")
            possible_actions.pop("left_down_diag")
            possible_actions.pop("left_up_diag")
            possible_actions.pop("right_down_diag")
        elif self.state.index(0) == 3:
            possible_actions.pop("right")
            possible_actions.pop("right_wrap")
            possible_actions.pop("right_down_diag")
            possible_actions.pop("right_up_diag")
            possible_actions.pop("left_up_diag")
        elif self.state.index(0) == 7:
            possible_actions.pop("right")
            possible_actions.pop("right_wrap")
            possible_actions.pop("right_down_diag")
            possible_actions.pop("right_up_diag")
            possible_actions.pop("left_down_diag")
        else:
            possible_actions.pop("wrap_diag")
            possible_actions.pop("left_wrap")
            possible_actions.pop("right_wrap")
            possible_actions.pop("right_down_diag")
            possible_actions.pop("right_up_diag")
            possible_actions.pop("left_down_diag")
            possible_actions.pop("left_up_diag")

        if self.state.index(0) == 0 or self.state.index(0) == 1 or self.state.index(0) == 2 or self.state.index(0) == 3:
            possible_actions.pop("up")

        elif self.state.index(0) == 4 or self.state.index(0) == 5 or self.state.index(0) == 6 or self.state.index(0) == 7:
            possible_actions.pop("down")

        return possible_actions

    #swap positions of 2 elements of a list
    def swap_pos(self, pos1, pos2):
        temp = self.state[pos1]
        self.state[pos1] = self.state[pos2]
        self.state[pos2] = temp
        return

    #calls swap_pos() to alter the state, depending on which action is selected
    def result(self, state, action):

        if action == "up":
            self.swap_pos(self.state.index(0), self.state.index(0) - 4)
        elif action == "down":
            self.swap_pos(self.state.index(0), self.state.index(0) + 4)
        elif action == "left":
            self.swap_pos(self.state.index(0), self.state.index(0) - 1)
        elif action == "right":
            self.swap_pos(self.state.index(0), self.state.index(0) + 1)
        elif action == "left_wrap":
            self.swap_pos(self.state.index(0), self.state.index(0) - 3)
        elif action == "right_wrap":
            self.swap_pos(self.state.index(0), self.state.index(0) + 3)
        elif action == "wrap_diag":
            self.swap_pos(self.state.index(0), 17 % (self.state.index(0) + 10))
        elif action == "left_up_diag":
            self.swap_pos(self.state.index(0), self.state.index(0) - 5)
        elif action == "left_down_diag":
            self.swap_pos(self.state.index(0), self.state.index(0) + 3)
        elif action == "right_up_diag":
            self.swap_pos(self.state.index(0), self.state.index(0) - 3)
        elif action == "right_down_diag":
            self.swap_pos(self.state.index(0), self.state.index(0) + 5)

        return self.state

    def __init__(self, state, path_cost, parent, move, action=0, goal1=[1,2,3,4,5,6,7,0], goal2=[1,3,5,7,2,4,6,0]):
        self.state = state
        self.parent = parent
        self.action = action
        self.move = move
        self.path_cost = path_cost
        self.goal1 = goal1
        self.goal2 = goal2
        if parent:
            self.path_cost = self.path_cost + action

    #manhattan distance heuristic
    def Heuristic2(self, goal1, goal2):
        manhattan_distance1 = 0
        manhattan_distance2 = 0
        board = self.state
        for i in board:

            manhattan_distance1 += abs(board.index(i) - goal1.index(i))
            manhattan_distance2 += abs(board.index(i) - goal2.index(i))
        return min(manhattan_distance1, manhattan_distance2)

    #hamming distance heuristic
    def Heuristic1(self, goal1, goal2):
        hamming_distance1 = 0
        hamming_distance2 = 0
        board = self.state
        for i in board:
            if board.index(i) != goal1.index(i):
                hamming_distance1 = hamming_distance1 + 1
            if board.index(i) != goal2.index(i):
                hamming_distance2 = hamming_distance2 + 1
        return min(hamming_distance1, hamming_distance2)


class SetQueue(Queue):

    def _init(self,maxsize):
        Queue._init(self,maxsize)
        self.all_items = set()

    def _put(self, item):
        if item not in self.all_items:
            Queue._put(self, item)
            self.all_items.add(item)

#create tuple which contains node object and priority value.
@dataclass(order=True)
class PrioritizedItem:
    item: object = field()
    priority: int



#Exit function. If this is called, 60s have passed without finding a soln.
def exitfunc():
    with open('0' + algo + '_solution.txt', 'w') as f:
        f.write("No solution found")
    with open('0' + algo + '_search.txt', 'w') as f:
         f.write("No solution found")
    os._exit(0)

#call exit function after 60s
Timer(30000, exitfunc).start() # exit in 60 seconds
start_time = time.time()


algo = input("Select search algorithm (UCS, GBF-H1, GBF-H2, ASTAR-H1, ASTAR-H2):\n")




#set initial state and search algorithm
x = [2,6,4,0,5,1,3,7]
algo = "ASTAR-H1"


#create initial node
init_puzzle = Node(x,0,None,0)
#Create priority queue to hold the nodes that have not yet been visited.
frontier = PriorityQueue()

#if UCS, priority is path_cost.
#if GBF, priority is h(n)
#if ASTAR, priority is h(n) + path_cost
if algo == "UCS":
    frontier.put(PrioritizedItem(init_puzzle, init_puzzle.path_cost))
elif algo == "GBF-H1":
    frontier.put(PrioritizedItem(init_puzzle, init_puzzle.Heuristic1(init_puzzle.goal1,init_puzzle.goal2)))
elif algo == "GBF-H2":
    frontier.put(PrioritizedItem(init_puzzle, init_puzzle.Heuristic2(init_puzzle.goal1,init_puzzle.goal2)))
elif algo == "ASTAR-H1":
    frontier.put(PrioritizedItem(init_puzzle, (init_puzzle.Heuristic1(init_puzzle.goal1, init_puzzle.goal2) + init_puzzle.path_cost)))
elif algo == "ASTAR-H2":
    frontier.put(PrioritizedItem(init_puzzle, (init_puzzle.Heuristic2(init_puzzle.goal1, init_puzzle.goal2) + init_puzzle.path_cost)))

#Create normal queue to hold the nodes that hav not yet been explored
explored = SetQueue()
#Generate child nodes
y = frontier.get()
explored.put(y.item)

#search until state reaches either goal1 or goal2
while (y.item.state != y.item.goal1) and (y.item.state != y.item.goal2):
    y.item.actions(y.item.state)
    #generate child nodes of y
    for key,value in possible_actions.items():
        #copy node y to x, so we can manipulate x without changing y
        x = copy.deepcopy(y.item)
        child = Node(x.result(x.state, key), x.path_cost, y.item, x.state.index(0), value)
        if algo == "UCS":
            frontier.put(PrioritizedItem(child, child.path_cost))
        elif algo == "GBF-H1":
            frontier.put(PrioritizedItem(child, child.Heuristic1(child.goal1, child.goal2)))
        elif algo == "GBF-H2":
            frontier.put(PrioritizedItem(child, child.Heuristic2(child.goal1, child.goal2)))
        elif algo == "ASTAR-H1":
            frontier.put(PrioritizedItem(child, (child.Heuristic1(child.goal1, child.goal2) + child.path_cost)))
        elif algo == "ASTAR-H2":
            frontier.put(PrioritizedItem(child, (child.Heuristic2(child.goal1, child.goal2) + child.path_cost)))

    #get new y from queue, should have the lowest value for priority
    y = frontier.get()
    explored.put(y.item)



#write data to files
with open('667'+algo+'_solution.txt', 'w') as f:
    for item in y.item.path():
        f.write("%d %d %s\n" % (item.action, item.move , item.state))

    f.write("%d %f" %( y.item.path_cost, (time.time() - start_time)))

with open('667'+algo+'_search.txt', 'w') as f:
    for item in y.item.path():
        f.write("%d %d %d %s\n" % (item.Heuristic2(item.goal1,item.goal2) + item.path_cost, item.Heuristic2(item.goal1,item.goal2), item.path_cost, item.state))

    f.write("%d %f" %( y.item.path_cost, (time.time() - start_time)))
