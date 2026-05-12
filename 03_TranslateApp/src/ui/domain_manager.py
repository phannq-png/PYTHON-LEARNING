"""UI for managing glossary domains (Add/Rename/Delete)."""

import tkinter as tk
from typing import Callable, Optional
import customtkinter as ctk

from src.data.glossary_repo import GlossaryRepository
from src.utils import constants as c
from src.ui.components.tooltip import add_tooltip

class DomainRow(ctk.CTkFrame):
    """A row representing a single domain in the manager."""
    def __init__(self, master, domain_name, on_rename, on_delete, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        self.domain_name = domain_name
        
        self.grid_columnconfigure(0, weight=1)
        
        # Domain Name
        lbl_name = ctk.CTkLabel(self, text=domain_name, font=ctk.CTkFont(weight="bold"), anchor="w")
        lbl_name.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        # Restriction: Common cannot be renamed or deleted
        is_common = (domain_name.lower() == "common")
        
        # Rename Button
        btn_rename = ctk.CTkButton(
            self, text="✎", width=32, 
            fg_color=("gray80", "gray30"), text_color=("black", "white"),
            state="disabled" if is_common else "normal",
            command=lambda: on_rename(domain_name)
        )
        btn_rename.grid(row=0, column=1, padx=2)
        add_tooltip(btn_rename, "Đổi tên lĩnh vực")
        
        # Delete Button
        btn_delete = ctk.CTkButton(
            self, text="✕", width=32, 
            fg_color=c.COLOR_DANGER, hover_color="#C42B1C",
            state="disabled" if is_common else "normal",
            command=lambda: on_delete(domain_name)
        )
        btn_delete.grid(row=0, column=2, padx=2)
        add_tooltip(btn_delete, "Xóa lĩnh vực này")

class DomainManagerWindow(ctk.CTkToplevel):
    """Toplevel window for managing domains."""

    def __init__(self, master, on_change: Optional[Callable[[], None]] = None, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Quản lý lĩnh vực chuyên ngành")
        self.geometry("500x600")
        self.on_change = on_change
        
        self.after(10, self.lift)
        self.focus_set(); self.grab_set()
        
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)
        
        self._build_ui()
        self._refresh_list()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        
        ctk.CTkLabel(header, text="Danh sách Lĩnh vực", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        self.btn_add = ctk.CTkButton(
            header, text="+ Thêm lĩnh vực", 
            fg_color=c.COLOR_PRIMARY,
            command=self._on_add_domain
        )
        self.btn_add.pack(side="right")
        add_tooltip(self.btn_add, "Thêm một chuyên ngành mới")

        # List Area
        self.scroll_frame = ctk.CTkScrollableFrame(self, corner_radius=c.CORNER_RADIUS)
        self.scroll_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        # Footer
        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        ctk.CTkButton(footer, text="Đóng", fg_color="gray30", command=self.destroy).pack(side="right")

    def _refresh_list(self):
        for child in self.scroll_frame.winfo_children(): child.destroy()
        
        domains = GlossaryRepository("common").get_all_domains()
        for i, name in enumerate(domains):
            row = DomainRow(self.scroll_frame, name, on_rename=self._on_rename, on_delete=self._on_delete)
            row.grid(row=i, column=0, sticky="ew", pady=2)

    def _on_add_domain(self):
        dialog = ctk.CTkInputDialog(text="Nhập tên lĩnh vực mới:", title="Thêm lĩnh vực")
        name = dialog.get_input()
        if name:
            name = name.strip()
            if not name: return
            try:
                # Simply initializing a repo creates the file
                GlossaryRepository(name)
                self._refresh_list()
                if self.on_change: self.on_change()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", str(e), parent=self)

    def _on_rename(self, old_name):
        dialog = ctk.CTkInputDialog(text=f"Đổi tên lĩnh vực '{old_name}' thành:", title="Đổi tên lĩnh vực")
        new_name = dialog.get_input()
        if new_name:
            new_name = new_name.strip()
            if not new_name or new_name == old_name: return
            try:
                GlossaryRepository.rename_domain(old_name, new_name)
                self._refresh_list()
                if self.on_change: self.on_change()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", str(e), parent=self)

    def _on_delete(self, name):
        # Check if domain has terms
        repo = GlossaryRepository(name)
        terms = repo.get_terms()
        
        msg = f"Bạn có chắc chắn muốn xóa lĩnh vực '{name}' không?"
        if terms:
            msg = f"⚠️ CẢNH BÁO: Lĩnh vực '{name}' đang chứa {len(terms)} thuật ngữ.\n\n" + msg
            
        if tk.messagebox.askyesno("Xác nhận xóa", msg, parent=self):
            try:
                GlossaryRepository.delete_domain(name)
                self._refresh_list()
                if self.on_change: self.on_change()
            except Exception as e:
                tk.messagebox.showerror("Lỗi", str(e), parent=self)
