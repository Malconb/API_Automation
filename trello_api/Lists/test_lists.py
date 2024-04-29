import logging
import pytest

from config.config import url_trello, key_trello, token_trello, credentials, body_main
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

    @pytest.mark.sanity
    def test_get_all_lists(self, create_board, log_test_name):
        """
        test get lists from a board
        """
        self.url_trello_lists = f"{url_trello}/boards/{create_board}/lists?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        self.validate.validate_response(response, "lists", "get_all_lists")

    @pytest.mark.sanity
    def test_get_list(self, create_list, log_test_name):
        """
        test get a specific a list from a board
        """
        self.url_trello_lists = f"{url_trello}/lists/{create_list}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_lists)
        self.validate.validate_response(response, "lists", "get_list")

    @pytest.mark.sanity
    def test_create_list(self, create_board, log_test_name):
        """
        test create a specific list from a board
        """
        body_project = body_main
        body_project["name"] = "Test Create a list"
        body_project["idBoard"] = create_board
        response = self.rest_client.request("post", f"{url_trello}/lists", body=body_project)
        self.validate.validate_response(response, "lists", "create_list")

    @pytest.mark.sanity
    def test_update_list(self, create_list, log_test_name):
        """
            test update a list from a board
        """
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated list'
        }
        response = self.rest_client.request("put", f"{url_trello}/lists/{create_list}", body=body_project)
        self.validate.validate_response(response, "lists", "update_list")

    @pytest.mark.acceptance
    def test_delete_list(self, create_list, log_test_name):
        """
            test archive a list from a board
        """
        body_project = body_main
        body_project["value"] = "true"
        response = self.rest_client.request("put", f"{url_trello}/lists/{create_list}/closed", body=body_project)
        self.validate.validate_response(response, "lists", "update_list")

