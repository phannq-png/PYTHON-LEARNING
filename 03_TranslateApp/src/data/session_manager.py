import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

class SessionManager:
    """Manages the lifecycle of translation sessions (loading, saving, and creating).
    
    Sessions are stored as JSON files in the 'data/sessions' directory.
    """

    def __init__(self, data_dir: str = "data") -> None:
        """Initialize the session manager and ensure the sessions directory exists."""
        self.sessions_dir = Path(data_dir) / "sessions"
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensure the sessions directory exists."""
        os.makedirs(self.sessions_dir, exist_ok=True)

    def create_session(
        self, 
        docx_path: str, 
        segments: List[str], 
        domain: str = "common"
    ) -> Dict[str, Any]:
        """Create a new session object from a source document and its segments.
        
        Args:
            docx_path: Absolute path to the original DOCX file.
            segments: List of Japanese text segments (pages).
            domain: The selected translation domain.
            
        Returns:
            A dictionary representing the new session.
        """
        now = datetime.now()
        timestamp_str = now.strftime("%Y%m%d_%H%M%S")
        filename = Path(docx_path).stem
        session_id = f"{timestamp_str}_{filename}"

        pages = []
        for i, text in enumerate(segments):
            pages.append({
                "id": i,
                "jp": text,
                "vn": "",
                "is_translated": False,
                "check_status": None, # None (unchecked), 'ok', 'error'
                "is_reviewed": False,
                "tokens": 0
            })

        session_data = {
            "id": session_id,
            "source_file": str(docx_path),
            "domain": domain,
            "pages": pages,
            "current_page": 0,
            "total_tokens": 0,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat()
        }

        return session_data

    def save_session(self, session_data: Dict[str, Any]) -> str:
        """Save session data to a JSON file.
        
        Args:
            session_data: The session dictionary to save.
            
        Returns:
            The path to the saved session file.
        """
        session_id = session_data.get("id")
        if not session_id:
            raise ValueError("Session data must contain an 'id'.")

        file_path = self.sessions_dir / f"{session_id}.json"
        
        # Update timestamp
        session_data["updated_at"] = datetime.now().isoformat()

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
            logger.info(f"Session saved to {file_path}")
            return str(file_path)
        except Exception as e:
            logger.error(f"Failed to save session {session_id}: {e}")
            raise

    def load_session(self, session_id: str) -> Dict[str, Any]:
        """Load session data from a JSON file.
        
        Args:
            session_id: The ID of the session to load.
            
        Returns:
            The session dictionary.
        """
        file_path = self.sessions_dir / f"{session_id}.json"
        
        if not file_path.exists():
            raise FileNotFoundError(f"Session file not found: {file_path}")

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load session {session_id}: {e}")
            raise

    def list_sessions(self) -> List[Dict[str, str]]:
        """List all available sessions in the directory.
        
        Returns:
            A list of dictionaries containing session metadata (id, filename, updated_at).
        """
        sessions = []
        for file in self.sessions_dir.glob("*.json"):
            try:
                # We only need metadata for the list, so we might only read part of the file
                # but for simplicity we load the whole thing
                with open(file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    sessions.append({
                        "id": data["id"],
                        "source_file": data["source_file"],
                        "updated_at": data["updated_at"]
                    })
            except Exception:
                continue
        
        # Sort by updated_at descending
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
