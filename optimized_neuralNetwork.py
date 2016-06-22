#!/usr/bin/env python
#
#  Copyright (c) 2012, Jake Marsh  (http://jakemmarsh.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.

#  As a guide I took the following code: http://iamtrask.github.io/2015/07/12/basic-python-network/
#  Add visualization of neural network :) 

import math, random, string

random.seed(0)

#2nd Change: Lines 365, 368
#3rd Change: Lines 366, 377, 368

## ================================================================

# calculate a random number a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

def makeMatrix(I, J, fill = 0.0):
    m = []
    for i in range(I): #loops 4 times
        m.append([fill]*J) #[0.0, 0.0, 0.0]
    return m

# m = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

####Value of the activation function parameter: 0.5
def sigmoid(x):
    # tanh is a little nicer than the standard 1/(1+e^-x)
    return math.tanh(x)

# derivative of our sigmoid function, in terms of the output (i.e. y)
def dsigmoid(y):
    return 1.0 - y**2

## ================================================================

class NeuralNetwork:
    def __init__(self, inputNodes, hiddenNodes, outputNodes):
        # number of input, hidden, and output nodes
        self.inputNodes = inputNodes + 1 # +1 for bias node
        self.hiddenNodes = hiddenNodes
        self.outputNodes = outputNodes

        # activations for nodes
        self.inputActivation = [1.0]*self.inputNodes #>>> len(c) is 4; c = [1.0]*4 gives c = [1.0, 1.0, 1.0, 1.0]
        self.hiddenActivation = [1.0]*self.hiddenNodes#>>> len(d) is 3; d = [1.0]*3 gives d = [1.0, 1.0, 1.0]
        self.outputActivation = [1.0]*self.outputNodes#>>> len(e) is 1; e = [1.0]*1 gives e = [1.0]
        
        # create weights
        self.inputWeight = makeMatrix(self.inputNodes, self.hiddenNodes) #len(m) is 4; m = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        self.outputWeight = makeMatrix(self.hiddenNodes, self.outputNodes)#len(n) is 1; n = [[0.0], [0.0], [0.0]]
        # set them to random vaules
        for i in range(self.inputNodes): #loops 4 times
            for j in range(self.hiddenNodes): #loops 3 times 
                self.inputWeight[i][j] = rand(-0.2, 0.2) #it's m but with rand(-0.2, 0.2)

        print "self.inputWeight fed with rand(-0.2, 0.2): ", self.inputWeight #len(m) is 4

        #self.inputWeight fed with rand(-0.2, 0.2):  
        #[[0.13776874061001926, 0.10318176117612099, -0.031771367667662004], 
        # [-0.09643329988281467, 0.004509888547443414, -0.03802634501983429], 
        # [0.11351943561390904, -0.07867490956842903, -0.009361218339057675], 
        # [0.03335281578201249, 0.16324515407813406, 0.0018747423269561136]]

        for j in range(self.hiddenNodes): #loops 3 times 
            for k in range(self.outputNodes): #loops 1 time
                self.outputWeight[j][k] = rand(-2.0, 2.0) #it's m but with rand(-0.2, 0.2)
        print "self.outputWeight fed with rand(-0.2, 0.2): ", self.outputWeight #len(n) is 1
        # self.outputWeight fed with rand(-0.2, 0.2):  
        #[[-0.8726486224011847], [1.0232168166288957], [0.4734759867013265]]
        
        # last change in weights for momentum   
        self.ci = makeMatrix(self.inputNodes, self.hiddenNodes) #m = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
        print "self.ci last change for momentum: ", self.ci
        # self.ci last change for momentum:  
        #[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]

        self.co = makeMatrix(self.hiddenNodes, self.outputNodes) #n = [[0.0], [0.0], [0.0]]
        print "self.co last change for momentum: ", self.co
        # self.co last change for momentum:  
        #[[0.0], [0.0], [0.0]]

 
