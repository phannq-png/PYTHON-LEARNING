import logging
import threading
from typing import Callable, Dict, Optional
import google.generativeai as genai
from openai import OpenAI

logger = logging.getLogger(__name__)

class TranslationEngine:
    """Core engine for handling translations via OpenAI and Google Gemini APIs.
    
    This class handles prompt construction, API interaction, and error management.
    API calls are performed in separate threads to avoid blocking the main UI.
    """

    def __init__(self, api_key: str, provider: str, model_name: str) -> None:
        """Initialize the translation engine.
        
        Args:
            api_key: The API key for the chosen provider.
            provider: 'gemini' or 'openai'.
            model_name: The specific model ID to use (e.g., 'gpt-4', 'gemini-1.5-flash').
        """
        self.api_key = api_key
        self.provider = provider.lower()
        self.model_name = model_name
        
        # Initialize clients lazily or directly
        self._setup_client()

    def _setup_client(self) -> None:
        """Configure the API client based on the provider."""
        try:
            if self.provider == "gemini":
                genai.configure(api_key=self.api_key)
                self.client = genai.GenerativeModel(self.model_name)
            elif self.provider == "openai":
                self.client = OpenAI(api_key=self.api_key)
            else:
                logger.error(f"Unsupported provider: {self.provider}")
        except Exception as e:
            logger.exception(f"Failed to setup {self.provider} client: {e}")

    def _build_prompt(self, text: str, glossary: Optional[Dict[str, str]] = None) -> str:
        """Construct the prompt for the AI model according to TL's guidelines."""
        prompt_parts = []
        prompt_parts.append("Hãy dịch đoạn văn sau từ tiếng Nhật sang tiếng Việt, giữ nguyên định dạng.")
        prompt_parts.append("Yêu cầu ngữ pháp tiếng Việt tự nhiên và chính xác về mặt kỹ thuật.")
        
        if glossary:
            prompt_parts.append("Bắt buộc sử dụng các thuật ngữ chuyên ngành sau (nếu xuất hiện trong văn bản):")
            prompt_parts.append("---GLOSSARY---")
            for jp, vn in glossary.items():
                prompt_parts.append(f"{jp} → {vn}")
            prompt_parts.append("---END GLOSSARY---")
        
        prompt_parts.append("\nVĂN BẢN CẦN DỊCH:")
        prompt_parts.append(text)
        
        return "\n".join(prompt_parts)

    def translate(
        self, 
        text: str, 
        glossary: Optional[Dict[str, str]] = None,
        on_success: Optional[Callable[[str], None]] = None,
        on_error: Optional[Callable[[str], None]] = None
    ) -> None:
        """Execute translation in a separate thread.
        
        Args:
            text: The source Japanese text.
            glossary: Optional mapping of JP terms to VN terms.
            on_success: Callback function called with the translated string.
            on_error: Callback function called with an error message string.
        """
        thread = threading.Thread(
            target=self._run_translation,
            args=(text, glossary, on_success, on_error),
            daemon=True
        )
        thread.start()

    def _run_translation(
        self, 
        text: str, 
        glossary: Optional[Dict[str, str]],
        on_success: Optional[Callable[[str], None]],
        on_error: Optional[Callable[[str], None]]
    ) -> None:
        """Internal method to be executed in a background thread."""
        try:
            prompt = self._build_prompt(text, glossary)
            result = ""

            if self.provider == "gemini":
                response = self.client.generate_content(prompt)
                if response.text:
                    result = response.text.strip()
                else:
                    raise ValueError("Gemini trả về kết quả rỗng.")

            elif self.provider == "openai":
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3
                )
                result = response.choices[0].message.content.strip()

            if result and on_success:
                on_success(result)
            elif not result and on_error:
                on_error("Không nhận được kết quả dịch từ AI.")

        except Exception as e:
            error_msg = f"Lỗi API ({self.provider}): {str(e)}"
            logger.error(error_msg)
            if on_error:
                on_error(error_msg)
