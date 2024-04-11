import logging

import pytest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


@pytest.fixture()
def fixture_example(request):
    LOGGER.debug("Fixture example run")
    url = "http://vault-api.com"

    environment = request.config.getoption("--env")
    LOGGER.debug("Environment to execute suite: %s", environment)

    return url


def pytest_addoption(parser):
    parser.addoption(
        '--env', action='store', default='dev', help="Environment where test will be executed"
    )
    parser.addoption(
        '--browser', action='store', default='firefox', help="Browser to be executed the UI tests"
    )