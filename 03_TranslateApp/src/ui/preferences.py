"""UI for user preferences (Appearance, etc.)."""

import customtkinter as ctk
from typing import Any, Dict
from src.data.config_manager import ConfigManager
from src.utils import constants as c

class PreferencesDialog(ctk.CTkToplevel):
    """Dialog for configuring user preferences."""

    def __init__(self, master: ctk.CTk, config_manager: ConfigManager, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        self.config_manager = config_manager
        
        self.title("Preferences")
        self.geometry("350x250")
        self.resizable(False, False)
        
        self.after(10, self.lift)
        self.focus_set(); self.grab_set()
        
        self._build_widgets()
        self._load_settings()

    def _build_widgets(self) -> None:
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        lbl_mode = ctk.CTkLabel(
            self.main_frame,
            text="Giao diện (Display Mode):",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_mode.pack(anchor="w", pady=(0, 10))
        
        self.seg_mode = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["Light", "Dark"],
            command=self._on_mode_change
        )
        self.seg_mode.pack(fill="x", pady=(0, 30))

        btn_close = ctk.CTkButton(
            self.main_frame,
            text="Đóng",
            fg_color=c.COLOR_PRIMARY,
            command=self.destroy
        )
        btn_close.pack(side="bottom")

    def _load_settings(self) -> None:
        prefs = self.config_manager.load_preferences()
        mode = prefs.get("appearance_mode", "dark").capitalize()
        self.seg_mode.set(mode)

    def _on_mode_change(self, mode: str) -> None:
        mode = mode.lower()
        ctk.set_appearance_mode(mode)
        
        prefs = self.config_manager.load_preferences()
        prefs["appearance_mode"] = mode
        self.config_manager.save_preferences(prefs)
