from brownie import accounts, web3, Wei, reverts, chain
from brownie.network.transaction import TransactionReceipt
from brownie.convert import to_address
import pytest
from brownie import Contract
from settings import *

@pytest.fixture(autouse=True)
def isolation(fn_isolation):
    pass

# def test_stake_genesis_nft(staking, staked_nft):
#     chain.sleep(GENESIS_AUCTION_TIME)
#     staked_nft.setApprovalForAll(staking_contract, True, {'from':accounts[2]})
#     txn = staking_contract.stake({'from':accounts[2]})
#     assert 'Staked' in txn.events
    
