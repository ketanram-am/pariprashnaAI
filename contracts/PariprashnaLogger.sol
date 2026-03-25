// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract PariprashnaLogger {
    event ChatLogged(bytes32 indexed chatHash, address indexed sender, uint256 timestamp);

    mapping(bytes32 => bool) public loggedChats;

    function logChat(bytes32 chatHash) external {
        loggedChats[chatHash] = true;
        emit ChatLogged(chatHash, msg.sender, block.timestamp);
    }
}
