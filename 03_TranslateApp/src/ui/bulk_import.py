"""Bulk import with AI translation UI (Polished)."""

import logging
import threading
import tkinter as tk
from typing import Callable, Dict, List, Optional, Tuple

import customtkinter as ctk

from src.data.glossary_repo import GlossaryRepository
from src.services.base_client import BaseAIClient
from src.utils import constants as c
from src.ui.components.spinner import LoadingSpinner

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

    def __init__(self, master, repo, ai_client, on_success, domain="common", **kwargs):
        super().__init__(master, **kwargs)
        self.title("Nhập thuật ngữ hàng loạt (AI ✨)")
        width, height = 650, 650
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.repo = repo; self.ai_client = ai_client; self.on_success = on_success; self.domain = domain
        self.spinner = LoadingSpinner(self)

        self.after(10, self.lift); self.focus_set()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1) # Terms textbox
        self.grid_rowconfigure(3, weight=1) # Reqs textbox

        self._build_ui()

    def _build_ui(self):
        # ── 1. Terms Input ────────────────────────────────────────────────
        ctk.CTkLabel(self, text="1. Dán danh sách thuật ngữ tiếng Nhật (mỗi dòng một từ):", 
                    font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.txt_input = ctk.CTkTextbox(self, corner_radius=c.CORNER_RADIUS, border_width=c.BORDER_WIDTH, font=ctk.CTkFont(family=c.FONT_FAMILY[2], size=12))
        self.txt_input.grid(row=1, column=0, padx=20, pady=5, sticky="nsew")

        # ── 2. Additional Requirements ─────────────────────────────────────
        ctk.CTkLabel(self, text='2. Yêu cầu bổ sung (Prompt rules) - Theo format "Ưu tiên: ...":', 
                    font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13, weight="bold")).grid(row=2, column=0, padx=20, pady=(15, 5), sticky="w")

        self.txt_reqs = ctk.CTkTextbox(self, corner_radius=c.CORNER_RADIUS, border_width=c.BORDER_WIDTH, font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=12))
        self.txt_reqs.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")
        
        # Load saved rules for domain or use default
        config_manager = getattr(self.master, 'config_manager', None)
        saved_reqs = ""
        if config_manager:
            saved_reqs = config_manager.get_domain_prompt(self.domain)

        if not saved_reqs:
            saved_reqs = (
                "Ưu tiên 1: Nếu có \"部材\" → BẮT BUỘC dịch là \"linh kiện\"\n"
                "Ví dụ: 建築部材 → linh kiện xây dựng\n\n"
                "Ưu tiên 2: Nếu có \"部分\" → BẮT BUỘC dịch là \"phần\"\n"
                "Ví dụ: 接合部分 → phần tiếp giáp\n\n"
                "Ưu tiên 3: Nếu có \"部\" (đứng độc lập, không thuộc 部材 hay 部分) → BẮT BUỘC dịch là \"bộ phận\"\n"
                "Ví dụ: 構造部 → bộ phận kết cấu"
            )
        self.txt_reqs.insert("1.0", saved_reqs)

        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        # Spinner replaces progress bar and status label

        # Tools frame
        self.tools_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tools_frame.grid(row=5, column=0, padx=20, sticky="ew")
        
        self.btn_clean = ctk.CTkButton(
            self.tools_frame, 
            text="✨ Làm sạch (Xóa số/ký hiệu đầu)", 
            fg_color=("gray75", "gray30"),
            text_color=("gray10", "gray90"),
            width=100,
            height=28,
            corner_radius=c.CORNER_RADIUS,
            command=self._clean_input
        )
        self.btn_clean.pack(side="left")

        self.footer = ctk.CTkFrame(self, fg_color="transparent")
        self.footer.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        self.btn_import = ctk.CTkButton(self.footer, text="Dịch & Nhập vào ✨", fg_color=c.COLOR_AI, hover_color="#8E44AD", corner_radius=c.CORNER_RADIUS, command=self._start_import)
        self.btn_import.pack(side="right")
        self.btn_cancel = ctk.CTkButton(self.footer, text="Đóng", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy)
        self.btn_cancel.pack(side="right", padx=10)

    def _start_import(self):
        text = self.txt_input.get("1.0", tk.END).strip()
        reqs = self.txt_reqs.get("1.0", tk.END).strip()
        if not text: return
        
        raw_terms = [t.strip() for t in text.split("\n") if t.strip()]
        terms = list(dict.fromkeys(raw_terms))
        if not terms: return
        
        self.btn_import.configure(state="disabled"); self.txt_input.configure(state="disabled"); self.txt_reqs.configure(state="disabled")
        
        # Save reqs for this domain
        config_manager = getattr(self.master, 'config_manager', None)
        if config_manager:
            config_manager.save_domain_prompt(self.domain, reqs)

        self.spinner.start("AI đang dịch thuật ngữ với các quy tắc bổ sung...")
        threading.Thread(target=self._run_translation, args=(terms, reqs), daemon=True).start()

    def _run_translation(self, terms, reqs):
        try:
            # Implement local failover for batch translation
            import random
            from src.services.gemini_client import GeminiClient
            from src.services.openai_client import OpenAIClient
            
            # Note: We need config_manager here, but master (GlossaryManagerWindow) has it.
            config_manager = getattr(self.master, 'config_manager', None)
            if not config_manager:
                # Fallback to the passed ai_client if no config_manager for failover
                res = self.ai_client.translate_batch(terms, domain=self.domain, additional_reqs=reqs)
                self.after(0, self._process_results, res)
                return

            config = config_manager.load_api_config()
            available_keys = [k for k in config.get("keys", []) if k.get("is_enabled", True)]
            if not available_keys:
                active_id = config.get("active_id")
                available_keys = [k for k in config.get("keys", []) if k["id"] == active_id]
            random.shuffle(available_keys)
            
            res = None
            last_err = "No API keys"
            
            for k_data in available_keys:
                try:
                    if k_data["provider"] == "gemini":
                        client = GeminiClient(api_key=k_data["key"], model_name=k_data["model"])
                    else:
                        client = OpenAIClient(api_key=k_data["key"], model_name=k_data["model"])
                    
                    res = client.translate_batch(terms, domain=self.domain, additional_reqs=reqs)
                    break
                except Exception as e:
                    last_err = str(e)
                    logger.warning(f"Bulk API Key {k_data.get('name')} failed: {e}. Trying next...")
                    continue
            
            if res is None: raise Exception(last_err)
            self.after(0, self._process_results, res)
        except Exception as e:
            logger.error(f"Bulk import error: {e}")
            self.after(0, lambda err=e: self._handle_error(str(err)))

    def _process_results(self, translated_map):
        self.spinner.stop()
        
        existing = self.repo.get_terms()
        to_add, to_resolve = [], []
        
        for jp, vn in translated_map.items():
            if jp in existing:
                if existing[jp] != vn:
                    to_resolve.append((jp, existing[jp], vn))
                # If existing_vn == vn, we just skip it (no need to add)
            else:
                to_add.append((jp, vn))

        if to_resolve:
            ConflictResolutionWindow(self, conflicts=to_resolve, on_complete=lambda ups: self._finalize_import(to_add, ups))
        else:
            self._finalize_import(to_add, [])

    def _finalize_import(self, added, updated):
        for jp, vn in added + updated: self.repo.add_term(jp, vn)
        self.on_success()
        tk.messagebox.showinfo("Thành công", f"Đã nhập {len(added) + len(updated)} thuật ngữ.", parent=self)
        self.destroy()

    def _clean_input(self):
        """Clean input by splitting by standard and Japanese spaces and taking the last part."""
        import re
        raw_text = self.txt_input.get("1.0", tk.END)
        lines = raw_text.split("\n")
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if not line: 
                continue
            
            # Split by standard space ' ' and Japanese space '　'
            parts = re.split(r'[ \u3000]', line)
            
            # Take the last part and strip it
            val = parts[-1].strip()
            if val:
                cleaned_lines.append(val)
            
        # De-duplicate while keeping order
        unique_lines = list(dict.fromkeys(cleaned_lines))
        
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.insert("1.0", "\n".join(unique_lines).strip())

    def _handle_error(self, msg):
        self.spinner.stop()
        self.btn_import.configure(state="normal"); self.txt_input.configure(state="normal"); self.txt_reqs.configure(state="normal")
        tk.messagebox.showerror("Lỗi AI", msg, parent=self)
        self.lift(); self.focus_set()
