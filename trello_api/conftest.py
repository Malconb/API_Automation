import logging
import pytest

from config.config import key_trello, token_trello, url_trello
from entities.board import Board
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_board():
    board_test_id = None
    LOGGER.info("Test Create a Board from conftest")
    board = Board()
    response, rest_client = board.create_board()
    if response["status_code"] == 200:
        board_test_id = response["body"]["id"]

    yield board_test_id
    LOGGER.debug("Yield fixture delete board: %s", board_test_id)
    delete_board(board_test_id, board)


def delete_board(board_test_id, board):
    LOGGER.debug("yield process for board_id: %s", board_test_id)
    board.delete_board(board_test_id)


@pytest.fixture()
def create_label(create_board):
    label_id = None
    rest_client = RestClient()
    LOGGER.info("Test Create a label for a board from conftest")
    body_project = {
        'name': 'Create a label from confTest',
        'color': 'blue',
        'idBoard': create_board,
        'key': key_trello,
        'token': token_trello
    }
    response = rest_client.request("post", f"{url_trello}/labels", body=body_project)
    assert response["status_code"] == 200, "HTTP response error, expected 200"
    if response["status_code"] == 200:
        label_id = response["body"]["id"]
    return label_id


@pytest.fixture()
def create_list(create_board):
    list_id = None
    rest_client = RestClient()
    LOGGER.info("Test Create a list for a board from conftest")
    body_project = {
        'name': 'Create a list from confTest',
        'idBoard': create_board,
        'key': key_trello,
        'token': token_trello
    }
    response = rest_client.request("post", f"{url_trello}/lists", body=body_project)
    assert response["status_code"] == 200, "HTTP response error, expected 200"
    if response["status_code"] == 200:
        list_id = response["body"]["id"]
    return list_id

@pytest.fixture()
def create_card(create_list):
    card_id = None
    rest_client = RestClient()
    LOGGER.info("Test Create a Card for a list from conftest")
    body_project = {
        'name': 'Create a Card from confTest',
        'idList': create_list,
        'key': key_trello,
        'token': token_trello
    }
    response = rest_client.request("post", f"{url_trello}/cards", body=body_project)
    assert response["status_code"] == 200, "HTTP response error, expected 200"
    if response["status_code"] == 200:
        card_id = response["body"]["id"]
    return card_id

@pytest.fixture()
def main_body():
    body_main = {
        'key': key_trello,
        'token': token_trello
    }
    return body_main


@pytest.fixture()
def log_test_name(request):
    LOGGER.info("Test '%s' STARTED", request.node.name)

    def fin():
        LOGGER.info("Test '%s' COMPLETED", request.node.name)

    request.addfinalizer(fin)
