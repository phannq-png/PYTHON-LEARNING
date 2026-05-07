import unittest
from unittest.mock import MagicMock, patch
from src.core.translation_engine import TranslationEngine

class TestTranslationEngine(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.glossary = {"用語": "thuật ngữ"}
        self.text = "これはテストです。"

    def test_build_prompt_with_glossary(self):
        engine = TranslationEngine(self.api_key, "openai", "gpt-4")
        prompt = engine._build_prompt(self.text, self.glossary)
        
        self.assertIn("---GLOSSARY---", prompt)
        self.assertIn("用語 → thuật ngữ", prompt)
        self.assertIn("VĂN BẢN CẦN DỊCH:", prompt)
        self.assertIn(self.text, prompt)

    @patch('src.core.translation_engine.OpenAI')
    def test_openai_translation_success(self, mock_openai):
        # Mocking the OpenAI response structure
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Đây là một bài kiểm tra."
        mock_client.chat.completions.create.return_value = mock_response

        engine = TranslationEngine(self.api_key, "openai", "gpt-4")
        
        success_called = False
        result_text = ""
        
        def on_success(text):
            nonlocal success_called, result_text
            success_called = True
            result_text = text

        # Use _run_translation directly to avoid threading in test
        engine._run_translation(self.text, self.glossary, on_success, None)
        
        self.assertTrue(success_called)
        self.assertEqual(result_text, "Đây là một bài kiểm tra.")

    @patch('src.core.translation_engine.genai')
    def test_gemini_translation_success(self, mock_genai):
        mock_model = MagicMock()
        mock_genai.GenerativeModel.return_value = mock_model
        mock_response = MagicMock()
        mock_response.text = "Đây là một bài kiểm tra."
        mock_model.generate_content.return_value = mock_response

        engine = TranslationEngine(self.api_key, "gemini", "gemini-pro")
        
        success_called = False
        def on_success(text):
            nonlocal success_called
            success_called = True

        engine._run_translation(self.text, self.glossary, on_success, None)
        self.assertTrue(success_called)

    def test_unsupported_provider_error(self):
        engine = TranslationEngine(self.api_key, "unsupported", "model")
        
        error_called = False
        def on_error(msg):
            nonlocal error_called
            error_called = True
            
        engine._run_translation(self.text, self.glossary, None, on_error)
        self.assertTrue(error_called)

if __name__ == '__main__':
    unittest.main()
