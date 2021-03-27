import numpy as np
import pandas as pd

df = pd.read_csv('spi_matches.csv')
ix = (df['league_id'] == 2411) & (df['season'] == 2019)
newdf = df[ix].copy()
cols = ['date', 'team1', 'team2', 'prob1', 'prob2']
newdf = newdf[cols]
newdf.reset_index(drop=True, inplace=True)
gameweeks = []
for i in range(38):
    gameweeks += [i] * 10
for i in [279, 278, 179]:
    del gameweeks[i]
gameweeks.insert(239, 17)
gameweeks.insert(288, 27)
gameweeks.insert(289, 27)
newdf['gameweek'] = gameweeks
teams = np.unique(newdf['team1'])
teamsdic = {}
for i in range(20):
    teamsdic[teams[i]] = i
newdf['team1'] = [teamsdic[t] for t in newdf['team1']]
newdf['team2'] = [teamsdic[t] for t in newdf['team2']]
newdf.to_csv('clean_matches.csv')
