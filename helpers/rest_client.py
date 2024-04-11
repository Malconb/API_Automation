import logging

import requests

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class RestClient:

    def __init__(self):
        self.session = requests.session()

    def request(self, method_name, url, body=None):
        """
        response["status_code"]
        response["headers"]
        response["body"]
        """
        
        response = self.select_method(method_name, self.session)(url=url, data=body)
        LOGGER.debug("Response to request: %s", response.json())
        LOGGER.debug("Status Code: %s", response.status_code)
        return response

    @staticmethod
    def select_method(method_name, session):
        """
        Select REST method with session object
        :param method_name:
        :param session:
        :return:
        """
        methods = {
            "get": session.get,
            "post": session.post,
            "put": session.put,
            "delete": session.delete
        }
        return methods.get(method_name)
