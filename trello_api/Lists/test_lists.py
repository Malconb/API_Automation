import logging
import pytest

from config.config import url_trello, key_trello, token_trello, credentials, body_main, org_id
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Testlist:

    @classmethod
    def setup_class(cls):
        """
        Setup class for labels
        """
        cls.validate = ValidateResponse()
        cls.rest_client = RestClient()
        cls.board_list = []

    @pytest.mark.acceptance
    def test_get_all_lists(self, create_board, log_test_name):
        """
        test get lists from a board
        """
        self.url_trello_lists = f"{url_trello}/boards/{create_board}/lists?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        self.validate.validate_response(response, "lists", "get_all_lists")

    @pytest.mark.acceptance
    @pytest.mark.sanity
    def test_get_list(self, create_list, log_test_name):
        """
        test get a specific a list from a board
        """
        self.url_trello_lists = f"{url_trello}/lists/{create_list}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        self.validate.validate_response(response, "lists", "get_list")

    @pytest.mark.acceptance
    def test_create_list(self, create_board, main_body, log_test_name):
        """
        test create a specific list from a board
        """
        body_project = main_body
        body_project["name"] = "Test Create a list"
        body_project["idBoard"] = create_board
        response = self.rest_client.request("post", f"{url_trello}/lists", body=body_project)
        self.validate.validate_response(response, "lists", "create_list")

    @pytest.mark.acceptance
    def test_update_list(self, create_list, main_body, log_test_name):
        """
            test update a list from a board
        """
        body_project = main_body
        body_project["name"] = "Updated list"
        response = self.rest_client.request("put", f"{url_trello}/lists/{create_list}", body=body_project)
        self.validate.validate_response(response, "lists", "update_list")

    @pytest.mark.acceptance
    def test_delete_list(self, create_list, main_body, log_test_name):
        """
            test archive a list from a board
        """
        body_project = main_body
        body_project["value"] = "true"
        response = self.rest_client.request("put", f"{url_trello}/lists/{create_list}/closed", body=body_project)
        self.validate.validate_response(response, "lists", "update_list")

    @pytest.mark.functional
    def test_move_list_between_boards(self, create_list, main_body, log_test_name):
        """
            test to validate cards are as archived after list is deleted
        """
        body_move = main_body

        self.url_trello_lists = f"{url_trello}/lists/{create_list}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        list_board_id = response["body"]["idBoard"]
        LOGGER.debug("current board for list in scope: %s", list_board_id)

        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'New Board created for Test move list between boards'
        }
        response = self.rest_client.request("post", f"{url_trello}/boards", body=body_project)
        LOGGER.debug("New board for test: %s", response["body"]["id"])
        new_board_id = response["body"]["id"]
        if response["status_code"] == 200:
            self.board_list.append(response["body"]["id"])

        body_move["value"] = response["body"]["id"]
        url_move = f"{url_trello}/lists/{create_list}/idBoard"
        response = self.rest_client.request("put", url_move, body=body_move)
        assert response["body"]["idBoard"] == new_board_id
        self.validate.validate_response(response, "lists", "update_list")
        LOGGER.debug("List moved to board: %s", response["body"]["idBoard"])

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class for Cleaning created boards")
        for test_board_id in cls.board_list:
            response = cls.rest_client.request("delete", f"{url_trello}/boards/{test_board_id}", body=body_main)
            if response["status_code"] == 200:
                LOGGER.debug("Deleted board by teardown: %s", test_board_id)
