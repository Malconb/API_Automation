import logging
import pytest
import requests

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class Testlist:

    @classmethod
    def setup_class(cls):
        """
        Setup class for artist
        """
        cls.apikey = "5ac0c437ec18dffa026109fd7663759f"
        cls.apitoken = "ATTA846ab480e3aa57a03aaae484a9a29f79791b08edebb2a37588ed5b84426028240D8B858A"
        cls.url_trello = "https://api.trello.com/1"
        cls.board_id = "660a22a04497144c6200e487"
        cls.list_id = "660a22aac61158da1bff6975"
        response = requests.get(f"{cls.url_trello}/boards/{cls.board_id}/lists?key={cls.apikey}&token={cls.apitoken}")
        cls.trellolist_id = response.json()[0]["id"]
        LOGGER.debug("list %s", cls.trellolist_id)

    @pytest.mark.sanity
    def test_get_lists(self):
        """
        test get lists from a board
        """
        LOGGER.info("Test Get lists from a board")
        self.url_trello_labels = f"{self.url_trello}/boards/{self.board_id}/lists?key={self.apikey}&token={self.apitoken}"
        response = requests.get(self.url_trello_labels)
        LOGGER.debug("Json response: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_get_list(self):
        """
        test get an specific list from a board
        """
        LOGGER.info("Test Get an specific list from a board")
        self.url_trello_lists = f"{self.url_trello}/lists/{self.trellolist_id}?key={self.apikey}&token={self.apitoken}"
        response = requests.get(self.url_trello_lists)
        LOGGER.debug("Response to get a list Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.sanity
    def test_create_list(self):
        """
        test create an specific list from a board
        """
        LOGGER.info("Test Create a list for a board")
        body_project = {
            'name': 'Test Create a list2',
            'idBoard': self.board_id,
            'key': self.apikey,
            'token': self.apitoken
        }
        response = requests.post(f"{self.url_trello}/lists", data=body_project)
        LOGGER.debug("Response to CREATE a list Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"

    @pytest.mark.acceptance
    def test_update_list(self):
        """
            test update a list from a board
        """
        LOGGER.info("Test Update a list from a board")
        body_project = {
            'key': self.apikey,
            'token': self.apitoken,
            'name': 'Updated Test list'
        }
        response = requests.put(f"{self.url_trello}/lists/{self.trellolist_id}", data=body_project)
        LOGGER.debug("Response to UPDATE a list Json: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        assert response.status_code == 200, "HTTP response error, expected 200"
