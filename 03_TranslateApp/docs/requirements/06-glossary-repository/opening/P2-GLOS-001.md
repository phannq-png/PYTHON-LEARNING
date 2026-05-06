# Task P2-GLOS-001: Xây dựng JSON Repository cho Bộ thuật ngữ

## Metadata
- **Task ID**: P2-GLOS-001
- **Priority**: HIGH
- **Phase**: 2
- **Estimated Effort**: M
- **Dependencies**: P1-CONF-001
- **Status**: opening

## Mô tả

### Mục đích
Xây dựng Data Layer (Repository) cho bộ thuật ngữ (Glossary). Bộ thuật ngữ này sẽ được lưu trữ dưới dạng JSON, hỗ trợ các thao tác CRUD cơ bản để sau này UI có thể tương tác. Mỗi lĩnh vực (domain) sẽ có bộ thuật ngữ riêng.

### Phạm vi
**Làm:**
- [ ] Tạo file `src/data/glossary_repo.py` chứa class `GlossaryRepository`.
- [ ] Hàm khởi tạo nhận tham số domain (lĩnh vực) và tự động trỏ đến file JSON tương ứng (VD: `data/glossaries/medical.json`).
- [ ] Các hàm CRUD: 
  - `load_glossary() -> dict`: Tải bộ thuật ngữ.
  - `save_glossary(data: dict)`: Lưu bộ thuật ngữ.
  - `add_term(jp_term: str, vn_term: str)`: Thêm hoặc cập nhật một thuật ngữ mới.
  - `delete_term(jp_term: str)`: Xóa một thuật ngữ.
- [ ] Đảm bảo thư mục `data/glossaries` tự động được tạo.

**KHÔNG làm:**
- Chưa làm UI quản lý glossary (sẽ làm ở Phase 3).
- Chưa làm chức năng highlight thuật ngữ trên UI.

### Acceptance Criteria
- [ ] AC1: Khởi tạo repository không bị lỗi, file JSON được tạo nếu chưa có.
- [ ] AC2: Hàm `add_term` ghi chính xác dữ liệu dạng dict `{ "jp_term": "vn_term" }` xuống file JSON.
- [ ] AC3: Hàm `load_glossary` đọc đúng dữ liệu đã lưu.
- [ ] AC4: Hàm `delete_term` xóa đúng thuật ngữ cần xóa.

### Technical Notes
- Sử dụng module `json` có sẵn của Python.
- Nhớ dùng `ensure_ascii=False` khi `json.dump` để không bị lỗi font tiếng Nhật/Việt.

## Testing Checklist
- [ ] Viết unit tests trong `tests/test_glossary_repo.py` cho tất cả các thao tác CRUD.

## References
- REQUIREMENTS_VI.md: Section 3.1, 6.5
