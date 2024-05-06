@labels
Feature: Labels

  @label_id 
  @acceptance @sanity @labels-get_all
  Scenario: Verify that get all label endpoint return all created labels
    As user, I want to get all labels from a board on Trello API

    When I call to "labels" endpoint using "get" option and with parameters
    Then I receive the response to validate with "get_all_labels" file
    And I validated the status code is 200


  @label_id 
  @acceptance @sanity @boards-get
  Scenario: Verify that get label endpoint return a label
    As user, I want to get an specific label on Trello

    Given a valid ID for "Label" object
    When I call to "labels" endpoint using "get" option for provided ID
    Then I receive the response to validate with "get_label" file
    And I validated the status code is 200

  @label_id 
  @acceptance @sanity @boards-put
  Scenario: Verify that update label endpoint return an updated label
    As user, I want to update an specific label on Trello

    Given a valid ID for "Label" object
    When I call to "labels" endpoint using "put" option for provided ID
    Then I receive the response to validate with "update_label" file
    And I validated the status code is 200

  @board_id
  @acceptance @sanity @boards-post
  Scenario: Verify that create board endpoint return a created label
    As user, I want to create a label on Trello

    Given a valid ID for "Board" object
    When I call to "labels" endpoint using "post" option for provided ID
    Then I receive the response to validate with "create_label" file
    And I validated the status code is 200