import logging
import unittest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestUnitTestExample(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Setup class
        """
        LOGGER.warning("Setup class")

    def setUp(self):
        """
        Setup method
        """
        LOGGER.warning("Setup method")

    def tearDown(self):
        """
        teardown method
        """
        LOGGER.warning("teardown method")

    def test_one(self):
        """
        Test one
        """
        LOGGER.debug("Test One")

    def test_two(self):
        """
        Test one
        """
        LOGGER.debug("Test two")

    def test_three(self):
        """
        Test one
        """
        LOGGER.debug("Test three")

    @classmethod
    def tearDownClass(cls):
        """
        teardown class
        """
        LOGGER.warning("Teardown class")