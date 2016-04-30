class DDist:
    def __init__(self, dictionary):
        if not (abs(sum(dictionary.values())-1) < 1e-6 and min(dictionary.values()) >= 0.0):
            raise Exception("Probabilities must be nonnegative, and must sum to 1")
        self.d = dictionary

    def prob(self, elt):
        if elt in self.d:
            return self.d[elt]
        return 0
        #pass #your code here

    def support(self):
        result = []
        for i in self.d:
            if self.prob(i) != 0:
                result.append(i)
        return result
        #pass #your code here

    def __repr__(self):
        return "DDist(%r)" % self.d
    
    __str__ = __repr__

    def project(self, map_func):
        result = {}
        for x in self.support():
            s = map_func(x)
            if s in result:
                result[s] += self.prob(x)
            else:
                result[s] = self.prob(x)
        return DDist(result)
      #pass #your code here

    def condition(self, test_func):
        sum = 0
        result = {}
        for x in self.support():
            if test_func(x):
                sum += self.prob(x)
                result[x] = self.prob(x)
        factor = 1./sum
        for x in result:
            result[x] *= factor
        return DDist(result)
        #pass #your code here

def make_joint_distribution(pr_A, pr_B_given_A):
    result = {}
    for a in pr_A.support():
        pr_B = pr_B_given_A(a)
        for b in pr_B.support():
            result[(a, b)] = pr_A.prob(a)*pr_B.prob(b)
    return DDist(result)
    #pass #your code here

def total_probability(pr_A, pr_B_given_A):
    result = {}
    for a in pr_A.support():
        pr_B = pr_B_given_A(a)
        for b in pr_B.support():
            if b in result:
                result[b] += pr_A.prob(a) * pr_B.prob(b)
            else:
                result[b] = pr_A.prob(a) * pr_B.prob(b)
    return DDist(result)
    #pass #your code here

def bayes_rule(pr_A, pr_B_given_A, b):
    # randA = 0 # get a random key in pr_A
    # for a in pr_A:
    #     randA = a
    #     break

    # pr_B = pr_B_given_A(randA)

    # # get keys in B
    # keys_B = []
    # for b in pr_B:
    #     keys_B.append(b)


    result = {}
    sum = 0
    for a in pr_A.support():
        pr_B = pr_B_given_A(a)
        if b in pr_B.support():
            v = pr_B.prob(b) * pr_A.prob(a)
            result[a] = v
            sum += v
        else:
            result[a] = 0
    if sum != 1:
        sum = 1/sum
        for r in result:
            result[r] *= sum
    return DDist(result)

    ###
    # for each thing in A, 
    # what is the probability of sensing b?





    # def func(x): # x is a tuple
    #     return x[1] #b value
    # mid.project(func)
    # def pr_A_given_B(x):
    #     ///

    # return 

    # mid = total_probability(pr_A, pr_B_given_A)

    # factor = mid[b] #probability we have symptoms

    # #want function to return true when the disease is linked
    # #with symptom b

    # def func(x):
    #     return b == x
    # return mid.condition(func)

    #pass #your code here


### Test Cases


print("First test of prob method")
print('Expected:', [0.3,0.5,0.1,0.1])
x = DDist({'b':0.3, 'c':0.5, 'd':0.1, 'e':0.1})
result = [x.prob(i) for i in ['b', 'c', 'd', 'e']]
print('Received:', result)


print()
print("Test that d.prob(x) is 0 if x is not in the DDist d")
print("Expected:", 0)
result = x.prob("x")
print("Received:", result)
#print('Expected:', "Test Case Not Implemented")
#print('Received:', "Test Case Not Implemented")


print()
print("First test of support method")
print('Expected:', ['b', 'c', 'd', 'e'])
x = DDist({'b':0.3, 'c':0.5, 'd':0.1, 'e':0.1})
result = list(sorted(x.support()))
print('Received:', result)


print()
print("Second test of support method")
print('Expected:', False)
x = DDist({'b':0.3, 'c':0.5, 'd':0.1, 'e':0.1})
result = 'B' in x.support()
print('Received:', result)


print()
print("Test that d.support() does not contain elements with zero probability")
example = []
for i in x.d:
    if x.prob(i) != 0:
        example.append(x.d[i])
print("Expected:", example)

result = x.support()
result2 = []
for i in result:
    result2.append(x.d[i])
print("Received:", result2)

#print('Expected:', "Test Case Not Implemented")
#print('Received:', "Test Case Not Implemented")


print()
print("Test for make_joint_distribution")
print("Expected: ", DDist({(True, "cat"): 0.07,
                           (True, "dog"): 0.03,
                           (False, "cat"): 0.18,
                           (False, "dog"): 0.72}))
pr_X = DDist({True: 0.1, False: 0.9})
def pr_Y_given_X(x):
    if x:
        return DDist({"cat": 0.7, "dog": 0.3})
    else:
        return DDist({"cat": 0.2, "dog": 0.8})
print("Received:", make_joint_distribution(pr_X, pr_Y_given_X))


print()
print("Test for project")
print('Expected:', DDist({"small": 0.2, "big": 0.8}))
x = DDist({0: 0.1, 1: 0.05, 2: 0.05, 2000: 0.1, 15: 0.7})
def map_func(x):
    if x < 10:
        return "small"
    else:
        return "big"
result = x.project(map_func)
print('Received:', result)


print()
print("Test for condition")
print('Expected:', DDist({2000: 0.4, 5: 0.6}))
x = DDist({0: 0.1, 1: 0.1, 2: 0.3, 2000: 0.2, 5: 0.3})
def should_keep(x):
    return x >= 5
result = x.condition(should_keep)
print('Received:', result)


print()
print("Test for total_probability")
print("Expected: ", DDist({"cat": 0.25,
                           "dog": 0.75}))
pr_X = DDist({True: 0.1, False: 0.9})
def pr_Y_given_X(x):
    if x:
        return DDist({"cat": 0.7, "dog": 0.3})
    else:
        return DDist({"cat": 0.2, "dog": 0.8})
print("Received:", total_probability(pr_X, pr_Y_given_X))


print()
print("Test for bayes_rule (Hint: we had some examples from SL9 which could be useful!)")
ideal = [1,8,8,1]
belief = DDist({0:0.1, 1:0.3, 2:0.2, 3: 0.4})

def obs_model_B(state):
    probabilities = [0.03]*10
    probabilities[ideal[state]] += 0.7
    dict = {}
    for i in range(len(probabilities)):
        dict[i] = probabilities[i]
    return DDist(dict)

print("Expected: DDist({0: 0.007894736842105265, 1: 0.5763157894736842, 2: 0.38421052631578945, 3: 0.03157894736842106})")
print(bayes_rule(belief, obs_model_B, 8))
#print('Expected:', "Test Case Not Implemented")
#print('Received:', "Test Case Not Implemented")

