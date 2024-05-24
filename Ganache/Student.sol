// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StudentAuthentication {
    // Struct to store student details
    struct Student {
        string username;
        string password;
        bool isAuthenticated;
    }

    // Mapping to store student records by their address
    mapping(address => Student) public students;

    // Event to log login events
    event StudentLoggedIn(address studentAddress, string username);

    // Function to authenticate a student
    function authenticateStudent(string memory _username, string memory _password) public {
        // Check if student exists and password matches
        require(keccak256(bytes(students[msg.sender].username)) == keccak256(bytes(_username)), "Invalid username");
        require(keccak256(bytes(students[msg.sender].password)) == keccak256(bytes(_password)), "Invalid password");

        // Mark student as authenticated
        students[msg.sender].isAuthenticated = true;

        // Emit event for student login
        emit StudentLoggedIn(msg.sender, _username);
    }
}
