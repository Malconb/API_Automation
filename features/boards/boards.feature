@boards
Feature: Boards

  @acceptance
  Scenario: Verify that get all boards endpoint return all created boards
    As user, I want to get all Boards on Trello API

    When I call to "Boards" endpoint using "GET" option and with parameters
    Then I receive the response to validate
    And I validated the status code is 200


  Scenario: Verify that create board endpoint return a created boards
    As user, I want to create a Board on Trello API

    When I call to "Boards" endpoint using "POST" option and with parameters test
    """
    {'key': key_trello, 'token': token_trello,'name': 'Updated Board'}
    """
    Then I receive the response to validate
    And I validated the status code is 200