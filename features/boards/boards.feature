@boards
Feature: Boards

  @acceptance @sanity
  Scenario: Verify that get all boards endpoint return all created boards
    As user, I want to get all Boards on Trello API

    When I call to "Boards" endpoint using "GET" option and with parameters
    Then I receive the response to validate
    And I validated the status code is 200

