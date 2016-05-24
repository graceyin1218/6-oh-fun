from highways import *
from lib601.search import search, SearchNode, PriorityQueue

def path_cost(path):
    #pass # your code here
    cost = 0
    prev = None
    for city in path:
        if prev:
            cost += distance(prev, city)
            prev = city
        else:
            prev = city
    return cost

def highway_successors(state): # state is an id number
    #pass # your code here
    n = neighbors[state]
    ans = []
    for loc in n:
        # for uniform cost search
        ans.append((loc, distance(state,loc)))

        # for bfs
        #ans.append(loc)
    return ans


def uniform_cost_search(successors, start_state, goal_test, heuristic=lambda s: 0):
    if goal_test(start_state):
        return [start_state]
    agenda = PriorityQueue()
    agenda.push(SearchNode(start_state, None, cost=0), heuristic(start_state))
    expanded = set()
    while len(agenda) > 0:
        priority, parent = agenda.pop()
        if parent.state not in expanded:
            expanded.add(parent.state)
            if goal_test(parent.state):
                print("Number of expanded states: " + str(len(expanded)))
                print("Cost of path: " + str(path_cost(parent.path())))
                return parent.path()
            for child_state, cost in successors(parent.state):
                child = SearchNode(child_state, parent, parent.cost+cost)
                if child_state not in expanded:
                    agenda.push(child, child.cost+heuristic(child_state))
    return None


def a_star (successors, start_state, goal_test, heuristic = lambda s: 0, alpha = 0):
    if goal_test(start_state):
        return [start_state]
    agenda = PriorityQueue()
    agenda.push(SearchNode(start_state, None, cost=0), alpha*heuristic(start_state))
    expanded = set()
    while len(agenda) > 0:
        priority, parent = agenda.pop()
        if parent.state not in expanded:
            expanded.add(parent.state)
            if goal_test(parent.state):
                print(str(len(expanded)) + ",")
                #print("Cost of path: " + str(path_cost(parent.path())))
                return parent.path()
            for child_state, cost in successors(parent.state):
                child = SearchNode(child_state, parent, parent.cost+cost)
                if child_state not in expanded:
                    agenda.push(child, (1-alpha)*child.cost+alpha*heuristic(child_state))
    return None


def breadth_first_search(successors, start_state, goal_test):
    return search(successors, start_state, goal_test)

