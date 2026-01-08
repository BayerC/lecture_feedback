Feature: room cleanup

Scenario: User leaves room and is cleaned up
    Given I am in an active room
    When another user joins the room
    Then both users should be visible in the user status report
    When the other user closes their session
    And a given timeout has passed
    Then only I should be visible in the user status report
