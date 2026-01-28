Feature: Question Voting

  Scenario: Client submits a question
    Given I host a room
    When a second user joins the room
    And the second user submits a question "How does this work?"
    Then "user, second_user" should see question "How does this work?"

  Scenario: Client upvotes a question
    Given I host a room
    When a second user joins the room
    And the second user submits a question "What is the answer?"
    And a third user joins the room
    And the third user upvotes the question "What is the answer?"
    Then "user, second_user, third_user" should see question "What is the answer?" with 1 vote

  Scenario: Client cannot upvote twice
    Given I host a room
    When a second user joins the room
    And the second user submits a question "Can I vote twice?"
    And the second user upvotes the question "Can I vote twice?"
    Then "user, second_user" should see question "Can I vote twice?" with 1 vote

  Scenario: Questions sorted by vote count
    Given I host a room
    When a second user joins the room
    And the second user submits a question "Low priority"
    And the second user submits a question "High priority"
    And a third user joins the room
    And the third user upvotes the question "High priority"
    Then the first question should be "High priority"

  Scenario: Host closes a question
    Given I host a room
    When a second user joins the room
    And the second user submits a question "To be closed"
    And I close the question "To be closed"
    Then "user, second_user" should not see question "To be closed"

  Scenario: Multiple questions with different vote counts
    Given I host a room
    When a second user joins the room
    And the second user submits a question "Question A"
    And the second user submits a question "Question B"
    And the second user submits a question "Question C"
    And a third user joins the room
    And the third user upvotes the question "Question B"
    And the third user upvotes the question "Question C"
    And the second user upvotes the question "Question C"
    Then questions should be ordered "Question C, Question B, Question A"
