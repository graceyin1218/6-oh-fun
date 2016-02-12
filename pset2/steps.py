def calculate_step(state, inp, steps):
  if steps == 0:
    return
  output = 2*state[2] + state[1] -3*state[0]
  print(output)
  state = (output, state[0], inp)
  calculate_step(state, 0, steps-1)

calculate_step((0,0,0), 1, 6)
