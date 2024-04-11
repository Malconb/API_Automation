"""
(c) Copyright Jalasoft. 2024

test_logger.py
    test file to test configuration of logger file levels
"""
import logging
import unittest

from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)


class TestLogger(unittest.TestCase):
    """
    Class to test get logger method
    """

    def test_logging(self):
        """
        Method to show log levels
        """
        LOGGER.debug("log DEBUG level")
        LOGGER.info("log INFO level")
        LOGGER.warning("log WARNING level")
        LOGGER.error("log ERROR level")
        LOGGER.critical("log CRITICAL level")
        # End-of-file (EOF)
