import logging

from config.config import url_trello, org_id, credentials, body_main
from entities.board import Board
from entities.card import Card
from entities.label import Label
from entities.list import List
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
    context.url_trello = url_trello
    context.org_id = org_id
    context.credentials = credentials
    context.body_main = body_main

    context.board = Board()
    context.list = List()
    context.label = Label()
    context.card = Card()

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
    context.board_list = []
    LOGGER.info("Before scenario")
    if "board_id" in scenario.tags:
        new_board = context.board.create_board()
        context.new_board_id = new_board["body"]["id"]
        context.board_list.append(new_board["body"]["id"])
    elif "list_id" in scenario.tags:
        new_list, context.new_board_id = context.list.create_list()
        context.new_list_id = new_list["body"]["id"]
        context.board_list.append(context.new_board_id)
    elif "label_id" in scenario.tags:
        new_label, context.new_board_id = context.label.create_label()
        context.new_label_id = new_label["body"]["id"]
        context.board_list.append(context.new_board_id)
    elif "card_id" in scenario.tags:
        new_card, context.new_board_id = context.card.create_card()
        context.new_card_id = new_card["body"]["id"]
        context.board_list.append(context.new_board_id)
        



def after_scenario(context, scenario):
    """
        :param context:
        :param scenario:
        """
    LOGGER.info("after scenario")
    for test_board_id in context.board_list:
            response = context.rest_client.request("delete", f"{context.url_trello}/boards/{test_board_id}", body=context.body_main)
            if response["status_code"] == 200:
                LOGGER.debug("Board deleted after scenario: %s", test_board_id)


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
