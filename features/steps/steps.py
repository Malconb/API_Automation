import logging

from utils.logger import get_logger
from behave import given, then, when

LOGGER = get_logger(__name__, logging.DEBUG)


@when(u'I call to "{endpoint}" endpoint using "{method_name}" option and with parameters')
def step_impl(context, endpoint, method_name):
    """
    Steps to call get endpoint
    :param context:
    :param endpoint:
    :param method_name:
    """
    LOGGER.debug(f"STEP: When I call to '{endpoint}' endpoint using '{method_name}' option and with parameters")
    context.url_trello_board = f"{context.url_trello}/organizations/{context.org_id}/boards?{context.credentials}"
    context.response = context.rest_client.request("get", context.url_trello_board)
    context.endpoint = endpoint
    context.method_name = method_name




@when(u'I call to "{endpoint}" endpoint using "{method_name}" option and with parameters test')
def step_impl(context, endpoint, method_name):
    LOGGER.debug(f"STEP: When I call to '{endpoint}' endpoint using '{method_name}' option and with parameters")
    context.response = context.rest_client.request("post", f"{context.url_trello}/boards", body=context.body_project)
    if response["status_code"] == 200:
        self.board_list.append(response["body"]["id"])
    self.validate.validate_response(response, "boards", "create_board")


@then(u'I receive the response to validate')
def step_impl(context):
    LOGGER.debug(u'STEP: Then I receive the response to validate')
    context.validate.validate_response(context.response, "boards", "get_all_boards")


@then(u'I validated the status code is {status_code:d}')
def step_impl(context, status_code):
    LOGGER.debug(f"STEP: Then I validated the status code is {status_code}")
    assert context.response["status_code"] == status_code, \
        f"Expected {status_code} but got {context.response["status_code"]}"
