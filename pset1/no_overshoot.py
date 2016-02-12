import sys

k = 1
init_distance = 1.0
goal_distance = 0.5
dt = 0.1
num_samples = 10
while True:
	current_distance = init_distance
	velocity = 0

	solution = []

	for i in range(0, num_samples):
		current_distance = current_distance - velocity*dt
		solution.append(current_distance)
		if current_distance < goal_distance:
			print(k)
			sys.exit(0)
		velocity = k*(current_distance-goal_distance)

	k += 1
