@cards
Feature: Lists

  @card_id 
  @acceptance @sanity @method-get_all
  Scenario: Verify that get all cards endpoint return all created cards
    As user, I want to get all cards from a board on Trello API

    When I call to "cards" endpoint using "get" option and with parameters
    Then I receive the response to validate with "get_all_cards" file
    And I validated the status code is 200

  @card_id 
  @acceptance @method-get
  Scenario: Verify that get card endpoint return a card
    As user, I want to get an specific card on Trello

    Given a valid ID for "Card" object
    When I call to "cards" endpoint using "get" option for provided ID
    Then I receive the response to validate with "get_card" file
    And I validated the status code is 200

  @card_id 
  @acceptance @method-put
  Scenario: Verify that update card endpoint return an updated card
    As user, I want to update an specific card on Trello

    Given a valid ID for "Card" object
    When I call to "cards" endpoint using "put" option for provided ID
    Then I receive the response to validate with "update_card" file
    And I validated the status code is 200

  @list_id
  @acceptance @method-post
  Scenario: Verify that create board endpoint return a created card
    As user, I want to create a card on Trello

    Given a valid ID for "List" object
    When I call to "cards" endpoint using "post" option for provided ID
    Then I receive the response to validate with "create_card" file
    And I validated the status code is 200

  @card_id
  @acceptance  @method-delete
  Scenario: Verify that delete card endpoint deletes a card
    As user, I want to delete a card on Trello

    Given a valid ID for "Card" object
    When I call to "cards" endpoint using "delete" option for provided ID
    Then I receive the response to validate with "delete_card" file
    And I validated the status code is 200