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

   function testsignup() public{
      address _testaddress = 0x0000000000000000000000000000000000001234 ;
      _contestPrize.Addcomp(1, 10 ether , 0);
      vm.expectRevert(bytes("this ID is not exist"));
      _contestPrize.signup(2);
      vm.deal(_testaddress, 100 ether);
      vm.startPrank(_testaddress);
      _contestPrize.signup{value : 10 ether}(1);
      vm.stopPrank();
      assertEq(address(_contestPrize).balance , 10 ether);
      assertEq(_contestPrize.getcomptotal(1) , 10 ether);
   }

}