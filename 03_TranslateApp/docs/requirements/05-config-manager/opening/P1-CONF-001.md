# Task P1-CONF-001: Quản lý Cấu hình & Mã hóa API Key

## Metadata
- **Task ID**: P1-CONF-001
- **Priority**: CRITICAL
- **Phase**: 1
- **Estimated Effort**: M
- **Dependencies**: P1-SETUP-001
- **Status**: opening

## Mô tả

### Mục đích
Lưu trữ và truy xuất các cấu hình hệ thống (API keys, provider) một cách an toàn. Tuyệt đối không để lộ API Key dạng plaintext. (Section 4.8.3)

### Phạm vi
**Làm:**
- [ ] Tạo file `.secret.key` (để ngoài Git) để sinh key mã hóa Fernet.
- [ ] Viết class `config_repo.py` để đọc/ghi file `api_config.json`.
- [ ] Mã hóa (encrypt) API key khi lưu và giải mã (decrypt) khi đọc.

### Acceptance Criteria
- [ ] AC1: Ghi một API Key xuống file `api_config.json` sẽ thấy chuỗi mã hóa (encrypted string).
- [ ] AC2: Đọc file lên sẽ giải mã được chuỗi gốc.

### Technical Notes
- Thư viện: `cryptography.fernet.Fernet`
- Nơi lưu file: `data/config/`

## Testing Checklist
- [ ] Unit test mã hóa và giải mã.

## References
- REQUIREMENTS_VI.md: Section 4.8.3
