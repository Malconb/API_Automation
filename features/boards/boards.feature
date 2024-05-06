@boards
Feature: Boards

  @board_id 
  @acceptance @sanity @boards-get_all
  Scenario: Verify that get all boards endpoint return all created boards
    As user, I want to get all Boards on Trello API

    When I call to "boards" endpoint using "get" option and with parameters
    Then I receive the response to validate with "get_all_boards" file
    And I validated the status code is 200


  @board_id 
  @acceptance @sanity @boards-get
  Scenario: Verify that get board endpoint return a board
    As user, I want to get an specific board on Trello

    Given a valid ID for "Board" object
    When I call to "boards" endpoint using "get" option for provided ID
    Then I receive the response to validate with "get_board" file
    And I validated the status code is 200


  @board_id 
  @acceptance @sanity @boards-put
  Scenario: Verify that update board endpoint return an updated board
    As user, I want to update an specific board on Trello

    Given a valid ID for "Board" object
    When I call to "boards" endpoint using "put" option for provided ID
    Then I receive the response to validate with "update_board" file
    And I validated the status code is 200


  @acceptance @sanity @boards-post
  Scenario: Verify that create board endpoint return a created board
    As user, I want to create a board on Trello

    Given a valid ID for "Organization" object
    When I call to "boards" endpoint using "post" option for provided ID
    Then I receive the response to validate with "create_board" file
    And I validated the status code is 200