"""Bulk import with AI translation UI (Polished)."""

import logging
import threading
import tkinter as tk
from typing import Callable, Dict, List, Optional, Tuple

import customtkinter as ctk

from src.data.glossary_repo import GlossaryRepository
from src.services.base_client import BaseAIClient
from src.utils import constants as c

logger = logging.getLogger(__name__)


class ConflictResolutionWindow(ctk.CTkToplevel):
    """Polished window to resolve AI-Existing glossary conflicts."""

    def __init__(self, master, conflicts, on_complete, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Xử lý xung đột thuật ngữ")
        self.geometry("750x550")
        self.on_complete = on_complete

        self.after(10, self.lift)
        self.focus_set(); self.grab_set()

        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)

        f_h = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY, weight="bold")
        ctk.CTkLabel(self, text="⚠️ Phát hiện xung đột bản dịch. Hãy chọn bản dịch bạn muốn sử dụng:",
                    text_color=c.COLOR_WARNING, font=f_h, wraplength=700).grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Table header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=1, column=0, padx=20, sticky="nsew")
        header.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(header, text="TIẾNG NHẬT", font=f_h, text_color="gray50").grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(header, text="HIỆN TẠI", font=f_h, text_color="gray50").grid(row=0, column=1, sticky="w")
        ctk.CTkLabel(header, text="AI ĐỀ XUẤT", font=f_h, text_color="gray50").grid(row=0, column=2, sticky="w")

        self.scroll_frame = ctk.CTkScrollableFrame(header, corner_radius=c.CORNER_RADIUS)
        self.scroll_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        self.scroll_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.check_vars = []
        for i, (jp, old, new) in enumerate(conflicts):
            ctk.CTkLabel(self.scroll_frame, text=jp, font=ctk.CTkFont(family=c.FONT_FAMILY[2])).grid(row=i, column=0, sticky="w", pady=4, padx=5)
            ctk.CTkLabel(self.scroll_frame, text=old, text_color="gray60").grid(row=i, column=1, sticky="w", pady=4, padx=5)
            var = tk.BooleanVar(value=True)
            self.check_vars.append((jp, new, var))
            chk = ctk.CTkCheckBox(self.scroll_frame, text=new, variable=var, corner_radius=c.CORNER_RADIUS, checkbox_height=18, checkbox_width=18)
            chk.grid(row=i, column=2, sticky="w", pady=4, padx=5)

        # Footer
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        ctk.CTkButton(footer, text="Hoàn tất cập nhật", fg_color=c.COLOR_PRIMARY, corner_radius=c.CORNER_RADIUS, command=self._handle_complete).pack(side="right")
        ctk.CTkButton(footer, text="Hủy", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy).pack(side="right", padx=10)

    def _handle_complete(self):
        updates = [(jp, new) for jp, new, var in self.check_vars if var.get()]
        self.on_complete(updates); self.destroy()


class BulkImportWindow(ctk.CTkToplevel):
    """Polished AI-assisted bulk import window."""

    def __init__(self, master, repo, ai_client, on_success, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Nhập thuật ngữ hàng loạt (AI ✨)")
        self.geometry("650x600")
        self.repo = repo; self.ai_client = ai_client; self.on_success = on_success

        self.after(10, self.lift); self.focus_set()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Dán danh sách thuật ngữ tiếng Nhật (mỗi dòng một từ):", 
                    font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.txt_input = ctk.CTkTextbox(self, corner_radius=c.CORNER_RADIUS, border_width=c.BORDER_WIDTH, font=ctk.CTkFont(family=c.FONT_FAMILY[2], size=12))
        self.txt_input.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, corner_radius=c.CORNER_RADIUS, progress_color=c.COLOR_AI)
        self.progress_bar.set(0); self.progress_bar.pack(fill="x", pady=(0, 5)); self.progress_bar.pack_forget()
        self.lbl_status = ctk.CTkLabel(self.progress_frame, text="", font=ctk.CTkFont(size=11), text_color=c.COLOR_AI)
        self.lbl_status.pack()

        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        self.btn_import = ctk.CTkButton(self.footer, text="Dịch & Nhập vào ✨", fg_color=c.COLOR_AI, hover_color="#8E44AD", corner_radius=c.CORNER_RADIUS, command=self._start_import)
        self.btn_import.pack(side="right")
        self.btn_cancel = ctk.CTkButton(self.footer, text="Đóng", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy)
        self.btn_cancel.pack(side="right", padx=10)

    def _start_import(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        if not text: return
        terms = [t.strip() for t in text.split("\n") if t.strip()]
        if not terms: return
        self.btn_import.configure(state="disabled"); self.txt_input.configure(state="disabled")
        self.progress_bar.pack(fill="x", pady=(0, 5)); self.progress_bar.configure(mode="indeterminate"); self.progress_bar.start()
        self.lbl_status.configure(text="AI đang xử lý danh sách thuật ngữ...")
        threading.Thread(target=self._run_translation, args=(terms,), daemon=True).start()

    def _run_translation(self, terms):
        try:
            res = self.ai_client.translate_batch(terms)
            self.after(0, self._process_results, res)
        except Exception as e:
            logger.error(f"Bulk import error: {e}")
            self.after(0, lambda: self._handle_error(str(e)))

    def _process_results(self, translated_map):
        self.progress_bar.stop(); self.progress_bar.pack_forget()
        self.lbl_status.configure(text="Phân tích và gộp dữ liệu...")
        existing = self.repo.get_terms()
        to_add, to_resolve = [], []
        for jp, vn in translated_map.items():
            if jp in existing:
                if existing[jp] != vn: to_resolve.append((jp, existing[jp], vn))
            else: to_add.append((jp, vn))
        if to_resolve: ConflictResolutionWindow(self, conflicts=to_resolve, on_complete=lambda ups: self._finalize_import(to_add, ups))
        else: self._finalize_import(to_add, [])

    def _finalize_import(self, added, updated):
        for jp, vn in added + updated: self.repo.add_term(jp, vn)
        self.on_success()
        tk.messagebox.showinfo("Thành công", f"Đã nhập {len(added) + len(updated)} thuật ngữ.")
        self.destroy()

    def _handle_error(self, msg):
        self.progress_bar.stop(); self.progress_bar.pack_forget()
        self.btn_import.configure(state="normal"); self.txt_input.configure(state="normal")
        self.lbl_status.configure(text=""); tk.messagebox.showerror("Lỗi AI", msg)
