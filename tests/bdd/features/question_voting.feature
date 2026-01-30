Feature: Question Voting

  Scenario: Client submits a question
    Given I host a room
    When a second user joins the room
    And a third user joins the room
    Then "me, second_user, third_user" should see no questions
    When the second user submits a question "How does this work?"
    Then "me, second_user, third_user" should see question "How does this work?" with 1 vote
    When the third user upvotes the question
    Then "me, second_user, third_user" should see question "How does this work?" with 2 votes
    When I close the question
    Then "me, second_user, third_user" should see no questions