import logging
import pytest

from config.config import board_id, key_trello, token_trello, url_trello, body_main, credentials
from helpers.response_validator import ValidateResponse
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
        response = cls.rest_client.request("get",f"{url_trello}/boards/{board_id}/labels?{credentials}")
        cls.trellolabel_id = response["body"][0]["id"]
        LOGGER.debug("labels %s", cls.trellolabel_id)
        cls.label_list = []
        cls.validate = ValidateResponse()


    @pytest.mark.acceptance
    def test_get_all_labels(self, log_test_name):
        """
        test get all labels from a board
        """
        self.url_trello_labels = f"{url_trello}/boards/{board_id}/labels?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        self.validate.validate_response(response, "labels", "get_all_labels")

    @pytest.mark.sanity
    def test_get_label(self, log_test_name):
        """
        test get an specific label from a board
        """
        self.url_trello_labels = f"{url_trello}/labels/{self.trellolabel_id}?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        self.validate.validate_response(response, "labels", "get_label")

    @pytest.mark.acceptance
    def test_create_label(self, log_test_name):
        """
        test create an specific label from a board
        """
        body_project = {
            'name': 'Test Create a label',
            'color': 'black',
            'idBoard': board_id,
            'key': key_trello,
            'token': token_trello
        }
        response = self.rest_client.request("post",f"{url_trello}/labels", body=body_project)
        if response["status_code"] == 200:
            self.label_list.append(response["body"]["id"])
        self.validate.validate_response(response, "labels", "create_label")

    @pytest.mark.sanity
    def test_update_label(self, create_label, log_test_name):
        """
            test update a label from a board
        """
        body_project = {
            'key': key_trello,
            'token': token_trello,
            'name': 'Updated label'
        }
        response = self.rest_client.request("put",f"{url_trello}/labels/{create_label}", body=body_project)
        if response["status_code"] == 200:
            self.label_list.append(response["body"]["id"])
        self.validate.validate_response(response, "labels", "update_label")

    @pytest.mark.sanity
    def test_delete_label(self, create_label, log_test_name):
        """
            test delete a label from a board
        """
        response = self.rest_client.request("delete",f"{url_trello}/labels/{create_label}", body=body_main)
        self.validate.validate_response(response, "labels", "delete_label")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")
        LOGGER.debug("Cleanup labels")
        for label_id in cls.label_list:
            response = cls.rest_client.request("delete", f"{url_trello}/labels/{label_id}", body=body_main)
            if response["status_code"] == 200:
                LOGGER.debug("Deleted label by teardown: %s", label_id)

