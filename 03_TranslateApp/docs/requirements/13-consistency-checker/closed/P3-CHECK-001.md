# Task P3-CHECK-001: Bộ Kiểm tra Tính nhất quán

## Metadata
- **Task ID**: P3-CHECK-001
- **Priority**: MEDIUM
- **Phase**: 3
- **Estimated Effort**: M
- **Dependencies**: P2-GLOS-001, P2-UI-002
- **Status**: closed

## Mô tả

### Mục đích
Xây dựng chức năng cho phép người dùng kiểm tra tính nhất quán trong việc sử dụng thuật ngữ giữa văn bản gốc (tiếng Nhật) và văn bản dịch (tiếng Việt) trên trang hiện tại.

### Phạm vi
**Làm:**
- [x] Tạo một class `ConsistencyChecker`.
- [x] Method `check(jp_text, vn_text, glossary)` sẽ là hạt nhân xử lý.
- [x] Implement thuật toán xác thực:
    1. Đếm số lần xuất hiện của mỗi thuật ngữ trong `jp_text` (phân biệt full-width/half-width).
    2. Đếm số lần xuất hiện của bản dịch tương ứng trong `vn_text` (KHÔNG phân biệt chữ hoa/thường).
    3. So sánh hai số đếm và ghi lại các trường hợp không khớp.
- [x] Tích hợp vào UI: Nút "Check Page" trên `BottomBar` sẽ trigger việc kiểm tra.
- [x] Tạo một cửa sổ dialog `CheckResultWindow` để hiển thị kết quả.
- [x] Dialog hiển thị thông báo thành công hoặc danh sách các thuật ngữ không khớp.
- [x] Cập nhật danh sách thuật ngữ ở Thanh bên phải: Hiển thị icon `×` (Đỏ) thay cho `✓` nếu thuật ngữ bị sai sau khi check.

**KHÔNG làm:**
- Tự động sửa các lỗi không nhất quán.
- Kiểm tra toàn bộ tài liệu (chỉ kiểm tra trang hiện tại).

### Acceptance Criteria
- [ ] AC1: Với một trang có thuật ngữ được dùng đúng số lần, dialog báo "Tất cả thuật ngữ đều nhất quán".
- [ ] AC2: Với một trang có "システム" (5 lần) và "Hệ thống" (4 lần), dialog báo cáo chính xác sự không khớp.
- [ ] AC3: Logic đếm tiếng Việt phải bỏ qua sự khác biệt hoa/thường (ví dụ: "Hệ Thống" và "hệ thống" đều được đếm).
- [ ] AC4: Logic đếm tiếng Nhật phải phân biệt full-width và half-width.

### Technical Notes
- Để đếm không phân biệt hoa/thường, có thể chuyển cả `vn_text` và bản dịch của thuật ngữ về dạng chữ thường (`.lower()`) trước khi đếm.
- Việc đếm có thể dùng `string.count()` hoặc `re.findall()` với `re.IGNORECASE` cho tiếng Việt.
- Class `ConsistencyChecker` nên được tách biệt khỏi UI để dễ dàng unit test.

## Implementation Guide

### Input
- `jp_text` (str): Nội dung văn bản tiếng Nhật của trang hiện tại.
- `vn_text` (str): Nội dung văn bản tiếng Việt của trang hiện tại.
- `glossary` (dict): Bộ thuật ngữ đã được gộp.

### Output
- `mismatches` (list[dict]): Một danh sách các dictionary, mỗi dict chứa thông tin về một thuật ngữ không khớp:
  - `{'jp_term': str, 'vn_term': str, 'jp_count': int, 'vn_count': int}`
- Hoặc một danh sách rỗng nếu tất cả đều nhất quán.

### Algorithm/Logic
1.  Class `ConsistencyChecker` có method `check(jp_text, vn_text, glossary)`.
2.  Khởi tạo list `mismatches` rỗng.
3.  Duyệt qua `glossary.items()`:
    - `jp_term, vn_term = item`
    - `jp_count = jp_text.count(jp_term)` (tìm kiếm phân biệt ký tự).
    - `vn_count = vn_text.lower().count(vn_term.lower())` (tìm kiếm không phân biệt hoa/thường).
    - **if `jp_count != vn_count`**:
        - Thêm một dictionary kết quả vào `mismatches`.
4.  Return `mismatches`.
5.  **UI Logic**:
    - Nút "Check Page" gọi hàm xử lý.
    - Hàm xử lý lấy text từ `CenterPanel`, glossary từ `GlossaryRepository`, gọi `checker.check(...)`.
    - Dựa trên kết quả trả về, hiển thị `CheckResultWindow` với thông điệp phù hợp.

### Libraries Required
- `customtkinter` (cho UI dialog).
- `re` (tùy chọn, có thể dùng `count` là đủ).

### Error Handling
| Lỗi | Xử lý |
|------|-------|
| Glossary rỗng | Hàm `check` trả về danh sách rỗng, UI không cần làm gì đặc biệt. |
| Text đầu vào là `None` | Hàm `check` cần xử lý `None` một cách an toàn, trả về danh sách rỗng. |

## Testing Checklist

### Unit Tests
- [ ] Test logic đếm tiếng Việt (case-insensitive).
- [ ] Test logic đếm tiếng Nhật (case-sensitive, width-sensitive).
- [ ] Test trường hợp không có lỗi.
- [ ] Test trường hợp có nhiều lỗi không nhất quán.
- [ ] Test với thuật ngữ/văn bản rỗng hoặc `None`.

### Integration Tests
- [ ] Click nút "Check Page" và xác nhận `ConsistencyChecker.check` được gọi với đúng text.
- [ ] Mock hàm `check` để trả về lỗi và xác nhận `CheckResultWindow` hiển thị đúng thông tin lỗi.
- [ ] Mock hàm `check` để trả về thành công và xác nhận dialog thành công được hiển thị.

### Manual Testing
- [ ] Chuẩn bị một trang dịch, cố tình dịch sai số lượng một vài thuật ngữ.
- [ ] Nhấn "Check Page" và xác nhận dialog hiển thị đúng các lỗi đó.
- [ ] Sửa lại cho đúng và nhấn check lần nữa, xác nhận dialog báo thành công.
- [ ] Thử với trang không có thuật ngữ nào.

## References
- REQUIREMENTS_VI.md: Section 4.6
