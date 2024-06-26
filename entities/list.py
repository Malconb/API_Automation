import logging

from config.config import key_trello, token_trello, url_trello, body_main
from entities.board import Board
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class List:
    board_id = None

    def __init__(self, rest_client=None):
        self.url_trello_lists = f"{url_trello}/lists"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_list(self, body=None):
        board_test_id = None
        LOGGER.info("Test Create a Board from entity")
        board = Board()
        board_test = board.create_board()
        board_test_id = board_test["body"]["id"]
        body_project = body
        if body is None:
            body_project = {
                'name': 'list created from Entity',
                'idBoard': board_test_id,
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_lists}", body=body_project)

        return response, board_test_id
