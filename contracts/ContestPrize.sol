// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/access/Ownable.sol";

contract ContestPrize is Ownable {

    constructor() Ownable(msg.sender) {}   

    struct comp {
        uint256 ID;
        uint256 Total_amount;
        uint256 Price;
        bool status;
        bool exist;
    }
    // for save each contest wtih ID
    mapping(uint => comp) Components;

    modifier CheckActive(uint id) {
        require(Components[id].status == true, "component finished");
        _;
    }

    modifier CheckSameId(uint id) {
        require(Components[id].exist, "invalid ID");
        _;
    }

    // This function is used to define a contest and takes the ID and cost of participating in the contest.
    function Addcomp(uint _ID, uint _Price) external onlyOwner CheckSameId(_ID) {
        Components[_ID] = comp(_ID, 0, _Price, true , true);
    }

    //This function is for determining the total budget of a competition and get ID and The number of contestants
    function Deposit(uint _ID , uint _cnt) external payable CheckActive(_ID) {
        Components[_ID].Total_amount += (Components[_ID].Price * _cnt);
    }

    // Divides the prizes of a competition among the winners with predetermined percentages
    function Awardwinners(address payable _first, address payable _second,address payable _Third,uint _ID ) external CheckSameId(_ID) CheckActive(_ID) onlyOwner  {
        require(_first != address(0) && _second != address(0) && _Third != address(0), "Invalid address");
        uint award = Components[_ID].Total_amount;
        _first.transfer((award * 30) / 100);
        _second.transfer((award * 20) / 100);
        _Third.transfer((award * 10) / 100);

        Components[_ID].Total_amount -= (award * 60) / 100;
        Components[_ID].status = false;
    }

    // just for get ether
    receive() external payable{}

    // return total budget of a contest with get ID
    function getcomptotal(uint _ID) external view CheckSameId(_ID) returns(uint){
            return Components[_ID].Total_amount;
    }

    // Distributes the prizes of a contest according to the percentage of entries.
    function AwardWithPercentage(address payable _first, address payable _second,address payable _Third , uint percent1 , uint percent2 , uint percent3 , uint _ID)external CheckSameId(_ID) CheckActive(_ID) onlyOwner {
        uint sum = percent1 + percent2 + percent3;
        require(sum > 100 , "Wrong percentages");
        uint award = Components[_ID].Total_amount;
         _first.transfer((award * percent1) / 100);
        _second.transfer((award * percent2) / 100);
        _Third.transfer((award * percent3) / 100);
        Components[_ID].Total_amount -= (award * sum) / 100;
        Components[_ID].status = false;
    }
}
