// SPDX-License-Identifier: MIT

pragma solidity 0.6.12;

import "../DreamAuction.sol";

contract DreamAuctionMock is DreamAuction {
    uint256 public nowOverride;

    constructor(
        DreamAccessControls _accessControls,
        IDreamClothingNFT _clothingNft,
        address payable _platformReserveAddress
    )
        public
        DreamAuction(_accessControls, _clothingNft, _platformReserveAddress)
    {}

    function setNowOverride(uint256 _now) external {
        nowOverride = _now;
    }

    function _getNow() internal view override returns (uint256) {
        return nowOverride;
    }
}
