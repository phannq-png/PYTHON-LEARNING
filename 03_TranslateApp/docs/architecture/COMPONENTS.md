# DANH MỤC THÀNH PHẦN (COMPONENTS & RESPONSIBILITIES)

Tài liệu này liệt kê chi tiết trách nhiệm của các module chính trong mã nguồn TranslatorApp.

---

## 1. Tầng Trình diễn (UI)

### 🖥️ `src/ui/app_window.py` (The Orchestrator)
- **Trách nhiệm**: Khởi tạo toàn bộ ứng dụng, quản lý trạng thái phiên (session) và điều phối luồng dữ liệu giữa các component con.
- **Tương tác**: Gọi `Core` modules để xử lý, gọi `Services` để dịch, và cập nhật `Data` repositories.

### 📋 `src/ui/term_manager.py`
- **Trách nhiệm**: Cung cấp giao diện quản lý glossary. Hỗ trợ hiển thị tab-based cho nhiều domain.
- **Tương tác**: Sử dụng `GlossaryRepository` trực tiếp cho các thao tác CRUD.

### ✨ `src/ui/bulk_import.py`
- **Trách nhiệm**: Giao diện dịch thuật ngữ hàng loạt. 
- **Tương tác**: Sử dụng `BaseAIClient.translate_batch` để lấy bản dịch từ AI.

---

## 2. Tầng Logic (Core)

### ⚙️ `src/core/doc_processor.py`
- **Trách nhiệm**: Đọc file DOCX, trích xuất text thuần và lưu trữ metadata định dạng (font, color, bold, index).
- **Hành vi**: Chuyển đổi cấu trúc phức tạp của Word sang danh sách các đoạn văn đơn giản.

### ✂️ `src/core/segmenter.py`
- **Trách nhiệm**: Tách danh sách đoạn văn thành các Segment dựa trên cấu hình (hard/soft return, markers) và phân chia chúng vào các trang (Page).

### 💾 `src/core/docx_exporter.py`
- **Trách nhiệm**: Tái tạo file DOCX. Sử dụng metadata để áp dụng lại style cho văn bản tiếng Việt.
- **Đặc biệt**: Xử lý logic chèn đoạn song ngữ (JP/VN stacked).

---

## 3. Tầng Dữ liệu (Data)

### 🔑 `src/data/config_manager.py`
- **Trách nhiệm**: Lưu trữ cấu hình ứng dụng. Sử dụng mã hóa Fernet để bảo vệ API Keys.

### 📁 `src/data/glossary_repo.py`
- **Trách nhiệm**: Lưu trữ thuật ngữ dưới dạng file JSON. Quản lý việc gộp domain (priority rule).

---

## 4. Tầng Dịch vụ (Services)

### 🤖 `src/services/gemini_client.py`
- **Trách nhiệm**: Đóng gói các lời gọi API tới Google Gemini. Thực hiện trích xuất `usage_metadata` (tokens).

---
*Tài liệu được soạn thảo bởi Antigravity Agent.*
