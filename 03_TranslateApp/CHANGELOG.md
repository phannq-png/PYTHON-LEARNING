# Changelog

Tất cả các thay đổi đáng chú ý của dự án **TranslatorApp** sẽ được lưu lại trong file này.

Định dạng dựa trên [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), và dự án tuân thủ [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.2.0] - 2026-05-12

### Added
- **Hệ thống Nhật ký Hoạt động (Daily Logging)**:
    - Tự động quay vòng file log theo ngày với định dạng `yyyyMMdd_app.log`.
    - Tách biệt log hệ thống và log lỗi (`yyyyMMdd_error.log`).
- **Minh bạch API (API Transparency)**:
    - Ghi lại chi tiết Prompt gửi đi và kết quả AI trả về vào file riêng `yyyyMMdd_api.log`.
- **Tiện ích Resource Path**: Thêm `path_utils.py` để xử lý đường dẫn tài nguyên tương thích hoàn toàn với môi trường EXE.
- **Script Build Sạch**: Thêm `scratch/build_exe.py` hỗ trợ đóng gói ứng dụng chuyên nghiệp, loại bỏ dữ liệu cá nhân.

### Changed
- **Tối ưu hóa UI**: Cửa sổ ứng dụng giờ đây luôn mở ở chế độ phóng to (`zoomed`) ngay khi khởi động.
- **Khôi phục cấu hình**: Tự động đưa ứng dụng về chế độ phóng to sau khi thực hiện `Import All Settings`.
- **Cấu trúc đóng gói**: Chỉ đóng gói thư mục `assets` cần thiết, giữ cho file EXE tinh gọn.

### Fixed
- **Lỗi treo giao diện**: Khắc phục triệt để lỗi đứng máy (freeze) khi AI không nhận diện được lĩnh vực của tài liệu.
- **Lỗi hiển thị Spinner**: Sửa lỗi icon vòng xoay không hiển thị khi chạy bản `.exe`.
- **Duy trì trạng thái**: Sửa lỗi mất dấu hiệu lỗi thuật ngữ (Dấu X đỏ) khi người dùng chuyển đổi qua lại giữa các trang.

---

## [1.1.0] - 2026-05-10

### Added
- **Phát hiện Lĩnh vực tự động**: Gợi ý bộ thuật ngữ (Domain) phù hợp ngay khi nạp tài liệu.
- **Dịch Thuật ngữ hàng loạt**: Tính năng tự động dịch các thuật ngữ mới trong glossary.
- **Tìm kiếm Toàn cục**: Highlight từ khóa trên tất cả các trang của tài liệu.
- **Theo dõi Token**: Hiển thị số lượng token sử dụng theo thời gian thực ở BottomBar.

### Changed
- Cải thiện tốc độ nạp tài liệu DOCX lớn.
- Nâng cấp giao diện Sidebar với khả năng thu gọn phần chú thích (Legend).

---

## [1.0.0] - 2026-05-01

### Added
- **Core Engine**: Xử lý tài liệu DOCX, bảo toàn định dạng (Bold, Italic, Tables).
- **AI Integration**: Hỗ trợ Google Gemini và OpenAI GPT.
- **Glossary System**: Quản lý thuật ngữ theo Domain, hỗ trợ Import/Export CSV.
- **Navigation**: Hệ thống phân đoạn văn bản và điều hướng trang thông minh.
- **Export**: Xuất file dịch đơn ngữ (VN) hoặc song ngữ (JP/VN).

---
*Phát triển bởi P & Antigravity Agent.*
