def overshoot(distances, goal_distance):
  for distance in distances:
    if distance < goal_distance:
      return True
  return False
  #pass
