"""Logic for tracking and formatting API token usage."""

from typing import Dict, Any


class TokenTracker:
    """Manages token counts for the current session and formats them for UI."""

    def __init__(self):
        self.session_total = 0
        self.current_page = 0

    def add_usage(self, token_count: int):
        """Add tokens used in the latest operation."""
        self.current_page = token_count
        self.session_total += token_count

    def reset_page_counter(self):
        """Reset the per-page counter (e.g., when moving to a new untranslated page)."""
        self.current_page = 0

    def get_formatted_status(self) -> str:
        """Return a formatted string for the Bottom Bar."""
        page_str = self.format_count(self.current_page)
        total_str = self.format_count(self.session_total)
        return f"Tokens: {page_str} (Trang) | {total_str} (Tổng)"

    @staticmethod
    def format_count(n: int) -> str:
        """Format large numbers with suffixes (K, M)."""
        if n < 1000:
            return str(n)
        if n < 1000000:
            return f"{n/1000:.1f}K"
        return f"{n/1000000:.1f}M"
