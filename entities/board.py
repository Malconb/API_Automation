import logging

from config.config import key_trello, token_trello, url_trello, body_main
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Board:

    def __init__(self, rest_client=None):
        self.url_trello_boards = f"{url_trello}/boards"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_board(self, body=None):
        body_project = body
        if body is None:
            body_project = {
                'name': 'Board created from Entity',
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_boards}", body=body_project)

        return response, self.rest_client

    def delete_board(self, board_test_id):

        LOGGER.debug("Cleanup project")
        response = self.rest_client.request("delete", f"{url_trello}/boards/{board_test_id}", body=body_main)
        if response["status_code"] == 200:
            LOGGER.debug("Deleted board by entity: %s", board_test_id)

