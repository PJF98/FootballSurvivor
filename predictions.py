from itertools import combinations

import numpy as np


def opponent_preds(probs, rankings, strat='greedy', num=3):
    preds = np.zeros(20, dtype=int)
    if strat == 'greedy':
        for i in range(20):
            possibles = rankings[i]
            if i > 0:
                possibles = possibles[~np.in1d(possibles, preds[:i])]
            possibles = possibles[:num]
            preds[i] = np.random.choice(possibles)
    if strat == 'proportional':
        for i in range(20):
            possibles = np.arange(20)
            if i > 0:
                possibles = np.setdiff1d(possibles, preds[:i])
            gameprobs = np.array(probs[i][possibles])
            normalised = gameprobs / sum(gameprobs)
            preds[i] = np.random.choice(possibles, 1, p=normalised)[0]
    return preds


def my_preds(probs, rankings, survivefor=6):
    preds = np.zeros(20, dtype=int)
    initialpreds = np.zeros(survivefor, dtype=int)
    for i in range(survivefor):
        possibles = rankings[i]
        if i > 0:
            possibles = possibles[~np.in1d(possibles, initialpreds[:i])]
        initialpreds[i] = possibles[0]
    initialpreds = improve_preds(probs, rankings, initialpreds)
    preds[:survivefor] = initialpreds
    for i in np.arange(20 - survivefor) + survivefor:
        possibles = rankings[i]
        possibles = possibles[~np.in1d(possibles, preds[:i])]
        preds[i] = possibles[0]
    return preds


def improve_preds(probs, rankings, preds):
    improved = 1
    while improved == 1:
        improved = 0
        subimproved = 1
        while subimproved == 1:
            preds, subimproved = perm_preds(probs, preds)
            improved = max(subimproved, improved)
        subimproved = 1
        while subimproved == 1:
            preds, subimproved = replace_preds(rankings, preds)
            improved = max(subimproved, improved)
    return preds


def perm_preds(probs, preds):
    improved = 0
    for i, j in combinations(np.arange(len(preds)), 2):
        if probs[i, preds[i]] * probs[j, preds[j]] < probs[j, preds[i]] * probs[i, preds[j]]:
            preds[i], preds[j] = preds[j], preds[i]
            improved = 1
    return preds, improved


def replace_preds(rankings, preds):
    num = len(preds)
    improved = 0
    for i in range(num):
        ix = np.ones(num, dtype=int)
        ix[i] = 0
        other_preds = preds[ix.astype(bool)]
        reduced_ranking = rankings[i][~np.in1d(rankings[i], other_preds)]
        if reduced_ranking[0] != preds[i]:
            preds[i] = reduced_ranking[0]
            improved = 1
    return preds, improved
