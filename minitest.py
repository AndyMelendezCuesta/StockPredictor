import math, random

random.seed(0)

# calculate a random number a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

M = 0.1
for i in range(2000):
    alfa = rand(-0.000799, .000899) 
    M += M*alfa 
    M += M*0.001072

print "M: ", M