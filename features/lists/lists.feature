@lists
Feature: Lists

  @list_id 
  @acceptance @sanity @lists-get_all
  Scenario: Verify that get all lists endpoint return all created lists
    As user, I want to get all lists from a board on Trello API

    When I call to "lists" endpoint using "get" option and with parameters
    Then I receive the response to validate with "get_all_lists" file
    And I validated the status code is 200

  @list_id 
  @acceptance @sanity @boards-get
  Scenario: Verify that get list endpoint return a list
    As user, I want to get an specific list on Trello

    Given a valid ID for "list" object
    When I call to "lists" endpoint using "get" option for provided ID
    Then I receive the response to validate with "get_list" file
    And I validated the status code is 200

  @list_id 
  @acceptance @sanity @boards-put
  Scenario: Verify that update list endpoint return an updated list
    As user, I want to update an specific card on Trello

    Given a valid ID for "list" object
    When I call to "lists" endpoint using "put" option for provided ID
    Then I receive the response to validate with "get_list" file
    And I validated the status code is 200