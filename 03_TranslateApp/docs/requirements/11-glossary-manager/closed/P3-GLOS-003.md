# Task P3-GLOS-003: Cửa sổ Quản lý Thuật ngữ (Glossary Manager Window)

## Metadata
- **Task ID**: P3-GLOS-003
- **Priority**: MEDIUM
- **Phase**: 3
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

**KHÔNG làm:**
- Tự động dịch thuật ngữ hàng loạt trong cửa sổ này (đó là task `P4-AI-00x`).

### Acceptance Criteria
- [ ] AC1: Mở được cửa sổ quản lý từ Menu hoặc Top Bar.
- [ ] AC2: Hiển thị đúng danh sách thuật ngữ từ `GlossaryRepository`.
- [ ] AC3: Chức năng Import CSV hoạt động đúng (thêm mới hoặc ghi đè).
- [ ] AC4: Thêm, Sửa, Xóa thuật ngữ thành công và dữ liệu được lưu lại.
- [ ] AC5: Export CSV tạo ra file đúng định dạng.

### Technical Notes
- Cần xử lý việc cập nhật lại Sidebar bên phải (Active Glossary) sau khi người dùng thay đổi dữ liệu trong cửa sổ quản lý này. Có thể dùng callback function hoặc event system.
- Cửa sổ nên là dạng modal (chặn tương tác với cửa sổ chính) để tránh xung đột dữ liệu.
- Xử lý xung đột khi import CSV là một phần quan trọng (hỏi người dùng: Bỏ qua, Ghi đè).

## Implementation Guide

### Input
- `parent`: The root Tkinter window.
- `glossary_repo`: Một instance của `GlossaryRepository` để thao tác dữ liệu.

### Output
- Cửa sổ quản lý được hiển thị. Mọi thay đổi của người dùng được ghi lại vào `glossary_repo`.

### Algorithm/Logic
1.  **Khởi tạo Window**:
    - `GlossaryManagerWindow` kế thừa từ `ctk.CTkToplevel`.
    - Thiết lập cửa sổเป็น modal (sử dụng `transient` và `grab_set`).
2.  **Layout**:
    - Tạo `CTkTabview` để chứa các domain.
    - Với mỗi domain lấy từ `repo.get_all_domains()`, tạo một tab.
    - Trong mỗi tab, tạo một `CTkScrollableFrame` để làm bảng.
3.  **Hiển thị dữ liệu**:
    - Viết hàm `_redraw_table(domain)` để vẽ lại bảng thuật ngữ cho domain được chọn.
    - Hàm này sẽ xóa các widget cũ và tạo các hàng widget mới (Label cho term, Entry cho translation, Button cho Delete/Edit).
4.  **Chức năng CRUD**:
    - **Add**: Nút "Add" mở dialog yêu cầu nhập term JP/VN, sau đó gọi `repo.add_term()` và vẽ lại bảng.
    - **Edit**: Cho phép sửa trực tiếp trong `Entry` widget của bản dịch, khi người dùng focus out hoặc nhấn Enter, gọi `repo.update_term()`.
    - **Delete**: Nút "Delete" trên mỗi hàng sẽ hiện dialog xác nhận, sau đó gọi `repo.delete_term()` và vẽ lại bảng.
5.  **Import/Export**:
    - **Import**: Mở file dialog, đọc file CSV, xử lý logic xung đột và gọi `repo` tương ứng.
    - **Export**: Mở save dialog, lấy dữ liệu từ `repo` và ghi ra file CSV.

### Libraries Required
- `customtkinter`: Cho toàn bộ UI.
- `csv` (built-in): Để đọc/ghi file CSV.

### Error Handling
| Lỗi | Xử lý |
|------|-------|
| Thêm term đã tồn tại | Hiển thị `CTkMessagebox` báo lỗi "Thuật ngữ đã tồn tại". |
| File CSV không đúng định dạng | Hiển thị `CTkMessagebox` báo lỗi "File CSV không hợp lệ". |
| Lỗi quyền ghi/đọc file | Hiển thị `CTkMessagebox` báo lỗi quyền truy cập. |

## Testing Checklist

### Unit Tests
- [ ] Test logic đọc và ghi CSV (mock file system).
- [ ] Test logic xử lý xung đột khi import.
- [ ] Test các hàm add/update/delete bằng cách mock `GlossaryRepository`.

### Integration Tests
- [ ] Mở cửa sổ, thêm 1 term, đóng cửa sổ, kiểm tra xem `GlossaryRepository` có dữ liệu mới không.
- [ ] Mở cửa sổ, sửa term, đóng, kiểm tra repo có dữ liệu đã sửa.
- [ ] Test luồng import/export với file thực tế.

### Manual Testing
- [ ] Thực hiện mọi thao tác CRUD trên giao diện, sau đó khởi động lại app và kiểm tra xem dữ liệu có được lưu không.
- [ ] Thử import một file CSV lớn, có xung đột.
- [ ] Thử export tất cả domain và kiểm tra nội dung file.
- [ ] Cố gắng làm crash bằng cách nhập dữ liệu không hợp lệ.

## References
- REQUIREMENTS_VI.md: Section 4.4
