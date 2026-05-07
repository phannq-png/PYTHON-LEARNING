import unittest
import os
import shutil
import json
from src.data.session_manager import SessionManager

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.test_data_dir = "test_sessions_data"
        self.manager = SessionManager(data_dir=self.test_data_dir)
        self.docx_path = "C:/test/document.docx"
        self.segments = ["Segment 1 text", "Segment 2 text"]

    def tearDown(self):
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir, ignore_errors=True)

    def test_create_session(self):
        session = self.manager.create_session(self.docx_path, self.segments, domain="medical")
        
        self.assertIn("document", session["id"])
        self.assertEqual(session["source_file"], self.docx_path)
        self.assertEqual(session["domain"], "medical")
        self.assertEqual(len(session["pages"]), 2)
        self.assertEqual(session["pages"][0]["jp"], "Segment 1 text")
        self.assertEqual(session["pages"][0]["vn"], "")
        self.assertEqual(session["pages"][0]["status"], "pending")

    def test_save_and_load_session(self):
        session_data = self.manager.create_session(self.docx_path, self.segments)
        session_id = session_data["id"]
        
        # Save
        file_path = self.manager.save_session(session_data)
        self.assertTrue(os.path.exists(file_path))
        
        # Load
        loaded_data = self.manager.load_session(session_id)
        self.assertEqual(loaded_data["id"], session_id)
        self.assertEqual(loaded_data["source_file"], self.docx_path)
        self.assertEqual(len(loaded_data["pages"]), 2)

    def test_save_updates_timestamp(self):
        session_data = self.manager.create_session(self.docx_path, self.segments)
        initial_updated_at = session_data["updated_at"]
        
        # Simulate some delay if needed, but here we just check if it's called
        import time
        time.sleep(0.1) 
        
        self.manager.save_session(session_data)
        self.assertNotEqual(initial_updated_at, session_data["updated_at"])

    def test_list_sessions(self):
        # Create 2 sessions
        s1 = self.manager.create_session("file1.docx", ["s1"])
        s2 = self.manager.create_session("file2.docx", ["s2"])
        
        self.manager.save_session(s1)
        self.manager.save_session(s2)
        
        sessions = self.manager.list_sessions()
        self.assertEqual(len(sessions), 2)
        # Check sorting (most recent first)
        self.assertTrue(sessions[0]["updated_at"] >= sessions[1]["updated_at"])

if __name__ == '__main__':
    unittest.main()
