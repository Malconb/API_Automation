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
        case "Board":
            context.valid_id = context.new_board_id

        case "List":
            context.valid_id = context.new_list_id

        case "Label":
            context.valid_id = context.new_label_id

        case "Card":
            context.valid_id = context.new_card_id
        
        case "Organization":
            context.valid_id = context.org_id

    LOGGER.debug("new value: %s", context.valid_id)
    context.endpoint = endpoint


@when(u'I call to "{endpoints}" endpoint using "{method_name}" option and with parameters')
def step_impl(context, endpoints, method_name):
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
        context.url_trello_board = f"{context.url_trello}/boards/{context.new_board_id}/{endpoints}?{context.credentials}"
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
    query = []
    if method_name == "get":
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}?{context.credentials}"
        LOGGER.debug("method_name is: %s", method_name)
        context.response = context.rest_client.request(method_name, context.url_trello_call)
        
    elif method_name == "put":
        query = context.body_main
        query["name"] = f"Testing {method_name} for {context.endpoint} endpoint"
        query[f"id{context.endpoint}"] = context.valid_id
        context.body_request = query
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}"
        context.response = context.rest_client.request(method_name, context.url_trello_call, body=context.body_request)

    elif method_name == "post":
        query = context.body_main
        query["name"] = f"Testing {method_name} for {context.endpoint} endpoint"
        query[f"id{context.endpoint}"] = context.valid_id
        context.body_request = query
        context.url_trello_call = f"{context.url_trello}/{endpoints}"
        context.response = context.rest_client.request(method_name, context.url_trello_call, body=context.body_request)
        if endpoints == "boards":
            context.new_board_id = context.response["body"]["id"]
            context.board_list.append(context.new_board_id)
    
    elif method_name == "delete":
        query = context.body_main
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}"
        if endpoints == "lists":
            query["value"] = "true"
            context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}/closed"
            method_name = "put"
        context.body_request = query
        LOGGER.debug("body to use is: %s", context.body_request)
        LOGGER.debug("url to use is: %s", context.url_trello_call)
        LOGGER.debug("method to use is: %s", method_name)
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