# Results: 
# self.inputWeight fed with rand(-0.2, 0.2):  [[0.13776874061001926, 0.10318176117612099, -0.031771367667662004], [-0.09643329988281467, 0.004509888547443414, -0.03802634501983429], [0.11351943561390904, -0.07867490956842903, -0.009361218339057675], [0.03335281578201249, 0.16324515407813406, 0.0018747423269561136]]
# self.outputWeight fed with rand(-0.2, 0.2):  [[-0.8726486224011847], [1.0232168166288957], [0.4734759867013265]]
# self.ci last change for momentum:  [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
# self.co last change for momentum:  [[0.0], [0.0], [0.0]]

#http://cs231n.github.io/neural-networks-1/

#Analysis: train calls update(Line 290)
#          update uses self.inputWeight and self.outputWeightchanges 
#          update changes self.inputActivation, self.hiddenActivation, self.outputActivation
#          update returns self.outputActivation (as an array)
#          train calls backPropagate
#          backPropagate modifies self.inputWeight and self.outputWeight
#          self.inputWeight and self.outputWeight are used in update 
#          repeats itself 1000 times. Then in the analyzer code we call test 
#          test calls update (Line 260)
#          update uses self.inputWeight and self.outputWeightchanges (self.inputWeight and self.outputWeight were modified by backpropagate)
#          update changes self.inputActivation, self.hiddenActivation, self.outputActivation
#          update returns self.outputActivation (as an array) 
#That is how train and test relate to each other, through self.inputWeight and self.outputWeight
#because backpropagate inside train modifies self.inputWeight and self.outputWeight
#and then self.inputWeight and self.outputWeight are used by update which is called inside test

    def update(self, inputs): #input is [531.9904153999998, 524.052386, 539.172466]
        #print "inputs of update function from NeuralNetwork: ", inputs #[531.9904153999998, 524.052386, 539.172466]
        #print "length of inputs of update function from NeuralNetwork: ", len(inputs) # len(inputs) is 3
        if len(inputs) != self.inputNodes-1: #if len(inputs) != 3
            raise ValueError('wrong number of inputs')

        # input activations
        for i in range(self.inputNodes-1): #loops 3 times (4-1 = 3 times)
            self.inputActivation[i] = inputs[i] #we modify all the values except the default value of the bias input node
        print "self.inputActivation inside update function: ", self.inputActivation[:]
        #self.inputActivation inside update function:  [531.9904153999998, 524.052386, 539.172466, 1.0]
        #before, self.inputActivation was [1.0, 1.0, 1.0, 1.0]

        # hidden activations
        for j in range(self.hiddenNodes): #loops 3 times
            sum = 0.0
            for i in range(self.inputNodes): #loops 4 times
                sum = sum + self.inputActivation[i] * self.inputWeight[i][j] #len(m) is 4; m = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
                #self.inputActivation inside update function:  
                #[531.9904153999998, 524.052386, 539.172466, 1.0]

                #self.inputWeight fed with rand(-0.2, 0.2):  
                #[[0.13776874061001926, 0.10318176117612099, -0.031771367667662004], 
                # [-0.09643329988281467, 0.004509888547443414, -0.03802634501983429], 
                # [0.11351943561390904, -0.07867490956842903, -0.009361218339057675], 
                # [0.03335281578201249, 0.16324515407813406, 0.0018747423269561136]]

                #Extract (summary)
                #j, loops 3 times
                #i, loops 4 times
                ##j=0
                # Then: 
                #self.inputActivation = sia #len(sia) is 4
                # sia[0], sia[1], sia[2], sia[3] 
                #   m[0][0], m[1][0], m[2][0], m[3][0]
                #self.hiddenActivation[0] = sigmoid(sum) #part of the result
                ##j=1
                # Then: 
                #self.inputActivation = sia #len(sia) is 4
                # sia[0], sia[1], sia[2], sia[3] 
                #   m[0][1], m[1][1], m[2][1], m[3][1]
                #self.hiddenActivation[1] = sigmoid(sum) #part of the result 
                ##j=2
                # Then: 
                #self.inputActivation = sia #len(sia) is 4
                # sia[0], sia[1], sia[2], sia[3] 
                #   m[0][2], m[1][2], m[2][2], m[3][2]
                #self.hiddenActivation[2] = sigmoid(sum) #part of the result  


            self.hiddenActivation[j] = sigmoid(sum) #>>> len(d) is 3; d = [1.0]*3 gives d = [1.0, 1.0, 1.0]
            #before, self.inputActivation was [1.0, 1.0, 1.0]
        print "self.hiddenActivation inside update function: ", self.hiddenActivation[:]
        #self.hiddenActivation inside update function:  
        #[1.0, 0.9999999999998125, -1.0]

        # output activations
        print "range(self.outputNodes): ", range(self.outputNodes) #range(self.outputNodes):  [0]
        for k in range(self.outputNodes): #loops 1 time, k=0
            sum = 0.0
            for j in range(self.hiddenNodes): #loops 3 times
                sum = sum + self.hiddenActivation[j] * self.outputWeight[j][k] 
            self.outputActivation[k] = sigmoid(sum) #>>> len(e) is 1; e = [1.0]*1 gives e = [1.0]

        #print "This is full self.outputWeight: ", self.outputWeight[:]
        #This is full self.outputWeight:  [[-0.8726486224011847], [1.0232168166288957], [0.4734759867013265]]
        #before the update self.outputWeight was [[0.0], [0.0], [0.0]]

        # range(self.outputNodes):  [0], k is always [0], loops 1 time
        # This is [j][k]:  0 0 #k from the outer loop, j from the inner loop
        # This is [j][k]:  1 0
        # This is [j][k]:  2 0
        # n[0][0], n[1][0], n[2][0]  #len(n) is 1; n = [[0.0], [0.0], [0.0]]

        print "self.outputActivation inside update function: ", self.outputActivation[:]
        #self.outputActivation inside update function:  [0.9606026038505812]
        #before update self.outputActivation was [1.0]
        return self.outputActivation[:] #len(self.outputActivation) is 1; self.outputActivation = e, e = [1.0]*1 gives e = [1.0]


    #Note: self.inputWeight and self.outputWeight are modified in backPropagate (also self.co and self.ci)
    def backPropagate(self, targets, N, M):
        if len(targets) != self.outputNodes: #len(targets) is 1, self.outputNodes = 1
            raise ValueError('wrong number of target values')

        # calculate error terms for output
        output_deltas = [0.0] * self.outputNodes #output_deltas = [0.0]*1 or [0.0]
        for k in range(self.outputNodes): #loops 1 time, k is always [0] 
            error = targets[k]-self.outputActivation[k] #self.outputActivation[0] is [1.0]
            output_deltas[k] = dsigmoid(self.outputActivation[k]) * error #output_deltas = [0.0] with a different value rather than 0.0
        print "output deltas from backPropagate function: ", output_deltas #because of the loop with 1000 iterations
        #output deltas appears 1000 times with different values
        #example
        #output deltas from backPropagate function:  [0.0025952033592540847]

        # calculate error terms for hidden
        hidden_deltas = [0.0] * self.hiddenNodes #hidden_deltas = [0.0]*3 or [0.0, 0.0, 0.0]
        for j in range(self.hiddenNodes): #loops 3 times
            error = 0.0
            for k in range(self.outputNodes): #loops 1 time, k is always [0] 
                error = error + output_deltas[k]*self.outputWeight[j][k] #self.outputWeight is [[0.0], [0.0], [0.0]] #of course as update function is called it gives self.outputWeight different values rather than 0.0 
            hidden_deltas[j] = dsigmoid(self.hiddenActivation[j]) * error #hidden_deltas = [0.0, 0.0, 0.0] (result from [0.0]*3) with different values rather than 0.0
        #hidden_Activation is [1.0, 1.0, 1.0] but with different values, from [1.0]*3 gives [1.0, 1.0, 1.0]
        print "hidden deltas from backPropagate function: ", hidden_deltas #because of the loop with 1000 iterations
        #hidden deltas appears 1000 times with different values
        #example
        #hidden deltas from backPropagate function:  [-0.0, 1.7789468019844285e-15, -0.0]

        # update output weights
        for j in range(self.hiddenNodes): #loops 3 times
            for k in range(self.outputNodes): #loops 1 time, k is always [0] 
                change = output_deltas[k]*self.hiddenActivation[j] #output_deltas = [0.0] with a different value rather than 0.0
                print "change for self.co :", change
                self.outputWeight[j][k] = self.outputWeight[j][k] + N*change + M*self.co[j][k] #self.outputWeight is [[0.0], [0.0], [0.0]] #of course as update function is called it gives self.outputWeight different values rather than 0.0
                self.co[j][k] = change #self.co is [[0.0], [0.0], [0.0]] and the float type zeros are substituted by new values, change
        print "self.co from backPropagate function: ", self.co #because of the loop with 1000 iterations
        #self.co appears 1000 times with different values
        #example
        #self.co from backPropagate function:  
        #[[0.00013728964264772642], [0.00013728964264770067], [-0.00013728964264772642]]

        # update input weights
        for i in range(self.inputNodes): #loops 4 times (3+1=4)
            for j in range(self.hiddenNodes): #loops 3 times
                change = hidden_deltas[j]*self.inputActivation[i] #hidden_deltas = [0.0, 0.0, 0.0] (result from [0.0]*3) with different values rather than 0.0
                print "change for self.ci: ", change
                self.inputWeight[i][j] = self.inputWeight[i][j] + N*change + M*self.ci[i][j] #self.inputWeight has length 4 and is [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]. The float type zeros are substituted by new values
                self.ci[i][j] = change #self.ci has length 4 and is [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]. The float type zeros are substituted by new values, change
        print "self.ci from backPropagate function: ", self.ci #because of the loop with 1000 iterations
        #self.ci appears 1000 times with different values
        #example
        #self.ci from backPropagate function:  
        #[[0.0, 5.599362764540085e-14, -0.0], 
        # [0.0, 5.515812563334366e-14, -0.0], 
        # [0.0, 5.674956056333596e-14, -0.0], 
        # [0.0, 1.0525307604141634e-16, -0.0]]

        # calculate error
        error = 0.0
        for k in range(len(targets)): #loops 1 time, k is always [0] 
            error = error + 0.5*(targets[k] - self.outputActivation[k])**2
        print "error, return value from backPropagate function: ", error
        return error #because of the loop with 1000 iterations
        #error appears 1000 times with different values
        #example (last value, 1000th value)
        #error, return value from backPropagate function:  3.42294633473e-05 


    def test(self, inputNodes):
        print "This is self from input from test from NeuralNetwork: ", self
        print "This is the input from test from NeuralNetwork: ", inputNodes
        print(inputNodes, '->', self.update(inputNodes))
        print "test1 from NeuralNetwork.py (self.update(inputNodes): ", self.update(inputNodes) #returns an array with only one value
        print "test2 from NeuralNetwork.py (self.update(inputNodes)[0])", self.update(inputNodes)[0] #returns the value (only) without being inside the array
        return self.update(inputNodes)[0] #returns the value (only) without being inside the array
        #example: -0.3763290104856086

        #from function **test** from neuralNetwork.py. Line 134
        # ([699.7640014000001, 692.359985, 711.119995], '->', [-0.3763290104856086])
    

    def weights(self):
        print('Input weights:')
        for i in range(self.inputNodes):
            print(self.inputWeight[i])
        print()
        print('Output weights:')
        for j in range(self.hiddenNodes):
            print(self.outputWeight[j])


