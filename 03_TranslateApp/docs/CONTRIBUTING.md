# HƯỚNG DẪN PHÁT TRIỂN (DEVELOPER GUIDE)
## Dự án: TranslatorApp

Chào mừng bạn đến với đội ngũ phát triển TranslatorApp. Tài liệu này cung cấp các thông tin cần thiết để bạn bắt đầu đóng góp cho dự án một cách hiệu quả.

---

## 🏗️ 1. Cấu trúc Thư mục
Dự án tuân theo kiến trúc 4 lớp (Layered Architecture):

- `src/ui/`: Tầng trình diễn (CustomTkinter). Các component UI và Dialogs.
- `src/core/`: Tầng logic nghiệp vụ. Các bộ xử lý DOCX, Segmenter, Exporter.
- `src/services/`: Tầng dịch vụ. Giao tiếp với AI APIs (Gemini, OpenAI).
- `src/data/`: Tầng truy cập dữ liệu. Quản lý Config, Session, Glossary.
- `src/utils/`: Các hàm tiện ích, hằng số style và Logger.
- `docs/`: Toàn bộ tài liệu đặc tả, kiến trúc và release notes.

---

## 🎨 2. Quy chuẩn Code (Coding Standards)

### Ngôn ngữ:
- **Code (Biến, Hàm, Class)**: Tiếng Anh 100%.
- **Comments/Tài liệu**: Tiếng Việt (theo yêu cầu Project Owner).

### Quy tắc Đặt tên:
- Class: `PascalCase` (VD: `AppWindow`, `TextSegmenter`).
- Hàm/Biến: `snake_case` (VD: `_handle_save`, `current_page_idx`).
- Hằng số: `UPPER_SNAKE_CASE` (VD: `COLOR_PRIMARY`).
- Hàm private: Bắt đầu bằng dấu gạch dưới `_`.

---

## 🚀 3. Quy trình Thêm Tính năng Mới

Nếu bạn muốn thêm một tính năng mới (ví dụ: Dịch PDF):
1.  **Phân tích**: Đọc `REQUIREMENTS_VI.md` để đảm bảo không conflict với logic hiện tại.
2.  **Thiết kế**: Cập nhật `docs/architecture/` nếu cấu trúc thay đổi.
3.  **Tạo Task**: Tạo file markdown trong `docs/requirements/[feature-name]/opening/`.
4.  **Triển khai**: 
    - Thêm hằng số vào `src/utils/constants.py` nếu có liên quan đến UI.
    - Implement logic trong `src/core/` trước.
    - Gắn UI vào `src/ui/` sau.
5.  **Kiểm thử**: Chạy `python main.py` và thực hiện theo kịch bản trong `MANUAL_TEST_SCENARIOS.md`.

---

## ⚠️ 4. Các Lưu ý Quan trọng
- **Bảo mật**: Tuyệt đối không commit file `data/config/.secret.key`.
- **UI Consistency**: Luôn sử dụng hằng số từ `src/utils/constants.py` để đảm bảo Dark Mode và Corner Radius 10px đồng nhất.
- **Threading**: Mọi lời gọi API AI phải chạy trong `threading.Thread` để tránh treo giao diện, và cập nhật UI thông qua `self.after(0, callback)`.

---
*Cảm ơn bạn đã đóng góp cho TranslatorApp!*
