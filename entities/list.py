import logging

from config.config import key_trello, token_trello, url_trello, body_main
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
        body_project = body
        if body is None:
            body_project = {
                'name': 'list created from Entity',
                'idBoard': self.board_id,
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_lists}", body=body_project)

        return response, self.rest_client

    def delete_list(self, list_test_id):

        LOGGER.debug("Cleanup project")
        response = self.rest_client.request("delete", f"{url_trello}/boards/{list_test_id}", body=body_main)
        if response["status_code"] == 200:
            LOGGER.debug("Deleted card by entity: %s", list_test_id)

