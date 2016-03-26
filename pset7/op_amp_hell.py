#variable

# alpha1 = 0.54
# alpha2 = 0.54
# alpha3 = 0.54

# alpha1 = 0
# alpha2 = 1
# alpha3 = 0

alpha1 = 0.85
alpha2 = 0.97
alpha3 = 0.33


# apparently they changed how alpha works...
alpha1 = 1-alpha1
alpha2 = 1-alpha2
alpha3 = 1-alpha3


#given

V_1 = 16 * 10**(-3)
V_2 = 82 * 10**(-3)
V_3 = 73 * 10**(-3)

R_1 = 1000
R_2 = 1000
R_3 = 1000

R_4 = 450
R_5 = 450
R_6 = 450

R_7 = 4500

R_8 = 2400

R_9 = 24000


#calculated

I_1 = V_1/(alpha1*R_1 + R_4)
I_2 = V_2/(alpha2*R_2 + R_4)
I_3 = V_3/(alpha3*R_3 + R_4)

V_x = -R_7*(I_1 + I_2 + I_3)

I_8 = V_x/R_8

V_out = -I_8*R_9

print(V_out)

