"""Google Gemini API client."""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple

import google.generativeai as genai

from src.services.base_client import BaseAIClient

logger = logging.getLogger(__name__)


class GeminiClient(BaseAIClient):
    """Client for interacting with Google Gemini API."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        """Initialize the Gemini client."""
        self.api_key = api_key
        self.model_name = model_name
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)

    def translate(self, text: str, glossary: Optional[Dict[str, str]] = None) -> Tuple[str, int]:
        """Translate Japanese text to Vietnamese with glossary enforcement."""
        prompt = "Bạn là một dịch giả chuyên nghiệp Nhật-Việt.\n"
        if glossary:
            prompt += "Hãy sử dụng các thuật ngữ sau đây một cách nhất quán:\n"
            for jp, vn in glossary.items():
                prompt += f"- {jp}: {vn}\n"
        
        prompt += f"\nDịch văn bản sau sang tiếng Việt, giữ nguyên ngữ pháp tự nhiên:\n\n{text}"
        
        try:
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            # Extract token usage
            tokens = 0
            if hasattr(response, 'usage_metadata'):
                tokens = response.usage_metadata.total_token_count
                
            return translated_text, tokens
        except Exception as e:
            logger.error(f"Gemini translation error: {e}")
            raise

    def translate_batch(self, terms: List[str]) -> Dict[str, str]:
        """Translate a list of terms using structured JSON output."""
        if not terms:
            return {}

        prompt = (
            "Bạn là một chuyên gia thuật ngữ Nhật-Việt. "
            "Dịch danh sách các thuật ngữ sau đây sang tiếng Việt. "
            "Yêu cầu trả về kết quả dưới định dạng JSON thuần túy như ví dụ bên dưới, "
            "không có bất kỳ văn bản giải thích nào khác.\n\n"
            "Ví dụ:\n"
            '{"terms": [{"jp": "心臓", "vn": "Tim"}, {"jp": "病院", "vn": "Bệnh viện"}]}\n\n'
            "Danh sách thuật ngữ cần dịch:\n"
            + "\n".join(f"- {t}" for t in terms)
        )

        try:
            # Using JSON mode or similar if supported, otherwise rely on prompt
            response = self.model.generate_content(prompt)
            raw_text = response.text.strip()
            
            # Extract JSON from potential Markdown blocks
            json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                result = {}
                for item in data.get("terms", []):
                    result[item["jp"]] = item["vn"]
                return result
            
            return {}
        except Exception as e:
            logger.error(f"Gemini batch translation error: {e}")
            raise

    def detect_domain(self, text: str) -> str:
        """Analyze text and suggest a domain name (e.g., medical, it, legal)."""
        prompt = (
            "Phân tích đoạn văn bản sau và cho biết nó thuộc lĩnh vực chuyên ngành nào "
            "(ví dụ: y tế, công nghệ thông tin, luật, kỹ thuật, kinh tế). "
            "Chỉ trả về tên lĩnh vực bằng tiếng Anh, không dấu, viết thường.\n\n"
            f"Văn bản: {text[:2000]}"
        )
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip().lower()
        except Exception as e:
            logger.error(f"Gemini domain detection error: {e}")
            return "common"
