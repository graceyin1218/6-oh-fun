import maps
import highways

costs = []
#expanded = []

for i in range(101):
    a = i*0.01
    s = maps.a_star(maps.highway_successors, 6002971, lambda x: x == 25000502, lambda x: highways.distance(25000502, x), a)
    costs.append(maps.path_cost(s))
print(costs)

