# FootballSurvivor

Finding a good algorithm for winning a game of football survivor against 9
other players and estimating it's value.

My Approach:

After downloading the football fixtures and win probabilities data (spi_matches.csv)
from fivethirtyeight I wrote clean_data.py to select the rows and columns I
needed for this project. I choose to use the 2019-2020 season as there were
fewer postponements and so it was easier to add the gameweek column. I also
replaced the football team names with integers to make the data easier to work
with. I saved this cleaned data to clean_matches.csv.

The next step was using this data to get the probabilities for and opponents of
each team for each week. This is done by the create_matrices function in
create_matrices.py. This function either choses the fixtures for the first 20
weeks of the season or a random selection of weeks in a random order.

After creating matrices of probabilities and fixtures (which can easily be used
to rank the teams by win probability each week) it was time to think of
strategies for the opponents. For the opponents I came up with 2 main
strategies:

The first is just a modified greedy algorithm. The opponents are
given an input n and then in each week chose randomly between the top n teams
that they haven't already chosen. Hence for n=1 this is just the greedy
algorithm.

The second is more random. The opponents chose between the teams they haven't
already chosen with probabilities proportional to that teams win probability
for the week. This is therefore just slightly better than chosing teams
completely at random.

After creating the opponents strategies I decided the general approach for my
own strategy would be to optimise the probability of survival for n rounds and
then use the greedy algorithm to fill in the rest of my predictions. The logic
being there's not much difference between surving for 1 round and 3 rounds if 
you need to survive for 5 rounds to win.

In order to optimise this probability it choses the first n predictions using
the greedy algorithm and then tries permutating and replacing the predictions
until it can no longer find an improvement. This won't always find the absolute
best first n but it'll be pretty close (it could find a local max).

In order to help determine the best value of n I simulated the opponents against each
other in opponents_simulation.py. I used 1 traditional greedy algorithm, 5 copies of 
the greedy variant with n=3 and 3 copies of the proportional strat. I kept track of 
the gamelength and winners for each run producing these two graphs:


<img src= "https://github.com/PJF98/FootballSurvivor/blob/main/Gamelengths.png"/>

<img src= "https://github.com/PJF98/FootballSurvivor/blob/main/OpponentsStratValues.png"/>

From this I found that the mean number of rounds survived by the best opponent
is 5.6 and the mode number is 5. It's also clear that the traditional greedy
algorithm is the best and should be the benchmark to beat for my algorithm.

I then coded up my algorithm in predictions.py (which contains the opponents
algorithms are also). The full simulation is in full_simulation.py. I found
several values of n for my algorithm where beating the greedy algorithm with
n=5 being the best (I tried 10,000 runs with n = 3,4,5,6). For the full simulation
I also decided to chose to randomise the weeks which were used each time in case 
the greedy algorithm was particularly good on the first 20 weeks for example.

To conclude my strategy is to optimise the probability of surviving for the
first 5 weeks and then fill in the rest of the predictions with the greedy
algorithm. As can be seen in the following graph the expected value of this
strategy against these opponents is approximately £15.2.
