// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ReentrancyVictim {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw(uint256 amount) external {
        require(balances[msg.sender] >= amount, "insufficient");
        // vulnerable: interaction before effect
        (bool ok,) = msg.sender.call{value: amount}("");
        require(ok, "call failed");
        balances[msg.sender] -= amount;
    }
}
