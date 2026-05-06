# Task P1-SETUP-001: Khởi tạo Project Boilerplate & Dependencies

## Metadata
- **Task ID**: P1-SETUP-001
- **Priority**: CRITICAL
- **Phase**: 1
- **Estimated Effort**: XS
- **Dependencies**: None
- **Status**: opening

## Mô tả

### Mục đích
Tạo nền tảng cơ bản cho ứng dụng, bao gồm các file gốc và cấu trúc thư mục để các developer khác có thể bắt đầu làm việc. Đảm bảo tất cả các dependencies được cài đặt đúng phiên bản.

### Phạm vi
**Làm:**
- [ ] Khởi tạo virtual environment
- [ ] Cài đặt các thư viện bắt buộc trong requirements.txt
- [ ] Thiết lập file main.py cơ bản để chạy app

**KHÔNG làm:**
- Code giao diện thực tế (sẽ làm ở P1-UI-001)

### Acceptance Criteria
- [ ] AC1: File `main.py` chạy thành công mà không văng lỗi thư viện.
- [ ] AC2: Chứa đủ các thư viện yêu cầu trong `requirements.txt`.

### Technical Notes
- Ứng dụng dùng Python 3.10+
- `cryptography` là bắt buộc để mã hóa API sau này.

## Implementation Guide

### Input
- requirements.txt

### Output
- Môi trường chạy được

### Libraries Required
- `customtkinter>=5.2.0`: UI Framework
- `python-docx>=1.1.0`: Xử lý Word
- `cryptography>=42.0.5`: Mã hóa

## Testing Checklist

### Manual Testing
- [ ] Chạy `python main.py` kiểm tra start ứng dụng

## References
- REQUIREMENTS_VI.md: Section 7 & 8
