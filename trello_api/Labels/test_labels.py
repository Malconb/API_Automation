import logging
import pytest
import requests

from config.config import board_id, key_trello, token_trello, url_trello, body_main
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Testlabel:

    @classmethod
    def setup_class(cls):
        """
        Setup class for labels
        """
        response = requests.get(f"{url_trello}/boards/{board_id}/labels?key={key_trello}&token={token_trello}")
        LOGGER.debug("labels: %s", response.json())
        cls.trellolabel_id = response.json()[0]["id"]
        LOGGER.debug("labels %s", cls.trellolabel_id)
        cls.label_list = []

    @pytest.mark.acceptance
    def test_get_labels(self):
        """
        test get all labels from a board
        """
        LOGGER.info("Test Get all labels from a board")
        self.url_trello_labels = f"{url_trello}/boards/{board_id}/labels?key={key_trello}&token={token_trello}"
        response = requests.get(self.url_trello_labels)
        LOGGER.debug("Json response: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_get_label(self):
        """
        test get an specific label from a board
        """
        LOGGER.info("Test Get an specific label from a board")
        self.url_trello_labels = f"{url_trello}/labels/{self.trellolabel_id}?key={key_trello}&token={token_trello}"
        response = requests.get(self.url_trello_labels)
        LOGGER.debug("Response to get a label Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.acceptance
    def test_create_label(self):
        """
        test create an specific label from a board
        """
        LOGGER.info("Test Create a label for a board")
        body_project = {
            'name': 'Test Create a label',
            'color': 'black',
            'idBoard': board_id,
            'key': key_trello,
            'token': token_trello
        }
        response = requests.post(f"{url_trello}/labels", data=body_project)
        if response.status_code == 200:
            self.label_list.append(response.json()["id"])
        LOGGER.debug("Response to CREATE a list Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_update_labels(self, create_label):
        """
            test update a label from a board
        """
        LOGGER.info("Test Update a label from a board")
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated label'
        }
        response = requests.put(f"{url_trello}/labels/{create_label}", data=body_project)
        if response.status_code == 200:
            self.label_list.append(response.json()["id"])
        LOGGER.debug("Response to UPDATE a labels Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_delete_labels(self, create_label):
        """
            test delete a label from a board
        """
        LOGGER.info("Test Delete a label from a board")
        response = requests.delete(f"{url_trello}/labels/{create_label}", data=body_main)
        LOGGER.debug("Response to DELETE a labels Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        body_label = {
            'key': key_trello,
            'token': token_trello
        }
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup labels")
        for label_id in cls.label_list:
            response = requests.delete(f"{url_trello}/labels/{label_id}", data=body_label)
            if response.status_code == 200:
                LOGGER.debug("Deleted label by teardown: %s", label_id)