# Momentum factor:
# To avoid oscillating weight changes the momentum factor is defined. Therefore the calculated weight change would not be the same always. 
# alpha (Greek letter) is called the momentum factor, and typically take values in the 
# range [0.7, 0.95]: 0.1 #change it 

# #Momentum
# Momentum basically allows a change to the weights to persist for a number of adjustment cycles. 
# The magnitude of the persistence is controlled by the momentum factor. 
# If the momentum factor is set to 0, then the equation reduces to that of Equation 3. 
# If the momentum factor is increased from 0, then increasingly greater persistence of previous adjustments 
# is allowed in modifying the current adjustment. 
# This can improve the learning rate in some situations, by helping to smooth out unusual conditions 
# in the training set. Link: http://www.cheshireeng.com/Neuralyst/nnbg.htm
# Another technique that can help the network out of local minima is the use of a momentum term. 
# This is probably the most popular extension of the backprop algorithm; 
# it is hard to find cases where this is not used. 
# With momentum m, the weight update at a given time t becomes (the equation where M is included)
# where 0 < m < 1 is a new global parameter which must be determined by trial and error. 
# Momentum simply adds a fraction m of the previous weight update to the current one. 
# When the gradient keeps pointing in the same direction, 
# this will increase the size of the steps taken towards the minimum. 
# It is otherefore often necessary to reduce the global learning rate mu (Greek letter) when using a lot of momentum (m close to 1). 
# If you combine a high learning rate with a lot of momentum, you will rush past the minimum with huge steps!

