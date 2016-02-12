import cmath

class Polynomial:
    # initialize the Polynomial with a list of coefficients
    # the coefficient list starts with the lowest-order term
    coefficients = []
    order = 0
    def __init__(self, c):
        self.coefficients = c
        self.removeTrailingZeros()
        self.order = len(c)-1
        #pass # your code here

    def removeTrailingZeros(self):
        while self.coefficients[-1] == 0:
            self.coefficients.pop()
        return


    # return the coefficient associated with the x**i term
    def coeff(self,i):
        if i >= len(self.coefficients) or i < 0:
            return 0 
        return self.coefficients[i]
        #pass # your code here

    # return the value of this Polynomial evaluated at x=v
    def val(self, v):
        sum = 0
        for i in range(0, len(self.coefficients)):
            sum = sum + self.coefficients[i] * v **i
        return sum
        #pass # your code here

    # add two Polynomials, return a new Polynomial
    def add(self, other):
        smaller_size = min(len(self.coefficients), len(other.coefficients))
        larger_polynomial = []
        if len(self.coefficients) > len(other.coefficients):
            larger_polynomial = self.coefficients
        else:
            larger_polynomial = other.coefficients

        new_coefficients = [0]*len(larger_polynomial)
        for i in range(0, smaller_size):
            new_coefficients[i] = self.coefficients[i] + other.coefficients[i]
        for i in range(smaller_size, len(larger_polynomial)):
            new_coefficients[i] = larger_polynomial[i]
        return Polynomial(new_coefficients)
        #pass # your code here

    # multiply two Polynomials, return a new Polynomial
    def mul(self, other):
        products = []
        for i in range(0, len(self.coefficients)):
            for j in range(0, len(other.coefficients)):
                products.append((i + j, self.coefficients[i] * other.coefficients[j]))
        result = []
        for i in range(0, len(self.coefficients) + len(other.coefficients)):
            result.append(0)
        for i in range(0, len(products)):
            location = products[i][0]
            result[location] += products[i][1]
        return Polynomial(result)

        #pass # your code here

    # return the roots of this Polynomial
    def roots(self):
        # can assume that polynomials are of order 1 or 2.
        result = [0,0]
        if len(self.coefficients) == 2:
            # bx + c = 0
            return (self.coefficients[0]/self.coefficients[1])
        elif len(self.coefficients) == 3:
            # ax^2 + bx + c = 0
            result[0] = (self.coefficients[1]*-1 + cmath.sqrt(self.coefficients[1]**2 - 4*self.coefficients[2]*self.coefficients[0]))/(2*self.coefficients[2])
            result[1] = (self.coefficients[1]*-1 - cmath.sqrt(self.coefficients[1]**2 - 4*self.coefficients[2]*self.coefficients[0]))/(2*self.coefficients[2])
            return result
        print("error")

        #pass # your code here

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.mul(other)

    def __repr__(self):
        return 'Polynomial([%s])' % ', '.join(repr(i) for i in self.coeffs)

    def __str__(self):
        out = ''
        for i in range(self.order,-1,-1):
            c = self.coeff(i)
            if c == 0:
                continue
            if c.real >= 0 and len(out) != 0:
                out += ' + '
            elif len(out) != 0:
                out += ' - '
                c = -c
            if c != 1:
                out += '(%r)' % c
            elif c == 1 and i == 0:
                out += repr(c)
            if i == 1:
                out += 'x'
            elif i != 0:
                out += '(x^%d)' % i
        return out


### Test Cases:

# Test Case 1 (Should print: [2, 0, 100])
# Test of order attribute
import random
p1 = Polynomial([1, 3, 2])
p2 = Polynomial([1])
p3 = Polynomial([random.randint(1, 100) for i in range(101)])
ans = [p1.order, p2.order, p3.order]
print("Test Case 1:", ans)
print("Expected:", [2, 0, 100])

# Test Case 2 (Should print: [4.0, 5.0, 8.0, 6.0, 7.0])
# Test of coeff method
a = Polynomial([4, 5, 8, 6, 7])
ans = [a.coeff(i) for i in range(a.order+1)]
print("Test Case 2:", ans)
print("Expected:", [4.0, 5.0, 8.0, 6.0, 7.0])

# Test Case 3 (Should print: [[10.0, 10.0, 8.0, 4.0], [10.0, 10.0, 8.0, 4.0]])
# Test of add method
p1 = Polynomial([1, 3, 2, 4])
p2 = Polynomial([9, 7, 6])
a = p1.add(p2)
b = p2.add(p1)
ans = [[a.coeff(i) for i in range(a.order+1)], [b.coeff(j) for j in range(b.order+1)]]
print("Test Case 3:", ans)
print("Expected:", [[10.0, 10.0, 8.0, 4.0], [10.0, 10.0, 8.0, 4.0]])

# Test Case 4 (Should print: [2.0, 4.0, 6.0, 1.0, 2.0, 3.0])
# Test of mul method
p1 = Polynomial([1,2,3])
p2 = Polynomial([2, 0, 0, 1])
a = p1.mul(p2)
ans = [a.coeff(i) for i in range(a.order+1)]
print("Test Case 4:", ans)
print("Expected:", [2.0, 4.0, 6.0, 1.0, 2.0, 3.0])

# Test Case 5 (Should print: [(-0.5+0j), (-1+0j)])
# Roots
p = Polynomial([1, 3, 2])
ans = p.roots()
print("Test Case 5:", ans)
print("Expected:", [(-0.5+0j), (-1+0j)])

# Test Case 6 (Should print: [(-0.33333333333333326+0.9428090415820635j), (-0.3333333333333334-0.9428090415820635j)])
# Roots
p = Polynomial([3, 2, 3])
ans = p.roots()
print("Test Case 6:", ans)
print("Expected:", [(-0.33333333333333326+0.9428090415820635j), (-0.3333333333333334-0.9428090415820635j)])
