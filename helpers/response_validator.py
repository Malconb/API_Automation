import json
import logging

from config.config import abs_path
from utils.logger import get_logger

LOGGER = get_logger(__name__, logging.DEBUG)
class ValidateResponse:

    def validate_response(self, actual_response=None, endpoint=None, file_name=None):
        """

        :param actual_response: REST response
        :param endpoint:        endpoint used i.e. labels
        """
        #read from json file
        expected_response = self.read_input_data_json(f"{abs_path}/trello_api/input_data/{endpoint}/{file_name}.json")

        #compare results

        #validate status_code
        self.validate_value(actual_response["status_code"], expected_response["status_code"], key_compare="status_code")
        #validate headers
        self.validate_value(actual_response["headers"], expected_response["headers"], key_compare="headers")
        #validate body
        self.validate_value(actual_response["body"], expected_response["response"]["body"], key_compare="body")

    def validate_value(self, actual_value, expected_value, key_compare):
        error_message = f"Expected '{expected_value}' but received '{actual_value}'"
        LOGGER.debug("Validating: '%s'", key_compare)
        LOGGER.debug("Expected '%s': '%s'", key_compare, expected_value)
        LOGGER.debug("Actual '%s': %s", key_compare, actual_value)
        if key_compare == "body":
            if isinstance(actual_value, list):
                assert self.compare_json_keys(actual_value[0], expected_value[0]), error_message
            else:
                assert self.compare_json_keys(actual_value, expected_value), error_message
        elif key_compare == "headers":
            assert expected_value.items() <= actual_value.items()
        else:

            assert expected_value == actual_value, error_message

    @staticmethod
    def read_input_data_json(file_name):
        LOGGER.debug("Reading from file: %s", file_name)
        with open(file_name) as json_file:
            data = json.load(json_file)
        LOGGER.debug("Content of file: %s", data)
        json_file.close()
        return data

    @staticmethod
    def compare_json_keys(json1, json2):
        """

        :param json1:
        :param json2:
        :return:  boolean   True if json1 == json2
        """
        for key in json1.keys():
            if key in json2.keys():
                LOGGER.debug("Key '%s' found in json2", key)
            else:
                LOGGER.debug("Key '%s' not found in json2", key)
                return False
        return True

if __name__ == '__main__':
    val = ValidateResponse()
    val.validate_response()
