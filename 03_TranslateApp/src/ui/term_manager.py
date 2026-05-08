"""Glossary management UI (Polished)."""

import csv
import logging
import os
import tkinter as tk
from pathlib import Path
from typing import Callable, Dict, List, Optional

import customtkinter as ctk

from src.data.glossary_repo import GlossaryRepository
from src.services.base_client import BaseAIClient
from src.ui.bulk_import import BulkImportWindow
from src.utils import constants as c

logger = logging.getLogger(__name__)


class TermRow(ctk.CTkFrame):
    """A single row in the glossary table with modern styling."""

    def __init__(
        self,
        master: any,
        jp_term: str,
        vn_term: str,
        on_delete: Callable[[str], None],
        on_update: Callable[[str, str, str], None],
        **kwargs
    ):
        super().__init__(
            master, 
            fg_color="transparent", 
            corner_radius=c.CORNER_RADIUS,
            **kwargs
        )
        self.jp_term = jp_term
        self.vn_term = vn_term
        self.on_delete = on_delete
        self.on_update = on_update

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=0)

        # JP Entry
        self.ent_jp = ctk.CTkEntry(
            self, 
            corner_radius=c.CORNER_RADIUS,
            font=ctk.CTkFont(family=c.FONT_FAMILY[2], size=c.FONT_SIZE_BODY),
            border_width=c.BORDER_WIDTH
        )
        self.ent_jp.insert(0, jp_term)
        self.ent_jp.grid(row=0, column=0, padx=(0, 5), pady=2, sticky="ew")
        self.ent_jp.bind("<FocusOut>", self._handle_update)
        self.ent_jp.bind("<Return>", self._handle_update)

        # VN Entry
        self.ent_vn = ctk.CTkEntry(
            self, 
            corner_radius=c.CORNER_RADIUS,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY),
            border_width=c.BORDER_WIDTH
        )
        self.ent_vn.insert(0, vn_term)
        self.ent_vn.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.ent_vn.bind("<FocusOut>", self._handle_update)
        self.ent_vn.bind("<Return>", self._handle_update)

        # Delete Button
        self.btn_delete = ctk.CTkButton(
            self,
            text="✕",
            width=32,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_DANGER,
            hover_color="#C42B1C",
            command=lambda: self.on_delete(self.jp_term)
        )
        self.btn_delete.grid(row=0, column=2, padx=(5, 0), pady=2)

    def _handle_update(self, event=None):
        new_jp = self.ent_jp.get().strip()
        new_vn = self.ent_vn.get().strip()
        if not new_jp:
            self.ent_jp.delete(0, tk.END)
            self.ent_jp.insert(0, self.jp_term)
            return
        if new_jp != self.jp_term or new_vn != self.vn_term:
            self.on_update(self.jp_term, new_jp, new_vn)
            self.jp_term = new_jp
            self.vn_term = new_vn


