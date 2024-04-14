import logging

from config.config import key_trello, token_trello, url_trello
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Board:

    def __init__(self, rest_client=None):
        self.url_trello_boards = f"{url_trello}/boards"
        self.rest_client = rest_client
        if rest_client is None:
            self.rest_client = RestClient()

    def create_project(self, body=None):
        body_project = body
        if body is None:
            body_project = {
                'name': 'Board created from Entity',
                'key': key_trello,
                'token': token_trello
            }
        response = self.rest_client.request("post", f"{self.url_trello_boards}", body=body_project)

        return response, self.rest_client

    def delete_board(self, project_id):

        LOGGER.info("Board_id to be deleted: %s", create_board()[0])
        response = self.rest_client.request("delete", f"{url_trello}/boards/{create_board()[0]}", body=body_main)
        self.validate.validate_response(response, "boards", "delete_board")


        url_delete_project = f"{URL_TODO}/projects/{project_id}"
        response = self.rest_client.request("delete", url_delete_project)
        if response["status_code"] == 204:
            LOGGER.info("project Id deleted : %s", project_id)