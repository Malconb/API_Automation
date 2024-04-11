import logging
import pytest
import requests

from config.config import board_id, key_trello, token_trello, url_trello
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def create_label():
    label_id = None

    LOGGER.info("Test Create a label for a board from conftest")
    body_project = {
        'name': 'Create a label from confTest',
        'color': 'blue',
        'idBoard': board_id,
        'key': key_trello,
        'token': token_trello
    }
    response = requests.post(f"{url_trello}/labels", data=body_project)
    LOGGER.debug("Response to CREATE a list Json: %s", response.json())
    LOGGER.debug("Status Code: %s", response.status_code)
    assert response.status_code == 200, "HTTP response error, expected 200"

    if response.status_code == 200:
        label_id = response.json()["id"]

    return label_id
