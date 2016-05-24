import highways
import maps


#bfs = maps.breadth_first_search(maps.highway_successors, 20000071, lambda x: x == 25000502)

#print("Length of trip: " + str(len(bfs)))
#print("Total Cost: " + str(maps.path_cost(bfs)))


uniform = maps.uniform_cost_search(maps.highway_successors, 20000071, lambda x: x == 25000502, lambda x: highways.distance(25000502, x)) 

print("Length of trip: " + str(len(uniform)))
print("Total Cost: " + str(maps.path_cost(uniform)))

