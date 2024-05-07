import logging

from entities.board import Board
from utils.logger import get_logger
from behave import given, then, when

LOGGER = get_logger(__name__, logging.DEBUG)


#### Steps for basic scenarios: ######

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
    query = context.body_main
    if method_name == "get":
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}?{context.credentials}"
        LOGGER.debug("method_name is: %s", method_name)
        context.response = context.rest_client.request(method_name, context.url_trello_call)
        
    elif method_name == "put":
        query["name"] = f"Testing {method_name} for {context.endpoint} endpoint"
        query[f"id{context.endpoint}"] = context.valid_id
        context.body_request = query
        context.url_trello_call = f"{context.url_trello}/{endpoints}/{context.valid_id}"
        context.response = context.rest_client.request(method_name, context.url_trello_call, body=context.body_request)

    elif method_name == "post":
        if context.text:
            LOGGER.debug("doc string received: %s", context.text)
            query["name"] = context.text
        else:
            query["name"] = f"Testing {method_name} for {context.endpoint} endpoint"
        query[f"id{context.endpoint}"] = context.valid_id
        context.body_request = query
        LOGGER.debug("body formated: %s", context.body_request)
        context.url_trello_call = f"{context.url_trello}/{endpoints}"
        context.response = context.rest_client.request(method_name, context.url_trello_call, body=context.body_request)
        if endpoints == "boards":
            context.new_board_id = context.response["body"]["id"]
            context.board_list.append(context.new_board_id)
        context.resource_list.append(context.response["body"]["id"])
    
    elif method_name == "delete":
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


#### Steps for functional scenarios: ###### 

@given(u'current quantity of created boards')
def step_impl(context):
    context.url_trello_board = f"{context.url_trello}/organizations/{context.valid_id}/boards?{context.credentials}"
    context.response = context.rest_client.request("get", context.url_trello_board)
    context.num_of_boards = len(context.response["body"])
    LOGGER.debug("There is current boards: %s", context.num_of_boards)


@when(u'I created boards until limit provided for free accounts: {qtt:d}')
def step_impl(context, qtt):
    for index in range(context.num_of_boards, qtt):
            context.body_project = context.body_main
            context.body_project["name"] = "Board created for Max num of Boards test"
            new_board = context.board.create_board(body=context.body_project)
            context.new_board_id = new_board["body"]["id"]
            context.board_list.append(new_board["body"]["id"])
            LOGGER.debug("Board num: %s", index)

    LOGGER.debug("I created boards until limit provided for free accounts: 10")


@then(u'I try to create an extra board')
def step_impl(context):
        LOGGER.debug("I try to create an extra board")
        context.body_project["name"] = "Board created for Exceeded Max num of Boards test"
        new_board = context.board.create_board(body=context.body_project)
        context.response = new_board
    

@given(u'compile all available "{endpoints}" on a board')
def step_impl(context, endpoints):
    context.url_trello_board = f"{context.url_trello}/boards/{context.new_board_id}/{endpoints}?{context.credentials}"
    context.response = context.rest_client.request("get", context.url_trello_board)
    context.num_of_objects = len(context.response["body"])
    LOGGER.debug(f"Current quantity of {endpoints}: %s", context.num_of_objects)
    context.list_of_objects = context.response["body"]
    LOGGER.debug(f"list of {endpoints}: %s", context.num_of_objects)
    context.endpoints = endpoints


@when(u'I move card between all avaiable "{endpoints}"')
def step_impl(context, endpoints):
    LOGGER.debug(u'STEP: When I move card between all avaiable lists')
    for index in range(0, context.num_of_objects):
            context.body_moved_card = context.body_main
            context.body_moved_card["idList"] = context.list_of_objects[index]["id"]
            LOGGER.debug("Moving card to list_id: %s", context.body_moved_card["idList"])
            context.url_trello_move = f"{context.url_trello}/{context.endpoints}/{context.valid_id}"
            context.response = context.rest_client.request("put", context.url_trello_move, body=context.body_moved_card)
            context.endpoints = "cards"

@then(u'I update "{endpoints}" between all previous resources created')
def step_impl(context, endpoints):
    context.num_of_sources = len(context.resource_list)
    LOGGER.debug("cantidad de res: %s", context.num_of_sources)
    LOGGER.debug(u'STEP: When I move card between all avaiable lists')
    for index in range(0, context.num_of_sources):
            body_object = context.body_main
            body_object["value"] = context.resource_list[index]
            context.body_card = body_object
            context.url_trello_move = f"{context.url_trello}/{endpoints}/{context.valid_id}/idLabels"
            context.response = context.rest_client.request("put", context.url_trello_move, body=context.body_card)
            context.endpoints = "cards"

