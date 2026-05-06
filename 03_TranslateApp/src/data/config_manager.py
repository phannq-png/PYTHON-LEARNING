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

        self._ensure_config_dir()
        self.fernet = Fernet(self._get_or_create_key())

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

    # ── API Configuration (Encrypted) ───────────────────────────────────────

    def load_api_config(self) -> Dict[str, Any]:
        """Load and decrypt the API configuration.
        
        If an InvalidToken error occurs (e.g., the secret key was reset), 
        the old config is backed up and an empty dict is returned.
        """
        if not self.api_config_path.exists():
            return {}
        
        try:
            with open(self.api_config_path, "r", encoding="utf-8") as f:
                encrypted_data = json.load(f)
            
            decrypted_data = {}
            for key, value in encrypted_data.items():
                if isinstance(value, str):
                    try:
                        decrypted_val = self.fernet.decrypt(value.encode("utf-8")).decode("utf-8")
                        decrypted_data[key] = decrypted_val
                    except InvalidToken:
                        logger.warning("Invalid token, secret key might have been reset.")
                        self._backup_invalid_config()
                        return {}
                else:
                    decrypted_data[key] = value
            return decrypted_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode API config: {e}. Using empty config.")
            return {}
        except Exception as e:
            logger.error(f"Error loading API config: {e}")
            return {}

    def save_api_config(self, data: Dict[str, Any]) -> None:
        """Encrypt and save the API configuration."""
        encrypted_data = {}
        for key, value in data.items():
            if isinstance(value, str):
                encrypted_val = self.fernet.encrypt(value.encode("utf-8")).decode("utf-8")
                encrypted_data[key] = encrypted_val
            else:
                encrypted_data[key] = value
                
        try:
            with open(self.api_config_path, "w", encoding="utf-8") as f:
                json.dump(encrypted_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving API config: {e}")
            raise

    def _backup_invalid_config(self) -> None:
        """Backup the invalid API config file."""
        backup_path = self.api_config_path.with_suffix(".json.bak")
        try:
            shutil.copy2(self.api_config_path, backup_path)
            logger.info(f"Backed up invalid API config to {backup_path}")
        except Exception as e:
            logger.error(f"Failed to backup invalid API config: {e}")
