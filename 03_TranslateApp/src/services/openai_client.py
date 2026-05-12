"""OpenAI API client implementation."""

import json
import logging
from typing import Dict, List, Optional, Tuple

from openai import OpenAI
from src.services.base_client import BaseAIClient

from src.utils.logger import setup_logger, get_logger

logger = get_logger(__name__)
api_logger = get_logger("api")


class OpenAIClient(BaseAIClient):
    """Client for interacting with OpenAI API (GPT-4o, etc.)."""

    def __init__(self, api_key: str, model_name: str = "gpt-4o"):
        """Initialize the OpenAI client."""
        self.api_key = api_key
        self.model_name = model_name
        self.client = OpenAI(api_key=self.api_key)

    def translate(self, text: str, glossary: Optional[Dict[str, str]] = None, domain: Optional[str] = None) -> Tuple[str, int]:
        """Translate Japanese text to Vietnamese with strict rules and glossary adherence."""
        domain_str = domain if domain else "Chung"
        
        system_prompt = "Bạn là một dịch giả chuyên nghiệp. Chỉ trả về bản dịch tiếng Việt."
        
        user_prompt = (
            "Bạn là một dịch giả chuyên nghiệp. Hãy dịch danh sách các đoạn văn Markdown sau từ tiếng Nhật SANG TIẾNG VIỆT.\n"
            f"Văn bản thuộc lĩnh vực: {domain_str}.\n\n"
            "QUY TẮC BẮT BUỘC (STRICT RULES):\n"
            "1. NGÔN NGỮ ĐẦU RA: BẮT BUỘC trả về kết quả bằng TIẾNG VIỆT. Tuyệt đối không trả về tiếng Anh hay ngôn ngữ khác.\n"
            "2. TUÂN THỦ THUẬT NGỮ: Bạn PHẢI sử dụng đúng các cặp thuật ngữ dưới đây:\n"
        )
        
        relevant_glossary = {jp: vn for jp, vn in glossary.items() if jp in text} if glossary else {}
        
        if relevant_glossary:
            for jp, vn in relevant_glossary.items():
                user_prompt += f"- {jp} -> {vn}\n"
        else:
            user_prompt += "(Không có thuật ngữ cụ thể)\n"

        user_prompt += (
            "\n3. GIỮ NGUYÊN ĐỊNH DẠNG: Tuyệt đối giữ nguyên Markdown (**, *, _, #) và các ký hiệu đặc biệt như 【 】, 「 」, 『 』. KHÔNG ĐƯỢC thay thế 【 】 bằng [ ].\n"
            "4. GIỮ CẤU TRÚC DÒNG: Nếu trong một đoạn văn có xuống dòng, hãy giữ nguyên vị trí xuống dòng đó.\n"
            "5. KHÔNG GIẢI THÍCH: Chỉ trả về bản dịch tiếng Việt.\n"
            "6. TƯƠNG ĐỒNG SỐ CÂU: Số lượng câu trong bản dịch tiếng Việt phải BẰNG CHÍNH XÁC số lượng câu trong văn bản tiếng Nhật gốc. Tuyệt đối không tự ý gộp hoặc tách câu.\n\n"
            "Văn bản gốc:\n"
            f"[1] {text}"
        )
        
        try:
            api_logger.info(f"--- OPENAI REQUEST (translate) ---\nDOMAIN: {domain_str}\nSYSTEM:\n{system_prompt}\nUSER:\n{user_prompt}\n--- END REQUEST ---")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3
            )
            res_text = response.choices[0].message.content.strip()
            api_logger.info(f"--- OPENAI RESPONSE (translate) ---\nRESULT:\n{res_text}\n--- END RESPONSE ---")
            translated_text = response.choices[0].message.content.strip()
            # Remove the index prefix [1] if the model mistakenly includes it in the output
            import re
            translated_text = re.sub(r'^\[1\]\s*', '', translated_text)
            tokens = response.usage.total_tokens
            
            return translated_text, tokens
        except Exception as e:
            logger.error(f"OpenAI translation error: {e}")
            raise

    def translate_batch(self, terms: List[str], domain: Optional[str] = None, additional_reqs: Optional[str] = None) -> Dict[str, str]:
        """Translate a list of terms using structured JSON output and custom rules."""
        if not terms:
            return {}

        domain_str = domain if domain else "Chung"
        reqs_str = additional_reqs if additional_reqs and additional_reqs.strip() else "(Không có yêu cầu cụ thể)"
        terms_list = "\n".join(f"- {t}" for t in terms)
        
        prompt = (
            f"Bạn là chuyên gia dịch thuật ngữ kỹ thuật Nhật-Việt lĩnh vực {domain_str}.\n\n"
            "NHIỆM VỤ: Dịch danh sách thuật ngữ tiếng Nhật sang tiếng Việt.\n\n"
            "QUY TẮC BẮT BUỘC (STRICT RULES):\n\n"
            "1. NGÔN NGỮ ĐẦU RA:\n"
            "   - BẮT BUỘC trả về kết quả bằng TIẾNG VIỆT\n"
            "   - TUYỆT ĐỐI KHÔNG dùng tiếng Anh hay ngôn ngữ khác\n\n"
            "2. QUY TẮC DỊCH THUẬT NGỮ (theo thứ tự ưu tiên từ cao xuống thấp):\n\n"
            f"{reqs_str}\n\n"
            "3. ĐỊNH DẠNG ĐẦU RA:\n"
            "   - BẮT BUỘC trả về JSON thuần túy (không có markdown, không có ```json)\n"
            "   - Cấu trúc chính xác như ví dụ bên dưới\n"
            "   - Không thêm bất kỳ văn bản giải thích nào ngoài JSON\n\n"
            "VÍ DỤ ĐỊNH DẠNG:\n"
            "{\n"
            '  "terms": [\n'
            '    {"jp": "心臓", "vn": "Tim"},\n'
            '    {"jp": "病院", "vn": "Bệnh viện"},\n'
            '    {"jp": "鋼部材", "vn": "linh kiện thép"},\n'
            '    {"jp": "接合部分", "vn": "phần tiếp giáp"},\n'
            '    {"jp": "構造部", "vn": "bộ phận kết cấu"}\n'
            "  ]\n"
            "}\n\n"
            "DANH SÁCH THUẬT NGỮ CẦN DỊCH:\n"
            f"{terms_list}\n\n"
            "CHỈ trả về JSON, không thêm bất kỳ nội dung nào khác."
        )

        try:
            api_logger.info(f"--- OPENAI REQUEST (translate_batch) ---\nDOMAIN: {domain_str}\nPROMPT:\n{prompt}\n--- END REQUEST ---")
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            res_text = response.choices[0].message.content.strip()
            api_logger.info(f"--- OPENAI RESPONSE (translate_batch) ---\nRESULT:\n{res_text}\n--- END RESPONSE ---")
            
            data = json.loads(response.choices[0].message.content)
            result = {item["jp"]: item["vn"] for item in data.get("terms", [])}
            return result
        except Exception as e:
            logger.error(f"OpenAI batch translation error: {e}")
            raise

    def detect_domain(self, text: str, existing_domains: Optional[List[str]] = None) -> str:
        """Analyze text and suggest a domain name in Vietnamese."""
        domains_str = ""
        if existing_domains:
            # Filter out 'common' and format list
            valid_domains = [d for d in existing_domains if d.lower() != "common"]
            if valid_domains:
                domains_str = f"\nCÁC LĨNH VỰC ĐÃ CÓ: {', '.join(valid_domains)}\n"

        prompt = (
            "Phân tích đoạn văn bản sau và cho biết nó thuộc lĩnh vực chuyên ngành nào."
            f"{domains_str}"
            "YÊU CẦU:\n"
            "1. Nếu nội dung phù hợp với một trong các LĨNH VỰC ĐÃ CÓ ở trên, hãy trả về chính xác tên đó.\n"
            "2. Nếu không phù hợp, hãy đề xuất một lĩnh vực mới bằng tiếng Việt (1-3 từ, ví dụ: Y tế, Kỹ thuật).\n"
            "3. Chỉ trả về tên lĩnh vực, không thêm giải thích.\n\n"
            f"VĂN BẢN: {text[:2000]}"
        )
        
        try:
            api_logger.info(f"--- OPENAI REQUEST (detect_domain) ---\nPROMPT:\n{prompt}\n--- END REQUEST ---")
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )
            res_text = response.choices[0].message.content.strip()
            api_logger.info(f"--- OPENAI RESPONSE (detect_domain) ---\nRESULT:\n{res_text}\n--- END RESPONSE ---")
            return res_text
        except Exception as e:
            logger.error(f"OpenAI domain detection error: {e}")
            return "common"

    def test_connection(self) -> bool:
        """Verify if OpenAI API key is valid by listing models."""
        try:
            self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI connection test failed: {e}")
            return False
