import logging
import pytest
import requests

from config.config import board_id, key_trello, token_trello, url_trello
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_label():
    label_id = None
    rest_client = RestClient()
    LOGGER.info("Test Create a label for a board from conftest")
    body_project = {
        'name': 'Create a label from confTest',
        'color': 'blue',
        'idBoard': board_id,
        'key': key_trello,
        'token': token_trello
    }
    response = rest_client.request("post", f"{url_trello}/labels", body=body_project)
    assert response["status_code"] == 200, "HTTP response error, expected 200"
    if response["status_code"] == 200:
        label_id = response["body"]["id"]
    return label_id

@pytest.fixture()
def create_board():
    board_test_id = None
    rest_client = RestClient()
    LOGGER.info("Test Create a Board from conftest")
    body_project = {
        'name': 'Board created from confTest',
        'key': key_trello,
        'token': token_trello
    }
    response = rest_client.request("post", f"{url_trello}/boards", body=body_project)
    assert response.status_code == 200, "HTTP response error, expected 200"
    if response.status_code == 200:
        board_test_id = response.json()["id"]
    return board_test_id

@pytest.fixture()
def log_test_name (request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)