Feature: Room cleanup

Scenario: Disconnected user is removed from user status after timeout
    Given I am in an active room
    When a second user joins the room
    Then the second user should be visible in the user status report
    When the second user closes their session
    And a given timeout has passed
    Then only I should be visible in the user status report

Scenario: Empty rooms are removed after cleanup
    Given I create a room with one user
    When the user leaves
    And the room cleanup process runs
    Then the room should no longer exist in the application state
    Then no users should be visible in the user status report
