"""About Window component — displays application information and credits."""

import customtkinter as ctk
from src.utils import constants as c

class AboutWindow(ctk.CTkToplevel):
    """A professional About window for the application."""

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("About TranslatorApp")
        
        # Dimensions
        width = 450
        height = 400
        
        # Center on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)
        self.after(200, self.lift)
        self.attributes("-topmost", True) # Keep on top

        self.grid_columnconfigure(0, weight=1)
        self._build_widgets()

    def _build_widgets(self):
        """Build the about content UI."""
        
        # 1. Header Section (Logo/Name)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(pady=(30, 10))
        
        lbl_logo = ctk.CTkLabel(
            header_frame, 
            text="🚀", 
            font=ctk.CTkFont(size=50)
        )
        lbl_logo.pack()
        
        lbl_name = ctk.CTkLabel(
            header_frame,
            text="TranslatorApp",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=c.COLOR_PRIMARY
        )
        lbl_name.pack()
        
        lbl_version = ctk.CTkLabel(
            header_frame,
            text="Phiên bản v1.2.0",
            font=ctk.CTkFont(size=12),
            text_color="gray50"
        )
        lbl_version.pack()

        # 2. Description Section
        desc_text = (
            "Giải pháp dịch thuật tài liệu chuyên ngành Nhật - Việt\n"
            "tối ưu cho độ chính xác và bảo toàn định dạng."
        )
        lbl_desc = ctk.CTkLabel(
            self,
            text=desc_text,
            font=ctk.CTkFont(size=13),
            justify="center"
        )
        lbl_desc.pack(pady=10, padx=40)

        # 3. Info List
        info_frame = ctk.CTkFrame(self, fg_color=("gray90", "gray20"), corner_radius=10)
        info_frame.pack(pady=10, padx=40, fill="x")
        
        credits = [
            ("Phát triển bởi", "P"),
            ("Hỗ trợ bởi", "Antigravity Agent"),
            ("Công nghệ", "Gemini / OpenAI / CustomTkinter"),
            ("GitHub", "github.com/phannq-png"),
            ("Bản quyền", "© 2026 P. All rights reserved.")
        ]
        
        for label, value in credits:
            row = ctk.CTkFrame(info_frame, fg_color="transparent")
            row.pack(fill="x", padx=15, pady=5)
            
            ctk.CTkLabel(row, text=label, font=ctk.CTkFont(size=11, weight="bold"), text_color="gray50").pack(side="left")
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=11)).pack(side="right")

        # 4. Close Button
        btn_close = ctk.CTkButton(
            self,
            text="Đóng",
            width=100,
            command=self.destroy,
            fg_color="gray30",
            hover_color="gray40"
        )
        btn_close.pack(side="bottom", pady=25)
