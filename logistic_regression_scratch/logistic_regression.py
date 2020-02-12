#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 12 10:55:23 2020

@author: maximilianstaebler
"""

import numpy as np
import seaborn as sns

# =============================================================================
# Create a dataset
# =============================================================================

np.random.seed(7)
num_observations = 5000

x1 = np.random.multivariate_normal([0, 0], [[1, .75],[.75, 1]], num_observations)
x2 = np.random.multivariate_normal([1, 4], [[1, .75],[.75, 1]], num_observations)

features = np.vstack((x1, x2)).astype(np.float32)
labels = np.hstack((np.zeros(num_observations),
                              np.ones(num_observations)))

# Plot the created dataset
sns.scatterplot(x = features[:, 0], y = features[:, 1], hue = labels)

# =============================================================================
# Logistic Regression
# =============================================================================

print(features.shape[1])

def sigmoid(scores):
    return(1 / (1 + np.exp(-scores)))

def log_likelihood(features, target, weights):
    scores = np.dot(features, weights)
    ll = np.sum( target*scores - np.log(1 + np.exp(scores)) )
    return(ll)

def logistic_regression(features, target, num_steps, learning_rate, add_intercept = False):
    if add_intercept:
        intercept = np.ones((features.shape[0], 1))
        features = np.hstack((intercept, features))
    
    
    weights = np.zeros(features.shape[1])
    
    for step in range(num_steps):
        scores = np.dot(features, weights)
        predictions = sigmoid(scores)

        # Update weights with gradient
        output_error_signal = target - predictions
        gradient = np.dot(features.T, output_error_signal)
        weights += learning_rate * gradient
        
        # Print log-likelihood every so often
        if step % 10000 == 0:
            print(log_likelihood(features, target, weights))
        
    return(weights)

weights = logistic_regression(features, labels, num_steps = 100000, learning_rate = 5e-5, add_intercept=True)

# =============================================================================
# sklearn approach
# =============================================================================

from sklearn.linear_model import LogisticRegression

clf = LogisticRegression(fit_intercept=True, C = 1e15)
clf.fit(features, labels)

# =============================================================================
# Compare results
# =============================================================================

print('Own Log-Reg Function parameters:')
print(weights)
print()
print('#'*10)
print()
print('Sklearn results:')
print(clf.intercept_, clf.coef_[0][0])

# =============================================================================
# Accuracy
# =============================================================================

data_with_intercept = np.hstack((np.ones((features.shape[0], 1)),
                                 features))
final_scores = np.dot(data_with_intercept, weights)
preds = np.round(sigmoid(final_scores))

print('Accuracy from scratch: {0}'.format((preds == labels).sum().astype(float) / len(preds)))
print('Accuracy from sk-learn: {0}'.format(clf.score(features, labels)))

