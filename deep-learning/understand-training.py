#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 23:13:18 2020

@author: maximilianstaebler
"""

import numpy as np

np.random.seed(7)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

training_inputs = np.array([[0, 0, 1], \
                             [1, 1, 1], \
                             [1, 0, 1], \
                             [0, 1, 1]])

# print('Training Inputs')    
# print(training_inputs)

# print('#'*10)

# print('Training Inputs Transposed')
# print(training_inputs.T)


training_outputs = np.array([[0, 1, 1, 0]]).T

# print('Training Outputs')
# print(training_outputs)

weights = 2 * np.random.random((3, 1)) -1 


for iteration in range(0, 10000):
    
    input_layer = training_inputs
    
    outputs = sigmoid(np.dot(input_layer, weights))
    
    error = training_outputs - outputs
    
    adjustments = error * sigmoid_derivative(outputs)
    
    # Adding the new value to the weights
    weights += np.dot(input_layer.T, adjustments)
    
print('Weights after Training')
print(weights)
    
print('Outputs')
print(outputs)
