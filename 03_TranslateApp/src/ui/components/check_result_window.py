"""Window to display consistency check results (Polished)."""

from typing import Dict, List, Any

import customtkinter as ctk
from src.utils import constants as c


class CheckResultWindow(ctk.CTkToplevel):
    """Polished toplevel window for displaying term mismatches."""

    def __init__(self, master, mismatches, page_number, **kwargs):
        super().__init__(master, **kwargs)
        self.title(f"Kiểm tra Tính nhất quán - Trang {page_number}")
        self.geometry("700x500")

        self.after(10, self.lift); self.focus_set(); self.grab_set()
        self.grid_columnconfigure(0, weight=1); self.grid_rowconfigure(1, weight=1)

        # Header status
        status_color = c.COLOR_SUCCESS if not mismatches else c.COLOR_DANGER
        status_text = "✅ Tất cả thuật ngữ đều nhất quán!" if not mismatches else f"⚠️ Tìm thấy {len(mismatches)} trường hợp không khớp"
        
        self.lbl_status = ctk.CTkLabel(
            self,
            text=status_text,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=15, weight="bold"),
            text_color=status_color
        )
        self.lbl_status.grid(row=0, column=0, padx=25, pady=25, sticky="w")

        if mismatches: self._build_mismatch_table(mismatches)
        else: self._build_success_view()

        # Footer
        btn_close = ctk.CTkButton(self, text="Đóng", corner_radius=c.CORNER_RADIUS, command=self.destroy)
        btn_close.grid(row=2, column=0, padx=25, pady=20, sticky="e")

    def _build_mismatch_table(self, mismatches):
        table_frame = ctk.CTkFrame(self, fg_color="transparent")
        table_frame.grid(row=1, column=0, padx=25, sticky="nsew")
        table_frame.grid_columnconfigure((0, 1), weight=2); table_frame.grid_columnconfigure((2, 3), weight=1)

        f_h = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_SMALL, weight="bold")
        headers = ["THUẬT NGỮ", "BẢN DỊCH", "NGUỒN", "DỊCH"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(table_frame, text=h, font=f_h, text_color="gray50").grid(row=0, column=i, sticky="w", padx=5)

        scroll_frame = ctk.CTkScrollableFrame(table_frame, corner_radius=c.CORNER_RADIUS)
        scroll_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", pady=(10, 0))
        scroll_frame.grid_columnconfigure((0, 1), weight=2); scroll_frame.grid_columnconfigure((2, 3), weight=1)

        f_b = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY)
        f_b_bold = ctk.CTkFont(family=c.FONT_FAMILY[0], size=c.FONT_SIZE_BODY, weight="bold")
        
        for i, m in enumerate(mismatches):
            ctk.CTkLabel(scroll_frame, text=m["jp_term"], font=ctk.CTkFont(family=c.FONT_FAMILY[2], size=c.FONT_SIZE_BODY)).grid(row=i, column=0, sticky="w", padx=5, pady=3)
            ctk.CTkLabel(scroll_frame, text=m["vn_term"], font=f_b).grid(row=i, column=1, sticky="w", padx=5, pady=3)
            ctk.CTkLabel(scroll_frame, text=str(m["jp_count"]), font=f_b, text_color=c.COLOR_PRIMARY).grid(row=i, column=2, sticky="", pady=3)
            ctk.CTkLabel(scroll_frame, text=str(m["vn_count"]), font=f_b_bold, text_color=c.COLOR_DANGER).grid(row=i, column=3, sticky="", pady=3)

    def _build_success_view(self):
        ctk.CTkLabel(
            self,
            text="Hệ thống đã rà soát toàn bộ glossary và không phát hiện sự sai lệch nào. Bản dịch của bạn hoàn toàn nhất quán với thuật ngữ chuyên ngành.",
            wraplength=600, justify="left", font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=13), text_color="gray60"
        ).grid(row=1, column=0, padx=40, pady=20, sticky="nw")
