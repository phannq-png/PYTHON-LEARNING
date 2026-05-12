# Task P3-BULK-001: Chức năng Nhập Hàng loạt với Dịch AI

## Metadata
- **Task ID**: P3-BULK-001
- **Priority**: MEDIUM
- **Phase**: 3
- **Estimated Effort**: L
- **Dependencies**: P3-GLOS-003, P2-API-001
- **Status**: closed

## Mô tả

### Mục đích
Xây dựng chức năng cho phép người dùng nhập hàng loạt thuật ngữ tiếng Nhật, tự động dịch chúng bằng AI, và xử lý xung đột một cách thông minh trước khi thêm vào bộ thuật ngữ.

### Phạm vi
**Làm:**
- [x] Tạo một cửa sổ dialog mới `BulkImportWindow`.
- [x] Giao diện có một `CTkTextbox` lớn để người dùng dán danh sách thuật ngữ (mỗi dòng một thuật ngữ).
- [x] Một nút "Translate & Import" để bắt đầu quá trình.
- [x] Gọi API dịch (ví dụ: Gemini/OpenAI) để dịch toàn bộ danh sách.
- [x] Xử lý kết quả:
    - Thuật ngữ mới: Tự động thêm.
    - Trùng lặp (cùng bản dịch): Bỏ qua.
    - Xung đột (khác bản dịch): Hiển thị dialog `ConflictResolutionWindow` để người dùng quyết định "Giữ cũ" hay "Dùng mới" cho từng trường hợp.
- [x] Hiển thị một dialog tóm tắt kết quả cuối cùng (thêm mới, bỏ qua, cập nhật).
- [x] Cân đối 2 textarea, tránh khoảng trắng không cần thiết.
- [x] Tự động căn giữa cửa sổ khi khởi động.
- [x] Lưu lại và tự động nạp "Yêu cầu bổ sung" (Prompt rules) cho từng lĩnh vực.

**KHÔNG làm:**
- Lưu trữ lịch sử import.
- Cho phép chọn nhiều API để dịch cùng lúc.

### Acceptance Criteria
- [ ] AC1: Dán 10 thuật ngữ mới, tất cả được dịch và thêm thành công.
- [ ] AC2: Dán 5 thuật ngữ mới và 5 thuật ngữ đã có (cùng bản dịch), 5 thuật ngữ mới được thêm và 5 cũ được bỏ qua.
- [ ] AC3: Dán 1 thuật ngữ có xung đột, dialog `ConflictResolutionWindow` hiện ra và cho phép chọn "Dùng mới", và thuật ngữ được cập nhật thành công.
- [ ] AC4: Quá trình hiển thị chỉ báo tiến trình (progress bar).

### Technical Notes
- Cần có một prompt đặc biệt để yêu cầu AI trả về kết quả dưới dạng có cấu trúc (ví dụ JSON: `{"term_jp": "term_vn"}`) để dễ phân tích.
- Việc gọi API cho một danh sách dài có thể mất thời gian, cần chạy ở background thread để không block UI và cập nhật progress bar.
- `ConflictResolutionWindow` cần được thiết kế rõ ràng, hiển thị term, bản dịch cũ, và bản dịch mới.

## Implementation Guide

### Input
- `BulkImportWindow` nhận một tham chiếu đến `GlossaryRepository`.
- Danh sách thuật ngữ tiếng Nhật từ người dùng (dán vào `CTkTextbox`).

### Output
- Các thuật ngữ mới/cập nhật được lưu vào `GlossaryRepository`.
- Dialog tóm tắt kết quả cho người dùng.

### Algorithm/Logic
1.  Người dùng dán text và nhấn nút. Lấy danh sách các terms từ `CTkTextbox`.
2.  Vô hiệu hóa cửa sổ và hiển thị progress bar.
3.  **Background Thread**:
    - Chuẩn bị một prompt lớn yêu cầu dịch toàn bộ danh sách sang tiếng Việt và trả về dạng JSON.
    - Gọi API dịch (ví dụ `gemini_client.translate_batch(terms)`).
    - Phân tích chuỗi JSON trả về thành dictionary.
4.  **Main Thread (sau khi có kết quả)**:
    - Duyệt qua từng cặp `(jp_term, new_vn_translation)` từ kết quả AI.
    - Kiểm tra `jp_term` trong `repo`.
    - **if not exists**: Thêm vào danh sách `to_add`.
    - **if exists with same translation**: Thêm vào danh sách `to_ignore`.
    - **if exists with different translation**: Thêm `(jp_term, old_translation, new_translation)` vào danh sách `to_resolve`.
5.  **Xử lý xung đột**:
    - Nếu `to_resolve` không rỗng, mở `ConflictResolutionWindow` với danh sách này.
    - Người dùng quyết định cho từng mục. Kết quả được thêm vào danh sách `to_update`.
6.  **Lưu vào Repo**:
    - Gọi `repo.add_multiple_terms(to_add)`.
    - Gọi `repo.update_multiple_terms(to_update)`.
7.  Hiển thị dialog tóm tắt.

### Libraries Required
- `customtkinter`
- `json` (built-in)
- `threading` (built-in)

### Error Handling
| Lỗi | Xử lý |
|------|-------|
| AI API call thất bại | Hiển thị `CTkMessagebox` báo lỗi API và dừng quá trình. |
| AI trả về JSON không hợp lệ | Hiển thị `CTkMessagebox` báo lỗi "Không thể phân tích phản hồi từ AI". |
| Người dùng đóng cửa sổ giữa chừng | Hủy background thread nếu có thể, không lưu gì cả. |

## Testing Checklist

### Unit Tests
- [ ] Test hàm phân tích danh sách terms từ `CTkTextbox`.
- [ ] Test logic phân loại (add, ignore, resolve) với dữ liệu giả.
- [ ] Test hàm tạo prompt cho batch translation.

### Integration Tests
- [ ] Test toàn bộ luồng với mock API (trả về JSON thành công, JSON lỗi, API error).
- [ ] Test `ConflictResolutionWindow` hoạt động đúng và cập nhật lại repo.

### Manual Testing
- [ ] Dán một danh sách dài (50+ terms) để kiểm tra performance và progress bar.
- [ ] Thử kịch bản hỗn hợp: term mới, term trùng, term xung đột.
- [ ] Thử dán text có dòng trống, khoảng trắng thừa.
- [ ] Thử đóng cửa sổ khi đang dịch.

## References
- REQUIREMENTS_VI.md: Section 4.4.5
