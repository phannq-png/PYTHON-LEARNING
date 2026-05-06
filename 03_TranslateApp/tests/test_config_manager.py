import json
import os
import shutil
import unittest
from pathlib import Path

from cryptography.fernet import Fernet

from src.data.config_manager import ConfigManager


class TestConfigManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_data_dir = "test_data"
        self.config_dir = Path(self.test_data_dir) / "config"
        self.manager = ConfigManager(data_dir=self.test_data_dir)

    def tearDown(self):
        # Clean up the test directory after each test
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)

    def test_ensure_config_dir_and_key_creation(self):
        self.assertTrue(self.config_dir.exists())
        self.assertTrue((self.config_dir / ".secret.key").exists())

    def test_app_config_save_load(self):
        test_data = {"max_chars": 1000, "use_enter": True}
        
        # Save
        self.manager.save_app_config(test_data)
        self.assertTrue(self.manager.app_config_path.exists())
        
        # Verify plaintext
        with open(self.manager.app_config_path, "r", encoding="utf-8") as f:
            saved_content = json.load(f)
        self.assertEqual(saved_content, test_data)
        
        # Load
        loaded_data = self.manager.load_app_config()
        self.assertEqual(loaded_data, test_data)

    def test_api_config_save_load_encryption(self):
        test_data = {"openai_key": "sk-123456789", "model": "gpt-4"}
        
        # Save
        self.manager.save_api_config(test_data)
        self.assertTrue(self.manager.api_config_path.exists())
        
        # Verify it is encrypted (not equal to plaintext)
        with open(self.manager.api_config_path, "r", encoding="utf-8") as f:
            saved_content = json.load(f)
        self.assertNotEqual(saved_content["openai_key"], "sk-123456789")
        self.assertNotEqual(saved_content["model"], "gpt-4")
        
        # Load (should decrypt correctly)
        loaded_data = self.manager.load_api_config()
        self.assertEqual(loaded_data, test_data)

    def test_api_config_invalid_token(self):
        # Save data
        test_data = {"api_key": "secret"}
        self.manager.save_api_config(test_data)
        
        # Simulate secret key change
        new_key = Fernet.generate_key()
        with open(self.manager.secret_key_path, "wb") as f:
            f.write(new_key)
            
        # Re-initialize manager with new key
        new_manager = ConfigManager(data_dir=self.test_data_dir)
        
        # Attempt to load, should catch InvalidToken and backup
        loaded_data = new_manager.load_api_config()
        self.assertEqual(loaded_data, {})
        
        # Verify backup was created
        backup_path = self.manager.api_config_path.with_suffix(".json.bak")
        self.assertTrue(backup_path.exists())


if __name__ == '__main__':
    unittest.main()
