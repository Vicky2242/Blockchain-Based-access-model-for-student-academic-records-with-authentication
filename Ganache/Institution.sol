// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InstitutionAuthentication {
    // Struct to store institution details
    struct Institution {
        string username;
        string password;
        bool isAuthenticated;
    }

    // Mapping to store institution records by their address
    mapping(address => Institution) public institutions;

    // Event to log login events
    event InstitutionLoggedIn(address institutionAddress, string username);

    // Function to authenticate an institution
    function authenticateInstitution(string memory _username, string memory _password) public {
        // Check if institution exists and password matches
        require(keccak256(bytes(institutions[msg.sender].username)) == keccak256(bytes(_username)), "Invalid username");
        require(keccak256(bytes(institutions[msg.sender].password)) == keccak256(bytes(_password)), "Invalid password");

        // Mark institution as authenticated
        institutions[msg.sender].isAuthenticated = true;

        // Emit event for institution login
        emit InstitutionLoggedIn(msg.sender, _username);
    }
}

contract AuthorityAuthentication {
    // Struct to store authority details
    struct Authority {
        string username;
        string password;
        bool isAuthenticated;
    }

    // Mapping to store authority records by their address
    mapping(address => Authority) public authorities;

    // Event to log login events
    event AuthorityLoggedIn(address authorityAddress, string username);

    // Function to authenticate an authority
    function authenticateAuthority(string memory _username, string memory _password) public {
        // Check if authority exists and password matches
        require(keccak256(bytes(authorities[msg.sender].username)) == keccak256(bytes(_username)), "Invalid username");
        require(keccak256(bytes(authorities[msg.sender].password)) == keccak256(bytes(_password)), "Invalid password");

        // Mark authority as authenticated
        authorities[msg.sender].isAuthenticated = true;

        // Emit event for authority login
        emit AuthorityLoggedIn(msg.sender, _username);
    }
}
