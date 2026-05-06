# Task P2-SESS-001: Quản lý Phiên Làm Việc (Session Management)

## Metadata
- **Task ID**: P2-SESS-001
- **Priority**: HIGH
- **Phase**: 2
- **Estimated Effort**: M
- **Dependencies**: P1-SEG-001
- **Status**: opening

## Mô tả

### Mục đích
Quản lý trạng thái và tiến độ dịch thuật của người dùng để không bị mất dữ liệu. Chức năng này đọc cấu trúc tài liệu sau phân đoạn và lưu trữ liên tục (auto-save hoặc save thủ công) ra file JSON trong thư mục `sessions/`.

### Phạm vi
**Làm:**
- [ ] Tạo class `SessionManager` ở `src/data/session_manager.py`.
- [ ] Cấu trúc dữ liệu Session JSON bao gồm: ID, tên file gốc, mảng các trang (nội dung JP, nội dung VN, trạng thái hoàn thành).
- [ ] Hàm `create_session(docx_path, segments)`: Khởi tạo phiên mới.
- [ ] Hàm `save_session(session_data)`: Ghi tiến độ hiện tại xuống file `.json`.
- [ ] Hàm `load_session(session_id)`: Đọc lại tiến độ cũ.
- [ ] Đảm bảo thư mục `data/sessions` (hoặc `sessions/` tùy quy chuẩn thư mục) luôn tồn tại.

### Acceptance Criteria
- [ ] AC1: `create_session` sinh ra một object/dict với đầy đủ thông tin trang và nội dung rỗng cho tiếng Việt.
- [ ] AC2: `save_session` ghi thành công object xuống file JSON, nội dung không bị lỗi font.
- [ ] AC3: `load_session` phục hồi chính xác lại trạng thái đã lưu.

### Technical Notes
- Thư mục lưu session nên đặt ở `data/sessions/`.
- Định dạng JSON tương tự như mô tả trong REQUIREMENTS_VI.md (Section 3.2).

## Testing Checklist
- [ ] Viết test lưu và tải lại một session mẫu xem dữ liệu có khớp không.

## References
- REQUIREMENTS_VI.md: Section 3.2, 6.4
