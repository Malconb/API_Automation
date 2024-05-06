import logging

from entities.board import Board
from utils.logger import get_logger
from behave import given, then, when

LOGGER = get_logger(__name__, logging.DEBUG)


@given(u'a valid ID for "{endpoint}" object')
def step_impl(context, endpoint):
    """
    Steps to call get endpoint
    :param endpoint:
    """
    LOGGER.debug(f"STEP: a valid ID for '{endpoint}' object")
    match endpoint:
        case "board":
            context.valid_id = context.new_board_id

        case "list":
            context.valid_id = context.new_list_id

        case "label":
            context.valid_id = context.new_label_id

        case "card":
            context.valid_id = context.new_card_id

    LOGGER.debug("new value: %s", context.valid_id)
    context.endpoint = endpoint


@when(u'I call to "{endpoints}" endpoint using "{method_name}" option and with parameters')
def step_impl(context, endpoint, method_name):
    """
    Steps to call get endpoint
    :param context:
    :param endpoint:
    :param method_name:
    """
    LOGGER.debug(f"STEP: When I call to '{endpoints}' endpoint using '{method_name}' option and with parameters")
    if endpoints == "boards":
        context.url_trello_board = f"{context.url_trello}/organizations/{context.org_id}/boards?{context.credentials}"
    else:
        context.url_trello_board = f"{context.url_trello}/boards/{context.new_board_id}/{endpoint}?{context.credentials}"
    context.response = context.rest_client.request(method_name, context.url_trello_board)
    context.endpoints = endpoints
    context.method_name = method_name

    
@when(u'I call to "{endpoints}" endpoint using "{method_name}" option for provided ID')
def step_impl(context, endpoints, method_name):
    """
    Steps to call get endpoint
    :param context:
    :param endpoint:
    :param method_name:
    """
    LOGGER.debug(f"STEP: When I call to '{endpoints}' endpoint using '{method_name}' option and with parameters")
    if method_name == "get":
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}?{context.credentials}"
        LOGGER.debug("method_name is: %s", method_name)
        context.response = context.rest_client.request(method_name, context.url_trello_call)
        
    else:
        LOGGER.debug("else from when i call to...")
        query = context.body_main
        query["name"] = f"Test Update a {context.endpoint}"
        query[f"id{context.endpoint}"] = context.valid_id
        context.body_request = query
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}"
        LOGGER.debug("url to call: %s", context.url_trello_call)
        LOGGER.debug("body to use: %s", context.body_request)
        context.response = context.rest_client.request(method_name, context.url_trello_call, body=context.body_request)
        
    context.endpoints = endpoints



@then(u'I receive the response to validate with "{json_file}" file')
def step_impl(context, json_file):
    """
    """
    LOGGER.debug(u'STEP: Then I receive the response to validate')
    context.validate.validate_response(context.response, context.endpoints, json_file)


@then(u'I validated the status code is {status_code:d}')
def step_impl(context, status_code):
    LOGGER.debug(f"STEP: Then I validated the status code is {status_code}")
    assert context.response["status_code"] == status_code, \
        f"Expected {status_code} but got {context.response['status_code']}"
