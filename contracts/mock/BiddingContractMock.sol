// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

import "../DreamAuction.sol";

contract BiddingContractMock {
    DreamAuction public auctionContract;

    constructor(DreamAuction _auctionContract) public {
        auctionContract = _auctionContract;
    }

    function bid(uint256 _clothingokenId) external payable {
        auctionContract.placeBid{value: msg.value}(_clothingTokenId);
    }
}
