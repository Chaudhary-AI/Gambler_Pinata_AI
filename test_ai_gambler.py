# 🧪 Test Suite for AI Gambler Customized
# File: test_ai_gambler.py

import unittest
from unittest.mock import patch, mock_open
from pathlib import Path
import json
import logging
import os
from ai_gambler_customized import load_custom_config, get_param

# Logging setup
LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)  # Ensure logs/ folder exists
LOG_FILE = os.path.join(LOG_FOLDER, "test_results.log")
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

class TestAIGamblerCustomized(unittest.TestCase):

    def setUp(self):
        logging.info(f"Starting test: {self._testMethodName}")

    def tearDown(self):
        logging.info(f"Finished test: {self._testMethodName}")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", new_callable=mock_open, read_data='{"key1": "value1", "key2": "value2"}')
    def test_load_custom_config_valid_file(self, mock_file):
        # Test when the config file exists and contains valid JSON
        config = load_custom_config()
        self.assertEqual(config, {"key1": "value1", "key2": "value2"})
        mock_file.assert_called_once_with(Path("mock_ruleset.json"), "r")
        logging.info("Test PASSED: test_load_custom_config_valid_file")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", side_effect=FileNotFoundError)
    def test_load_custom_config_file_not_found(self, mock_file):
        # Test when the config file does not exist
        config = load_custom_config()
        self.assertEqual(config, {})
        mock_file.assert_called_once_with(Path("mock_ruleset.json"), "r")
        logging.info("Test PASSED: test_load_custom_config_file_not_found")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", new_callable=mock_open, read_data='invalid json')
    def test_load_custom_config_invalid_json(self, mock_file):
        # Test when the config file contains invalid JSON
        with patch("ai_gambler_customized.json.load", side_effect=json.JSONDecodeError("Invalid JSON", "", 0)):
            config = load_custom_config()
            self.assertEqual(config, {})
        mock_file.assert_called_once_with(Path("mock_ruleset.json"), "r")
        logging.info("Test PASSED: test_load_custom_config_invalid_json")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", new_callable=mock_open, read_data='{"key1": "value1", "key2": "value2"}')
    def test_get_param_existing_key(self, mock_file):
        # Test get_param with an existing key
        value = get_param("key1")
        self.assertEqual(value, "value1")
        logging.info("Test PASSED: test_get_param_existing_key")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", new_callable=mock_open, read_data='{"key1": "value1", "key2": "value2"}')
    def test_get_param_non_existing_key(self, mock_file):
        # Test get_param with a non-existing key
        value = get_param("key3", default="default_value")
        self.assertEqual(value, "default_value")
        logging.info("Test PASSED: test_get_param_non_existing_key")

    @patch("ai_gambler_customized.CONFIG_FILE", Path("mock_ruleset.json"))
    @patch("ai_gambler_customized.open", new_callable=mock_open, read_data='{}')
    def test_load_custom_config_empty_file(self, mock_file):
        # Test when the config file is empty
        config = load_custom_config()
        self.assertEqual(config, {})
        logging.info("Test PASSED: test_load_custom_config_empty_file")

if __name__ == "__main__":
    unittest.main()