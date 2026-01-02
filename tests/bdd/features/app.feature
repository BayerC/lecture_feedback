Feature: Running lecture feedback app

  Scenario: Create a new Room
    Given I am on the room selection screen
    When I click the "Create Room" button
    Then I should see the active room screen
    And the room should have a valid room ID
