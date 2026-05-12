import json
import logging
import os
import shutil
from pathlib import Path
from typing import Any, Dict

from cryptography.fernet import Fernet, InvalidToken

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manages application configurations and secure API settings.
    
    Adheres to the data layer principles by encapsulating file I/O and encryption.
    """

    def __init__(self, data_dir: str = "data") -> None:
        """Initialize the ConfigManager with the root data directory."""
        self.config_dir = Path(data_dir) / "config"
        self.app_config_path = self.config_dir / "config.json"
        self.api_config_path = self.config_dir / "api_config.json"
        self.secret_key_path = self.config_dir / ".secret.key"
        self.preferences_path = self.config_dir / "preferences.json"

        self._ensure_config_dir()
        self.fernet = Fernet(self._get_or_create_key())

    def load_preferences(self) -> Dict[str, Any]:
        """Load user preferences (Dark/Light mode, etc.)."""
        if not self.preferences_path.exists():
            return {"appearance_mode": "dark"}
        try:
            with open(self.preferences_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"appearance_mode": "dark"}

    def save_preferences(self, data: Dict[str, Any]) -> None:
        """Save user preferences."""
        try:
            with open(self.preferences_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving preferences: {e}")

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        os.makedirs(self.config_dir, exist_ok=True)

    def _get_or_create_key(self) -> bytes:
        """Get the existing secret key or create a new one."""
        if self.secret_key_path.exists():
            with open(self.secret_key_path, "rb") as f:
                return f.read().strip()
        
        # Generate new key
        key = Fernet.generate_key()
        with open(self.secret_key_path, "wb") as f:
            f.write(key)
        return key

    # ── App Configuration (Plaintext) ───────────────────────────────────────

    def load_app_config(self) -> Dict[str, Any]:
        """Load the standard application configuration."""
        if not self.app_config_path.exists():
            return {}
        try:
            with open(self.app_config_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode app config: {e}. Using empty config.")
            return {}
        except Exception as e:
            logger.error(f"Error loading app config: {e}")
            return {}

    def save_app_config(self, data: Dict[str, Any]) -> None:
        """Save the standard application configuration."""
        try:
            with open(self.app_config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving app config: {e}")
            raise

    def get_segmentation_config(self) -> Dict[str, Any]:
        """Get processed segmentation settings with consistent keys."""
        config = self.load_app_config()
        custom_markers_str = config.get("custom_markers", "")
        custom_markers = [m.strip() for m in custom_markers_str.split(",") if m.strip()]
        
        return {
            "max_chars": config.get("max_chars_per_page", 1000),
            "split_on_enter": config.get("use_hard_return", True),
            "split_on_soft_return": config.get("use_soft_return", False),
            "custom_markers": custom_markers
        }

    def get_domain_prompt(self, domain: str) -> str:
        """Get the specific prompt rules for a domain."""
        config = self.load_app_config()
        prompts = config.get("domain_prompts", {})
        return prompts.get(domain, "")

    def save_domain_prompt(self, domain: str, prompt: str) -> None:
        """Save specific prompt rules for a domain."""
        config = self.load_app_config()
        if "domain_prompts" not in config:
            config["domain_prompts"] = {}
        config["domain_prompts"][domain] = prompt
        self.save_app_config(config)

    # ── API Configuration (Encrypted) ───────────────────────────────────────

    def load_api_config(self) -> Dict[str, Any]:
        """Load and decrypt the API configuration.
        
        Supports the new list-based format and migrates from the old format.
        """
        if not self.api_config_path.exists():
            return {"keys": [], "active_id": None}
        
        try:
            with open(self.api_config_path, "r", encoding="utf-8") as f:
                encrypted_data = json.load(f)
            
            # Migration: if 'gemini_api_key' exists, it's the old format
            if "gemini_api_key" in encrypted_data or "openai_api_key" in encrypted_data:
                return self._migrate_old_api_config(encrypted_data)

            # New format: {"keys": [...], "active_id": "..."}
            decrypted_keys = []
            for k_obj in encrypted_data.get("keys", []):
                new_k = k_obj.copy()
                if "key" in new_k:
                    try:
                        new_k["key"] = self.fernet.decrypt(new_k["key"].encode("utf-8")).decode("utf-8")
                    except InvalidToken:
                        new_k["key"] = "" # Key is lost if secret reset
                decrypted_keys.append(new_k)
            
            return {
                "keys": decrypted_keys,
                "active_id": encrypted_data.get("active_id")
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode API config: {e}. Using empty config.")
            return {"keys": [], "active_id": None}
        except Exception as e:
            logger.error(f"Error loading API config: {e}")
            return {"keys": [], "active_id": None}

    def _migrate_old_api_config(self, old_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert old single-key config to the new list format."""
        new_keys = []
        import uuid
        
        # Migrate Gemini
        gemini_key = old_data.get("gemini_api_key")
        if gemini_key:
            try:
                decrypted_key = self.fernet.decrypt(gemini_key.encode("utf-8")).decode("utf-8")
                new_keys.append({
                    "id": str(uuid.uuid4()),
                    "provider": "gemini",
                    "model": old_data.get("gemini_model", "gemini-1.5-flash"),
                    "key": decrypted_key,
                    "status": "unknown"
                })
            except: pass
            
        # Migrate OpenAI
        openai_key = old_data.get("openai_api_key")
        if openai_key:
            try:
                decrypted_key = self.fernet.decrypt(openai_key.encode("utf-8")).decode("utf-8")
                new_keys.append({
                    "id": str(uuid.uuid4()),
                    "provider": "openai",
                    "model": old_data.get("openai_model", "gpt-4o"),
                    "key": decrypted_key,
                    "status": "unknown"
                })
            except: pass
            
        active_id = new_keys[0]["id"] if new_keys else None
        migrated = {"keys": new_keys, "active_id": active_id}
        self.save_api_config(migrated) # Save migrated version immediately
        return migrated

    def save_api_config(self, data: Dict[str, Any]) -> None:
        """Encrypt and save the API configuration (list-based)."""
        encrypted_keys = []
        for k_obj in data.get("keys", []):
            new_k = k_obj.copy()
            if "key" in new_k and new_k["key"]:
                new_k["key"] = self.fernet.encrypt(new_k["key"].encode("utf-8")).decode("utf-8")
            encrypted_keys.append(new_k)
            
        encrypted_data = {
            "keys": encrypted_keys,
            "active_id": data.get("active_id")
        }
                
        try:
            with open(self.api_config_path, "w", encoding="utf-8") as f:
                json.dump(encrypted_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving API config: {e}")
            raise

    def update_api_key_status(self, key_id: str, status: str, is_enabled: bool = None) -> None:
        """Update the operational status and enabled state of a specific API key."""
        config = self.load_api_config()
        changed = False
        for k in config.get("keys", []):
            if k.get("id") == key_id:
                k["status"] = status
                if is_enabled is not None:
                    k["is_enabled"] = is_enabled
                changed = True
                break
        if changed:
            self.save_api_config(config)

    def export_full_backup(self, export_path: str) -> None:
        """Create a ZIP backup of all configurations and glossaries."""
        import zipfile
        try:
            with zipfile.ZipFile(export_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Add config files
                if self.app_config_path.exists(): zipf.write(self.app_config_path, "config/config.json")
                if self.api_config_path.exists(): zipf.write(self.api_config_path, "config/api_config.json")
                if self.secret_key_path.exists(): zipf.write(self.secret_key_path, "config/.secret.key")
                
                # Add glossaries
                glossary_dir = self.config_dir.parent / "glossaries"
                if glossary_dir.exists():
                    for file in glossary_dir.glob("*.json"):
                        zipf.write(file, f"glossaries/{file.name}")
                        
            logger.info(f"Full backup exported to {export_path}")
        except Exception as e:
            logger.error(f"Failed to export backup: {e}")
            raise

    def import_full_backup(self, import_path: str) -> None:
        """Restore all configurations and glossaries from a ZIP backup."""
        import zipfile
        try:
            with zipfile.ZipFile(import_path, 'r') as zipf:
                # Validate contents
                names = zipf.namelist()
                if not any(n.startswith("config/") for n in names):
                    raise ValueError("File ZIP không hợp lệ hoặc không chứa cấu hình ứng dụng.")
                
                # Extract to data directory
                data_root = self.config_dir.parent
                zipf.extractall(data_root)
            
            # Reload encryption
            self.fernet = Fernet(self._get_or_create_key())
            logger.info(f"Full backup imported from {import_path}")
        except Exception as e:
            logger.error(f"Failed to import backup: {e}")
            raise
