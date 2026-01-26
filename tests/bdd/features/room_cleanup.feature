Feature: Room cleanup

Scenario: Disconnected user is removed from user status after timeout
    Given I host a room
    When a second user joins the room
    Then there should be 1 participant in my room
    When the second user closes their session
    And a given timeout has passed
    Then I should see info message "No participants yet. Share the Room ID to get started!"


Scenario: Room host disconnects
    Given I host a room
    When a second user joins the room
    When I close my session
    And a given timeout has passed
    Then second user should be on the room selection screen
