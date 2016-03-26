# variable

# Part 1
# x = 300.0
# y = 300.0

# Part 2
alphax = 0.547
alphay = 0.911

# given

R_x = 90000.0
R_y = 30000.0


width = 1280.0
height = 768.0

# calculations

# Part 1
# (alphax, alphay)
# alphax = x/width
# alphay = y/height
# print("(" + str(alphax) + ", " + str(alphay) + ")")

# Part 2
# (x, y)
x = width*alphax
y = height*alphay
print("(" + str(x) + ", " + str(y) + ")")


# Resistance from X_A to Y_A (in kOhms)
print((alphax*R_x + alphay*R_y)/1000.)

# Resistance from X_A to X_B (in kOhms)
print((R_x)/1000.)

# Resistance from X_A to Y_B (in kOhms)
print((alphax*R_x + (1.-alphay)*R_y)/1000.)
