import logging

import allure
import pytest
from entities.board import Board
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger
from config.config import url_trello, body_main, credentials, org_id

LOGGER = get_logger(__name__, logging.DEBUG)


@allure.feature("feature board")
class TestBoard:
    @classmethod
    def setup_class(cls):
        """
        Setup class for boards
        """
        cls.rest_client = RestClient()
        cls.validate = ValidateResponse()
        cls.board_list = []
        cls.board = Board()

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_get_all_boards(self, log_test_name):
        """
        test get a board
        """
        self.url_trello_board = f"{url_trello}/organizations/{org_id}/boards?{credentials}"
        response = self.rest_client.request("get", self.url_trello_board)
        self.validate.validate_response(response, "boards", "get_all_boards")

    @allure.severity("normal")
    @pytest.mark.sanity
    @pytest.mark.acceptance
    def test_get_board(self, create_board, log_test_name):
        """
        test get a board
        """
        self.url_trello_board = f"{url_trello}/boards/{create_board}?{credentials}"
        response = self.rest_client.request("get", self.url_trello_board)
        if response["status_code"] == 200:
            self.board_list.append(response["body"]["id"])
        self.validate.validate_response(response, "boards", "get_board")

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_update_board(self, create_board, main_body, log_test_name):
        """
            test update a board
        """
        body_project = main_body
        body_project["name"] = "Updated board"
        response = self.rest_client.request("put", f"{url_trello}/boards/{create_board}", body=body_project)
        if response["status_code"] == 200:
            self.board_list.append(response["body"]["id"])
        self.validate.validate_response(response, "boards", "update_board")

    @allure.severity("normal")
    @pytest.mark.acceptance
    def test_create_board(self, main_body, log_test_name):
        """
        test create a board
        """
        body_project = main_body
        body_project["name"] = "Board created for Test Create request"
        response = self.rest_client.request("post", f"{url_trello}/boards", body=body_project)
        if response["status_code"] == 200:
            self.board_list.append(response["body"]["id"])
        self.validate.validate_response(response, "boards", "create_board")

    @allure.severity ("normal")
    @pytest.mark.acceptance
    def test_delete_board(self, create_board, main_body, log_test_name):
        """
            test delete a board
        """
        LOGGER.info("Board_id to be deleted: %s", create_board)
        response = self.rest_client.request("delete", f"{url_trello}/boards/{create_board}", body=main_body)
        self.validate.validate_response(response, "boards", "delete_board")

    @allure.severity("critical")
    @pytest.mark.functional
    def test_max_number_boards(self, main_body, log_test_name):
        """
        Test to validate
        """
        self.url_trello_board = f"{url_trello}/organizations/{org_id}/boards?{credentials}"
        response = self.rest_client.request("get", self.url_trello_board)
        num_of_boards = len(response["body"])
        LOGGER.debug("number of boards: %s", num_of_boards)
        for index in range(num_of_boards, 10):
            body_project = main_body
            body_project["name"] = "Board created for Max num of Boards test"
            response, _ = self.board.create_board(body=body_project)
            if response["status_code"] == 200:
                self.board_list.append(response["body"]["id"])

        # Try for exceeded board
        response, _ = self.board.create_board()
        if response["status_code"] == 200:
            self.board_list.append(response["body"]["id"])
        self.validate.validate_response(response, "boards", "max_number_boards")

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class for Cleaning created boards")
        for test_board_id in cls.board_list:
            response = cls.rest_client.request("delete", f"{url_trello}/boards/{test_board_id}", body=body_main)
            if response["status_code"] == 200:
                LOGGER.debug("Deleted board by teardown: %s", test_board_id)
