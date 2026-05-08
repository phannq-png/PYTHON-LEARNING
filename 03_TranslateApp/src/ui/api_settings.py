"""API Settings dialog for AI provider configuration."""

import logging
import tkinter as tk
from typing import Dict, Any

import customtkinter as ctk
from src.data.config_manager import ConfigManager
from src.utils import constants as c

logger = logging.getLogger(__name__)


class ApiSettingsDialog(ctk.CTkToplevel):
    """Dialog for configuring OpenAI and Gemini API settings."""

    def __init__(self, master: any, config_manager: ConfigManager, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Cấu hình API")
        self.geometry("500x450")
        self.config_manager = config_manager

        self.after(10, self.lift)
        self.focus_set()
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_ui()
        self._load_current_config()

    def _build_ui(self):
        # ── Active Provider Selection ──────────────────────────────────────
        self.provider_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.provider_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        
        ctk.CTkLabel(self.provider_frame, text="Dịch vụ AI ưu tiên:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        
        self.active_provider_var = tk.StringVar(value="gemini")
        self.seg_provider = ctk.CTkSegmentedButton(
            self.provider_frame, 
            values=["gemini", "openai"], 
            variable=self.active_provider_var,
            corner_radius=c.CORNER_RADIUS
        )
        self.seg_provider.pack(side="left", padx=10)

        # ── Tabview for Providers ──────────────────────────────────────────
        self.tabview = ctk.CTkTabview(self, corner_radius=c.CORNER_RADIUS)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        
        self.tabview.add("Google Gemini")
        self.tabview.add("OpenAI")
        
        # ── Gemini Tab ─────────────────────────────────────────────────────
        self._build_gemini_tab(self.tabview.tab("Google Gemini"))
        
        # ── OpenAI Tab ─────────────────────────────────────────────────────
        self._build_openai_tab(self.tabview.tab("OpenAI"))

        # ── Footer ─────────────────────────────────────────────────────────
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.btn_save = ctk.CTkButton(
            btn_frame, 
            text="Lưu cấu hình", 
            fg_color=c.COLOR_PRIMARY,
            corner_radius=c.CORNER_RADIUS,
            command=self._handle_save
        )
        self.btn_save.pack(side="right")

        ctk.CTkButton(
            btn_frame, 
            text="Hủy", 
            fg_color="gray30", 
            corner_radius=c.CORNER_RADIUS,
            command=self.destroy
        ).pack(side="right", padx=10)

    def _build_gemini_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tab, text="Google Gemini API Key:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.ent_gemini_key = ctk.CTkEntry(tab, show="*", width=350, corner_radius=c.CORNER_RADIUS)
        self.ent_gemini_key.grid(row=1, column=0, sticky="ew", pady=5)
        
        ctk.CTkLabel(tab, text="Model:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, sticky="w", pady=(15, 5))
        self.cmb_gemini_model = ctk.CTkComboBox(
            tab, 
            values=["gemini-1.5-pro", "gemini-1.5-flash", "gemini-pro"],
            corner_radius=c.CORNER_RADIUS
        )
        self.cmb_gemini_model.grid(row=3, column=0, sticky="ew", pady=5)
        self.cmb_gemini_model.set("gemini-1.5-pro")

    def _build_openai_tab(self, tab):
        tab.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(tab, text="OpenAI API Key:", font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=(10, 5))
        self.ent_openai_key = ctk.CTkEntry(tab, show="*", width=350, corner_radius=c.CORNER_RADIUS)
        self.ent_openai_key.grid(row=1, column=0, sticky="ew", pady=5)
        
        ctk.CTkLabel(tab, text="Model:", font=ctk.CTkFont(weight="bold")).grid(row=2, column=0, sticky="w", pady=(15, 5))
        self.cmb_openai_model = ctk.CTkComboBox(
            tab, 
            values=["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            corner_radius=c.CORNER_RADIUS
        )
        self.cmb_openai_model.grid(row=3, column=0, sticky="ew", pady=5)
        self.cmb_openai_model.set("gpt-4o")

    def _load_current_config(self):
        """Populate fields with existing encrypted config."""
        config = self.config_manager.load_api_config()
        
        self.active_provider_var.set(config.get("active_provider", "gemini"))
        
        self.ent_gemini_key.insert(0, config.get("gemini_api_key", ""))
        self.cmb_gemini_model.set(config.get("gemini_model", "gemini-1.5-pro"))
        
        self.ent_openai_key.insert(0, config.get("openai_api_key", ""))
        self.cmb_openai_model.set(config.get("openai_model", "gpt-4o"))

    def _handle_save(self):
        """Encrypt and save the new configuration."""
        new_config = {
            "active_provider": self.active_provider_var.get(),
            "gemini_api_key": self.ent_gemini_key.get().strip(),
            "gemini_model": self.cmb_gemini_model.get(),
            "openai_api_key": self.ent_openai_key.get().strip(),
            "openai_model": self.cmb_openai_model.get()
        }
        
        try:
            self.config_manager.save_api_config(new_config)
            tk.messagebox.showinfo("Thành công", "Cấu hình API đã được lưu an toàn.")
            self.destroy()
        except Exception as e:
            logger.error(f"Failed to save API config: {e}")
            tk.messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")
