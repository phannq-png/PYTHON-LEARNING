# Task P3-EXPORT-001: Chức năng Export sang DOCX

## Metadata
- **Task ID**: P3-EXPORT-001
- **Priority**: MEDIUM
- **Phase**: 3
- **Estimated Effort**: L
- **Dependencies**: P1-DOC-001, P2-SESS-001
- **Status**: opening

## Mô tả

### Mục đích
Xây dựng chức năng cho phép người dùng export bản dịch ra file DOCX, với tùy chọn chỉ xuất các trang đã dịch hoặc xuất phiên bản song ngữ, đồng thời áp dụng lại định dạng gốc.

### Phạm vi
**Làm:**
- [ ] Tạo một cửa sổ dialog `ExportWindow` với các tùy chọn:
    - [ ] Checkbox "Chỉ export các trang đã dịch".
    - [ ] Checkbox "Export phiên bản song ngữ".
    - [ ] Nút "Export" để mở file save dialog và bắt đầu quá trình.
- [ ] Tạo class `DocxExporter`.
- [ ] Implement logic export tiêu chuẩn (chỉ tiếng Việt):
    - Dựa trên `format_metadata` đã lưu từ `DocProcessor`, tạo một tài liệu DOCX mới.
    - Áp dụng lại font, size, color, bold/italic, tables, lists cho văn bản tiếng Việt.
- [ ] Implement logic export song ngữ:
    - Với mỗi đoạn, ghi đoạn tiếng Nhật gốc, sau đó ghi đoạn tiếng Việt đã dịch.
    - Áp dụng định dạng gốc cho cả hai.
- [ ] Hiển thị progress bar trong quá trình export.

**KHÔNG làm:**
- Export ra các định dạng khác ngoài DOCX (PDF, HTML, v.v.).

### Acceptance Criteria
- [ ] AC1: Export thành công file DOCX chỉ chứa tiếng Việt với định dạng (màu sắc, font, bảng) được giữ nguyên.
- [ ] AC2: Tùy chọn "Chỉ export các trang đã dịch" hoạt động đúng, bỏ qua các trang chưa dịch.
- [ ] AC3: Export thành công file DOCX song ngữ, với các cặp đoạn văn JP/VN xen kẽ.
- [ ] AC4: File DOCX được tạo ra có thể mở được bằng Microsoft Word hoặc các trình đọc tương thích.

### Technical Notes
- Cần tái sử dụng `format_metadata` đã được tạo bởi `DocProcessor` ở Phase 1.
- Logic tái tạo bảng và danh sách (bullets/numbering) có thể phức tạp và cần test kỹ.
- Thư viện `python-docx` sẽ là công cụ chính để tạo file DOCX.

## Implementation Guide

### Input
- `session_data` (dict): Toàn bộ dữ liệu của phiên làm việc hiện tại, bao gồm:
  - Mảng các trang (với text JP/VN).
  - `format_metadata` (thông tin định dạng gốc).
- `export_options` (dict): Các tùy chọn từ `ExportWindow`.
  - `only_translated` (bool)
  - `bilingual` (bool)

### Output
- Một file `.docx` được lưu vào vị trí do người dùng chọn.

### Algorithm/Logic
1.  **UI**: Nút "Export" trên Top Bar mở `ExportWindow`.
2.  Người dùng chọn tùy chọn và nhấn "Export". Một `filedialog.asksaveasfilename` được hiển thị để chọn vị trí lưu.
3.  **Exporter Logic**:
    - `DocxExporter` nhận `session_data` và `export_options`.
    - Tạo một đối tượng `docx.Document` mới.
    - Lọc danh sách các trang cần export dựa trên `export_options['only_translated']`.
    - Duyệt qua từng `paragraph` trong các trang đã lọc.
    - Lấy `style_info` tương ứng từ `format_metadata`.
    - **If not bilingual**:
        - Thêm đoạn văn bản tiếng Việt vào document.
        - Áp dụng style (font, color, size, bold, italic) cho đoạn văn đó.
    - **If bilingual**:
        - Thêm đoạn văn tiếng Nhật, áp dụng style.
        - Thêm đoạn văn tiếng Việt, áp dụng style.
    - Logic đặc biệt để tái tạo lại `tables` và `lists` từ `format_metadata`.
4.  Lưu file: `document.save(output_path)`.
5.  Hiển thị thông báo export thành công.

### Libraries Required
- `customtkinter` (cho UI dialog).
- `python-docx`

### Error Handling
| Lỗi | Xử lý |
|------|-------|
| Lỗi quyền ghi file | Hiển thị `CTkMessagebox` báo lỗi "Không thể ghi file tại vị trí đã chọn". |
| `format_metadata` bị thiếu hoặc hỏng | Hiển thị `CTkMessagebox` báo lỗi "Dữ liệu định dạng gốc bị lỗi, không thể export". |
| Quá trình export thất bại | Hiển thị `CTkMessagebox` báo lỗi chung và ghi chi tiết vào log. |

## Testing Checklist

### Unit Tests
- [ ] Test logic lọc trang với tùy chọn `only_translated`.
- [ ] Test hàm áp dụng style cho một đoạn văn (mock `python-docx`).
- [ ] Test logic tái tạo một bảng đơn giản.

### Integration Tests
- [ ] Test toàn bộ luồng: Mở session -> Dịch vài trang -> Mở Export Dialog -> Export -> Kiểm tra file output.
- [ ] Test với một session có `format_metadata` phức tạp (nhiều màu, bảng, list).

### Manual Testing
- [ ] Chuẩn bị một file DOCX gốc phức tạp.
- [ ] Dịch toàn bộ, sau đó export với cả 2 chế độ (tiêu chuẩn và song ngữ).
- [ ] So sánh file export với file gốc để đánh giá mức độ giữ lại định dạng.
- [ ] Thử export khi chưa dịch trang nào (với tùy chọn `only_translated` được bật và tắt).
- [ ] Thử lưu file vào một thư mục không có quyền ghi.

## References
- REQUIREMENTS_VI.md: Section 4.10, 4.1.1, 4.1.2
