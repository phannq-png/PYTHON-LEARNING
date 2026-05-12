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
from src.ui.components.tooltip import add_tooltip

logger = logging.getLogger(__name__)


class QuickAddGlossaryDialog(ctk.CTkToplevel):
    """Small dialog to add a term with domain selection."""

    def __init__(self, master, jp_text, domains, current_domain, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Thêm thuật ngữ nhanh")
        self.geometry("400x320")
        self.result = None

        self.after(10, self.lift)
        self.focus_set(); self.grab_set()

        self.grid_columnconfigure(0, weight=1)

        # JP Term (Read-only or Label)
        ctk.CTkLabel(self, text="Tiếng Nhật:", font=ctk.CTkFont(weight="bold")).pack(pady=(20, 5), padx=20, anchor="w")
        self.lbl_jp = ctk.CTkLabel(self, text=jp_text, fg_color=("gray90", "gray25"), corner_radius=6, height=32, anchor="w")
        self.lbl_jp.pack(fill="x", padx=20)
        self.jp_text = jp_text

        # VN Term
        ctk.CTkLabel(self, text="Bản dịch tiếng Việt:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.ent_vn = ctk.CTkEntry(self, placeholder_text="Nhập nghĩa tiếng Việt...")
        self.ent_vn.pack(fill="x", padx=20)
        self.ent_vn.focus_set()

        # Domain Selection
        ctk.CTkLabel(self, text="Lưu vào lĩnh vực:", font=ctk.CTkFont(weight="bold")).pack(pady=(15, 5), padx=20, anchor="w")
        self.cmb_domain = ctk.CTkComboBox(self, values=domains)
        self.cmb_domain.pack(fill="x", padx=20)
        self.cmb_domain.set(current_domain)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=25)

        self.btn_save = ctk.CTkButton(btn_frame, text="Lưu", fg_color=c.COLOR_PRIMARY, command=self._on_save)
        self.btn_save.pack(side="right")

        self.btn_cancel = ctk.CTkButton(btn_frame, text="Hủy", fg_color="gray30", command=self.destroy)
        self.btn_cancel.pack(side="right", padx=10)

    def _on_save(self):
        vn = self.ent_vn.get().strip()
        if not vn:
            tk.messagebox.showwarning("Cảnh báo", "Vui lòng nhập bản dịch tiếng Việt.", parent=self)
            return
        
        self.result = {
            "jp": self.jp_text,
            "vn": vn,
            "domain": self.cmb_domain.get()
        }
        self.destroy()


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
        add_tooltip(self.btn_delete, "Xóa thuật ngữ này")

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
        active_domain: str = "common",
        data_dir: str = "data",
        on_change_callback: Optional[Callable[[], None]] = None,
        has_session: bool = False,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.title("Quản lý Thuật ngữ")
        self.geometry("900x650")
        self.ai_client = ai_client
        self.config_manager = getattr(master, 'config_manager', None)
        self.active_domain = active_domain
        self.data_dir = data_dir
        self.on_change_callback = on_change_callback
        self.has_session = has_session
        
        self.after(10, self.lift)
        self.focus_set()

        self.repos: Dict[str, GlossaryRepository] = {}
        self._load_available_domains()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_tabs()
        
    def _load_available_domains(self):
        # Only load 'common' and the currently active domain
        self.repos["common"] = GlossaryRepository("common", self.data_dir)
        if self.active_domain and self.active_domain.lower() != "common":
            self.repos[self.active_domain] = GlossaryRepository(self.active_domain, self.data_dir)

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
        add_tooltip(self.btn_add, "Thêm một cặp thuật ngữ mới thủ công")

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
        add_tooltip(self.btn_bulk_import, "Tự động trích xuất thuật ngữ từ văn bản bằng AI")

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
        add_tooltip(self.btn_export, "Xuất danh sách thuật ngữ ra file CSV")

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
        add_tooltip(self.btn_import, "Nhập danh sách thuật ngữ từ file CSV")

    def _build_tabs(self):
        if not self.has_session:
            self._build_empty_state(no_session=True)
            return

        if len(self.repos) <= 1 and self.active_domain.lower() == "common":
            self._build_empty_state(no_session=False)
            return

        self.tabview = ctk.CTkTabview(self, corner_radius=c.CORNER_RADIUS)
        self.tabview.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.tabview._segmented_button.configure(font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=12, weight="bold"))
        
        self.tab_frames = {}
        # Ensure common is first
        domains = ["common"]
        if self.active_domain.lower() != "common":
            domains.append(self.active_domain)

        for domain in domains:
            if domain in self.repos:
                self.tabview.add(domain)
                self._build_domain_tab(domain)

    def _build_empty_state(self, no_session: bool = False):
        """Show message when no specialized domain is selected or no session exists."""
        self.empty_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.empty_frame.grid(row=1, column=0, sticky="nsew")
        
        if no_session:
            msg = (
                "Bạn chưa tải lên tài liệu nào.\n\n"
                "Vui lòng quay lại màn hình chính và tải lên tài liệu (Docx)\n"
                "để bắt đầu quản lý thuật ngữ theo ngữ cảnh."
            )
        else:
            msg = (
                "Bạn chưa chọn lĩnh vực chuyên ngành nào.\n\n"
                "Để quản lý thuật ngữ chuyên ngành, vui lòng quay lại màn hình chính,\n"
                "chọn một lĩnh vực trong danh sách hoặc sử dụng tính năng nhận diện (✨).\n"
                "Sau đó mới quay lại đây để chỉnh sửa."
            )
        
        lbl = ctk.CTkLabel(
            self.empty_frame, 
            text=msg,
            font=ctk.CTkFont(size=16),
            text_color="gray60",
            justify="center"
        )
        lbl.place(relx=0.5, rely=0.4, anchor="center")
        
        btn_back = ctk.CTkButton(
            self.empty_frame,
            text="Đã hiểu, quay lại",
            command=self.destroy,
            fg_color=c.COLOR_PRIMARY,
            corner_radius=c.CORNER_RADIUS
        )
        btn_back.place(relx=0.5, rely=0.55, anchor="center")

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

        # Delete All Button
        self.btn_clear_all = ctk.CTkButton(
            header,
            text="Xóa tất cả",
            width=100,
            height=24,
            corner_radius=c.CORNER_RADIUS,
            fg_color=c.COLOR_DANGER,
            hover_color="#C42B1C",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=11, weight="bold"),
            command=lambda d=domain: self._delete_all_terms(d)
        )
        self.btn_clear_all.grid(row=0, column=2, padx=5, sticky="e")
        add_tooltip(self.btn_clear_all, "Xóa sạch toàn bộ thuật ngữ của lĩnh vực này")

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
                tk.messagebox.showerror("Lỗi", f"Thuật ngữ '{jp_term}' đã tồn tại.", parent=self)
                self.lift(); self.focus_set()
                return
            dialog_vn = ctk.CTkInputDialog(text=f"Nhập bản dịch tiếng Việt cho '{jp_term}':", title="Thêm thuật ngữ")
            vn_term = dialog_vn.get_input()
            if vn_term is not None:
                self.repos[current_domain].add_term(jp_term, vn_term.strip())
                self._refresh_domain_terms(current_domain); self._notify_change()

    def _delete_term(self, domain: str, jp_term: str):
        if tk.messagebox.askyesno("Xác nhận", f"Xóa thuật ngữ '{jp_term}'?", parent=self):
            if self.repos[domain].delete_term(jp_term):
                self._refresh_domain_terms(domain); self._notify_change()

    def _delete_all_terms(self, domain: str):
        """Delete all terms in the specified domain with confirmation."""
        msg = f"⚠️ Bạn có chắc chắn muốn xóa TOÀN BỘ thuật ngữ trong lĩnh vực '{domain}' không?\n\nHành động này không thể hoàn tác."
        if tk.messagebox.askyesno("XÁC NHẬN XÓA TẤT CẢ", msg, parent=self):
            self.repos[domain].clear_all_terms()
            self._refresh_domain_terms(domain)
            self._notify_change()
        self.lift(); self.focus_set()

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
        file_path = tk.filedialog.askopenfilename(title="Chọn file CSV", filetypes=[("CSV Files", "*.csv")], parent=self)
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
            tk.messagebox.showinfo("Thành công", f"Đã import {added_count} thuật ngữ.", parent=self)
        except Exception as e: tk.messagebox.showerror("Lỗi", str(e), parent=self)
        self.lift(); self.focus_set()

    def _export_csv(self):
        domain = self.tabview.get()
        file_path = tk.filedialog.asksaveasfilename(title="Lưu file CSV", defaultextension=".csv", initialfile=f"glossary_{domain}.csv", parent=self)
        if not file_path: return
        try:
            terms = self.repos[domain].get_terms()
            with open(file_path, mode='w', encoding='utf-8-sig', newline='') as f:
                writer = csv.writer(f); writer.writerow(["JP_Term", "VN_Term"])
                for jp, vn in terms.items(): writer.writerow([jp, vn])
            tk.messagebox.showinfo("Thành công", f"Đã export lĩnh vực {domain}.", parent=self)
        except Exception as e: tk.messagebox.showerror("Lỗi", str(e), parent=self)
        self.lift(); self.focus_set()

    def _open_bulk_import(self):
        domain = self.tabview.get()
        BulkImportWindow(self, repo=self.repos[domain], ai_client=self.ai_client,
                        domain=domain,
                        on_success=lambda: self._refresh_domain_terms(domain))
