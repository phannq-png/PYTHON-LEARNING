import json
import os
import shutil
import unittest
from pathlib import Path
from datetime import datetime

from src.data.glossary_repo import GlossaryRepository


class TestGlossaryRepository(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_data_dir = "test_data"
        self.domain = "test_domain"
        self.repo = GlossaryRepository(domain=self.domain, data_dir=self.test_data_dir)

    def tearDown(self):
        # Clean up the test directory after each test
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_init_creates_file_and_metadata(self):
        self.assertTrue(self.repo.file_path.exists())
        
        data = self.repo.load_glossary()
        self.assertEqual(data["domain"], self.domain)
        self.assertIn("created_at", data)
        self.assertIn("updated_at", data)
        self.assertEqual(data["terms"], {})

    def test_add_term_updates_metadata(self):
        # Capture initial updated_at
        initial_data = self.repo.load_glossary()
        initial_time = initial_data["updated_at"]
        
        # Add term
        self.repo.add_term("用語", "thuật ngữ")
        
        # Verify term was added
        terms = self.repo.get_terms()
        self.assertIn("用語", terms)
        self.assertEqual(terms["用語"], "thuật ngữ")
        
        # Verify updated_at changed
        new_data = self.repo.load_glossary()
        self.assertNotEqual(initial_time, new_data["updated_at"])

    def test_delete_term_updates_metadata(self):
        self.repo.add_term("テスト", "kiểm tra")
        
        # Capture updated_at before delete
        data_before = self.repo.load_glossary()
        time_before = data_before["updated_at"]
        
        # Delete term
        deleted = self.repo.delete_term("テスト")
        self.assertTrue(deleted)
        
        # Verify term was deleted
        terms = self.repo.get_terms()
        self.assertNotIn("テスト", terms)
        
        # Verify updated_at changed
        data_after = self.repo.load_glossary()
        self.assertNotEqual(time_before, data_after["updated_at"])

    def test_delete_nonexistent_term(self):
        deleted = self.repo.delete_term("không_tồn_tại")
        self.assertFalse(deleted)


if __name__ == '__main__':
    unittest.main()
