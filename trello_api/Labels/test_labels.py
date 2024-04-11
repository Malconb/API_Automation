import logging
import pytest

from config.config import board_id, key_trello, token_trello, url_trello, body_main
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Testlabel:

    @classmethod
    def setup_class(cls):
        """
        Setup class for labels
        """
        cls.rest_client = RestClient()
        response = cls.rest_client.request("get",f"{url_trello}/boards/{board_id}/labels?key={key_trello}&token={token_trello}")
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
        response = self.rest_client.request("get",self.url_trello_labels)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_get_label(self):
        """
        test get an specific label from a board
        """
        LOGGER.info("Test Get an specific label from a board")
        self.url_trello_labels = f"{url_trello}/labels/{self.trellolabel_id}?key={key_trello}&token={token_trello}"
        response = self.rest_client.request("get",self.url_trello_labels)
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
        response = self.rest_client.request("post",f"{url_trello}/labels", body=body_project)
        if response.status_code == 200:
            self.label_list.append(response.json()["id"])
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
        response = self.rest_client.request("put",f"{url_trello}/labels/{create_label}", body=body_project)
        if response.status_code == 200:
            self.label_list.append(response.json()["id"])
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_delete_labels(self, create_label):
        """
            test delete a label from a board
        """
        LOGGER.info("Test Delete a label from a board")
        response = self.rest_client.request("delete",f"{url_trello}/labels/{create_label}", body=body_main)
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
            response = cls.rest_client.request("delete", f"{url_trello}/labels/{label_id}", body=body_label)
            if response.status_code == 200:
                LOGGER.debug("Deleted label by teardown: %s", label_id)