# When the gradient keeps changing direction, momentum will smooth out the variations. 
# This is particularly useful when the network is not well-conditioned. 
# In such cases the error surface has substantially different curvature along different directions, 
# leading to the formation of long narrow valleys. For most points on the surface, 
# the gradient does not point towards the minimum, 
# and successive steps of gradient descent can oscillate from one side to the other,
# progressing only very slowly to the minimum (Fig. 2a). 
# Fig. 2b shows how the addition of momentum helps to speed up convergence to the minimum 
# by damping these oscillations. Link: https://www.willamette.edu/~gorr/classes/cs449/momrate.html


#Learning rate
# With momentum m, the weight update at a given time t becomes (the equation where M is included)
# where 0 < m < 1 is a new global parameter which must be determined by trial and error. 
# Momentum simply adds a fraction m of the previous weight update to the current one. 
# When the gradient keeps pointing in the same direction, 
# this will increase the size of the steps taken towards the minimum. 
# It is otherefore often necessary to reduce the global learning rate mu (Greek letter) when using a lot of momentum (m close to 1). 
# If you combine a high learning rate with a lot of momentum, you will rush past the minimum with huge steps!
# Link: https://www.willamette.edu/~gorr/classes/cs449/momrate.html


#Iterations
#Ya! 
# Minimum performance gradient: #1e-7 http://www.mathworks.com/help/nnet/ref/trainlm.html
# The network training terminates when either the maximum number of iterations is reached or the performance gradient falls below 10-6. Furthermore, the generalization performance is evaluated using classification accuracy for the classification problem.
# Example:
# *the maximum number of training iterations is: 500
# *the minimum performance gradient is 10-6;and
# *the learning rate is 0.01
# https://books.google.com.mx/books?id=rD2FCwAAQBAJ&pg=PA79&lpg=PA79&dq=artificial+neural+network+minimum+performance+gradient&source=bl&ots=Dhj2ag-SMv&sig=oUeCenJ4zbYU5YBMMgjdK0d1ZvA&hl=en&sa=X&ved=0ahUKEwioodKS7fPMAhUSE1IKHaJ3BXYQ6AEIQzAF#v=onepage&q=artificial%20neural%20network%20minimum%20performance%20gradient&f=false


    def train(self, patterns, iterations = 1500, N = 0.5, M = 0.1):
        # N: learning rate, M: momentum factor
        print "Test1 This is patterns: ", patterns
        #This is patterns (input of train function from NeuralNetwork):  
        #[[[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]]
        for i in range(iterations):
            error = 0.0
            print "Test2 This is patterns: ", patterns
            for p in patterns: #an array of 5 arrays (each array has two arrays)
                print "Test3 This is patterns: ", patterns
                print "This is p from patterns: ", p 
                inputs = p[0] #three items
                print "This is p[0]: ", inputs
                targets = p[1] #one item
                print "This is targets: ", targets
                self.update(inputs)
                error = error + self.backPropagate(targets, N, M)
                # #ADDED 2500 (iterations) Lines 361-364, Suggested: http://stackoverflow.com/questions/957320/need-good-way-to-choose-and-adjust-a-learning-rate
                # N = N*.9977 #With 2500 iterations yields 0.0015808859879340542 #2nd Change
                # alfa = rand(-0.000799, .000899) #3rd Change
                # M += M*alfa #3rd Change
                # M += M*0.000899 #With 2500 iterations yields 0.9454495605361839 #2nd Change (including it) and 3rd Change (commenting it out)
                
                # Modifying, 1500 (iterations). ADDED Lines 361-364, Suggested: http://stackoverflow.com/questions/957320/need-good-way-to-choose-and-adjust-a-learning-rate
                N = N*.99615 #With 2500 iterations yields 0.001534895971089129 #2nd Change
                alfa = rand(-0.000799, .000899) #3rd Change
                M += M*alfa #3rd Change
                M += M*0.00144699 #With 1500 iterations yields 0.9464520719173348 #2nd Change (including it) and 3rd Change (commenting it out)

                #Modifying, 2000 (iterations). ADDED Lines 361-364, Suggested: http://stackoverflow.com/questions/957320/need-good-way-to-choose-and-adjust-a-learning-rate
                # N = N*.9971 #With 2000 iterations yields 0.001534895971089129 #2nd Change
                # alfa = rand(-0.000799, .000899) #3rd Change
                # M += M*alfa #3rd Change
                # M += M*0.001072 #With 2000 iterations yields 0.951237508365 #2nd Change (including it) and 3rd Change (commenting it out)
                
                #Modifying, 3000 (iterations). ADDED Lines 361-364, Suggested: http://stackoverflow.com/questions/957320/need-good-way-to-choose-and-adjust-a-learning-rate
                # N = N*.9981 #With 3000 iterations yields 0.0016639365815662131 #2nd Change
                # alfa = rand(-0.000799, .000899) #3rd Change
                # M += M*alfa #3rd Change
                # M += M*0.000696 #With 1500 iterations yields 0.951532342208 #2nd Change (including it) and 3rd Change (commenting it out)
                
                #Modifying, 3500 (iterations). ADDED Lines 361-364, Suggested: http://stackoverflow.com/questions/957320/need-good-way-to-choose-and-adjust-a-learning-rate
                # N = N*.99835 #With 3500 iterations yields 0.001544713530669535 #2nd Change
                # alfa = rand(-0.000799, .000899) #3rd Change
                # M += M*alfa #3rd Change
                # M += M*0.000585 #With 3500 iterations yields 0.950514712679 #2nd Change (including it) and 3rd Change (commenting it out)

            if i % 100 == 0:
                print('error %-.5f' % error)

    #Output:
    # Test1 This is patterns:  [[[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]]
    # Test2 This is patterns:  [[[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]]
    # Test3 This is patterns:  [[[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]]
    # This is p from patterns:  [[531.9904153999998, 524.052386, 539.172466], [1.0000000000000075]]
    # This is p[0]:  [531.9904153999998, 524.052386, 539.172466]
    # This is targets:  [1.0000000000000075]
