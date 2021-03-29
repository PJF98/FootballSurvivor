from matplotlib import pyplot as plt
import numpy as np
import pandas as pd

from create_matrices import create_matrices
from predictions import opponent_preds, my_preds
from match_outcomes import match_outcomes

df = pd.read_csv('clean_matches.csv')

num = 10000
winners = np.zeros([num, 10])
for i in range(num):
    print(i)
    sim = i
    fixtures, probs = create_matrices(df, random=True)
    rankings = np.argsort(-probs)
    all_preds = np.zeros([10, 20], dtype=int)
    all_preds[0] = my_preds(probs, rankings, survivefor=7)
    all_preds[1] = opponent_preds(probs, rankings, num=1)
    for i in np.arange(5) + 2:
        all_preds[i] = opponent_preds(probs, rankings)
    for i in np.arange(3) + 7:
        all_preds[i] = opponent_preds(probs, rankings, strat='proportional')
    results = match_outcomes(probs, fixtures)
    still_in = np.ones(10, dtype=int)
    rnum = 0
    while sum(still_in) > 0 and rnum < 20:
        last_round = still_in.copy()
        for j in range(10):
            if still_in[j] == 1:
                if results[rnum, all_preds[j][rnum]] == 0:
                    still_in[j] = 0
        rnum += 1
    winners[sim] = last_round / sum(last_round)
values = sum(winners)
barplot = plt.bar(np.arange(10), 100 * values / num)
barplot[0].set_color('k')
barplot[1].set_color('r')
for i in [7, 8, 9]:
    barplot[i].set_color('g')
plt.xlabel('Opponent Stratergy Number')
plt.ylabel('Value from £10 Entry (£)')
plt.savefig('OpponentStratValues.png')
plt.show()
