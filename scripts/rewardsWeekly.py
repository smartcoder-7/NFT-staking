import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
## An mvp python script to model reward payouts
############CHANGE THIS AS REQUIRED#############
LOCATION_TO_DUMP_CSV = "./outputs/tokensAllocationPerWeek.csv"

totalTokens = 9000
tokensMonth_1_2 = 2000

def exponentialDist(tokens : float):
    weights = np.exp(-np.arange(0,44) * 0.07)
    normalization = np.sum(weights)

    return tokens * weights / normalization


def getRewardsWeekly():
    tokensAllocationPerWeek = np.zeros(52)
    tokensAllocationPerWeek[0:8] = tokensMonth_1_2 / 4
    tokensAllocationPerWeek[8:] = exponentialDist(totalTokens - np.sum(tokensAllocationPerWeek[0:8]))
    print(tokensAllocationPerWeek)
    print(np.sum(tokensAllocationPerWeek))
    plt.plot(tokensAllocationPerWeek, label="Tokens released every week")
    plt.legend()
    plt.show()  
    col_name = ['WeeklyRewards']
    pd.DataFrame(tokensAllocationPerWeek).to_csv(LOCATION_TO_DUMP_CSV,header = col_name)
    return tokensAllocationPerWeek


def main():
    getRewardsWeekly()
