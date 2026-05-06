# Task P1-CONF-002: UI Setting Phân đoạn văn bản

## Metadata
- **Task ID**: P1-CONF-002
- **Priority**: HIGH
- **Phase**: 1
- **Estimated Effort**: S
- **Dependencies**: P1-SEG-001
- **Status**: opening

## Mô tả

### Mục đích
Cung cấp giao diện người dùng (UI) để cấu hình các thiết lập cho tính năng phân đoạn văn bản, sau đó lưu trữ xuống hệ thống cấu hình cục bộ (`config.json`).

### Phạm vi
**Làm:**
- [ ] Xây dựng màn hình/popup Setting.
- [ ] Thêm input: **Số lượng ký tự tối đa mỗi page** (nhập số nguyên, mặc định: 1000).
- [ ] Thêm cấu hình **Ký tự bắt đầu đoạn văn** với các lựa chọn:
  - Checkbox: Phím Enter (Hard Return)
  - Checkbox: Phím Shift + Enter (Soft Return)
  - Text Input: Ký tự tùy chỉnh (Customize) - Cho phép nhập nhiều ký tự cách nhau bằng dấu phẩy (VD: `【,※`).
- [ ] Tích hợp tính năng lưu các thông số này xuống `config.json`.
- [ ] Tích hợp việc đọc ngược thông số từ `config.json` để gán lên giao diện mỗi khi mở Setting.

**KHÔNG làm:**
- Không viết lại logic phân đoạn (đã làm ở P1-SEG-001).

### Acceptance Criteria
- [ ] AC1: UI hiển thị đủ các lựa chọn (Max chars, 2 Checkbox Enter/Soft Return, và Input Customize).
- [ ] AC2: Người dùng có thể tích chọn đồng thời nhiều Checkbox và nhập text.
- [ ] AC3: Lưu thành công thông tin vào file cấu hình `config.json` dưới dạng các key rõ ràng.
- [ ] AC4: Khôi phục lại đúng trạng thái đã lưu khi mở lại màn hình Setting.

## Testing Checklist
- [ ] Manual test mở giao diện, thay đổi cấu hình, ấn lưu và kiểm tra nội dung file `config.json`.
- [ ] Mở lại ứng dụng và kiểm tra trạng thái hiển thị của các checkbox/input.

## References
- REQUIREMENTS_VI.md: Phần thiết lập hệ thống (Settings)
