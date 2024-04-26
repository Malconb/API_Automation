import logging

from config.config import url_trello, org_id, credentials
from entities.board import Board
from helpers.response_validator import ValidateResponse
from helpers.rest_client import RestClient
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def before_all(context):
    """
    Fixture to initialize variables and objects
    """
    LOGGER.info("Before all")
    context.rest_client = RestClient()
    context.validate = ValidateResponse()
    context.board_list = []
    context.board = Board()
    context.url_trello = url_trello
    context.org_id = org_id
    context.credentials = credentials

def before_feature(context, feature):
    """
    :param context:
    :param feature:
    """
    LOGGER.info("Before feature")


def before_scenario(context, scenario):
    """
        :param context:
        :param scenario:
        """
    LOGGER.info("Before scenario")


def after_scenario(context, scenario):
    """
        :param context:
        :param scenario:
        """
    LOGGER.info("after scenario")


def after_feature(context, feature):
    """
            :param context:
            :param feature:
            """
    LOGGER.info("after feature")


def after_all(context):
    """
            :param context:
            """
    LOGGER.info("after all")
