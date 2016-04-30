from collections import deque

def search(successors, start_state, goal_test, dfs = False, dp=True):
    if goal_test(start_state):
        return [start_state]
    else:
        agenda = deque([(start_state, None)])
        visited = {start_state}
        while len(agenda) > 0:
            if dfs:
                parent = agenda.pop()
            else:
                parent = agenda.popleft()
            for child_state in successors(parent[0]):
                child = (child_state, parent)
                if goal_test(child_state):
                    return _get_path(child)
                if ((dp and child_state not in visited) or
                    ((not dp) and child_state not in _get_path(parent))):
                    agenda.append(child)
                    visited.add(child_state)
        return None

def _get_path(node):
    if node is None:
        return []
    path = []
    current, parent = node
    while parent is not None:
        path.append(current)
        node = parent
        current, parent = node
    return path[::-1]
