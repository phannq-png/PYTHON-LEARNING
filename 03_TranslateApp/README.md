# TranslatorApp v1.1 🚀
### Ứng dụng Dịch Tài liệu Chuyên ngành Nhật - Việt (Bảo toàn Định dạng)

**TranslatorApp** là giải pháp phần mềm Desktop mạnh mẽ giúp dịch các tài liệu kỹ thuật, y tế, pháp luật từ tiếng Nhật sang tiếng Việt sử dụng công nghệ AI tiên tiến (Gemini/OpenAI), đồng thời giữ nguyên 100% định dạng gốc của file Microsoft Word.

---

## ✨ Tính năng Nổi bật

### 🧠 Trí tuệ Nhân tạo (AI-Powered)
- **Dịch thuật Thông minh**: Tích hợp Google Gemini và OpenAI để dịch sát nghĩa chuyên ngành, ngữ pháp tự nhiên.
- **Phát hiện Lĩnh vực**: Tự động phân tích nội dung tài liệu để gợi ý bộ thuật ngữ phù hợp ngay khi upload.
- **Dịch Thuật ngữ Hàng loạt**: Tự động dịch hàng trăm thuật ngữ mới chỉ với một cú click.

### 📄 Xử lý Tài liệu Nâng cao
- **Bảo toàn Định dạng**: Giữ nguyên Font chữ, màu sắc, kích thước, in đậm/nghiêng, cấu trúc bảng và danh sách (bullets/numbering).
- **Phân đoạn Thông minh**: Tự động tách trang và đoạn văn bản hợp lý dựa trên cấu hình tùy chỉnh.
- **Duy trì Trạng thái (Persistence)**: Tự động lưu và khôi phục kết quả kiểm tra thuật ngữ (mismatches) khi chuyển trang.
- **Tìm kiếm Toàn cục**: Tìm và highlight từ khóa trên tất cả các trang, hiển thị trực quan ở Sidebar.
- **Export DOCX**: Hỗ trợ xuất file dịch tiêu chuẩn (tiếng Việt) hoặc phiên bản song ngữ (Nhật-Việt xen kẽ).

### 📖 Quản lý Thuật ngữ (Glossary)
- **Hệ thống Domain**: Phân chia thuật ngữ theo lĩnh vực (Medical, IT, Legal, Common...).
- **Cửa sổ Quản lý**: Giao diện CRUD trực quan, hỗ trợ Import/Export CSV tương thích hoàn toàn với Excel.
- **Interactive Sidebar**: 
    - Hiển thị thuật ngữ active trong trang, click để highlight (Toggle mode).
    - Phần chú thích trạng thái (Legend) có thể thu gọn để tối ưu không gian danh sách trang.
- **Hệ thống Trợ giúp**: Tích hợp màn hình Hướng dẫn sử dụng chi tiết ngay trong menu Help.

---

## 🛠️ Công nghệ Sử dụng
- **Ngôn ngữ**: Python 3.10+
- **Giao diện**: CustomTkinter (Modern Dark Mode)
- **Xử lý DOCX**: python-docx
- **AI Clients**: Google Generative AI, OpenAI API
### 🛡️ Hệ thống Giám sát & Bảo mật
- **Daily Logging**: Hệ thống log tự động quay vòng theo ngày với định dạng `yyyyMMdd_app.log`.
- **API Transparency**: Tách riêng log yêu cầu và phản hồi từ AI vào file `api.log` giúp kiểm soát chi phí và chất lượng dịch thuật.
- **Mã hóa Fernet**: Bảo vệ API Keys an toàn trong file cấu hình.

---

## 🚀 Hướng dẫn Cài đặt

1. **Clone repository**:
   ```bash
   git clone https://github.com/phannq-png/PYTHON-LEARNING.git
   cd PYTHON-LEARNING/03_TranslateApp
   ```

2. **Cài đặt phụ thuộc**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Chạy ứng dụng**:
   ```bash
   python main.py
   ```

---

## 📖 Hướng dẫn Sử dụng Nhanh

1. **Cấu hình API**: Vào `Settings` -> `API Settings` để nhập API Key (Gemini hoặc OpenAI).
2. **Nạp Tài liệu**: Nhấn `Mở tài liệu` để chọn file `.docx`. AI sẽ tự động gợi ý lĩnh vực.
3. **Quản lý Thuật ngữ**: Vào `Tools` -> `Quản lý thuật ngữ` để chuẩn bị bộ từ điển chuyên ngành.
4. **Dịch & Kiểm tra**: 
    - Sử dụng `⚡ Translate` để dịch. 
    - Sử dụng `✅ Check Page` để kiểm tra tính nhất quán (Kết quả sẽ được lưu lại kể cả khi chuyển trang).
5. **Tìm kiếm nhanh**: Sử dụng ô tìm kiếm ở TopBar hoặc phím `Esc` để xóa toàn bộ highlight.
6. **Xem Hướng dẫn**: Vào `Help` -> `Hướng dẫn sử dụng` để xem chi tiết các phím tắt và mẹo dùng.
7. **Xuất file**: Nhấn `Export DOCX` để nhận kết quả cuối cùng.

---

## 📝 Tài liệu Dự án
- [Đặc tả Yêu cầu (Specs)](docs/requirements/REQUIREMENTS_VI.md)
- [Báo cáo Tiến độ](docs/requirements/PROJECT_STATUS_REPORT.md)
- [Kịch bản Kiểm thử](docs/requirements/MANUAL_TEST_SCENARIOS.md)

---
**Phát triển bởi Antigravity Agent.**
*Chúc bạn có những bản dịch chất lượng nhất!*
