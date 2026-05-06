import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


class GlossaryRepository:
    """Manages the storage and retrieval of glossary terms for a specific domain.
    
    Data is stored in JSON format with metadata (created_at, updated_at).
    """

    def __init__(self, domain: str, data_dir: str = "data") -> None:
        """Initialize the repository for a specific domain."""
        self.domain = domain
        self.glossaries_dir = Path(data_dir) / "glossaries"
        self.file_path = self.glossaries_dir / f"{domain}.json"

        self._ensure_dir()
        if not self.file_path.exists():
            self._init_empty_glossary()

    def _ensure_dir(self) -> None:
        """Ensure the glossaries directory exists."""
        os.makedirs(self.glossaries_dir, exist_ok=True)

    def _init_empty_glossary(self) -> None:
        """Initialize an empty glossary JSON file with required metadata."""
        now = datetime.now().isoformat()
        initial_data = {
            "domain": self.domain,
            "created_at": now,
            "updated_at": now,
            "terms": {}
        }
        self.save_glossary(initial_data)

    def load_glossary(self) -> Dict[str, Any]:
        """Load the entire glossary object including metadata."""
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode glossary for domain '{self.domain}': {e}")
            return {"domain": self.domain, "terms": {}}
        except Exception as e:
            logger.error(f"Error loading glossary for domain '{self.domain}': {e}")
            return {"domain": self.domain, "terms": {}}

    def get_terms(self) -> Dict[str, str]:
        """Retrieve only the dictionary of terms (jp -> vn mapping)."""
        data = self.load_glossary()
        return data.get("terms", {})

    def save_glossary(self, data: Dict[str, Any]) -> None:
        """Save the entire glossary object to file."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving glossary for domain '{self.domain}': {e}")
            raise

    def add_term(self, jp_term: str, vn_term: str) -> None:
        """Add or update a single term in the glossary."""
        data = self.load_glossary()
        
        if "terms" not in data:
            data["terms"] = {}
            
        data["terms"][jp_term] = vn_term
        data["updated_at"] = datetime.now().isoformat()
        
        self.save_glossary(data)

    def delete_term(self, jp_term: str) -> bool:
        """Delete a term from the glossary. Returns True if deleted, False if not found."""
        data = self.load_glossary()
        
        if "terms" not in data or jp_term not in data["terms"]:
            return False
            
        del data["terms"][jp_term]
        data["updated_at"] = datetime.now().isoformat()
        
        self.save_glossary(data)
        return True
