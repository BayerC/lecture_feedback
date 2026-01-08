Feature: Multiple sessions interacting

  Scenario: Two users in one room share statistics
    Given I am in an active room
    When another user joins the room
    When I click the status "🔴 Red" button
    Then all users in the room should see one red and one unknown
    When other user clicks the status "🟢 Green" button
    Then all users in the room should see one red and one green
