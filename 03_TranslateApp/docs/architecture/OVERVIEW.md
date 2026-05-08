# TỔNG QUAN KIẾN TRÚC (ARCHITECTURE OVERVIEW)
## Dự án: TranslatorApp

Ứng dụng được thiết kế theo mô hình **Kiến trúc Phân lớp (Layered Architecture)** với 4 tầng tách biệt, giúp đảm bảo tính dễ bảo trì và mở rộng.

---

## 1. Các Tầng Kiến trúc

### 1.1 Tầng Trình diễn (Presentation Layer - `src/ui/`)
- **Trách nhiệm**: Hiển thị giao diện, nhận tương tác người dùng và phản hồi trạng thái.
- **Công nghệ**: CustomTkinter (Python wrapper cho Tkinter).
- **Thành phần chính**:
    - `AppWindow`: Container chính điều phối toàn bộ ứng dụng.
    - `CenterPanel`: Vùng làm việc trung tâm (JP/VN text areas).
    - `Sidebars`: Điều hướng và hiển thị thuật ngữ active.
    - `Dialogs`: Các cửa sổ chức năng (Glossary Manager, Bulk Import, Settings).

### 1.2 Tầng Logic Nghiệp vụ (Business Logic Layer - `src/core/`)
- **Trách nhiệm**: Xử lý các quy tắc nghiệp vụ cốt lõi, không phụ thuộc giao diện.
- **Thành phần chính**:
    - `DocumentProcessor`: Trích xuất text và metadata định dạng từ DOCX.
    - `TextSegmenter`: Logic phân đoạn và phân trang văn bản động.
    - `ConsistencyChecker`: Kiểm tra tính nhất quán thuật ngữ.
    - `DocxExporter`: Tái tạo file DOCX từ bản dịch và metadata.
    - `TokenTracker`: Theo dõi và tính toán chi phí API.

### 1.3 Tầng Dịch vụ Bên ngoài (Service Layer - `src/services/`)
- **Trách nhiệm**: Giao tiếp với các API bên ngoài (AI Providers).
- **Thành phần chính**:
    - `BaseAIClient`: Interface chung cho các AI providers.
    - `GeminiClient`: Tích hợp Google Gemini (mặc định).
    - `OpenAIClient`: Tích hợp OpenAI.

### 1.4 Tầng Truy cập Dữ liệu (Data Access Layer - `src/data/`)
- **Trách nhiệm**: Đọc/Ghi dữ liệu xuống hệ thống file (Local Storage).
- **Thành phần chính**:
    - `ConfigManager`: Quản lý cấu hình và mã hóa API Key.
    - `GlossaryRepository`: Quản lý dữ liệu thuật ngữ (JSON/CSV).
    - `SessionManager`: Quản lý lưu trữ tiến độ phiên làm việc.

---

## 2. Các Mẫu Thiết kế (Design Patterns)
- **Singleton-like Access**: `ConfigManager` và các Repository thường được truy cập tập trung.
- **Observer/Callback Pattern**: Sử dụng callbacks để các component con (Sidebars, BottomBar) gửi tín hiệu về `AppWindow`.
- **Strategy Pattern**: `BaseAIClient` cho phép thay đổi nhà cung cấp AI linh hoạt.

---
*Tài liệu được soạn thảo bởi Antigravity Agent.*
