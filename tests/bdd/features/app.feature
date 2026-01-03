Feature: Running lecture feedback app

  Scenario: Create a new Room
    Given I am on the room selection screen
    When I click the "Create Room" button
    Then I should see the active room screen
    And the room should have a valid room ID

  Scenario: Try to join non existing room
    Given I am on the room selection screen
    When I enter a non-existing room ID
    And I click the "Join Room" button
    Then I should see an error message "Room ID not found"
    And I should still be on the room selection screen
