// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/ContestPrize.sol";

contract ContestPrizeTest is Test {
   ContestPrize _contestPrize;
   function setUp() public {
      _contestPrize = new ContestPrize();
   }

   function testaddcomp() public {
      _contestPrize.Addcomp(1, 10, 0);
      vm.expectRevert(bytes("this ID is already exist"));
      _contestPrize.Addcomp(1, 10, 0);
      vm.prank(0x0000000000000000000000000000000000001234);
      vm.expectRevert();
      _contestPrize.Addcomp(2, 2, 2);
   }
}