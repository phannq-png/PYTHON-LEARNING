"""UI components for domain detection suggestions (Polished)."""

import customtkinter as ctk
from src.utils import constants as c


class DomainSuggestionWindow(ctk.CTkToplevel):
    """Polished popup window to suggest a new domain."""

    def __init__(self, master, suggested_name, on_confirm, **kwargs):
        super().__init__(master, **kwargs)
        self.title("✨ Gợi ý Lĩnh vực")
        self.geometry("450x280")
        self.suggested_name = suggested_name
        self.on_confirm = on_confirm

        self.after(10, self.lift); self.focus_set(); self.grab_set()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)

        self._build_ui()

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, padx=25, pady=25, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        f_h = ctk.CTkFont(family=c.FONT_FAMILY[0], size=15, weight="bold")
        ctk.CTkLabel(container, text="✨ AI Phát hiện Lĩnh vực", font=f_h, text_color=c.COLOR_AI).grid(row=0, column=0, pady=(0, 15), sticky="w")

        msg = (
            f"Dựa trên nội dung tài liệu, AI nhận thấy nó thuộc về lĩnh vực:\n\n"
            f"   💠  '{self.suggested_name.upper()}'\n\n"
            "Bạn có muốn tạo và áp dụng bộ thuật ngữ mới cho lĩnh vực này?"
        )
        ctk.CTkLabel(container, text=msg, justify="left", font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=12), wraplength=400).grid(row=1, column=0, pady=10, sticky="w")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=25, pady=20, sticky="ew")

        ctk.CTkButton(btn_frame, text="Tạo & Áp dụng", fg_color=c.COLOR_AI, hover_color="#8E44AD", corner_radius=c.CORNER_RADIUS, font=ctk.CTkFont(family=c.FONT_FAMILY[0], weight="bold"), command=self._handle_confirm).pack(side="right")
        ctk.CTkButton(btn_frame, text="Bỏ qua", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy).pack(side="right", padx=10)

    def _handle_confirm(self):
        self.on_confirm(self.suggested_name); self.destroy()