class GlossaryManagerWindow(ctk.CTkToplevel):
    """Polished toplevel window for managing glossary terms."""

    def __init__(
        self,
        master: any,
        ai_client: BaseAIClient,
        data_dir: str = "data",
        on_change_callback: Optional[Callable[[], None]] = None,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.title("Quản lý Thuật ngữ")
        self.geometry("900x650")
        self.ai_client = ai_client
        self.data_dir = data_dir
        self.on_change_callback = on_change_callback
        
        self.after(10, self.lift)
        self.focus_set()

        self.repos: Dict[str, GlossaryRepository] = {}
        self._load_available_domains()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_tabs()
        
    def _load_available_domains(self):
        glossaries_dir = Path(self.data_dir) / "glossaries"
        os.makedirs(glossaries_dir, exist_ok=True)
        for file in glossaries_dir.glob("*.json"):
            domain = file.stem
            self.repos[domain] = GlossaryRepository(domain, self.data_dir)
        if "common" not in self.repos:
            self.repos["common"] = GlossaryRepository("common", self.data_dir)

    def _build_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        
        f_btn = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY)

        self.btn_add = ctk.CTkButton(
            self.header_frame,
            text="+ Thêm thuật ngữ",
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_PRIMARY,
            font=f_btn,
            command=self._add_new_term
        )
        self.btn_add.pack(side="left", padx=(0, 10))

        # Check if AI is available
        bulk_text = "✨ Bulk Import (AI)"
        bulk_state = "normal"
        if self.ai_client is None:
            bulk_text = "✨ AI (Cần API Key)"
            bulk_state = "disabled"

        self.btn_bulk_import = ctk.CTkButton(
            self.header_frame,
            text=bulk_text,
            state=bulk_state,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_AI,
            font=f_btn,
            command=self._open_bulk_import
        )
        self.btn_bulk_import.pack(side="left", padx=5)

        # Right aligned buttons
        self.btn_export = ctk.CTkButton(
            self.header_frame,
            text="Export CSV",
            corner_radius=c.CORNER_RADIUS,
            fg_color=("gray75", "gray30"),
            text_color=("gray10", "gray90"),
            font=f_btn,
            command=self._export_csv
        )
        self.btn_export.pack(side="right", padx=c.PADDING_STD)

        self.btn_import = ctk.CTkButton(
            self.header_frame,
            text="Import CSV",
            corner_radius=c.CORNER_RADIUS,
            fg_color=("gray75", "gray30"),
            text_color=("gray10", "gray90"),
            font=f_btn,
            command=self._import_csv
        )
        self.btn_import.pack(side="right", padx=c.PADDING_STD)

    def _build_tabs(self):
        self.tabview = ctk.CTkTabview(self, corner_radius=c.CORNER_RADIUS)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.tabview._segmented_button.configure(font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=12, weight="bold"))
        
        self.tab_frames = {}
        sorted_domains = sorted(self.repos.keys())
        if "common" in sorted_domains:
            sorted_domains.remove("common"); sorted_domains.insert(0, "common")

        for domain in sorted_domains:
            self.tabview.add(domain)
            self._build_domain_tab(domain)

    def _build_domain_tab(self, domain: str):
        tab = self.tabview.tab(domain)
        tab.grid_columnconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(tab, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header.grid_columnconfigure((0, 1), weight=1)
        
        f_h = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold")
        ctk.CTkLabel(header, text="TIẾNG NHẬT", font=f_h, text_color="gray50").grid(row=0, column=0, sticky="w", padx=5)
        ctk.CTkLabel(header, text="TIẾNG VIỆT", font=f_h, text_color="gray50").grid(row=0, column=1, sticky="w", padx=5)

        scroll_frame = ctk.CTkScrollableFrame(tab, corner_radius=c.CORNER_RADIUS)
        scroll_frame.grid(row=1, column=0, sticky="nsew")
        scroll_frame.grid_columnconfigure(0, weight=1)
        self.tab_frames[domain] = scroll_frame
        self._refresh_domain_terms(domain)

    def _refresh_domain_terms(self, domain: str):
        scroll_frame = self.tab_frames[domain]
        for child in scroll_frame.winfo_children(): child.destroy()
        terms = self.repos[domain].get_terms()
        for i, (jp, vn) in enumerate(terms.items()):
            row = TermRow(scroll_frame, jp_term=jp, vn_term=vn,
                        on_delete=lambda t, d=domain: self._delete_term(d, t),
                        on_update=lambda old, new_j, new_v, d=domain: self._update_term(d, old, new_j, new_v))
            row.grid(row=i, column=0, sticky="ew", pady=1)

    def _add_new_term(self):
        current_domain = self.tabview.get()
        dialog = ctk.CTkInputDialog(text=f"Nhập thuật ngữ tiếng Nhật:", title="Thêm thuật ngữ")
        jp_term = dialog.get_input()
        if jp_term:
            jp_term = jp_term.strip()
            if jp_term in self.repos[current_domain].get_terms():
                tk.messagebox.showerror("Lỗi", f"Thuật ngữ '{jp_term}' đã tồn tại.")
                return
            dialog_vn = ctk.CTkInputDialog(text=f"Nhập bản dịch tiếng Việt cho '{jp_term}':", title="Thêm thuật ngữ")
            vn_term = dialog_vn.get_input()
            if vn_term is not None:
                self.repos[current_domain].add_term(jp_term, vn_term.strip())
                self._refresh_domain_terms(current_domain); self._notify_change()

    def _delete_term(self, domain: str, jp_term: str):
        if tk.messagebox.askyesno("Xác nhận", f"Xóa thuật ngữ '{jp_term}'?"):
            if self.repos[domain].delete_term(jp_term):
                self._refresh_domain_terms(domain); self._notify_change()

    def _update_term(self, domain: str, old_jp: str, new_jp: str, new_vn: str):
        repo = self.repos[domain]
        if old_jp != new_jp: repo.delete_term(old_jp)
        repo.add_term(new_jp, new_vn)
        self._notify_change()
        if old_jp != new_jp: self._refresh_domain_terms(domain)

    def _notify_change(self):
        if self.on_change_callback: self.on_change_callback()

    def _import_csv(self):
        domain = self.tabview.get()
        file_path = tk.filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV Files", "*.csv")])
        if not file_path: return
        try:
            added_count = 0
            with open(file_path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                header = next(reader, None)
                if header and len(header) < 2: f.seek(0); reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        jp, vn = row[0].strip(), row[1].strip()
                        if jp: self.repos[domain].add_term(jp, vn); added_count += 1
            self._refresh_domain_terms(domain); self._notify_change()
            tk.messagebox.showinfo("Thành công", f"Đã import {added_count} thuật ngữ.")
        except Exception as e: tk.messagebox.showerror("Lỗi", str(e))

    def _export_csv(self):
        domain = self.tabview.get()
        file_path = tk.filedialog.asksaveasfilename(title="Lưu file CSV", defaultextension=".csv", initialfile=f"glossary_{domain}.csv")
        if not file_path: return
        try:
            terms = self.repos[domain].get_terms()
            with open(file_path, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f); writer.writerow(["JP_Term", "VN_Term"])
                for jp, vn in terms.items(): writer.writerow([jp, vn])
            tk.messagebox.showinfo("Thành công", f"Đã export lĩnh vực {domain}.")
        except Exception as e: tk.messagebox.showerror("Lỗi", str(e))

    def _open_bulk_import(self):
        domain = self.tabview.get()
        BulkImportWindow(self, repo=self.repos[domain], ai_client=self.ai_client,
                        on_success=lambda: self._refresh_domain_terms(domain))
