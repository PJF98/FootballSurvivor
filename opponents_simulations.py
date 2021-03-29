from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from create_matrices import create_matrices
from predictions import opponent_preds
from match_outcomes import match_outcomes

df = pd.read_csv('clean_matches.csv')
fixtures, probs = create_matrices(df)
rankings = np.argsort(-probs)

num = 1000
gamelengths = np.zeros(num, dtype=int)
winners = np.zeros([num, 9])
for i in range(num):
    print(i)
    sim = i
    all_preds = np.zeros([9, 20], dtype=int)
    all_preds[0] = opponent_preds(probs, rankings, num=1)
    for i in np.arange(5) + 1:
        all_preds[i] = opponent_preds(probs, rankings)
    for i in np.arange(3) + 6:
        all_preds[i] = opponent_preds(probs, rankings, strat='proportional')
    results = match_outcomes(probs, fixtures)
    still_in = np.ones(9, dtype=int)
    rnum = 0
    while sum(still_in) > 0 and rnum < 20:
        last_round = still_in.copy()
        for j in range(9):
            if still_in[j] == 1:
                if results[rnum, all_preds[j][rnum]] == 0:
                    still_in[j] = 0
        rnum += 1
    gamelengths[sim] = rnum
    winners[sim] = last_round / sum(last_round)
gl, freq = np.unique(gamelengths, return_counts=True)
values = sum(winners)
plt.bar(gl, freq / num)
plt.xlabel('Gamelength')
plt.ylabel('Percentage of Games')
plt.savefig('Gamelengths.png')
plt.show()
barplot = plt.bar(np.arange(9), 90 * values / num)
barplot[0].set_color('r')
for i in [6, 7, 8]:
    barplot[i].set_color('g')
plt.xlabel('Opponent Stratergy Number')
plt.ylabel('Value from £10 Entry (£)')
plt.savefig('OpponentStratValues.png')
plt.show()
