Feature: Room cleanup

Scenario: Disconnected user is removed from user status after timeout
    Given I am in an active room
    When a second user joins the room
    Then both users should be visible in the user status report
    When the second user leaves
    And a given timeout has passed
    Then only I should be visible in the user status report

Scenario: Empty rooms are removed after cleanup
    Given I create a room with one user
    When the user leaves
    And the room cleanup process runs
    Then the room should no longer exist in the application state
