import numpy as np
import pandas as pd


def create_matrices(df, random=False):
    fixtures = np.zeros([20, 20]).astype(int)
    probs = np.zeros([20, 20])
    if random:
        weeks = np.random.choice(38, 20, replace=False)
    else:
        weeks = np.arange(20)
    for i in range(20):
        for index, row in df[df['gameweek'] == weeks[i]].iterrows():
            fixtures[i, row['team1']] = row['team2']
            fixtures[i, row['team2']] = row['team1']
            probs[i, row['team1']] = row['prob1']
            probs[i, row['team2']] = row['prob2']
    return fixtures, probs
