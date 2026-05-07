import unittest
from src.ui.app_window import AppWindow
import os

class TestIntegrationFlow(unittest.TestCase):
    def setUp(self):
        # We need to mock the UI parts that depend on the mainloop or screen
        # but we can test the data flow in AppWindow methods
        pass

    def test_logic_initialization(self):
        app = AppWindow()
        self.assertIsNotNone(app.doc_processor)
        self.assertIsNotNone(app.segmenter)
        self.assertIsNotNone(app.session_manager)
        app.destroy()

    def test_file_processing_logic(self):
        app = AppWindow()
        file_path = os.path.abspath("test_input.docx")
        
        # Manually trigger the flow steps with low char limit to force 2 pages
        app.segmenter.max_chars_per_page = 50
        
        texts, _ = app.doc_processor.extract_docx(file_path)
        segments = app.segmenter.segment(texts)
        pages_segments = app.segmenter.paginate(segments)
        pages_text = ["\n".join(p) for p in pages_segments]
        
        # Verify pagination worked
        self.assertGreaterEqual(len(pages_text), 2)
        self.assertIn("Introduction", pages_text[0])

if __name__ == '__main__':
    unittest.main()
