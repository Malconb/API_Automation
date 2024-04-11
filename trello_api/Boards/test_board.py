import logging

import pytest
import requests

from helpers import rest_client
from helpers.rest_client import RestClient
from utils.logger import get_logger
from config.config import url_trello, board_id, key_trello, token_trello, body_main, credentials

LOGGER = get_logger(__name__, logging.DEBUG)


class TestBoard:
    @classmethod
    def setup_class(cls):
        """
        Setup class for boards
        """
        cls.rest_client = RestClient()

    def test_get_board(self):
        """
        test get a board
        """
        LOGGER.info("Test Get a board")
        self.url_trello_board = f"{url_trello}/boards/{board_id}?{credentials}"
        response = requests.get(self.url_trello_board)
        LOGGER.debug("Json response: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.acceptance
    def test_create_board(self):
        """
        test create a board
        """
        board_test_id = None
        LOGGER.info("Test Create a Board from conftest")
        body_project = {
            'name': 'Board created from confTest',
            'key': key_trello,
            'token': token_trello
        }
        response = self.rest_client.request("post", f"{url_trello}/boards", body=body_project)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_delete_boards(self, create_board):
        """
            test delete a board from a board
        """
        LOGGER.info("Test Delete a board from a board")
        LOGGER.info("Board_id to be deleted: %s", create_board)
        response = self.rest_client.request("delete",f"{url_trello}/boards/{create_board}", body=body_main)
        assert response.status_code == 200, "HTTP response error, expected 200"

