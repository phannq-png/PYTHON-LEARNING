# Task P4-TOKEN-001: Theo dõi và Hiển thị Token tiêu thụ

## Metadata
- **Task ID**: P4-TOKEN-001
- **Priority**: LOW
- **Phase**: 4
- **Estimated Effort**: S
- **Dependencies**: P2-API-001, P2-SESS-001
- **Status**: opening

## Mô tả

### Mục đích
Xây dựng cơ chế theo dõi số lượng token tiêu thụ cho mỗi lần gọi API dịch và hiển thị thông tin này trên giao diện để người dùng quản lý chi phí.

### Phạm vi
**Làm:**
- [ ] Cập nhật `TokenTracker` class để tính toán token từ phản hồi của API (OpenAI/Gemini).
- [ ] Lưu trữ số token đã tiêu thụ vào dữ liệu của từng trang (`page_data`).
- [ ] Tính toán tổng số token đã tiêu thụ cho toàn bộ phiên làm việc.
- [ ] Hiển thị thông tin token trên `BottomBar` theo định dạng: `Tokens: [Trang] (Trang) | [Tổng] (Tổng)`.
- [ ] Tự động cập nhật số liệu ngay sau khi một trang được dịch xong.

**KHÔNG làm:**
- Giới hạn số lượng token người dùng được phép sử dụng.
- Tính toán giá tiền thực tế (chỉ theo dõi số lượng token).

### Acceptance Criteria
- [ ] AC1: Sau khi dịch một trang, số token của trang đó hiển thị đúng trên Bottom Bar.
- [ ] AC2: Tổng số token được cộng dồn chính xác từ tất cả các trang đã dịch trong phiên.
- [ ] AC3: Khi chuyển trang, số token "Trang" thay đổi tương ứng với trang mới, trong khi số token "Tổng" giữ nguyên.
- [ ] AC4: Thông tin token được lưu vào file session JSON và khôi phục đúng khi tải lại phiên.

### Technical Notes
- Hầu hết các API AI (OpenAI, Gemini) đều trả về thông tin `usage` (prompt_tokens, completion_tokens) trong response. Cần trích xuất dữ liệu này.
- Định dạng hiển thị yêu cầu sự rõ ràng: "Tokens: 1.5K (Trang) | 15.2K (Tổng)".

## Implementation Guide

### Input
- API response từ OpenAI hoặc Gemini.
- `current_session`: Để cập nhật dữ liệu.

### Output
- Dữ liệu `token_usage` được cập nhật trong session object.
- Giao diện `BottomBar` hiển thị số liệu mới.

### Algorithm/Logic
1.  **Trích xuất**: Sau khi nhận response từ AI Client, lấy object `usage`.
2.  **Lưu trữ**:
    - Cập nhật `current_page.tokens_used = usage['total_tokens']`.
    - Cập nhật `session.total_tokens += usage['total_tokens']`.
3.  **Hiển thị**:
    - Gọi hàm `bottom_bar.update_tokens(page_tokens, total_tokens)`.
    - Hàm này sẽ định dạng lại số (ví dụ 1500 -> 1.5K) và cập nhật label.

### Libraries Required
- Không cần thư viện ngoài (chỉ xử lý số học và string formatting).

### Error Handling
| Lỗi | Xử lý |
|------|-------|
| API không trả về thông tin usage | Gán giá trị 0 và ghi log cảnh báo. |
| Lỗi khi đọc/ghi vào session object | Truy bắt exception và đảm bảo UI không bị treo. |

## Testing Checklist

### Unit Tests
- [ ] Test logic trích xuất token từ mock response của OpenAI.
- [ ] Test logic trích xuất token từ mock response của Gemini.
- [ ] Test hàm định dạng số (ví dụ: 500 -> 500, 1200 -> 1.2K, 1000000 -> 1M).

### Integration Tests
- [ ] Dịch một trang và kiểm tra xem session object có được cập nhật đúng số token không.
- [ ] Kiểm tra xem label trên Bottom Bar có thay đổi ngay lập tức không.

### Manual Testing
- [ ] Thực hiện dịch nhiều trang liên tiếp và kiểm tra tính chính xác của phép cộng dồn tổng token.
- [ ] Tải lại một phiên cũ và kiểm tra xem số token tổng có được hiển thị lại đúng không.

## References
- REQUIREMENTS_VI.md: Section 4.8.4
