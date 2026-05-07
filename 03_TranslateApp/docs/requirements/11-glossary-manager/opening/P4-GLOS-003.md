# Task P4-GLOS-003: Cửa sổ Quản lý Thuật ngữ (Glossary Manager Window)

## Metadata
- **Task ID**: P4-GLOS-003
- **Priority**: HIGH
- **Phase**: 4
- **Estimated Effort**: L
- **Dependencies**: P2-GLOS-001
- **Status**: opening

## Mô tả

### Mục đích
Xây dựng một giao diện (Toplevel window) cho phép người dùng quản lý toàn bộ cơ sở dữ liệu thuật ngữ một cách trực quan, thay vì phải chỉnh sửa file JSON thủ công.

### Phạm vi
**Làm:**
- [ ] Tạo class `GlossaryManagerWindow` kế thừa `ctk.CTkToplevel`.
- [ ] Thiết kế bảng hiển thị thuật ngữ (có thể dùng `CTkScrollableFrame` kết hợp các row widgets hoặc thư viện bảng nếu có).
- [ ] Chức năng Thêm/Sửa/Xóa thuật ngữ trực tiếp trên giao diện.
- [ ] Chức năng Import CSV và Export CSV.
- [ ] Tab switcher để chuyển đổi giữa các lĩnh vực (Medical, Legal, Common, v.v.).

### Acceptance Criteria
- [x] AC1: Mở được cửa sổ quản lý từ Menu hoặc Top Bar.
- [x] AC2: Hiển thị đúng danh sách thuật ngữ từ `GlossaryRepository`.
- [x] AC3: Chức năng Import CSV hoạt động đúng (thêm mới hoặc ghi đè).

## Technical Notes
- Cần xử lý việc cập nhật lại Sidebar bên phải (Active Glossary) sau khi người dùng thay đổi dữ liệu trong cửa sổ quản lý này.

## References
- REQUIREMENTS_VI.md: Section 4.4
