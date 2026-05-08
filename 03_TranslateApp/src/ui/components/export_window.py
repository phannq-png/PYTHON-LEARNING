"""Export options dialog (Polished)."""

import tkinter as tk
from typing import Callable, Dict

import customtkinter as ctk
from src.utils import constants as c


class ExportWindow(ctk.CTkToplevel):
    """Polished dialog for selecting export options."""

    def __init__(self, master, default_filename, on_export, **kwargs):
        super().__init__(master, **kwargs)
        self.title("Export tài liệu")
        self.geometry("450x380")
        self.on_export = on_export
        self.default_filename = default_filename

        self.after(10, self.lift); self.focus_set(); self.grab_set()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(container, text="📤 Tùy chọn Export", font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=16, weight="bold")).grid(row=0, column=0, pady=(0, 20), sticky="w")

        self.var_only_translated = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(container, text="Chỉ export các trang đã dịch", variable=self.var_only_translated, corner_radius=c.CORNER_RADIUS).grid(row=1, column=0, pady=10, sticky="w")

        self.var_bilingual = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(container, text="Export phiên bản song ngữ (JP/VN)", variable=self.var_bilingual, corner_radius=c.CORNER_RADIUS).grid(row=2, column=0, pady=10, sticky="w")

        info_text = "💡 Ghi chú: Định dạng gốc (font, màu sắc, bảng) sẽ được giữ nguyên tối đa có thể."
        ctk.CTkLabel(container, text=info_text, font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=11), text_color="gray60", wraplength=350, justify="left").grid(row=3, column=0, pady=(25, 0), sticky="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=30, pady=20, sticky="ew")
        
        ctk.CTkButton(btn_frame, text="Chọn vị trí & Export", fg_color=c.COLOR_SUCCESS, corner_radius=c.CORNER_RADIUS, font=ctk.CTkFont(family=c.FONT_FAMILY[0], weight="bold"), command=self._handle_export).pack(side="right")
        ctk.CTkButton(btn_frame, text="Hủy", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy).pack(side="right", padx=10)

    def _handle_export(self):
        suffix = "_Bilingual" if self.var_bilingual.get() else "_VN"
        initial_file = self.default_filename.replace(".docx", f"{suffix}.docx")
        file_path = tk.filedialog.asksaveasfilename(title="Lưu file export", initialfile=initial_file, defaultextension=".docx", filetypes=[("Word documents", "*.docx")])
        if not file_path: return
        self.on_export({"only_translated": self.var_only_translated.get(), "bilingual": self.var_bilingual.get()}, file_path)
        self.destroy()
