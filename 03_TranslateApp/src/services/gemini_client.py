"""Google Gemini API client using the modern google-genai SDK."""

import json
import logging
import re
from typing import Dict, List, Optional, Tuple

from google import genai
from google.genai import types

from src.services.base_client import BaseAIClient

logger = logging.getLogger(__name__)


class GeminiClient(BaseAIClient):
    """Client for interacting with Google Gemini API via the new SDK."""

    def __init__(self, api_key: str, model_name: str = "gemini-1.5-pro"):
        """Initialize the Gemini client."""
        self.api_key = api_key
        self.model_name = model_name
        self.client = genai.Client(api_key=self.api_key)

    def translate(self, text: str, glossary: Optional[Dict[str, str]] = None) -> Tuple[str, int]:
        """Translate Japanese text to Vietnamese with strict marker preservation."""
        prompt = (
            "Bạn là một dịch giả chuyên nghiệp Nhật-Việt.\n"
            "QUY TẮC QUAN TRỌNG:\n"
            "1. GIỮ NGUYÊN các dấu ngoặc 【】 và nội dung bên trong nếu chúng xuất hiện.\n"
            "2. Sử dụng ngữ pháp tiếng Việt tự nhiên.\n"
        )
        if glossary:
            prompt += "\nHãy sử dụng các thuật ngữ sau đây một cách nhất quán:\n"
            for jp, vn in glossary.items():
                prompt += f"- {jp}: {vn}\n"
        
        prompt += f"\nDịch văn bản sau sang tiếng Việt:\n\n{text}"
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            translated_text = response.text.strip()
            
            # Extract token usage from the new response format
            tokens = 0
            if response.usage_metadata:
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
            "Yêu cầu trả về kết quả dưới định dạng JSON thuần túy như ví dụ bên dưới.\n\n"
            "Ví dụ:\n"
            '{"terms": [{"jp": "心臓", "vn": "Tim"}, {"jp": "病院", "vn": "Bệnh viện"}]}\n\n'
            "Danh sách thuật ngữ cần dịch:\n"
            + "\n".join(f"- {t}" for t in terms)
        )

        try:
            # Use the new structured output support if possible, or simple generation
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            
            raw_text = response.text.strip()
            data = json.loads(raw_text)
            
            result = {}
            for item in data.get("terms", []):
                result[item["jp"]] = item["vn"]
            return result
            
        except Exception as e:
            logger.error(f"Gemini batch translation error: {e}")
            # Fallback to regex if JSON parsing fails but some text exists
            try:
                json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(0))
                    return {item["jp"]: item["vn"] for item in data.get("terms", [])}
            except:
                pass
            raise

    def detect_domain(self, text: str) -> str:
        """Analyze text and suggest a domain name."""
        prompt = (
            "Phân tích đoạn văn bản sau và cho biết nó thuộc lĩnh vực chuyên ngành nào "
            "(ví dụ: y tế, công nghệ thông tin, luật, kỹ thuật, kinh tế). "
            "Chỉ trả về tên lĩnh vực bằng tiếng Anh, không dấu, viết thường.\n\n"
            f"Văn bản: {text[:2000]}"
        )
        
        try:
            response = self.client.models.generate_content(
                model="gemini-1.5-flash", # Use faster model for detection
                contents=prompt
            )
            return response.text.strip().lower()
        except Exception as e:
            logger.error(f"Gemini domain detection error: {e}")
            return "common"
