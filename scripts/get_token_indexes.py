from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import json
import csv
import collections
LOCATION_TO_DUMP_CSV = "./outputs/TokenOwner.csv"
def main():
   
    rows = []
    genesis_staking_address = CONTRACTS[network.show_active()]["genesis_staking"] 
    genesis_staking = DreamGenesisStaking.at(genesis_staking_address)
    for x in range(500):

        tokenOwner = genesis_staking.tokenOwner(x)
        print(tokenOwner)
        rows.append(tokenOwner)
   

    print("duplicates --------")
    print([item for item, count in collections.Counter(rows).items() if count > 1])
    counts = dict(collections.Counter(rows)) 
   
    print("---counts---")
    for count in counts.items():
       if count[1] > 1:
            print(count)
                    
