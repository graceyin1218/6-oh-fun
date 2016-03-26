
# variable
# x = 640.
# y = 384.

x = 500.
y = 500.

# given
R_x = 60000.
R_y = 70000.

width = 1280.
height = 768.


# calculated

alphax = x/width
alphay = y/height

V_x = 5 * (1-alphax)

V_y = 5 * (1-alphay)

print(V_x)
print(V_y)
