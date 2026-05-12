"""UI for browsing and opening saved translation sessions."""

import os
import logging
from datetime import datetime
import tkinter as tk
from typing import Callable, List, Dict

import customtkinter as ctk
from src.data.session_manager import SessionManager
from src.utils import constants as c

logger = logging.getLogger(__name__)

class SessionRow(ctk.CTkFrame):
    """A single row in the session history list."""
    def __init__(self, master, session_meta, on_open, on_delete, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.grid_columnconfigure(0, weight=1)
        
        # File info
        filename = os.path.basename(session_meta["source_file"])
        updated_at = datetime.fromisoformat(session_meta["updated_at"]).strftime("%d/%m/%Y %H:%M")
        
        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        lbl_file = ctk.CTkLabel(info_frame, text=filename, font=ctk.CTkFont(weight="bold"), anchor="w")
        lbl_file.pack(fill="x")
        
        lbl_meta = ctk.CTkLabel(info_frame, text=f"Lần sửa cuối: {updated_at}", font=ctk.CTkFont(size=11), text_color="gray60", anchor="w")
        lbl_meta.pack(fill="x")

        # Actions
        btn_open = ctk.CTkButton(self, text="Mở", width=60, fg_color=c.COLOR_PRIMARY, command=lambda: on_open(session_meta["id"]))
        btn_open.grid(row=0, column=1, padx=5)
        
        btn_del = ctk.CTkButton(self, text="✕", width=32, fg_color=c.COLOR_DANGER, hover_color="#C42B1C", command=lambda: on_delete(session_meta["id"]))
        btn_del.grid(row=0, column=2, padx=5)

class SessionHistoryWindow(ctk.CTkToplevel):
    """Toplevel window to manage and open saved sessions."""

    def __init__(self, master, session_manager: SessionManager, on_session_selected: Callable[[str], None], **kwargs):
        super().__init__(master, **kwargs)
        self.title("Lịch sử phiên dịch")
        self.geometry("600x500")
        self.session_manager = session_manager
        self.on_session_selected = on_session_selected
        
        self.after(10, self.lift)
        self.focus_set(); self.grab_set()
        
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        
        self._build_ui()
        self._load_sessions()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkLabel(header, text="Các tệp đang dịch dở", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")

        # List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=c.CORNER_RADIUS)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Footer
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        ctk.CTkButton(footer, text="Đóng", fg_color="gray30", command=self.destroy).pack(side="right")

    def _load_sessions(self):
        for child in self.scroll_frame.winfo_children(): child.destroy()
        
        sessions = self.session_manager.list_sessions()
        if not sessions:
            ctk.CTkLabel(self.scroll_frame, text="Chưa có phiên làm việc nào được lưu.", text_color="gray50").pack(pady=40)
            return

        for i, meta in enumerate(sessions):
            row = SessionRow(self.scroll_frame, meta, on_open=self._on_open, on_delete=self._on_delete)
            row.grid(row=i, column=0, sticky="ew", pady=2)
            # Add separator
            if i < len(sessions) - 1:
                ctk.CTkFrame(self.scroll_frame, height=1, fg_color="gray30").grid(row=i, column=0, sticky="ew", pady=(5, 0), padx=10)

    def _on_open(self, session_id):
        self.on_session_selected(session_id)
        self.destroy()

    def _on_delete(self, session_id):
        if tk.messagebox.askyesno("Xác nhận", "Xóa phiên làm việc này?", parent=self):
            # We need a delete_session in SessionManager. Let's assume it exists or I'll add it.
            try:
                file_path = self.session_manager.sessions_dir / f"{session_id}.json"
                if file_path.exists():
                    os.remove(file_path)
                self._load_sessions()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", str(e), parent=self)
