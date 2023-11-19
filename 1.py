from itertools import combinations
from typing import Sequence

# possibility of raining per each combination
def prob_rain_exact_combination(p: Sequence[float], rain_days) ->float:
    probability = 1
    for i in range(len(p)):
        if i in rain_days:
            probability *= p[i]
        # for days that do not rain, we multiply the 1-probabilty of raining
        else:
            probability *= (1-p[i])
    return probability

# possibility of raining on EXACTLY n days 
def prob_rain_exact_n(p: Sequence[float], n: int) -> float:
    list_range = list(range(len(p)))
    # find all combinations of which exact n days it will rain
    combination = combinations(list_range, n)
    probability = 0
    for rain_days in list(combination):
        probability += prob_rain_exact_combination(p, set(rain_days))
    return probability

# possibility of raining AT LEAST n days 
def prob_rain_more_than_n(p: Sequence[float], n: int) -> float:
    probability = 0
    for idx in range (n, len(p)+1):
        probability += prob_rain_exact_n(p, idx)
    return probability

def main():
    print(prob_rain_more_than_n([0.1,0.3, 0.5,0.6, 0.9],5))

if __name__ == "__main__":
    main()