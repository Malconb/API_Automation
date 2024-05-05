@cards
Feature: Lists

  @card_id 
  @acceptance @sanity @cards-get_all
  Scenario: Verify that get all cards endpoint return all created cards
    As user, I want to get all cards from a board on Trello API

    When I call to "cards" endpoint using "GET" option and with parameters
    Then I receive the response to validate with "get_all_cards" file
    And I validated the status code is 200

  @card_id 
  @acceptance @sanity @boards-get
  Scenario: Verify that get card endpoint return a card
    As user, I want to get an specific card on Trello

    Given a valid ID for "card" object
    When I call to "cards" endpoint using "GET" option for provided ID
    Then I receive the response to validate with "get_card" file
    And I validated the status code is 200