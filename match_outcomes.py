import numpy as np


def match_outcomes(probs, fixtures):
    results = np.zeros([20, 20], dtype=int) - 1
    for i in range(20):
        for j in range(20):
            if results[i, j] == -1:
                rand = np.random.random()
                if probs[i, j] > rand:
                    results[i][j] = 1
                    results[i][fixtures[i][j]] = 0
                elif probs[i, j] + probs[i, fixtures[i][j]] > rand:
                    results[i][j] = 0
                    results[i][fixtures[i][j]] = 1
                else:
                    results[i][j] = 0
                    results[i][fixtures[i][j]] = 0
    return results
