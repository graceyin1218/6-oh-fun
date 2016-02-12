import sys

if len(sys.argv) < 6:
  print("Not enough arguments")
  sys.exit(0)

k = float(sys.argv[1])
init_distance = float(sys.argv[2])
goal_distance = float(sys.argv[3])
dt = float(sys.argv[4])
num_samples = int(sys.argv[5])

current_distance = init_distance
velocity = 0

solution = []

for i in range(0, num_samples):
  current_distance = current_distance - velocity*dt
  solution.append(current_distance)
  velocity = k*(current_distance-goal_distance)

print(solution)

