Feature: Single session

  Scenario: Create a new room
    Given I am on the room selection screen
    When I click the "Create Room" button
    Then I should see the active room screen
    And the room should have a valid room ID
    And the URL should contain the room ID

  Scenario: Try to join a room without entering Room ID
    Given I am on the room selection screen
    When I click the "Join Room" button
    Then I should see warning message "Please enter a Room ID to join."
    And I should still be on the room selection screen

  Scenario: Try to join a non-existing room
    Given I am on the room selection screen
    When I enter a non-existing room ID
    And I click the "Join Room" button
    Then I should see error message "Room ID not found"
    And I should still be on the room selection screen
