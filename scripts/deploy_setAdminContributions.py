import csv
from .contracts import *

###########LOCATION##############
LOCATION_TO_RETRIEVE_CSV = "./outputs/SetAdminContributions.csv"

def set_contributions(genesis_staking):
    tokens = []
    amounts = []
    count = 0
    with open(LOCATION_TO_RETRIEVE_CSV) as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) #Skip Header
        for row in csvreader:
            if count > 50:
                genesis_staking.setContributions(tokens,amounts,{'from':accounts[0]})
                tokens = []
                amounts = []
                count = 0
            tokens.append(int(row[0]))
            amounts.append(float(row[1])*10**18)
            count = count + 1 

    print('tokens-----------', tokens)
    print('amounts -----------',amounts)
    genesis_staking.setContributions(tokens,amounts,{'from':accounts[0]})
    
    return genesis_staking

def main():
    # Acocunts
    load_accounts()

    # Get rewards contract
    genesis_staking_address = CONTRACTS[network.show_active()]["genesis_staking"]
    genesis_staking = DreamGenesisStaking.at(genesis_staking_address)

    # Set Rewards
    set_contributions(genesis_staking)