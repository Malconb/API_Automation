"""Module Test Cards """

import logging

import allure
import pytest

from config.config import url_trello, credentials, body_main
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.feature("feature card")
@allure.suite("Card suite")
@pytest.mark.cards
class TestCard:
    """
        class for Test Cards
    """
    @classmethod
    def setup_class(cls):
        """
        Setup class for Cards
        """
        cls.validate = ValidateResponse()
        cls.rest_client = RestClient()
        cls.url_trello_cards = None
        cls.url_trello_lists = None
        body_project = body_main
        body_project["name"] = "Board created for Card testing"
        response = cls.rest_client.request("post", f"{url_trello}/boards", body=body_project)
        cls.board_id = response["body"]["id"]
        LOGGER.debug("Board: %s", cls.board_id)
        response = cls.rest_client.request("get", f"{url_trello}/boards/{cls.board_id}/lists?{credentials}")
        list_id = response["body"][0]["id"]
        body_project = body_main
        body_project["name"] = "setup class, Create a Card"
        body_project["idList"] = list_id
        response = cls.rest_client.request("post", f"{url_trello}/Cards", body=body_project)
        cls.card_id = response["body"]["id"]

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_get_all_cards(self, log_test_name):
        """
        test get all Cards from a board
        """
        self.url_trello_cards = f"{url_trello}/boards/{self.board_id}/Cards?{credentials}"
        response = self.rest_client.request("get", self.url_trello_cards)
        self.validate.validate_response(response, "cards", "get_all_cards")

    @allure.severity("normal")
    @pytest.mark.sanity
    @pytest.mark.acceptance
    def test_get_card(self, create_card, log_test_name):
        """
        test get a specific a list from a board
        """
        self.url_trello_cards = f"{url_trello}/Cards/{create_card}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_cards)
        self.validate.validate_response(response, "cards", "get_card")

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_create_card(self, create_list, main_body, log_test_name):
        """
        test create a Card from a list
        """
        body_project = main_body
        body_project["name"] = "Test Create a Card"
        body_project["idList"] = create_list
        response = self.rest_client.request("post", f"{url_trello}/Cards", body=body_project)
        self.validate.validate_response(response, "cards", "create_card")

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_update_card(self, create_card, main_body, log_test_name):
        """
            test update a card from a Board
        """
        body_project = main_body
        body_project["name"] = "Updated Card"
        response = self.rest_client.request("put", f"{url_trello}/Cards/{create_card}", body=body_project)
        self.validate.validate_response(response, "cards", "update_card")

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_delete_card(self, create_card, main_body, log_test_name):
        """
            test delete a Card from a board
        """
        body_project = main_body
        response = self.rest_client.request("delete", f"{url_trello}/Cards/{create_card}", body=body_project)
        self.validate.validate_response(response, "cards", "delete_card")

    @allure.severity("critical")
    @allure.suite("Functional suite")
    @pytest.mark.functional
    def test_card_move_among_lists(self, main_body, log_test_name):
        """
            test card is able to move between all lists in a Board
        """
        self.url_trello_lists = f"{url_trello}/boards/{self.board_id}/lists?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        num_of_lists = len(response["body"])
        LOGGER.debug("number of lists: %s", num_of_lists)
        list_of_listids = response["body"]
        for index in range(0, num_of_lists):
            body_moved_card = main_body
            body_moved_card["idList"] = list_of_listids[index]["id"]
            LOGGER.debug("Moving card to list_id: %s", body_moved_card["idList"])
            response = self.rest_client.request("put", f"{url_trello}/Cards/{self.card_id}", body=body_moved_card)
            self.validate.validate_response(response, "cards", "update_card")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class for Cards
        """
        LOGGER.debug("Teardown class for Cleaning board created for Card testing")
        response = cls.rest_client.request("delete", f"{url_trello}/boards/{cls.board_id}", body=body_main)
        if response["status_code"] == 200:
            LOGGER.debug("Deleted board by Label teardown class: %s", cls.board_id)
