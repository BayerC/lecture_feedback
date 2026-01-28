Feature: Multiple sessions

  Scenario: Second user joins with room URL
    Given I host a room
    When a second user wants to join with invalid URL
    Then the second user should see warning message "Room ID from URL not found"
    When a third user wants to join with my room URL
    Then "me, third_user" should see status "Unknown"

  Scenario: Two users in one room share statistics
    Given I host a room
    When a second user joins the room
    Then "me, second_user" should see status "Unknown"
    When the second user selects the status "<status>"
    Then "me, second_user" should see status "<status>"
    Examples:
      | status      |
      | 🔴 Red      |
      | 🟡 Yellow   |
      | 🟢 Green    |

  Scenario: Three users in two separate rooms maintain independent statistics
    Given I host a room
    When a second user joins the room
    And a third user creates another room
    And the second user selects the status "🟢 Green"
    Then "me, second_user" should see status "🟢 Green"
