import logging

from config.config import key_trello, token_trello, url_trello, body_main
from entities.board import Board
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Label:
    board_id = None

    def __init__(self, rest_client=None):
        self.url_trello_labels = f"{url_trello}/labels"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_label(self, body=None):
        board_test_id = None
        LOGGER.info("Test Create a Board from entity")
        board = Board()
        board_test = board.create_board()
        board_test_id = board_test["body"]["id"]
        body_project = body
        if body is None:
            body_project = {
                'name': 'label created from Entity',
                'idBoard': board_test_id,
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_labels}", body=body_project)

        return response, board_test_id
