from brownie import *
from .settings import *
from .contracts import *
from .contract_addresses import *
import time
import csv


LOCATION_TO_DUMP_CSV = "./outputs/SetContributions.csv"

def main():
    genesis_nft_address = CONTRACTS[network.show_active()]["genesis_nft"]
    genesis_nft = DigitalaxGenesisNFT.at(genesis_nft_address)
    total_supply = genesis_nft.totalSupply()
    headers = ['tokens','contributions']
    owner_address = genesis_nft.ownerOf(460)
    contribution = genesis_nft.contribution(owner_address)
    print(owner_address)
    print(contribution)
    rows = []
    """ for token_id in range(1, total_supply+1):
        owner_address = genesis_nft.ownerOf(token_id)
        
        contribution = genesis_nft.contribution(owner_address)/TENPOW18
        row = [token_id, contribution]
        rows.append(row)
    
    with open(LOCATION_TO_DUMP_CSV,'w') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(headers)
        csvwriter.writerows(rows)

         """

    

    

    