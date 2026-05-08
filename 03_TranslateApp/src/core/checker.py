"""Consistency checker logic."""

import re
from typing import Dict, List, Any


class ConsistencyChecker:
    """Validator to ensure terms are used consistently between source and translation."""

    def check(self, jp_text: str, vn_text: str, glossary: Dict[str, str]) -> List[Dict[str, Any]]:
        """Compare term counts between Japanese source and Vietnamese translation.
        
        Rules:
        - JP: Case-sensitive and width-sensitive (full-width != half-width).
        - VN: Case-insensitive.
        
        Returns:
            List of mismatches, each containing jp_term, vn_term, jp_count, and vn_count.
        """
        if not jp_text or not glossary:
            return []

        # Safe handle for VN text
        vn_text = vn_text or ""
        vn_text_lower = vn_text.lower()
        
        mismatches = []

        for jp_term, vn_term in glossary.items():
            # Count JP occurrences (exact match)
            # We use re.escape to handle any special characters in the term
            jp_count = len(re.findall(re.escape(jp_term), jp_text))
            
            if jp_count == 0:
                continue

            # Count VN occurrences (case-insensitive)
            vn_count = len(re.findall(re.escape(vn_term.lower()), vn_text_lower))

            if jp_count != vn_count:
                mismatches.append({
                    "jp_term": jp_term,
                    "vn_term": vn_term,
                    "jp_count": jp_count,
                    "vn_count": vn_count
                })

        return mismatches
