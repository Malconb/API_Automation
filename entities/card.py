import logging

from config.config import key_trello, token_trello, url_trello, body_main

from entities.list import List
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Card:
    board_id = None

    def __init__(self, rest_client=None):
        self.url_trello_cards = f"{url_trello}/cards"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_card(self, body=None):
        board_test_id = None
        LOGGER.info("Test Create a Board/list from entity")
        list = List()
        list_test, board_test_id = list.create_list()
        list_test_id = list_test["body"]["id"]
        body_project = body
        if body is None:
            body_project = {
                'name': 'card created from Entity',
                'idList': list_test_id,
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_cards}", body=body_project)
        LOGGER.info("card response from entity: %s", response)
        LOGGER.info("Board from entity: %s", board_test_id)

        return response, board_test_id
