import logging
import sys

import pytest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


def setup_method():
    """
    Pytest setup method
    """
    LOGGER.debug("setup_method")


@pytest.mark.projects
class TestPytestExample:

    @classmethod
    def setup_class(cls):
        """
        Pytest setupClass
        """
        LOGGER.debug("Setup class")

    def teardown_class(self):
        """
        PyTest teardown method
        """
        LOGGER.debug("teardown method")

    @pytest.mark.sanity
    def test_one(self, fixture_example):
        """
        Test one
        """
        LOGGER.debug("Test One: %s", fixture_example)

    @pytest.mark.skip(reason="Bug: 1234 opened")
    @pytest.mark.skipif(sys.platform == "win32", reason="Test only runs on Linux")  # @pytest.mark.skip(condition, reason)
    @pytest.mark.acceptance
    def test_two(self):
        """
        Test one
        """
        LOGGER.debug("Test two")

    @pytest.mark.sanity
    @pytest.mark.acceptance
    @pytest.mark.parametrize("parameter_name", ["param1", "param2", "param3"])
    def test_three(self, parameter_name):
        """
        Test one
        """
        LOGGER.debug("Test three: %s", parameter_name)

    @classmethod
    def teardown_class(cls):
        """
        PyTest teardown class
        """
        LOGGER.debug("Teardown class")