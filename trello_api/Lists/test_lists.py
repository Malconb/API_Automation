import logging
import pytest
import requests

from config.config import url_trello, board_id, key_trello, token_trello, credentials
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
        cls.trellolist_id = response.json()[0]["id"]
        LOGGER.debug("list %s", cls.trellolist_id)
        cls.lists_list = []

    @pytest.mark.acceptance
    def test_get_lists(self):
        """
        test get lists from a board
        """
        LOGGER.info("Test Get lists from a board")
        self.url_trello_labels = f"{url_trello}/boards/{board_id}/lists?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_get_list(self):
        """
        test get an specific list from a board
        """
        LOGGER.info("Test Get an specific list from a board")
        self.url_trello_lists = f"{url_trello}/lists/{self.trellolist_id}?{credentials}"
        response = self.rest_client.request("get",self.url_trello_lists)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_create_list(self):
        """
        test create an specific list from a board
        """
        LOGGER.info("Test Create a list for a board")
        body_project = {
            'name': 'Test Create a list2',
            'idBoard': board_id,
            'key': key_trello,
            'token': token_trello
        }
        response = self.rest_client.request("post",f"{url_trello}/lists", body=body_project)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_update_list(self):
        """
            test update a list from a board
        """
        LOGGER.info("Test Update a list from a board")
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated Test list'
        }
        response = self.rest_client.request("put",f"{url_trello}/lists/{self.trellolist_id}", body=body_project)
        assert response.status_code == 200, "HTTP response error, expected 200"
