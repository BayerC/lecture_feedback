Feature: Multiple sessions

  Scenario: Two users in one room share statistics
    Given I am in an active room
    When a second user joins the room
    Then "user, second_user" should see statuses "Unknown, Unknown"
