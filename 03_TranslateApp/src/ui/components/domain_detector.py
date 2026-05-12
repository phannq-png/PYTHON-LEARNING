"""UI components for domain detection suggestions (Polished)."""

import customtkinter as ctk
from src.utils import constants as c


class DomainSuggestionWindow(ctk.CTkToplevel):
    """Polished popup window to suggest a new or existing domain."""

    def __init__(self, master, suggested_name, on_confirm, is_existing=False, **kwargs):
        super().__init__(master, **kwargs)
        self.title("✨ Gợi ý Lĩnh vực")
        self.geometry("450x300")
        self.suggested_name = suggested_name
        self.on_confirm = on_confirm
        self.is_existing = is_existing

        self.after(10, self.lift); self.focus_set(); self.grab_set()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(0, weight=1)

        self._build_ui()
        self._center_window()

    def _center_window(self):
        """Center the popup relative to the master window using fixed dimensions."""
        self.update_idletasks()
        
        # Dimensions set in __init__
        my_w = 450
        my_h = 300
        
        # Get master (AppWindow) position and size
        parent_x = self.master.winfo_rootx()
        parent_y = self.master.winfo_rooty()
        parent_w = self.master.winfo_width()
        parent_h = self.master.winfo_height()
        
        # Calculate center
        x = parent_x + (parent_w // 2) - (my_w // 2)
        y = parent_y + (parent_h // 2) - (my_h // 2)
        
        # Apply geometry: width x height + x + y
        self.geometry(f"{my_w}x{my_h}+{x}+{y}")

    def _build_ui(self):
        container = ctk.CTkFrame(self, fg_color="transparent")
        container.grid(row=0, column=0, padx=25, pady=25, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        f_h = ctk.CTkFont(family=c.FONT_FAMILY[0], size=15, weight="bold")
        title_text = "✨ AI Phát hiện Lĩnh vực"
        ctk.CTkLabel(container, text=title_text, font=f_h, text_color=c.COLOR_AI).grid(row=0, column=0, pady=(0, 15), sticky="w")

        if self.is_existing:
            msg = (
                f"Dựa trên nội dung tài liệu, AI nhận thấy nó thuộc về lĩnh vực đã có sẵn:\n\n"
                f"   💠  '{self.suggested_name.upper()}'\n\n"
                "Bạn có muốn áp dụng lĩnh vực này cho phiên làm việc hiện tại không?"
            )
            confirm_text = "Áp dụng ngay"
        else:
            msg = (
                f"Dựa trên nội dung tài liệu, AI nhận thấy nó thuộc về lĩnh vực mới:\n\n"
                f"   💠  '{self.suggested_name.upper()}'\n\n"
                "Bạn có muốn tạo và áp dụng bộ thuật ngữ mới cho lĩnh vực này?"
            )
            confirm_text = "Tạo & Áp dụng"

        ctk.CTkLabel(container, text=msg, justify="left", font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=12), wraplength=400).grid(row=1, column=0, pady=10, sticky="w")

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.grid(row=1, column=0, padx=25, pady=20, sticky="ew")

        ctk.CTkButton(btn_frame, text=confirm_text, fg_color=c.COLOR_AI, hover_color="#8E44AD", corner_radius=c.CORNER_RADIUS, font=ctk.CTkFont(family=c.FONT_FAMILY[0], weight="bold"), command=self._handle_confirm).pack(side="right")
        ctk.CTkButton(btn_frame, text="Bỏ qua", fg_color="gray30", corner_radius=c.CORNER_RADIUS, command=self.destroy).pack(side="right", padx=10)

    def _handle_confirm(self):
        self.on_confirm(self.suggested_name); self.destroy()
