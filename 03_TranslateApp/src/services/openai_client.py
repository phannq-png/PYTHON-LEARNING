"""OpenAI API client implementation."""

import json
import logging
from typing import Dict, List, Optional, Tuple

from openai import OpenAI
from src.services.base_client import BaseAIClient

logger = logging.getLogger(__name__)


class OpenAIClient(BaseAIClient):
    """Client for interacting with OpenAI API (GPT-4o, etc.)."""

    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        """Initialize the OpenAI client."""
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)

    def translate(self, text: str, glossary: Optional[Dict[str, str]] = None) -> Tuple[str, int]:
        """Translate Japanese text to Vietnamese with strict segment preservation."""
        system_prompt = (
            "Bạn là một dịch giả chuyên nghiệp Nhật-Việt.\n"
            "QUY TẮC QUAN TRỌNG:\n"
            "1. GIỮ NGUYÊN các dấu ngoặc 【】 và nội dung bên trong nếu chúng xuất hiện (đây là nhãn định dạng).\n"
            "2. Sử dụng ngữ pháp tiếng Việt tự nhiên, trang trọng."
        )
        
        user_prompt = ""
        if glossary:
            user_prompt += "Sử dụng các thuật ngữ sau đây một cách nhất quán:\n"
            for jp, vn in glossary.items():
                user_prompt += f"- {jp}: {vn}\n"
        
        user_prompt += f"\nDịch văn bản sau sang tiếng Việt:\n\n{text}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            translated_text = response.choices[0].message.content.strip()
            tokens = response.usage.total_tokens
            
            return translated_text, tokens
        except Exception as e:
            logger.error(f"OpenAI translation error: {e}")
            raise

    def translate_batch(self, terms: List[str]) -> Dict[str, str]:
        """Translate a list of terms using structured JSON output."""
        if not terms:
            return {}

        prompt = (
            "Bạn là một chuyên gia thuật ngữ Nhật-Việt. "
            "Dịch danh sách các thuật ngữ sau đây sang tiếng Việt. "
            "Trả về kết quả dưới định dạng JSON như ví dụ:\n"
            '{"terms": [{"jp": "心臓", "vn": "Tim"}]}\n\n'
            "Danh sách:\n" + "\n".join(terms)
        )

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.choices[0].message.content)
            result = {item["jp"]: item["vn"] for item in data.get("terms", [])}
            return result
        except Exception as e:
            logger.error(f"OpenAI batch translation error: {e}")
            raise

    def detect_domain(self, text: str) -> str:
        """Analyze text and suggest a domain name."""
        prompt = (
            "Phân tích đoạn văn bản sau và cho biết nó thuộc lĩnh vực nào "
            "(medical, it, legal, technical, economics). "
            "Chỉ trả về 1 từ duy nhất là tên lĩnh vực bằng tiếng Anh.\n\n"
            f"Văn bản: {text[:1000]}"
        )
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", # Faster model for detection
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip().lower()
        except Exception as e:
            logger.error(f"OpenAI domain detection error: {e}")
            return "common"
