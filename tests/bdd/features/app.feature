Feature: Running lecture feedback app

  Scenario: Create a new Room
    Given I am on the room selection screen
    When I click the "Create Room" button
    Then I should see the active room screen
    And the room should have a valid room ID

  Scenario: Try to join room without entering Room ID
    Given I am on the room selection screen
    When I click the "Join Room" button
    Then I should see warning message "Please enter a Room ID to join."
    And I should still be on the room selection screen

  Scenario: Try to join non existing room
    Given I am on the room selection screen
    When I enter a non-existing room ID
    And I click the "Join Room" button
    Then I should see error message "Room ID not found"
    And I should still be on the room selection screen

  Scenario Outline: User changes feedback status
    Given I am in an active room
    When I click the status "<status>" button
    Then my status should be "<status>"

    Examples:
      | status      |
      | 🔴 Red      |
      | 🟡 Yellow   |
      | 🟢 Green    |

  Scenario: Two users in one room share statistics
    Given user 1 and user 2
    And user 1 creates a room
    And user 2 joins user 1's room
    When user 1 changes status to "🔴 Red"
    Then all users in the room should see one red and one unknown
    When user 2 changes status to "🟢 Green"
    Then all users in the room should see one red and one green
