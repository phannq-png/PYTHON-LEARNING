# Task P1-CONF-002: UI Setting Phân đoạn văn bản

## Metadata
- **Task ID**: P1-CONF-002
- **Priority**: HIGH
- **Phase**: 1
- **Estimated Effort**: S
- **Dependencies**: P1-SEG-001, P1-UI-001

## Mô tả

### Mục đích
Cung cấp giao diện người dùng (UI) dạng **Dialog/Popup** để cấu hình các thiết lập cho tính năng phân đoạn văn bản. Dialog này được truy cập từ **Menu Bar > Settings > Segmentation Settings**, sau đó lưu trữ xuống hệ thống cấu hình cục bộ (`config.json`).

### Phạm vi
**Làm:**
- [ ] Xây dựng `SegmentationSettingsDialog` dạng **Modal Dialog** (dùng `CTkToplevel` hoặc `tk.Toplevel`).
- [ ] Dialog được gọi khi người dùng click **Menu Bar > Settings > Segmentation Settings**.
- [ ] Thêm input: **Số lượng ký tự tối đa mỗi page** (nhập số nguyên, mặc định: 1000).
- [ ] Thêm cấu hình **Ký tự bắt đầu đoạn văn** với các lựa chọn:
  - Checkbox: Phím Enter (Hard Return)
  - Checkbox: Phím Shift + Enter (Soft Return)
  - Text Input: Ký tự tùy chỉnh (Customize) - Cho phép nhập nhiều ký tự cách nhau bằng dấu phẩy (VD: `【,※`).
- [ ] Nút **Save** để lưu thông số xuống `config.json` và đóng dialog.
- [ ] Nút **Cancel** để đóng dialog không lưu.
- [ ] Tích hợp việc đọc ngược thông số từ `config.json` để gán lên giao diện mỗi khi mở Dialog.

**KHÔNG làm:**
- Không viết lại logic phân đoạn (đã làm ở P1-SEG-001).
- Không đặt button Settings trực tiếp trên màn hình chính.

### Acceptance Criteria
- [ ] AC1: Click **Menu Bar > Settings > Segmentation Settings** mở đúng Dialog.
- [ ] AC2: Dialog hiển thị đủ các lựa chọn (Max chars, 2 Checkbox Enter/Soft Return, và Input Customize).
- [ ] AC3: Dialog là **modal** — chặn tương tác với cửa sổ chính khi đang mở.
- [ ] AC4: Người dùng có thể tích chọn đồng thời nhiều Checkbox và nhập text.
- [ ] AC5: Lưu thành công thông tin vào file cấu hình `config.json` dưới dạng các key rõ ràng.
- [ ] AC6: Khôi phục lại đúng trạng thái đã lưu khi mở lại Dialog.

### Technical Notes
- Dùng `CTkToplevel` (CustomTkinter) để tạo Dialog, gọi `grab_set()` để tạo modal behavior.
- Kết nối với Menu Bar tại `app_window.py`: `settings_menu.add_command(label="Segmentation Settings", command=self.open_segmentation_settings)`.

## Testing Checklist
- [ ] Manual test: Click Menu Bar > Settings > Segmentation Settings → Dialog mở đúng.
- [ ] Thay đổi cấu hình, ấn Save → kiểm tra nội dung file `config.json`.
- [ ] Ấn Cancel → không lưu, dialog đóng.
- [ ] Mở lại Dialog → kiểm tra trạng thái hiển thị khớp với `config.json`.

## References
- REQUIREMENTS_VI.md: Section 4.2.1, 4.8 (Settings)
