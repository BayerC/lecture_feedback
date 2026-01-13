Feature: Multiple sessions

  Scenario: Two users in one room share statistics
    Given I am in an active room
    When a second user joins the room
    Then "user, second_user" should see statuses "unknown"
    When I select the status "🔴 Red"
    Then "user, second_user" should see statuses "red, unknown"
    When the second user selects the status "🟢 Green"
    Then "user, second_user" should see statuses "red, green"

  Scenario: Three users in two separate rooms maintain independent statistics
    Given I am in an active room
    When a second user joins the room
    And a third user creates another room
    And I select the status "🟡 Yellow"
    And the second user selects the status "🟢 Green"
    Then "user, second_user" should see statuses "yellow, green"
    And "third_user" should see statuses "unknown"
