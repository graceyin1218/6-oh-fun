import heapq

class SearchNode:
    def __init__(self, state, parent, cost = 0.):
        self.state = state
        self.parent = parent
        self.cost = cost

    def path(self):
        p = []
        node = self
        while node:
            p.append(node.state)
            node = node.parent
        return p[::-1]

    def __repr__(self):
        return '->'.join([str(state) for state in self.path()])


def uniform_cost_search(successors, startState, goalTest, heuristic=lambda s: 0):
    if goalTest(startState):
        return [startState]
    agenda = [(SearchNode(startState, None, cost=0), heuristic(startState))]
    expanded = set()
    while len(agenda) > 0:
        agenda.sort(key=lambda x: x[1])
        parent, priority = agenda.pop(0)
        if parent.state not in expanded:
            expanded.add(parent.state)
            if goalTest(parent.state):
                return parent.path()
            for childState, cost in successors(parent.state):
                child = SearchNode(childState, parent, parent.cost+cost)
                if childState not in expanded:
                    agenda.append((child, child.cost+heuristic(childState)))
    return None
