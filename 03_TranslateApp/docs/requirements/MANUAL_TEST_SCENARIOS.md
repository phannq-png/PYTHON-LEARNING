# KỊCH BẢN KIỂM THỬ THỦ CÔNG (MANUAL TEST SCENARIOS)
## Dự án: TranslatorApp

Tài liệu này hướng dẫn chi tiết các bước kiểm thử thủ công để đảm bảo ứng dụng đáp ứng đầy đủ các yêu cầu trong `REQUIREMENTS_VI.md`.

---

## 1. Kiểm thử Xử lý Tài liệu (Section 4.1)

### TS-DOC-01: Giữ nguyên định dạng cơ bản
- **Mục tiêu**: Xác nhận Font, Size, Color, Bold, Italic được giữ nguyên.
- **Dữ liệu mẫu**: File `test_format.docx` chứa văn bản nhiều màu, kích thước khác nhau.
- **Các bước**:
    1. Mở ứng dụng, nhấn "Upload" và chọn file mẫu.
    2. Quan sát hiển thị ở panel tiếng Nhật.
    3. Nhấn "Translate" (hoặc nhập text giả vào panel tiếng Việt).
    4. Nhấn "Export" và chọn "Export tiêu chuẩn".
    5. Mở file export bằng Word.
- **Kết quả mong đợi**: Định dạng trong file export giống hệt file gốc.

### TS-DOC-02: Xử lý Bảng và Danh sách
- **Mục tiêu**: Xác nhận cấu trúc bảng và bullet points không bị vỡ.
- **Dữ liệu mẫu**: File `test_table_list.docx` chứa bảng phức tạp và danh sách lồng nhau.
- **Các bước**: Tương tự TS-DOC-01.
- **Kết quả mong đợi**: Bảng trong file export có đủ số cột/hàng, nội dung nằm đúng ô. Bullet points giữ đúng ký tự đầu dòng.

---

## 2. Kiểm thử Quản lý Thuật ngữ (Section 4.4)

### TS-GLOS-01: CRUD Thuật ngữ
- **Mục tiêu**: Kiểm tra Thêm, Sửa, Xóa thuật ngữ.
- **Các bước**:
    1. Mở "Glossary Manager".
    2. Nhấn "Add", nhập "システム" -> "Hệ thống", chọn domain "Common".
    3. Tìm thuật ngữ vừa thêm, nhấn "Edit", đổi thành "Hệ thống xử lý".
    4. Nhấn "Delete" để xóa.
- **Kết quả mong đợi**: Dữ liệu cập nhật ngay lập tức trên bảng và không còn tồn tại sau khi xóa.

### TS-GLOS-02: Nhập hàng loạt và Xử lý xung đột
- **Mục tiêu**: Kiểm tra tính năng Bulk Import với dịch AI.
- **Các bước**:
    1. Mở "Bulk Import".
    2. Dán:
       ```
       診断
       治療
       ```
    3. Nhấn "Translate & Import".
    4. Nếu có xung đột (đã có term "診断"), kiểm tra xem dialog Resolution có hiện ra không.
    5. Chọn "Dùng mới" cho một mục và "Giữ cũ" cho mục khác.
- **Kết quả mong đợi**: Tổng kết hiển thị đúng số lượng thêm mới/cập nhật.

---

## 3. Kiểm thử Giao diện và Điều hướng (Section 4.2, 4.3)

### TS-UI-01: Phân trang và Cuộn
- **Mục tiêu**: Kiểm tra logic tạo trang và hành động cuộn.
- **Các bước**:
    1. Upload file dài 20 đoạn văn.
    2. Sử dụng mũi tên ◀ ▶ và Sidebar trái để chuyển trang.
    3. Cuộn panel tiếng Nhật.
- **Kết quả mong đợi**: Mỗi trang hiển thị đúng số đoạn văn (không quá dài). Panel tiếng Nhật và tiếng Việt cuộn độc lập (không đồng bộ).

### TS-UI-02: Sidebar Thuật ngữ và Highlight
- **Mục tiêu**: Kiểm tra hiển thị thuật ngữ active.
- **Các bước**:
    1. Mở một trang có chứa thuật ngữ đã có trong Glossary.
    2. Kiểm tra Sidebar phải có hiện thuật ngữ đó kèm số lần xuất hiện không.
    3. Click vào thuật ngữ trên Sidebar.
- **Kết quả mong đợi**: Văn bản tiếng Nhật được highlight tất cả các lần xuất hiện của từ đó.

---

## 4. Kiểm thử Engine Dịch và Kiểm tra nhất quán (Section 4.6, 4.7)

### TS-TRAN-01: Ép buộc thuật ngữ (Glossary Enforcement)
- **Mục tiêu**: Đảm bảo AI dùng đúng thuật ngữ trong bộ glossary.
- **Các bước**:
    1. Thêm thuật ngữ "猫" -> "Con hổ" (để dễ nhận biết lỗi) vào Common.
    2. Upload trang có chứa từ "猫".
    3. Nhấn "Translate".
- **Kết quả mong đợi**: Bản dịch tiếng Việt phải chứa từ "Con hổ", không phải "Con mèo".

### TS-CONS-01: Check Page
- **Mục tiêu**: Kiểm tra tính nhất quán.
- **Các bước**:
    1. Dịch một trang có chứa 3 từ "システム".
    2. Trong panel tiếng Việt, chỉ gõ "Hệ thống" 2 lần.
    3. Nhấn "Check Page".
- **Kết quả mong đợi**: Popup hiện thông báo tìm thấy 1 trường hợp không khớp (3 vs 2).

---

## 5. Kiểm thử Bảo mật và Cấu hình (Section 4.8)

### TS-SEC-01: Mã hóa API Key
- **Mục tiêu**: Đảm bảo API Key không lưu ở dạng plain text.
- **Các bước**:
    1. Vào API Settings, nhập key giả và nhấn Save.
    2. Mở file `data/config/api_config.json`.
- **Kết quả mong đợi**: File chứa chuỗi đã mã hóa (base64), không đọc được key gốc.

### TS-ERR-01: Mất kết nối mạng
- **Mục tiêu**: Kiểm tra xử lý lỗi API.
- **Các bước**:
    1. Ngắt kết nối internet.
    2. Nhấn "Translate".
- **Kết quả mong đợi**: Ứng dụng không treo, hiện thông báo "Lỗi kết nối mạng" kèm nút Retry.

---

## 6. Kiểm thử Export (Section 4.10)

### TS-EXP-01: Export Song ngữ
- **Mục tiêu**: Kiểm tra định dạng file song ngữ.
- **Các bước**:
    1. Dịch xong 2 trang.
    2. Mở Export dialog, chọn "Export phiên bản song ngữ".
    3. Mở file kết quả.
- **Kết quả mong đợi**: Mỗi đoạn văn bản gốc JP đi kèm ngay dưới là đoạn VN tương ứng.

---
*Tài liệu được soạn thảo bởi Agent BA.*
