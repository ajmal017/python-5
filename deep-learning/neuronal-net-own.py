#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Creation of a neuronal network from scratch
"""

import numpy as np


class NeuronalNetwork():

    def __init__(self):
        np.random.seed(7)
        self.weights = 2 * np.random.random((3, 1)) - 1

    def sigmoid(self, x):
        """
        Takes in weighted sum of the inputs and normalizes
        them through between 0 and 1 through a sigmoid function
        """
        return(1 / (1 + np.exp(-x)))

    def sigmoid_derivative(self, x):
        """
        The derivative of the sigmoid function used to
        calculate necessary weight adjustments
        """
        return(x * (1 - x))

    def train(self, inputs, outputs, iterations):
        """[Train Function]

        Arguments:
            inputs {[float]} -- [blah]
            outputs {[float]} -- [blah]
            iterations {[interger]} -- [between 1- 10000]
        """
        i = 0

        for i in range(0, iterations):
            # Get the new calculated neurons
            output = self.think(inputs)

            # Calculate the errors
            error = outputs - output

            # Claculate the adjustments which then
            # need to be added / subtracted to
            # the weights.
            adjustments = np.dot(
                inputs.T, error * self.sigmoid_derivative(output))

            # Adjusting the weights
            self.weights += adjustments

            # Give back the new weights
            # return(self.weights)

    def think(self, inputs):
        inputs = inputs.astype(float)
        self.output = self.sigmoid(np.dot(inputs, self.weights))

        return(self.output)


if __name__ == "__main__":
    training_inputs = np.array([[0, 0, 1],
                                [1, 1, 1],
                                [1, 0, 1],
                                [0, 1, 1]])

    training_outputs = np.array([[0, 1, 1, 0]]).T

    network = NeuronalNetwork()

    print('Initial weights:')
    print(network.weights)

    print('Now we will adjust the weights')
    network.train(training_inputs, training_outputs, 1000)

    print('Final weights:')
    print(network.weights)

    # Get user input
    print('You now can input three parameters - please consider that only 0 or 1 is allowed!')
    A = str(input("Input 1: "))
    B = str(input("Input 2: "))
    C = str(input("Input 3: "))

    pred = network.think(np.array([A, B, C]))
    print('The prediction for parameters {}, {}, and {} is {}'. format(A, B,
                                                                       C, round(float(pred))))