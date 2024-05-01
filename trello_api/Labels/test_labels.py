import logging
import pytest

from config.config import key_trello, token_trello, url_trello, body_main, credentials
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestLabel:

    @classmethod
    def setup_class(cls):
        """
        Setup class for labels
        """
        cls.validate = ValidateResponse()
        cls.rest_client = RestClient()


    @pytest.mark.acceptance
    def test_get_all_labels(self, create_board, log_test_name):
        """
        test get all labels from a board
        """
        self.url_trello_labels = f"{url_trello}/boards/{create_board}/labels?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        self.validate.validate_response(response, "labels", "get_all_labels")

    @pytest.mark.acceptance
    @pytest.mark.sanity
    def test_get_label(self, create_label, log_test_name):
        """
        test get an specific label from a board
        """
        self.url_trello_labels = f"{url_trello}/labels/{create_label}?{credentials}"
        response = self.rest_client.request("get",self.url_trello_labels)
        self.validate.validate_response(response, "labels", "get_label")

    @pytest.mark.acceptance
    def test_create_label(self, create_board, log_test_name):
        """
        test create a label from a board
        """
        body_project = body_main
        body_project["name"] = "Test Create a label"
        body_project["idBoard"] = create_board
        response = self.rest_client.request("post",f"{url_trello}/labels", body=body_project)
        self.validate.validate_response(response, "labels", "create_label")

    @pytest.mark.acceptance
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
        self.validate.validate_response(response, "labels", "update_label")

    @pytest.mark.acceptance
    def test_delete_label(self, create_label, log_test_name):
        """
            test delete a label from a board
        """
        response = self.rest_client.request("delete",f"{url_trello}/labels/{create_label}", body=body_main)
        self.validate.validate_response(response, "labels", "delete_label")

