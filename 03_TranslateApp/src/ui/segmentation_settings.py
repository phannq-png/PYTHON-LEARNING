"""UI component for segmentation settings dialog."""

import tkinter as tk
from tkinter import messagebox
from typing import Any, Dict

import customtkinter as ctk

from src.data.config_manager import ConfigManager


class SegmentationSettingsDialog(ctk.CTkToplevel):
    """Modal dialog for configuring text segmentation rules."""

    def __init__(self, master: ctk.CTk, config_manager: ConfigManager, **kwargs: Any) -> None:
        super().__init__(master, **kwargs)
        
        self.config_manager = config_manager
        
        self.title("Segmentation Settings")
        self.geometry("400x380")
        self.resizable(False, False)
        
        # Make the dialog modal
        self.transient(master)
        self.grab_set()
        
        self._build_widgets()
        self._load_current_settings()

    def _build_widgets(self) -> None:
        """Build the dialog's UI layout."""
        # Main padding frame
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ── Max Characters ──────────────────────────────────────────────────
        lbl_max_chars = ctk.CTkLabel(
            self.main_frame,
            text="Số lượng ký tự tối đa mỗi page:",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_max_chars.pack(anchor="w", pady=(0, 4))
        
        self.ent_max_chars = ctk.CTkEntry(self.main_frame, width=150)
        self.ent_max_chars.pack(anchor="w", pady=(0, 16))
        
        # ── Hard / Soft Returns ─────────────────────────────────────────────
        lbl_return_types = ctk.CTkLabel(
            self.main_frame,
            text="Ký tự ngắt đoạn (Return Types):",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_return_types.pack(anchor="w", pady=(0, 4))
        
        self.chk_hard_return = ctk.CTkCheckBox(
            self.main_frame,
            text="Phím Enter (Hard Return)",
        )
        self.chk_hard_return.pack(anchor="w", pady=(0, 8), padx=10)
        
        self.chk_soft_return = ctk.CTkCheckBox(
            self.main_frame,
            text="Phím Shift + Enter (Soft Return)",
        )
        self.chk_soft_return.pack(anchor="w", pady=(0, 16), padx=10)
        
        # ── Custom Markers ──────────────────────────────────────────────────
        lbl_custom = ctk.CTkLabel(
            self.main_frame,
            text="Ký tự tùy chỉnh (cách nhau bằng dấu phẩy):",
            font=ctk.CTkFont(weight="bold")
        )
        lbl_custom.pack(anchor="w", pady=(0, 4))
        
        self.ent_custom_markers = ctk.CTkEntry(self.main_frame, width=360, placeholder_text="Ví dụ: 【,※")
        self.ent_custom_markers.pack(anchor="w", pady=(0, 24))
        
        # ── Action Buttons ──────────────────────────────────────────────────
        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", side="bottom", pady=(10, 0))
        
        self.btn_cancel = ctk.CTkButton(
            self.btn_frame,
            text="Cancel",
            width=100,
            fg_color=("gray70", "gray30"),
            hover_color=("gray60", "gray40"),
            command=self.destroy
        )
        self.btn_cancel.pack(side="right", padx=(10, 0))
        
        self.btn_save = ctk.CTkButton(
            self.btn_frame,
            text="Save",
            width=100,
            command=self._on_save
        )
        self.btn_save.pack(side="right")

    def _load_current_settings(self) -> None:
        """Load settings from ConfigManager and populate the UI."""
        config = self.config_manager.load_app_config()
        
        # Default values
        max_chars = config.get("max_chars_per_page", 1000)
        use_hard = config.get("use_hard_return", True)
        use_soft = config.get("use_soft_return", False)
        custom = config.get("custom_markers", "")
        
        # Populate
        self.ent_max_chars.insert(0, str(max_chars))
        
        if use_hard:
            self.chk_hard_return.select()
        else:
            self.chk_hard_return.deselect()
            
        if use_soft:
            self.chk_soft_return.select()
        else:
            self.chk_soft_return.deselect()
            
        self.ent_custom_markers.insert(0, custom)

    def _on_save(self) -> None:
        """Validate input and save settings."""
        max_chars_str = self.ent_max_chars.get().strip()
        
        try:
            max_chars = int(max_chars_str)
            if max_chars <= 0:
                raise ValueError("Must be positive")
        except ValueError:
            messagebox.showerror(
                "Lỗi nhập liệu", 
                "Số lượng ký tự tối đa phải là một số nguyên dương.",
                parent=self
            )
            return  # Stop execution, do not save or close
            
        use_hard = bool(self.chk_hard_return.get())
        use_soft = bool(self.chk_soft_return.get())
        custom = self.ent_custom_markers.get().strip()
        
        # Load existing to not overwrite other settings
        config = self.config_manager.load_app_config()
        
        config["max_chars_per_page"] = max_chars
        config["use_hard_return"] = use_hard
        config["use_soft_return"] = use_soft
        config["custom_markers"] = custom
        
        self.config_manager.save_app_config(config)
        self.destroy()
