// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/ContestPrize.sol";

contract ContestPrizeTest is Test {
   ContestPrize contestPrize;
   function setUp() public {
      contestPrize = new ContestPrize();
   }
}