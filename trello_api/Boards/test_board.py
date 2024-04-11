import logging

import requests

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)

class TestBoard:
    @classmethod
    def setup_class(cls):
        """
        Setup class for boards
        """
        cls.apikey= "5ac0c437ec18dffa026109fd7663759f"
        cls.apitoken= "ATTA846ab480e3aa57a03aaae484a9a29f79791b08edebb2a37588ed5b84426028240D8B858A"
        cls.url_trello = "https://api.trello.com/1"
        cls.board_id = "660a22a04497144c6200e487"



    def test_get_board(self):
        """
        test get a board
        """
        LOGGER.info("Test Get a board")
        self.url_trello_board = f"{self.url_trello}/boards/{self.board_id}?key={self.apikey}&token={self.apitoken}"
        response = requests.get(self.url_trello_board)
        LOGGER.debug("Json response: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code== 200, "HTTP response error, expected 200"

