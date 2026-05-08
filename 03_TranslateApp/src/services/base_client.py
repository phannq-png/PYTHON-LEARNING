"""Base API client interface."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple


class BaseAIClient(ABC):
    """Abstract base class for all AI service providers."""

    @abstractmethod
    def translate(self, text: str, glossary: Optional[Dict[str, str]] = None) -> Tuple[str, int]:
        """Translate a single piece of text and return (translated_text, tokens_used)."""
        pass

    @abstractmethod
    def translate_batch(self, terms: List[str]) -> Dict[str, str]:
        """Translate a list of terms and return a mapping JP -> VN."""
        pass

    @abstractmethod
    def detect_domain(self, text: str) -> str:
        """Analyze text and suggest a domain name."""
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        """Verify if the API key and connection are valid."""
        pass
