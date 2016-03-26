import math

R_b = 0

def r_t(kelvin):
	return 10000.*math.e**(3977.*(1./kelvin - 1./298))

low = r_t(283)
high = r_t(343)

for i in range(10):
	R_b = i*100 + 1000
	print(R_b)
	print(10*low/(R_b + low))
	print(10*high/(R_b + high))
	print("difference: " + str(abs(10*low/(R_b + low)-10*high/(R_b + high))))
	print("\n")
