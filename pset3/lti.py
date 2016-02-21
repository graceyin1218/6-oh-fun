from lib601.poly import Polynomial
import cmath

class System:
    initial_state = None
    numerator = None
    denominator = None
    def calculate_step(self, state, inp):
        return (state, inp)

    def simulator(self):
        return SystemSimulator(self)

    def poles(self):
        z_array = []
        for i in range(0, self.denominator.order+1):
            z_array.append(self.denominator.coeff(i))
        if self.numerator.order > self.denominator.order:
            for i in range(self.denominator.order, self.numerator.order+2):
                z_array.append(0)
        z_reversed = []
        for i in range(0, len(z_array)):
            z_reversed.insert(0, z_array[i])
        z = Polynomial(z_reversed)
        return z.roots()
    def dominant_pole(self):
        pole_list = self.poles()
        dominant = None
        dominant_magnitude = 0
        for pole in pole_list:
            magnitude = cmath.sqrt(pole.real**2 + pole.imag**2)
            if magnitude > dominant_magnitude:
                dominant_magnitude = magnitude
                dominant = pole
        return dominant


class SystemSimulator:
    def __init__(self, system):
        self.system = system
        self.reset()

    def step(self, inp):
        new_state, out = self.system.calculate_step(self.state, inp)
        self.state = new_state
        return out

    def reset(self):
        self.state = self.system.initial_state

    def get_response(self, inputs, reset=True):
        if reset:
            self.reset()
        return [self.step(inp) for inp in inputs]

class R(System):
    def __init__(self, init_state): #output0=0):
        self.initial_state = init_state#None # modify if necessary
        self.numerator = Polynomial([0, 1])
        self.denominator = Polynomial([1])


    def calculate_step(self, state, inp):
        # your code here
        output = state
        new_state = inp
        
        return (new_state, output)

"""
class R(System):
    def __init__(self, output0=0):
        self.initial_state = None # modify if necessary

    def calculate_step(self, state, inp):
        # your code here
        return (new_state, output)
"""
class Gain(System):
    def __init__(self, k):
        self.initial_state = k # modify if necessary
        self.numerator = Polynomial([k])
        self.denominator = Polynomial([1])

    def calculate_step(self, state, inp):
        # your code here
        new_state = state
        output = state * inp
        return (new_state, output)

"""
class Gain(System):
    def __init__(self, k):
        self.initial_state = None # modify if necessary

    def calculate_step(self, state, inp):
        # your code here
        return (new_state, output)
"""
"""
class FeedforwardAdd(System):
    def __init__(self, s1, s2):
        self.initial_state = None # modify if necessary

    def calculate_step(self, state, inp):
        # your code here
        return (new_state, output)
"""
class FeedforwardAdd(System):
    def __init__(self, s1, s2):
        #self.initial_state = (s1, s2) # modify if necessary
        self.s1 = s1
        self.s2 = s2
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.numerator = s1.numerator.mul(s2.denominator) + s2.numerator.mul(s1.denominator)
        self.denominator = s1.denominator.mul(s2.denominator)



    def calculate_step(self, state, inp):
        # your code here
        #print(state[0])
        #print(state[1])
        #print(inp)
        #print(state[0].state)
        (state1, out1) = self.s1.calculate_step(state[0], inp)
        (state2, out2) = self.s2.calculate_step(state[1], inp)
        output = out1 + out2#state[0].calculate_step(state[0], inp)[1] + state[1].calculate_step(state[1], inp)[1]
        new_state = (state1, state2)
        return (new_state, output)
class Cascade(System):
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.initial_state = (s1.initial_state, s2.initial_state)#None # modify if necessary
        self.numerator = s1.numerator.mul(s2.numerator)
        self.denominator = s1.denominator.mul(s2.denominator)


    def calculate_step(self, state, inp):
        # your code here
        (state1, out1) = self.s1.calculate_step(state[0], inp)
        (state2, out2) = self.s2.calculate_step(state[1], out1)
        new_state = (state1, state2)
        output = out2
        return (new_state, output)

class FeedbackAdd(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2
        self.numerator = s1.numerator.mul(s2.denominator)
        self.denominator = s1.denominator.mul(s2.denominator).add((s1.numerator.mul(s2.numerator)).mul(Polynomial([-1])))

    def calculate_step(self, state, inp):
        s1_state, s2_state = state

        # Here we encounter a problem.  It seems like s1's output
        # depends on s2's output, and s2's output depends on s1's
        # output.  Which one do we run first?  It looks like getting
        # either output is impossible!
        #
        # Importantly, we will make the assumption that at least one of s1
        # and s2 has the property that its output at time n does not depend
        # on its input at time n (depends only on older inputs/outputs).
        # The net effect of this is that s2's output at time n does not
        # depend on the input to the system at time n.
        #
        # We need to know s2's output in order to compute s1's output (and
        # to know how to update s2's state).  We will get around this by
        # using a "fake" input to determine s2's output (which we know was
        # unaffected by our bogus input), and then using that result to
        # compute the real outputs and states of the two internal systems.

        # Firstly, we propagate a bogus input through the system in order
        # to find s2's output.
        s1_state_hyp, out1_hyp = self.s1.calculate_step(s1_state, 99999999)
        s2_state_hyp, out2_hyp = self.s2.calculate_step(s2_state, out1_hyp)

        # Because of the property mentioned above, we know that s2's output
        # did not depend on the bogus input, so this is the right value.
        out2_real = out2_hyp

        # Knowing s2's output, we can now know the actual value that we should
        # pass in to s1.  Now we can compute the outputs (and new states) of
        # s1 and s2 correctly.
        s1_real_inp = inp + out2_real
        s1_state_real, out1_real = self.s1.calculate_step(s1_state, s1_real_inp)
        s2_state_real, out2_real = self.s2.calculate_step(s2_state, out1_real)

        new_state = (s1_state_real, s2_state_real)
        output = out1_real

        return (new_state, output)

"""
### Test Cases:

# Test Case 1 (Should print: [90, 0, 5, 10, 15, 20, 25, 30, 35, 40])
r = R(18)
g = Gain(5)
s = Cascade(r,g).simulator()
ans = [s.step(i) for i in range(10)]
print("Test Case 1:", ans)
print("Expected:", [90, 0, 5, 10, 15, 20, 25, 30, 35, 40])
"""
"""
class Cascade(System):
    def __init__(self, s1, s2):
        self.initial_state = None # modify if necessary

    def calculate_step(self, state, inp):
        # your code here
        return (new_state, output)
"""


