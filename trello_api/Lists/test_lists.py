import logging
import pytest


from config.config import url_trello, board_id, key_trello, token_trello, credentials, body_main
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Testlist:

    @classmethod
    def setup_class(cls):
        """
        Setup class for artist
        """
        cls.rest_client = RestClient()
        response = cls.rest_client.request("get",f"{url_trello}/boards/{board_id}/lists?{credentials}")
        cls.trellolist_id = response["body"][0]["id"]
        LOGGER.debug("list %s", cls.trellolist_id)
        cls.lists_list = []
        cls.validate = ValidateResponse()

    @pytest.mark.sanity
    def test_get_all_lists(self, log_test_name):
        """
        test get lists from a board
        """
        self.url_trello_labels = f"{url_trello}/boards/{board_id}/lists?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        self.validate.validate_response(response, "lists", "get_all_lists")

    @pytest.mark.sanity
    def test_get_list(self, log_test_name):
        """
        test get an specific list from a board
        """
        self.url_trello_lists = f"{url_trello}/lists/660a22b1e9b74ea661d4cc0d?{credentials}"
        response = self.rest_client.request("get",self.url_trello_lists)
        self.validate.validate_response(response, "lists", "get_list")

    @pytest.mark.sanity
    def test_create_list(self, log_test_name):
        """
        test create an specific list from a board
        """
        body_project = {
            'name': 'Test Create a list2',
            'idBoard': board_id,
            'key': key_trello,
            'token': token_trello
        }
        response = self.rest_client.request("post",f"{url_trello}/lists", body=body_project)
        self.validate.validate_response(response, "lists", "create_list")

    @pytest.mark.sanity
    def test_update_list(self, log_test_name):
        """
            test update a list from a board
        """
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated Test list2'
        }
        response = self.rest_client.request("put",f"{url_trello}/lists/{self.trellolist_id}", body=body_project)
        self.validate.validate_response(response, "lists", "update_list")

    @pytest.mark.acceptance
    def test_archive_list(self, log_test_name):
        """
            test update a list from a board
        """
        body_archive = {
            'value': 'true',
            'key': key_trello,
            'token': token_trello
        }
        response = self.rest_client.request("put", f"{url_trello}/lists/660a22b1e9b74ea661d4cc0d/closed", body=body_archive)
        self.validate.validate_response(response, "lists", "update_list")
