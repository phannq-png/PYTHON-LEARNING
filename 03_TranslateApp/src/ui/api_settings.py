"""API Settings dialog for managing multiple AI provider keys."""

import logging
import tkinter as tk
import threading
import uuid
from typing import Dict, Any, List, Optional

import customtkinter as ctk
from src.data.config_manager import ConfigManager
from src.services.gemini_client import GeminiClient
from src.services.openai_client import OpenAIClient
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip

logger = logging.getLogger(__name__)


class ApiKeyDialog(ctk.CTkToplevel):
    """Dialog for adding or editing a single API key."""

    def __init__(self, master: any, initial_data: Optional[Dict[str, Any]] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Thông tin API Key")
        self.geometry("450x450")
        self.result = None

        self.after(10, self.lift)
        self.focus_set()
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        # Name
        ctk.CTkLabel(self, text="Tên gọi nhớ:", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.ent_name = ctk.CTkEntry(self, placeholder_text="Ví dụ: Key cá nhân, Dự án A...")
        self.ent_name.pack(fill="x", padx=20)

        # Provider
        ctk.CTkLabel(self, text="Dịch vụ AI:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.cmb_provider = ctk.CTkComboBox(self, values=["gemini", "openai"], command=self._on_provider_change)
        self.cmb_provider.pack(fill="x", padx=20)

        # Model
        ctk.CTkLabel(self, text="Model:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.cmb_model = ctk.CTkComboBox(self, values=[])
        self.cmb_model.pack(fill="x", padx=20)

        # API Key
        ctk.CTkLabel(self, text="API Key:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.ent_key = ctk.CTkEntry(self, show="*", placeholder_text="Nhập API Key tại đây...")
        self.ent_key.pack(fill="x", padx=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=25)

        self.btn_save = ctk.CTkButton(btn_frame, text="Lưu", fg_color=c.COLOR_PRIMARY, command=self._on_save)
        self.btn_save.pack(side="right")

        self.btn_cancel = ctk.CTkButton(btn_frame, text="Hủy", fg_color="gray30", command=self.destroy)
        self.btn_cancel.pack(side="right", padx=10)

        if initial_data:
            self.ent_name.insert(0, initial_data.get("name", ""))
            self.cmb_provider.set(initial_data["provider"])
            self._on_provider_change(initial_data["provider"])
            self.cmb_model.set(initial_data["model"])
            self.ent_key.insert(0, initial_data["key"])
        else:
            self.cmb_provider.set("gemini")
            self._on_provider_change("gemini")

    def _on_provider_change(self, choice):
        if choice == "gemini":
            models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.0-flash-exp", "gemini-2.5-flash"]
        else:
            models = ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"]
        self.cmb_model.configure(values=models)
        self.cmb_model.set(models[0])

    def _on_save(self):
        name = self.ent_name.get().strip()
        key = self.ent_key.get().strip()
        if not key:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng nhập API Key.", parent=self)
            return
        
        self.result = {
            "name": name if name else f"{self.cmb_provider.get().upper()} Key",
            "provider": self.cmb_provider.get(),
            "model": self.cmb_model.get(),
            "key": key
        }
        self.destroy()


class ApiKeyRow(ctk.CTkFrame):
    """A single row in the API key list with individual test button."""

    def __init__(self, master, key_data, is_selected, is_enabled, on_toggle_active, on_toggle_enabled, on_edit, on_delete, on_test, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.key_data = key_data
        
        self.grid_columnconfigure(3, weight=1) # Name/Provider
        self.grid_columnconfigure(4, weight=1) # Model

        # Checkbox for enabling/disabling the key
        self.chk_enabled = ctk.CTkCheckBox(
            self, text="", width=20, height=20, corner_radius=4,
            command=lambda: on_toggle_enabled(key_data["id"])
        )
        if is_enabled: self.chk_enabled.select()
        else: self.chk_enabled.deselect()
        self.chk_enabled.grid(row=0, column=0, padx=(5, 0))
        add_tooltip(self.chk_enabled, "Bật/Tắt sử dụng Key này")

        # Status Icon (Working/Broken)
        status = key_data.get("status", "unknown")
        status_color = "#107C10" if status == "active" else ("#E74856" if status == "inactive" else "gray40")
        lbl_status = ctk.CTkLabel(self, text="●", text_color=status_color, font=ctk.CTkFont(size=20))
        lbl_status.grid(row=0, column=1, padx=5)

        # Selected Indicator (Star)
        star_text = "★" if is_selected else "☆"
        star_color = c.COLOR_AI if is_selected else "gray60"
        self.btn_select = ctk.CTkButton(
            self, text=star_text, width=30, height=30, 
            fg_color="transparent", text_color=star_color,
            font=ctk.CTkFont(size=20),
            hover=False,
            command=lambda: on_toggle_active(key_data["id"])
        )
        self.btn_select.grid(row=0, column=2, padx=(0, 5), sticky="w")
        add_tooltip(self.btn_select, "Đặt làm Key mặc định")

        # Name & Provider
        name_text = key_data.get("name", "Unnamed Key")
        provider_text = f"({key_data['provider'].upper()})"
        lbl_info = ctk.CTkLabel(self, text=f"{name_text} {provider_text}", font=ctk.CTkFont(weight="bold"), anchor="w")
        lbl_info.grid(row=0, column=3, sticky="ew", padx=5)

        # Model
        lbl_model = ctk.CTkLabel(self, text=key_data["model"], text_color="gray60")
        lbl_model.grid(row=0, column=4, sticky="w", padx=10)

        # Actions
        # Individual Test Button (⚡)
        self.btn_test = ctk.CTkButton(self, text="⚡", width=32, fg_color=("gray80", "gray30"), text_color="#F1C40F", command=lambda: on_test(key_data["id"]))
        self.btn_test.grid(row=0, column=5, padx=2)
        add_tooltip(self.btn_test, "Kiểm tra kết nối cho Key này")

        # Edit
        btn_edit = ctk.CTkButton(self, text="✎", width=32, fg_color=("gray80", "gray30"), text_color=("black", "white"), command=lambda: on_edit(key_data))
        btn_edit.grid(row=0, column=6, padx=2)
        add_tooltip(btn_edit, "Chỉnh sửa thông tin Key")

        # Delete
        btn_del = ctk.CTkButton(self, text="✕", width=32, fg_color=c.COLOR_DANGER, hover_color="#C42B1C", command=lambda: on_delete(key_data["id"]))
        btn_del.grid(row=0, column=7, padx=2)
        add_tooltip(btn_del, "Xóa Key này")


class ApiSettingsDialog(ctk.CTkToplevel):
    """Dialog for managing multiple AI provider API keys in a list."""

    def __init__(self, master: any, config_manager: ConfigManager, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Quản lý API Keys")
        self.geometry("900x600")
        self.config_manager = config_manager
        self.config = {"keys": [], "active_id": None}
        self.spinner = None

        self.after(10, self.lift)
        self.focus_set()
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_ui()
        self._load_config()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        ctk.CTkLabel(header, text="Danh sách API Keys", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        self.btn_add = ctk.CTkButton(
            header, text="+ Thêm Key mới", 
            fg_color=c.COLOR_PRIMARY,
            corner_radius=c.CORNER_RADIUS,
            command=self._on_add_key
        )
        self.btn_add.pack(side="right")
        add_tooltip(self.btn_add, "Thêm một tài khoản API Key mới")

        # List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=c.CORNER_RADIUS)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Footer
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")

        self.btn_test_all = ctk.CTkButton(footer, text="Kiểm tra lại toàn bộ kết nối", fg_color=("gray75", "gray30"), text_color=("gray10", "gray90"), command=self._test_all)
        self.btn_test_all.pack(side="left")
        add_tooltip(self.btn_test_all, "Tự động kiểm tra trạng thái hoạt động của toàn bộ danh sách")
        
        ctk.CTkButton(footer, text="Đóng", fg_color="gray30", width=100, command=self.destroy).pack(side="right")

    def _load_config(self):
        self.config = self.config_manager.load_api_config()
        self._refresh_list()

    def _refresh_list(self):
        for child in self.scroll_frame.winfo_children():
            child.destroy()
        
        keys = self.config.get("keys", [])
        if not keys:
            ctk.CTkLabel(self.scroll_frame, text="Chưa có API Key nào. Vui lòng thêm mới.", text_color="gray50").grid(row=0, column=0, pady=20)
            return

        for i, k_data in enumerate(keys):
            is_selected = (k_data["id"] == self.config.get("active_id"))
            is_enabled = k_data.get("is_enabled", True)
            row = ApiKeyRow(
                self.scroll_frame, k_data, is_selected, is_enabled,
                on_toggle_active=self._on_toggle_active,
                on_toggle_enabled=self._on_toggle_enabled,
                on_edit=self._on_edit_key,
                on_delete=self._on_delete_key,
                on_test=self._on_test_individual
            )
            row.grid(row=i, column=0, sticky="ew", pady=2)

    def _on_add_key(self):
        dialog = ApiKeyDialog(self)
        self.wait_window(dialog)
        if dialog.result:
            new_key = dialog.result
            new_key["id"] = str(uuid.uuid4())
            new_key["status"] = "unknown"
            self.config["keys"].append(new_key)
            if not self.config["active_id"]:
                self.config["active_id"] = new_key["id"]
            self._save_and_refresh()

    def _on_edit_key(self, k_data):
        dialog = ApiKeyDialog(self, initial_data=k_data)
        self.wait_window(dialog)
        if dialog.result:
            for i, k in enumerate(self.config["keys"]):
                if k["id"] == k_data["id"]:
                    self.config["keys"][i].update(dialog.result)
                    self.config["keys"][i]["status"] = "unknown"
                    break
            self._save_and_refresh()

    def _on_delete_key(self, key_id):
        if tk.messagebox.askyesno("Xác nhận", "Xóa API Key này?", parent=self):
            self.config["keys"] = [k for k in self.config["keys"] if k["id"] != key_id]
            if self.config["active_id"] == key_id:
                self.config["active_id"] = self.config["keys"][0]["id"] if self.config["keys"] else None
            self._save_and_refresh()

    def _on_toggle_active(self, key_id):
        self.config["active_id"] = key_id
        self._save_and_refresh()

    def _on_toggle_enabled(self, key_id):
        for k in self.config["keys"]:
            if k["id"] == key_id:
                k["is_enabled"] = not k.get("is_enabled", True)
                break
        self._save_and_refresh()

    def _on_test_individual(self, key_id):
        """Test connection for a specific key with a spinner."""
        k_data = next((k for k in self.config["keys"] if k["id"] == key_id), None)
        if not k_data: return

        from src.ui.components.spinner import LoadingSpinner
        self.spinner = LoadingSpinner(self)
        self.spinner.start(f"Đang kiểm tra {k_data.get('name')}...")

        def run_test():
            success = False
            try:
                if k_data["provider"] == "gemini":
                    client = GeminiClient(api_key=k_data["key"], model_name=k_data["model"])
                else:
                    client = OpenAIClient(api_key=k_data["key"], model_name=k_data["model"])
                success = client.test_connection()
            except: success = False

            def on_done():
                # Update status
                for i, k in enumerate(self.config["keys"]):
                    if k["id"] == key_id:
                        self.config["keys"][i]["status"] = "active" if success else "inactive"
                        break
                self._save_and_refresh()
                if self.spinner: self.spinner.stop()
                if success:
                    tk.messagebox.showinfo("Thành công", f"Kết nối tới {k_data.get('name')} hợp lệ!", parent=self)
                else:
                    tk.messagebox.showerror("Lỗi", f"Không thể kết nối tới {k_data.get('name')}.", parent=self)
                # Bring dialog back to front
                self.lift()
                self.focus_set()
            
            self.after(0, on_done)
        
        threading.Thread(target=run_test, daemon=True).start()

    def _save_and_refresh(self):
        self.config_manager.save_api_config(self.config)
        self._refresh_list()

    def _test_all(self):
        """Test connection for all keys with a loading spinner."""
        if not self.config.get("keys"): return
            
        from src.ui.components.spinner import LoadingSpinner
        self.spinner = LoadingSpinner(self)
        self.spinner.start("Đang kiểm tra kết nối cho toàn bộ danh sách...")
        
        def run_test():
            updated_keys = []
            for k in self.config["keys"]:
                success = False
                try:
                    if k["provider"] == "gemini":
                        client = GeminiClient(api_key=k["key"], model_name=k["model"])
                    else:
                        client = OpenAIClient(api_key=k["key"], model_name=k["model"])
                    success = client.test_connection()
                except: success = False
                
                new_k = k.copy()
                new_k["status"] = "active" if success else "inactive"
                updated_keys.append(new_k)
            
            def on_done():
                self.config["keys"] = updated_keys
                self._save_and_refresh()
                if self.spinner: self.spinner.stop()
                tk.messagebox.showinfo("Hoàn tất", "Đã cập nhật trạng thái kết nối cho toàn bộ danh sách.", parent=self)
                self.lift()
                self.focus_set()
            
            self.after(0, on_done)
            
        threading.Thread(target=run_test, daemon=True).start()
