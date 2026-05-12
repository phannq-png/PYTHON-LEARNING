"""User Guide window for the TranslatorApp."""

import customtkinter as ctk
from src.utils import constants as c

class UserGuideWindow(ctk.CTkToplevel):
    """A window displaying help and instructions for the application."""

    def __init__(self, master: any, **kwargs):
        super().__init__(master, **kwargs)
        
        self.title("Hướng dẫn sử dụng - TranslatorApp")
        
        # Set dimensions
        width = 700
        height = 750
        
        # Calculate position to center on screen
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        self.after(200, self.lift) # Bring to front
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # ── Header ─────────────────────────────────────────────────────────
        lbl_header = ctk.CTkLabel(
            self,
            text="📖 HƯỚNG DẪN SỬ DỤNG",
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=20, weight="bold"),
            text_color=c.COLOR_PRIMARY
        )
        lbl_header.grid(row=0, column=0, pady=(20, 10))

        # ── Content ────────────────────────────────────────────────────────
        self.txt_content = ctk.CTkTextbox(
            self,
            font=ctk.CTkFont(family=c.FONT_FAMILY[0], size=14),
            padx=20,
            pady=20,
            wrap="word",
            corner_radius=c.CORNER_RADIUS
        )
        self.txt_content.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self._fill_content()
        self.txt_content.configure(state="disabled") # Read-only

    def _fill_content(self):
        guide_text = """
1. GIỚI THIỆU
Ứng dụng hỗ trợ dịch thuật tài liệu DOCX chuyên ngành Nhật-Việt, tích hợp AI (Gemini/OpenAI) và quản lý thuật ngữ thông minh.

2. CÁC BƯỚC CƠ BẢN
• Nạp file: Chọn 'File' -> 'Mở file DOCX...' hoặc nút 'Upload' ở TopBar.
• Chọn lĩnh vực: Chọn chuyên ngành phù hợp ở menu thả xuống để AI sử dụng đúng thuật ngữ.
• Dịch thuật:
  - Dịch trang hiện tại: Nhấn nút 'Dịch Trang' ở BottomBar.
  - Dịch toàn bộ: Nhấn 'Dịch Toàn Bộ' (AI sẽ tự động lật từng trang).
• Kiểm tra (Consistency Check):
  - Nhấn 'Check Page' để quét các lỗi thuật ngữ chưa đồng nhất giữa bản gốc và bản dịch. Các lỗi sẽ hiện màu đỏ ở Sidebar phải.

3. QUẢN LÝ THUẬT NGỮ
• Thêm nhanh: Bôi đen văn bản tiếng Nhật ở ô bên trái, nhấn chuột phải chọn '✨ Thêm vào thuật ngữ'.
• Sidebar phải: Hiển thị các thuật ngữ đang có trong văn bản hiện tại. 
  - Click vào thuật ngữ để highlight vị trí của nó trong văn bản.
  - Click lại lần nữa hoặc nhấn 'Esc' để xóa highlight.

4. TÌM KIẾM TOÀN CỤC (GLOBAL SEARCH)
• Nhập từ khóa vào ô tìm kiếm ở TopBar và nhấn Enter hoặc nút 🔍.
• Kết quả sẽ được highlight màu vàng ở danh sách trang bên trái.

5. PHÍM TẮT & TIỆN ÍCH
• Phím ESC: Xóa toàn bộ highlight tìm kiếm và highlight chọn thuật ngữ.
• Chuột phải: Menu tiện ích giúp tìm kiếm nhanh hoặc thêm thuật ngữ.
• Chuyển trang: Click vào danh sách trang bên trái. Trạng thái trang (Dịch xong/Lỗi) được đánh dấu bằng các chấm màu.

6. XUẤT FILE (EXPORT)
• Sau khi hoàn tất, chọn nút 'Export' ở TopBar.
• Có thể chọn xuất 'Song ngữ' (Nhật-Việt xen kẽ) hoặc 'Chỉ bản dịch'.

---
Cảm ơn bạn đã sử dụng TranslatorApp!
"""
        self.txt_content.insert("1.0", guide_text.strip())
