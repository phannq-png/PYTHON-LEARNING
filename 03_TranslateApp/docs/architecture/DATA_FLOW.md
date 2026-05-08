# LUỒNG DỮ LIỆU CHÍNH (PRIMARY DATA FLOW)

Ứng dụng TranslatorApp vận hành qua một quy trình xử lý dữ liệu khép kín gồm 4 bước chính:

---

## 1. Nạp và Phân tích (Ingestion & Analysis)
- **Input**: File `.docx` từ người dùng.
- **Process**:
    - `DocProcessor` quét cây XML của Word.
    - Lưu Text vào một list phẳng.
    - Lưu Formatting (styles) vào list metadata kèm index tương ứng.
    - AI `detect_domain` quét 5000 ký tự đầu để gợi ý domain.
- **Output**: List texts, List metadata, Suggested Domain ID.

## 2. Phân đoạn và Tổ chức (Segmentation & Pagination)
- **Input**: List texts, Cấu hình người dùng.
- **Process**:
    - `TextSegmenter` thực hiện tách đoạn theo regex/markers.
    - Gom các Segment vào các Page dựa trên giới hạn ký tự.
    - `SessionManager` tạo session object (JSON) để duy trì trạng thái.
- **Output**: Session object với cấu trúc trang JP/VN.

## 3. Chuyển đổi AI (AI Transformation)
- **Input**: Page text (JP), Glossary gộp.
- **Process**:
    - `AppWindow` gộp glossary (Domain overrides Common).
    - `GeminiClient` tạo prompt chuyên nghiệp kèm thuật ngữ.
    - API trả về bản dịch và số lượng Token tiêu thụ.
    - `TokenTracker` cập nhật bộ đếm.
- **Output**: Translated text (VN), Token count.

## 4. Tổng hợp và Kết xuất (Synthesis & Export)
- **Input**: Session data (VN texts), Formatting metadata, Template file gốc.
- **Process**:
    - `DocxExporter` mở template file gốc.
    - Ánh xạ bản dịch VN trở lại đúng Paragraph/Table-cell dựa trên metadata index.
    - Áp dụng font `Times New Roman` (hoặc font VN compatible) cùng màu sắc/size gốc.
    - Ghi đè hoặc chèn thêm (song ngữ) vào document.
- **Output**: File `{tên_gốc}_VN.docx`.

---
*Tài liệu được soạn thảo bởi Antigravity Agent.*
