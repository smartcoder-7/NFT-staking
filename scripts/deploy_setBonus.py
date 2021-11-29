import csv
from .contracts import *

###########LOCATION##############
LOCATION_TO_RETRIEVE_CSV = './outputs/bonusPerWeek.csv'

def set_bonus(pool, rewards):
    rewardWeeks = []
    amounts = []
    
    with open(LOCATION_TO_RETRIEVE_CSV) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) #Skip Header
        for row in csvreader:
            rewardWeeks.append(row[0])
            amounts.append(float(row[1]))
            
    
    print("reward weeks ------",rewardWeeks)
    print("amounts per week ---",amounts)
    
    rewards.bonusRewards(pool,rewardWeeks,amounts,{'from':accounts[0]})
    
    return rewards

def main():
    # Acocunts
    load_accounts()

    # Get rewards contract
    rewards_address = CONTRACTS[network.show_active()]["rewards_contract"]
    rewards = DreamRewards.at(rewards_address)
    genesis_staking_address = CONTRACTS[network.show_active()]["genesis_staking"]
    
    # Set Rewards
    set_bonus(genesis_staking_address, rewards)