@functional
Feature: Functional
 
  @functional-board_limit
  Scenario: Verify that error is returned after create board when limit of ten is exceded 
    As user, I want to get an error returned whe limit is reached for Board creation.

    Given a valid ID for "Organization" object
    And current quantity of created boards
    When I created boards until limit provided for free accounts: 10
    Then I try to create an extra board
    And I validated the status code is 400


  @card_id
  @functional-card_moving
  Scenario: Verify that a card can be moved betwwen all existent lists in a board
    As user, I want to see that a card can be moved between lists in a board

    Given a valid ID for "Card" object
    And compile all available "lists" on a board
    When I move card between all avaiable "lists"
    Then I receive the response to validate with "update_card" file
    And I validated the status code is 200