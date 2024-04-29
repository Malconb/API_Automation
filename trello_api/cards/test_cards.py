import logging
import pytest

from config.config import url_trello, key_trello, token_trello, credentials, body_main
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestCard:

    @classmethod
    def setup_class(cls):
        """
        Setup class for labels
        """
        cls.validate = ValidateResponse()
        cls.rest_client = RestClient()
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
        response = cls.rest_client.request("post", f"{url_trello}/cards", body=body_project)
        cls.card_id = response["body"]["id"]


    @pytest.mark.sanity
    def test_get_all_cards(self, log_test_name):
        """
        test get all cards from a board
        """
        self.url_trello_cards = f"{url_trello}/boards/{self.board_id}/cards?{credentials}"
        response = self.rest_client.request("get", self.url_trello_cards)
        self.validate.validate_response(response, "cards", "get_all_cards")

    @pytest.mark.sanity
    def test_get_card(self, create_card, log_test_name):
        """
        test get a specific a list from a board
        """
        self.url_trello_cards = f"{url_trello}/cards/{create_card}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_cards)
        self.validate.validate_response(response, "cards", "get_card")

    @pytest.mark.sanity
    def test_create_card(self, create_list, log_test_name):
        """
        test create a Card from a list
        """
        body_project = body_main
        body_project["name"] = "Test Create a Card"
        body_project["idList"] = create_list
        response = self.rest_client.request("post", f"{url_trello}/cards", body=body_project)
        self.validate.validate_response(response, "cards", "create_card")

    @pytest.mark.sanity
    def test_update_card(self, create_card, log_test_name):
        """
            test update a card from a Board
        """
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated Card'
        }
        response = self.rest_client.request("put", f"{url_trello}/cards/{create_card}", body=body_project)
        self.validate.validate_response(response, "cards", "update_card")

    @pytest.mark.acceptance
    def test_delete_card(self, create_card, log_test_name):
        """
            test delete a Card from a board
        """
        body_project = body_main
        response = self.rest_client.request("delete", f"{url_trello}/cards/{create_card}", body=body_project)
        self.validate.validate_response(response, "cards", "delete_card")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class for Cards
        """
        LOGGER.debug("Teardown class for Cleaning board created for Card testing")
        response = cls.rest_client.request("delete", f"{url_trello}/boards/{cls.board_id}", body=body_main)
        if response["status_code"] == 200:
            LOGGER.debug("Deleted board by Label teardown class: %s", cls.board_id)
