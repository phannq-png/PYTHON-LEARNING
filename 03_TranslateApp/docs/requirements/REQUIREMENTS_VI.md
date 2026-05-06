# TÀI LIỆU ĐẶC TẢ YÊU CẦU
## Ứng dụng Dịch Tài liệu Chuyên ngành Nhật-Việt

---

## 1. TỔNG QUAN DỰ ÁN

### 1.1 Thông tin Ứng dụng
- **Loại ứng dụng**: Ứng dụng Desktop
- **Ngôn ngữ lập trình**: Python 3.10+
- **Framework giao diện**: CustomTkinter
- **Nền tảng**: Đa nền tảng (Windows, macOS, Linux)
- **Mục đích**: Dịch tài liệu chuyên ngành từ tiếng Nhật sang tiếng Việt với việc giữ nguyên định dạng

### 1.2 Quy trình Xử lý Chính
Ứng dụng tuân theo quy trình chuyển đổi:
DOCX (Tiếng Nhật) → Markdown → Phân đoạn → Dịch → Markdown → DOCX (Tiếng Việt)

---

## 2. CÔNG NGHỆ SỬ DỤNG

### 2.1 Các Công nghệ Cốt lõi
- **Ngôn ngữ lập trình**: Python 3.10 trở lên
- **Framework UI**: CustomTkinter (thư viện UI Python hiện đại)
- **Xử lý Tài liệu**: 
  - python-docx để thao tác file DOCX
  - markdown để chuyển đổi Markdown
- **Tích hợp AI**:
  - OpenAI API
  - Google Gemini API
- **Lưu trữ Dữ liệu**: File JSON lưu cục bộ
- **Bảo mật**: cryptography.fernet để mã hóa API key

### 2.2 Kiến trúc Hệ thống
Ứng dụng được xây dựng với bốn tầng:

**Tầng Trình diễn (UI)**
- Cửa sổ dịch chính
- Giao diện quản lý thuật ngữ
- Giao diện cài đặt API
- Giao diện phát hiện lĩnh vực

**Tầng Logic Nghiệp vụ**
- Bộ xử lý tài liệu (chuyển đổi DOCX sang Markdown)
- Engine dịch (dịch dựa trên AI)
- Bộ khớp thuật ngữ (tìm và làm nổi bật thuật ngữ)
- Bộ kiểm tra tính nhất quán (xác thực)
- Quản lý phiên (lưu/tải tiến độ)
- Theo dõi token (giám sát sử dụng API)

**Tầng Truy cập Dữ liệu**
- Repository thuật ngữ (các thao tác CRUD)
- Quản lý cấu hình (lưu trữ mã hóa)
- Repository phiên (lưu trữ tiến độ)

**Tầng Dịch vụ Bên ngoài**
- Client API OpenAI/Gemini

---

## 3. CẤU TRÚC DỮ LIỆU

### 3.1 Dữ liệu Thuật ngữ
Mỗi bộ thuật ngữ được lưu dưới dạng file JSON chứa:
- Tên lĩnh vực (ví dụ: "medical", "legal", "common")
- Dictionary ánh xạ thuật ngữ tiếng Nhật sang bản dịch tiếng Việt
- Thời điểm tạo
- Thời điểm cập nhật gần nhất

**Định dạng CSV để Import/Export**:
Mỗi dòng chứa: Thuật ngữ tiếng Nhật, Thuật ngữ tiếng Việt, Tên lĩnh vực

### 3.2 Dữ liệu Phiên làm việc
File phiên lưu trữ:
- ID phiên duy nhất
- Đường dẫn đến file DOCX gốc
- Lĩnh vực đã chọn
- Mảng các trang với:
  - Số ID trang
  - Nội dung văn bản tiếng Nhật
  - Nội dung văn bản tiếng Việt
  - Trạng thái dịch (hoàn thành hay chưa)
  - Số token đã sử dụng cho trang đó
- Số trang hiện tại đang active
- Tổng số token đã sử dụng trên tất cả các trang
- Thời điểm tạo và sửa đổi

### 3.3 Cấu hình API
File cấu hình mã hóa lưu trữ:
- **Cài đặt API Dịch**:
  - Tên nhà cung cấp (OpenAI hoặc Gemini)
  - API key đã mã hóa
  - Tên model đã chọn
- **Cài đặt API Phát hiện Lĩnh vực**:
  - Tên nhà cung cấp
  - API key đã mã hóa
  - Tên model đã chọn

---

## 4. YÊU CẦU TÍNH NĂNG

### 4.1 Xử lý Tài liệu

#### 4.1.1 Giữ nguyên Định dạng
Ứng dụng phải giữ nguyên các yếu tố định dạng sau:
- Font chữ và kích thước
- Màu chữ
- Kiểu in đậm và in nghiêng
- Cấu trúc bảng
- Bullet points (dấu đầu dòng)
- Danh sách đánh số

**Không Hỗ trợ**:
- Hình ảnh (sẽ bị bỏ qua, không xử lý)
- Header và footer (có thể không giữ hoàn hảo)
- Track changes và comments

#### 4.1.2 Quy tắc Chuyển đổi Tài liệu
- Chuyển DOCX sang Markdown trong khi lưu metadata định dạng
- Lưu thông tin định dạng riêng để chuyển đổi ngược lại
- Định dạng của mỗi đoạn văn (font, size, color, styles) phải được giữ nguyên
- Khi chuyển đổi lại sang DOCX, áp dụng định dạng đã lưu cho văn bản tiếng Việt

#### 4.1.3 Phân đoạn Văn bản
- Mỗi đoạn bắt đầu với mẫu 【text】
- Ví dụ: 【序論】, 【方法】, 【結果】
- Các đoạn không bao giờ được tách ở giữa
- Luôn giữ nguyên các đoạn hoàn chỉnh
- Nếu một đoạn quá dài, vẫn giữ nó như một đơn vị duy nhất

#### 4.1.4 Tạo Trang
- Tối thiểu: 1 đoạn văn mỗi trang
- Tối đa: Nhiều đoạn văn có thể vừa mà không cần cuộn dọc
- Tính toán dựa trên ước lượng chiều cao văn bản
- Mục tiêu: Không cần thanh cuộn trong mỗi trang hiển thị

---

### 4.2 Giao diện Dịch Chính

#### 4.2.1 Cấu trúc Bố cục
Cửa sổ chính được chia thành:
- **Menu Bar**: Thanh menu hệ thống nằm trên cùng cửa sổ, chứa các mục:
  - `File`: Mở file, Thoát ứng dụng
  - `Settings`: Segmentation Settings (mở Dialog), API Settings (mở Dialog)
  - `Help`: About
- **Thanh Trên (Top Bar)**: Nút upload file, Dropdown chọn lĩnh vực, Nút Export
- **Thanh Bên Trái**: Danh sách điều hướng trang
- **Panel Trung tâm (Chia ngang)**:
  - Trên: Văn bản tiếng Nhật (chỉ đọc)
  - Dưới: Văn bản tiếng Việt (có thể chỉnh sửa)
  - Thanh phân cách ngang giữa chúng
- **Thanh Bên Phải**: Thuật ngữ đang active cho trang hiện tại
- **Thanh Dưới**: Các nút thao tác và bộ đếm token

#### 4.2.2 Yêu cầu Hiển thị
- Hướng chia: Ngang (tiếng Nhật trên, tiếng Việt dưới)
- Không đồng bộ cuộn giữa panel tiếng Nhật và tiếng Việt
- Vùng văn bản tiếng Nhật chỉ đọc
- Vùng văn bản tiếng Việt có thể chỉnh sửa hoàn toàn
- Theme mặc định: Dark mode

#### 4.2.3 Điều hướng Trang
- Định dạng hiển thị: ◀ [Số Trang Hiện tại]/[Tổng Số Trang] ▶
- Click nút mũi tên để di chuyển giữa các trang
- Click số trang trong thanh bên trái để nhảy trực tiếp
- Tự động lưu trang hiện tại khi điều hướng sang trang khác

#### 4.2.4 Chức năng Các Nút

**Nút Translate (Dịch)**
- Gửi văn bản tiếng Nhật đến API AI với ép buộc thuật ngữ
- Hiển thị thanh tiến trình trong lúc gọi API
- Cập nhật vùng văn bản tiếng Việt với kết quả dịch
- Theo dõi và ghi lại token đã sử dụng
- Hiển thị thông báo lỗi nếu gọi API thất bại (không tự động thử lại)

**Nút Get Prompt (Lấy Prompt)**
- Tạo prompt dịch hoàn chỉnh bao gồm thuật ngữ
- Sao chép prompt vào clipboard
- Hiển thị prompt trong cửa sổ dialog
- Người dùng có thể sao chép thủ công sang ChatGPT, Gemini hoặc công cụ AI khác

**Nút Check Page (Kiểm tra Trang)**
- Chạy xác thực tính nhất quán trên trang hiện tại
- So sánh tần suất thuật ngữ giữa tiếng Nhật và tiếng Việt
- Hiển thị dialog popup với kết quả kiểm tra
- Liệt kê các trường hợp không khớp nếu tìm thấy

**Nút Save (Lưu)**
- Lưu toàn bộ phiên vào file JSON
- Bao gồm tất cả các trang và trạng thái dịch của chúng
- Cập nhật timestamp sửa đổi gần nhất
- Xác nhận hoàn tất lưu cho người dùng

---

### 4.3 Thanh Bên Phải - Hiển thị Thuật ngữ Đang Active

#### 4.3.1 Quy tắc Hiển thị
- Chỉ hiển thị các thuật ngữ xuất hiện trong trang hiện tại
- Tự động cập nhật khi chuyển trang
- Định dạng hiển thị cho mỗi thuật ngữ:
  - Biểu tượng checkmark
  - Thuật ngữ tiếng Nhật
  - Ký hiệu mũi tên
  - Bản dịch tiếng Việt
- Hiển thị số lần xuất hiện trong ngoặc đơn

#### 4.3.2 Tính năng Tương tác
- Click vào bất kỳ thuật ngữ nào để nhảy đến lần xuất hiện đầu tiên trong văn bản
- Làm nổi bật tất cả các lần xuất hiện của thuật ngữ đã click
- Click lại để bỏ làm nổi bật
- Chỉ báo trực quan về thuật ngữ nào đang được chọn

---

### 4.4 Hệ thống Quản lý Thuật ngữ

#### 4.4.1 Tổ chức theo Lĩnh vực
- **Lĩnh vực Common**: Tự động áp dụng cho tất cả các lĩnh vực khác
- **Lĩnh vực Cụ thể**: y tế, pháp luật, CNTT, kỹ thuật, v.v.
- **Quy tắc Ưu tiên**: Thuật ngữ lĩnh vực cụ thể ghi đè lên Common
- Người dùng có thể tạo lĩnh vực tùy chỉnh khi cần

#### 4.4.2 Giao diện Quản lý Thuật ngữ
Cửa sổ quản lý thuật ngữ chứa:
- Các tab lĩnh vực ở trên để chuyển đổi giữa các lĩnh vực
- Các nút thao tác: Thêm, Xóa, Import CSV, Export CSV, Nhập Hàng loạt
- Bảng hiển thị tất cả thuật ngữ với các cột:
  - Thuật ngữ tiếng Nhật
  - Bản dịch tiếng Việt
  - Tên lĩnh vực
  - Thao tác (nút Edit, Delete)

#### 4.4.3 Thao tác CRUD

**Thêm Thuật ngữ**
- Form nhập thuật ngữ đơn
- Các trường: Thuật ngữ tiếng Nhật, Bản dịch tiếng Việt
- Kiểm tra trùng lặp trước khi lưu
- Thông báo lỗi nếu tồn tại trùng lặp trong cùng lĩnh vực

**Sửa Thuật ngữ**
- Click nút Edit hoặc double-click dòng trong bảng
- Chỉnh sửa trực tiếp trong bảng
- Lưu thay đổi ngay lập tức
- Xác thực để tránh trùng lặp

**Xóa Thuật ngữ**
- Xóa đơn: Click nút Delete trên dòng cụ thể
- Xóa hàng loạt: Chọn nhiều dòng và xóa
- Dialog xác nhận trước khi xóa
- Không thể hoàn tác việc xóa

**Xóa Tất cả**
- Nút để xóa tất cả thuật ngữ trong lĩnh vực hiện tại
- Dialog xác nhận với cảnh báo
- Không ảnh hưởng đến lĩnh vực khác

**Phát hiện Trùng lặp**
- Không cho phép thuật ngữ tiếng Nhật trùng lặp trong cùng lĩnh vực
- Trùng lặp giữa các lĩnh vực khác nhau được phép
- Kiểm tra phân biệt chữ hoa/thường cho thuật ngữ tiếng Nhật
- Hiển thị thông báo lỗi cho biết thuật ngữ đã tồn tại

#### 4.4.4 Import và Export

**Import CSV**
- Chấp nhận file CSV với định dạng: JP_term, VN_term, domain
- Phân tích từng dòng và xác thực định dạng
- Kiểm tra trùng lặp với thuật ngữ hiện có
- Đối với xung đột:
  - Hiển thị dialog xác nhận
  - Liệt kê tất cả thuật ngữ xung đột
  - Cho phép người dùng chọn: Bỏ qua, Thay thế, hoặc Hủy
- Import các mục thành công
- Hiển thị tóm tắt các mục đã import, bỏ qua và thất bại

**Export CSV**
- Export chỉ lĩnh vực hiện tại hoặc tất cả lĩnh vực
- Tạo file CSV với encoding đúng (UTF-8)
- Bao gồm dòng header: JP_term, VN_term, domain
- **Yêu cầu Bảo mật**: Không bao giờ bao gồm API key trong file export
- Cho phép người dùng chọn vị trí lưu

#### 4.4.5 Nhập Hàng loạt với Dịch AI

**Quy trình**
1. Người dùng mở dialog nhập hàng loạt
2. Dán danh sách thuật ngữ tiếng Nhật (mỗi dòng một thuật ngữ)
3. Click nút "Translate & Import"
4. Hệ thống gọi API AI để dịch tất cả thuật ngữ theo batch
5. Với mỗi thuật ngữ đã dịch:
   - **Nếu là thuật ngữ mới**: Tự động thêm vào glossary
   - **Nếu thuật ngữ tồn tại với cùng bản dịch**: Bỏ qua im lặng
   - **Nếu thuật ngữ tồn tại với bản dịch khác**:
     - Tạm dừng và hiển thị dialog xác nhận
     - Hiển thị cả bản dịch cũ và mới
     - Người dùng chọn: Giữ Cũ hoặc Dùng Mới
6. Lưu tất cả thuật ngữ được chấp nhận vào glossary
7. Hiển thị tóm tắt kết quả

**Luồng Giao diện Người dùng**
- Vùng văn bản để dán thuật ngữ tiếng Nhật
- Nút AI Translate
- Chỉ báo tiến trình trong khi dịch
- Dialog xem xét hiển thị:
  - Thuật ngữ mới (tự động chấp nhận)
  - Xung đột cần quyết định của người dùng
  - Tùy chọn cho mỗi xung đột: Giữ Cũ / Dùng Mới
- Nút Confirm All để hoàn tất import

---

### 4.5 Tính năng Phát hiện Lĩnh vực

#### 4.5.1 Phương thức Phát hiện
Người dùng có thể kích hoạt phát hiện lĩnh vực bằng:
- Chọn một trang từ giao diện chính
- Dán mẫu văn bản vào bộ phát hiện lĩnh vực

#### 4.5.2 Quy trình Phát hiện
1. Người dùng cung cấp đầu vào (chọn trang hoặc dán văn bản)
2. Hệ thống gọi API Phát hiện Lĩnh vực
3. AI phân tích văn bản và đề xuất tên lĩnh vực
4. Hệ thống tìm kiếm lĩnh vực hiện có để khớp
5. Nếu tìm thấy khớp: Hiển thị tên lĩnh vực đã khớp
6. Nếu không khớp: Đề xuất tạo lĩnh vực mới với tên do AI cung cấp
7. Người dùng xác nhận hoặc chỉnh sửa tên lĩnh vực
8. Hệ thống tải glossary tương ứng cho lĩnh vực đó

#### 4.5.3 Logic Khớp Lĩnh vực
- AI trả về tên lĩnh vực được đề xuất (ví dụ: "Medical", "Legal")
- Hệ thống thực hiện tìm kiếm không phân biệt chữ hoa/thường trong lĩnh vực hiện có
- Khớp mờ để tìm các khớp gần
- Nếu độ tin cậy cao: Tự động chọn lĩnh vực đã khớp
- Nếu độ tin cậy thấp: Hiển thị nhiều đề xuất để người dùng chọn

#### 4.5.4 Tạo Lĩnh vực Mới
- AI đề xuất tên lĩnh vực dựa trên nội dung văn bản
- Người dùng có thể chấp nhận hoặc chỉnh sửa tên được đề xuất
- Hệ thống tạo file glossary trống mới cho lĩnh vực đó
- **Quan trọng**: Không tạo glossary mẫu tự động
- Lĩnh vực mới xuất hiện trong danh sách lĩnh vực ngay lập tức
- Người dùng phải tự thêm thuật ngữ vào lĩnh vực mới

---

### 4.6 Bộ Kiểm tra Tính nhất quán

#### 4.6.1 Thuật toán Xác thực
Đối với mỗi thuật ngữ, bộ kiểm tra thực hiện:
1. Đếm tổng số lần xuất hiện trong văn bản tiếng Nhật
2. Đếm tổng số lần xuất hiện trong văn bản tiếng Việt
3. So sánh hai số đếm
4. Ghi lại không khớp nếu số đếm khác nhau

**Quy tắc Chuẩn hóa**
- **Phân biệt Chữ hoa/thường**: 
  - Tiếng Việt: Bỏ qua sự khác biệt về chữ hoa/thường
  - "Hệ thống" bằng "hệ thống"
  - "HỆ THỐNG" bằng "hệ thống"
- **Toàn giác/Bán giác (Tiếng Nhật)**:
  - Phân biệt giữa ký tự toàn giác và bán giác
  - "システム" (toàn giác) KHÔNG bằng "システム" (bán giác)
  - Phải khớp chính xác
- **Toàn giác/Bán giác (Tiếng Việt)**:
  - Không cần phân biệt (tiếng Việt không dùng)

#### 4.6.2 Hiển thị Kết quả
Sau khi kiểm tra, hiển thị dialog popup với:
- Thông báo thành công nếu tất cả thuật ngữ khớp
- Danh sách các trường hợp không khớp nếu tìm thấy
- Với mỗi trường hợp không khớp:
  - Thuật ngữ tiếng Nhật
  - Thuật ngữ tiếng Việt
  - Số lần xuất hiện trong văn bản tiếng Nhật
  - Số lần xuất hiện trong văn bản tiếng Việt
- Nút Close để đóng dialog
- Tùy chọn xuất kết quả ra file (nâng cấp tương lai)

**Ví dụ Nội dung Popup**
- Tiêu đề: "Kiểm tra Tính nhất quán - Trang 1"
- Trạng thái: "Tìm thấy 2 trường hợp không khớp"
- Không khớp 1:
  - Thuật ngữ: システム → Hệ thống
  - Tiếng Nhật: 5 lần xuất hiện
  - Tiếng Việt: 4 lần xuất hiện
- Không khớp 2:
  - Thuật ngữ: 診断 → Chẩn đoán
  - Tiếng Nhật: 3 lần xuất hiện
  - Tiếng Việt: 2 lần xuất hiện

---

### 4.7 Engine Dịch

#### 4.7.1 Ép buộc Thuật ngữ trong Dịch
Engine dịch phải:
- Gộp glossary Common và Domain trước khi dịch
- Áp dụng ưu tiên glossary domain hơn common
- Tạo prompt ép buộc nghiêm ngặt việc sử dụng glossary
- Bao gồm tất cả thuật ngữ trong prompt API
- Hướng dẫn AI sử dụng bản dịch chính xác từ glossary
- Giữ nguyên các dấu 【】 ở vị trí gốc
- Duy trì ngữ pháp tiếng Việt tự nhiên

#### 4.7.2 Logic Gộp Glossary
Khi chuẩn bị dịch:
1. Tải glossary lĩnh vực Common
2. Tải glossary lĩnh vực đã chọn
3. Tạo dictionary đã gộp
4. Với xung đột: Glossary domain ghi đè Common
5. Sử dụng glossary đã gộp để dịch

**Ví dụ**
- Glossary Common: {"システム": "Hệ thống"}
- Glossary Medical: {"システム": "Hệ thống y tế"}
- Kết quả gộp: {"システム": "Hệ thống y tế"} (Medical thắng)

#### 4.7.3 Cấu trúc Prompt Dịch
Prompt gửi đến AI phải bao gồm:
- Định nghĩa vai trò (dịch giả chuyên nghiệp)
- Phần quy tắc glossary quan trọng
- Danh sách tất cả thuật ngữ với bản dịch
- Hướng dẫn tuân thủ nghiêm ngặt glossary
- Hướng dẫn duy trì các dấu định dạng
- Văn bản tiếng Nhật cần dịch
- Yêu cầu đầu ra bản dịch tiếng Việt

---

### 4.8 Quản lý API

#### 4.8.1 Cấu hình API Kép
Ứng dụng yêu cầu hai cấu hình API riêng biệt:

**API Dịch**
- Dùng cho: Dịch nội dung tài liệu
- Nhà cung cấp có thể cấu hình: OpenAI hoặc Gemini
- Người dùng chọn model cụ thể (ví dụ: gpt-4o, gemini-1.5-pro)

**API Phát hiện Lĩnh vực**
- Dùng cho: Xác định lĩnh vực/chủ đề tài liệu
- Nhà cung cấp có thể cấu hình: OpenAI hoặc Gemini
- Người dùng chọn model cụ thể (thường là model nhẹ/nhanh hơn)

#### 4.8.2 Giao diện Cài đặt API
Cửa sổ cài đặt API chứa:
- Hai phần cấu hình riêng biệt (Dịch và Phát hiện Lĩnh vực)
- Với mỗi API:
  - Dropdown chọn nhà cung cấp (OpenAI / Gemini)
  - Trường văn bản API Key (ẩn dưới dạng mật khẩu)
  - Dropdown chọn model
- Nút Import/Export cấu hình
- Nút Save và Cancel

#### 4.8.3 Yêu cầu Bảo mật
- Tất cả API key phải được mã hóa trước khi lưu trữ
- Sử dụng mã hóa đối xứng Fernet từ thư viện cryptography
- Key mã hóa được lưu trong file riêng: data/config/.secret.key
- Không bao giờ hiển thị API key trong UI (hiển thị dưới dạng ẩn: **********)
- API key không bao giờ được đưa vào file export glossary
- API key không bao giờ được đưa vào file session
- API key không bao giờ được ghi vào file log

#### 4.8.4 Theo dõi Sử dụng Token
Ứng dụng phải theo dõi:
- **Sử dụng token mỗi trang**: Token tiêu thụ cho mỗi trang dịch
- **Tổng sử dụng token**: Tổng của tất cả các trang trong phiên hiện tại
- Định dạng hiển thị: "Tokens: 1.5K (Trang) | 15.2K (Tổng)"
- Theo dõi riêng cho API Dịch và API Phát hiện Lĩnh vực
- Lưu số lượng token vào dữ liệu phiên
- Hiển thị trong thanh dưới của cửa sổ chính

**Không Giới hạn Tốc độ**
- Không áp đặt giới hạn nhân tạo trên số lần gọi API
- Theo dõi sử dụng chỉ cho mục đích thông tin
- Để nhà cung cấp API xử lý giới hạn tốc độ
- Hiển thị sử dụng để giúp người dùng quản lý chi phí

---

### 4.9 Quản lý Phiên làm việc

#### 4.9.1 Nội dung Dữ liệu Phiên
Mỗi phiên lưu trữ:
- ID phiên duy nhất (UUID)
- Đường dẫn đến file DOCX gốc
- Tên lĩnh vực đã chọn
- Mảng trang hoàn chỉnh với:
  - ID trang
  - Văn bản tiếng Nhật
  - Văn bản tiếng Việt
  - Trạng thái hoàn thành dịch
  - Token đã sử dụng
- Số trang đang active hiện tại
- Tổng token đã sử dụng
- Timestamp tạo phiên
- Timestamp sửa đổi gần nhất

#### 4.9.2 Hành vi Lưu Phiên
Phiên được tự động lưu khi:
- Người dùng click nút Save
- Người dùng điều hướng sang trang khác
- Người dùng đóng ứng dụng
- Mỗi 5 phút (bộ hẹn giờ tự động lưu)

Quy trình lưu phiên:
- Serialize trạng thái hiện tại thành JSON
- Ghi vào file: data/sessions/{session_id}.json
- Cập nhật timestamp last_modified
- Hiển thị xác nhận ngắn (toast notification)

#### 4.9.3 Hành vi Tải Phiên
Khi khởi động ứng dụng:
- Kiểm tra các file phiên hiện có
- Nếu phiên tồn tại:
  - Hiển thị dialog "Tiếp tục phiên gần nhất?"
  - Hiển thị thông tin phiên: tên file, ngày, phần trăm tiến độ
  - Tùy chọn: Tiếp tục hoặc Bắt đầu Mới
- Nếu người dùng tiếp tục:
  - Tải dữ liệu phiên hoàn chỉnh
  - Khôi phục vị trí trang
  - Khôi phục tất cả bản dịch
  - Tiếp tục từ nơi người dùng dừng lại

#### 4.9.4 Giới hạn Phiên Đơn
- Chỉ một phiên có thể active tại một thời điểm
- Mở file mới yêu cầu lưu phiên hiện tại
- Không thể làm việc trên nhiều tài liệu cùng lúc
- Chuyển phiên yêu cầu xác nhận lưu hoặc hủy

---

### 4.10 Chức năng Export

#### 4.10.1 Tùy chọn Export
Dialog export cung cấp:
- **Checkbox**: Chỉ export các trang đã dịch
  - Khi được chọn: Chỉ các trang có is_translated=true được export
  - Khi không chọn: Tất cả trang được export (trống cho chưa dịch)
- **Checkbox**: Export phiên bản song ngữ
  - Khi được chọn: Mỗi đoạn hiển thị JP sau đó VN
  - Khi không chọn: Chỉ văn bản tiếng Việt
- **Bộ chọn đường dẫn file**: Chọn vị trí và tên file đầu ra
- **Nút Export**: Thực thi export
- **Nút Cancel**: Đóng mà không export

#### 4.10.2 Quy tắc Xử lý Export
Export Tiêu chuẩn (Chỉ tiếng Việt):
- Lấy từng trang đã dịch
- Áp dụng metadata định dạng đã lưu cho văn bản tiếng Việt
- Giữ nguyên font, size, color từ bản gốc
- Duy trì cấu trúc bảng
- Giữ nguyên bullet points và numbering
- Bỏ qua các trang chưa dịch nếu tùy chọn được chọn

Export Song ngữ:
- Với mỗi đoạn:
  - Chèn đoạn văn tiếng Nhật
  - Chèn đoạn văn tiếng Việt bên dưới
  - Áp dụng định dạng gốc cho cả hai
  - Thêm dấu phân cách hoặc khoảng cách nhỏ
- Xen kẽ trong toàn bộ tài liệu

#### 4.10.3 Giữ nguyên Định dạng trong Export
Quy trình export phải:
- Lấy metadata định dạng đã lưu trong khi import
- Áp dụng font family cho văn bản tiếng Việt
- Áp dụng font size cho văn bản tiếng Việt
- Áp dụng màu chữ (giá trị RGB)
- Áp dụng kiểu in đậm/in nghiêng
- Tái tạo cấu trúc bảng với cùng độ rộng cột
- Giữ nguyên kiểu bullet point
- Giữ nguyên định dạng đánh số
- Duy trì khoảng cách và thụt lề đoạn văn

---

## 5. XỬ LÝ LỖI

### 5.1 Lỗi Thao tác File

**File DOCX Không hợp lệ**
- Phát hiện file DOCX bị hỏng hoặc không hợp lệ
- Hiển thị thông báo lỗi cụ thể giải thích vấn đề
- Ví dụ: "File bị hỏng", "Không phải định dạng DOCX hợp lệ"
- Đề xuất hành động của người dùng: kiểm tra file, thử lưu lại, chuyển đổi từ DOC

**Lỗi Quyền File**
- Phát hiện khi không thể đọc file
- Hiển thị lỗi: "Không thể truy cập file. Kiểm tra quyền file."
- Đề xuất đóng file trong các ứng dụng khác

**Cảnh báo File Lớn**
- Với file trên 100 trang:
  - Hiển thị dialog cảnh báo
  - Ước lượng thời gian xử lý
  - Hiển thị thanh tiến trình trong khi xử lý
  - Cho phép người dùng hủy

### 5.2 Lỗi Thao tác API

**API Key Không hợp lệ**
- Phát hiện lỗi xác thực
- Hiển thị thông báo lỗi: "API key không hợp lệ cho [Nhà cung cấp]"
- Tự động mở dialog Cài đặt API
- Làm nổi bật trường API key có vấn đề

**Hết thời gian Kết nối**
- Phát hiện lỗi hết thời gian kết nối mạng
- Hiển thị thông báo lỗi với thời gian hết hạn
- **Không tự động thử lại**
- Cung cấp nút Retry để người dùng thử lại thủ công

**Giới hạn Tốc độ API**
- Phát hiện lỗi giới hạn tốc độ từ nhà cung cấp
- Hiển thị lỗi với chi tiết giới hạn tốc độ
- Hiển thị thời gian chờ ước tính nếu được cung cấp
- Đề xuất người dùng chờ hoặc kiểm tra quota API

**Phản hồi API Không hợp lệ**
- Phát hiện phản hồi sai định dạng hoặc không mong đợi
- Ghi chi tiết lỗi đầy đủ vào error.log
- Hiển thị thông báo thân thiện với người dùng: "Dịch thất bại. Vui lòng thử lại."
- Đề nghị lưu kết quả một phần

### 5.3 Lỗi Thao tác Dữ liệu

**Trùng lặp Glossary**
- Ngăn chặn lưu thuật ngữ trùng lặp trong cùng lĩnh vực
- Làm nổi bật mục trùng lặp
- Hiển thị thuật ngữ hiện có với cùng văn bản tiếng Nhật
- Đề nghị chỉnh sửa thuật ngữ hiện có thay thế

**Định dạng CSV Không hợp lệ**
- Phát hiện CSV sai định dạng trong khi import
- Hiển thị lỗi với số dòng cụ thể
- Hiển thị ví dụ định dạng mong đợi
- Cho phép người dùng sửa file và thử lại

**Lỗi Tải Phiên**
- Phát hiện file phiên bị hỏng
- Hiển thị lỗi: "Không thể tải phiên đã lưu"
- Đề nghị bắt đầu phiên mới
- Tùy chọn thử khôi phục hoặc xóa phiên bị hỏng

### 5.4 Ghi Log Lỗi
- Tất cả lỗi được ghi vào: data/logs/error.log
- Định dạng log bao gồm:
  - Timestamp
  - Loại lỗi
  - Thông báo lỗi
  - Stack trace (cho developers)
  - Hành động người dùng tại thời điểm lỗi
- File log tự động xoay vòng khi vượt quá 10MB
- Giữ 5 file log gần nhất

---

## 6. YÊU CẦU GIAO DIỆN NGƯỜI DÙNG

### 6.1 Thiết kế Trực quan

**Theme**
- Mặc định: Dark mode
- Bảng màu: Hiện đại, độ tương phản cao
- Nền: Xám đậm (#1E1E1E)
- Chữ: Xám sáng (#CCCCCC)
- Màu nhấn: Xanh dương (#0078D4)
- Màu lỗi: Đỏ (#E74856)
- Màu thành công: Xanh lá (#107C10)

**Typography (Kiểu chữ)**
- Font mặc định hệ thống
- Phải hỗ trợ ký tự tiếng Nhật (MS Gothic, Yu Gothic, v.v.)
- Phải hỗ trợ ký tự tiếng Việt có dấu
- Kích thước font: 
  - Văn bản thân: 11pt
  - Tiêu đề: 14pt
  - Nhãn UI: 9pt

**Khoảng cách**
- Padding nhất quán: 8px tiêu chuẩn, 16px lớn
- Lề giữa các phần: 16px
- Khoảng cách nút: 8px giữa các nút

### 6.2 Chỉ báo Tiến trình

**Thanh Tiến trình Bắt buộc Cho**
- Upload file và chuyển đổi DOCX sang Markdown
- Các lần gọi dịch API (mỗi trang)
- Dịch nhập hàng loạt (xử lý batch)
- Tạo export DOCX
- Xử lý file lớn (trên 100 trang)

**Định dạng Thanh Tiến trình**
- Thanh ngang với phần trăm
- Văn bản mô tả bên dưới thanh
- Ví dụ: "[████████░░] 80% - Đang dịch trang 20/25"
- Thời gian còn lại ước tính (khi có thể tính)
- Nút Cancel khi phù hợp

**Trạng thái Đang tải**
- Spinner cho các thao tác ngắn (dưới 3 giây)
- Vô hiệu hóa các yếu tố UI trong khi xử lý
- Thay đổi con trỏ thành con trỏ đang tải
- Ngăn tương tác người dùng trong các thao tác quan trọng

### 6.3 Hành vi Cửa sổ

**Cửa sổ Chính**
- Kích thước tối thiểu: 1200px chiều rộng × 800px chiều cao
- Có thể thay đổi kích thước bởi người dùng
- Nhớ kích thước và vị trí cuối cùng
- Khôi phục khi khởi động lại ứng dụng

**Thay đổi Kích thước Panel**
- Thanh bên trái: Có thể thay đổi kích thước, tối thiểu 150px
- Thanh bên phải: Có thể thay đổi kích thước, tối thiểu 200px
- Panel trung tâm: Có thể thay đổi kích thước giữa JP và VN
- Thanh phân cách có thể kéo

**Bố cục Responsive**
- Thích ứng với thay đổi kích thước cửa sổ
- Duy trì kích thước tối thiểu có thể đọc
- Thu gọn thanh bên khi cửa sổ quá nhỏ
- Hiển thị nút thu gọn/mở rộng

### 6.4 Yêu cầu Tương tác

**Không có Phím tắt**
- Tất cả tương tác qua chuột/nút
- Không yêu cầu triển khai phím tắt
- Phím tắt chỉnh sửa văn bản tiêu chuẩn hoạt động trong vùng văn bản (Ctrl+C, Ctrl+V, v.v.)

**Trạng thái Nút**
- Bình thường, Hover, Nhấn, Vô hiệu hóa
- Phản hồi trực quan khi click
- Vô hiệu hóa nút trong khi xử lý
- Tooltip khi hover hiển thị chức năng nút

**Hành vi Dialog**
- Dialog modal chặn cửa sổ chính
- Dialog không modal cho phép tương tác nền
- Dialog xác nhận cho các hành động phá hủy
- Phím ESC đóng dialog (khi phù hợp)

---

## 7. TỔ CHỨC FILE

### 7.1 Cấu trúc Thư mục
Ứng dụng tạo và quản lý các thư mục này:

**Thư mục Gốc**
- main.py: Điểm vào ứng dụng
- requirements.txt: Phụ thuộc Python
- README.md: Tài liệu người dùng
- .gitignore: Quy tắc bỏ qua Git

**Thư mục data/** (Được tạo khi chạy lần đầu, loại trừ khỏi git)
- glossary/: Tất cả file JSON glossary
  - common.json
  - medical.json
  - legal.json
  - it.json
  - (các lĩnh vực do người dùng tạo)
- sessions/: File lưu phiên
  - {session_id}.json cho mỗi phiên
- config/: File cấu hình
  - .secret.key: Key mã hóa (QUAN TRỌNG: không bao giờ commit)
  - api_config.json: Cài đặt API đã mã hóa
- temp/: File làm việc tạm thời
  - Xóa khi đóng ứng dụng
- logs/: Log lỗi và hoạt động
  - error.log: Ghi log lỗi

**Thư mục src/** (Mã nguồn)
- ui/: Các component giao diện người dùng
- core/: Các module logic nghiệp vụ
- data/: Tầng truy cập dữ liệu
- utils/: Các hàm tiện ích

**Thư mục tests/** (Kiểm thử đơn vị)
- File test cho mỗi module

### 7.2 Quy ước Đặt tên File
- File phiên: session_{timestamp}_{uuid}.json
- File đã export: {tên_gốc}_vn.docx hoặc {tên_gốc}_bilingual.docx
- File log: error_{date}.log
- File glossary: {tên_lĩnh_vực}.json

---

## 8. PHỤ THUỘC

### 8.1 Các Gói Python Bắt buộc
Ứng dụng yêu cầu các gói Python sau:

**Framework UI**
- customtkinter phiên bản 5.2.0 trở lên

**Xử lý Tài liệu**
- python-docx phiên bản 1.1.0 trở lên
- markdown phiên bản 3.5.1 trở lên

**Tích hợp AI**
- openai phiên bản 1.12.0 trở lên
- google-generativeai phiên bản 0.3.2 trở lên

**Bảo mật**
- cryptography phiên bản 41.0.7 trở lên

**Tiện ích**
- python-dateutil phiên bản 2.8.2 trở lên

**Kiểm thử**
- pytest phiên bản 7.4.3 trở lên
- pytest-cov phiên bản 4.1.0 trở lên

### 8.2 Phiên bản Python
- Tối thiểu: Python 3.10
- Khuyến nghị: Python 3.11 trở lên
- Không tương thích với: Python 3.9 trở xuống

### 8.3 Hệ điều hành
- Windows 10 trở lên
- macOS 10.15 trở lên
- Linux (Ubuntu 20.04 hoặc tương đương)

---

## 9. ĐỘ ƯU TIÊN TRIỂN KHAI

### Giai đoạn 1: Nền tảng (QUAN TRỌNG - Phải Hoàn thành Đầu tiên)
Các tính năng này cần thiết cho chức năng cơ bản:
1. Thiết lập cấu trúc dự án và cấu hình
2. Bộ xử lý tài liệu (chuyển đổi DOCX sang Markdown)
3. Phân đoạn văn bản theo mẫu 【text】
4. Khung UI cơ bản với CustomTkinter
5. Quản lý cấu hình với mã hóa

### Giai đoạn 2: Tính năng Cốt lõi (CAO - Chức năng Chính)
Các tính năng này cho phép quy trình dịch cốt lõi:
6. Repository glossary với lưu trữ JSON
7. UI dịch chính (chế độ xem chia JP/VN)
8. Tích hợp API để dịch
9. Hệ thống điều hướng trang
10. Chức năng lưu và tải phiên

### Giai đoạn 3: Tính năng Nâng cao (TRUNG BÌNH - Chức năng Cải tiến)
Các tính năng này cải thiện khả năng sử dụng và hiệu quả:
11. Giao diện người dùng quản lý glossary
12. Nhập hàng loạt với dịch AI
13. Triển khai bộ kiểm tra tính nhất quán
14. Hiển thị glossary thanh bên phải
15. Export sang DOCX với giữ nguyên định dạng

### Giai đoạn 4: Hoàn thiện (THẤP - Tốt để Có)
Các tính năng này nâng cao trải nghiệm người dùng:
16. Tính năng phát hiện lĩnh vực
17. Hiển thị theo dõi token
18. Thanh tiến trình và chỉ báo đang tải
19. Xử lý lỗi toàn diện
20. Tinh chỉnh theme dark mode

---

## 10. YÊU CẦU KIỂM THỬ

### 10.1 Kiểm thử Đơn vị
Các kiểm thử đơn vị bắt buộc cho:
- Bộ xử lý tài liệu (độ chính xác chuyển đổi)
- Các thao tác glossary (CRUD, gộp, phát hiện trùng lặp)
- Bộ kiểm tra tính nhất quán (đếm thuật ngữ với chuẩn hóa)
- Chức năng lưu và tải phiên
- Xử lý lỗi client API
- Mã hóa và giải mã

### 10.2 Kiểm thử Tích hợp
Các kiểm thử tích hợp bắt buộc cho:
- Quy trình dịch hoàn chỉnh từ đầu đến cuối
- Tích hợp API với phản hồi giả lập
- Tương tác component UI
- Lưu trữ dữ liệu qua các phiên
- Xử lý tài liệu nhiều trang

### 10.3 Danh sách Kiểm thử Thủ công
Trước khi phát hành, xác minh thủ công:
- Upload các định dạng và kích thước DOCX khác nhau
- Kiểm thử với tài liệu trên 100 trang
- Xác minh giữ nguyên định dạng (fonts, colors, tables)
- Kiểm thử nhập hàng loạt glossary với xung đột thuật ngữ
- Xác minh độ chính xác bộ kiểm tra tính nhất quán trên các văn bản khác nhau
- Kiểm thử tiếp tục phiên sau khi đóng ứng dụng bắt buộc
- Export tài liệu song ngữ và xác minh định dạng
- Kiểm thử tất cả các tình huống lỗi API
- Xác minh mã hóa API key
- Kiểm thử trên các hệ điều hành khác nhau
- Xác minh render ký tự tiếng Nhật và tiếng Việt

---

## 11. GIỚI HẠN ĐÃ BIẾT

Người dùng nên biết về các giới hạn này:

### 11.1 Tính năng Tài liệu Không Hỗ trợ
- **Hình ảnh**: Bị bỏ qua và không bao gồm trong bản dịch
- **Header và Footer**: Có thể không giữ hoàn hảo trong tất cả trường hợp
- **Track Changes**: Không hỗ trợ, các thay đổi sẽ được chấp nhận
- **Comments**: Không được giữ trong bản dịch
- **Đối tượng Nhúng**: Biểu đồ, sơ đồ sẽ bị bỏ qua
- **Macro**: Sẽ bị xóa trong khi chuyển đổi

### 11.2 Giới hạn Hiệu năng
- **File Lớn**: Tài liệu trên 100 trang có thể chậm
- **Sử dụng Bộ nhớ**: Tài liệu rất lớn có thể tiêu thụ RAM đáng kể
- **Tốc độ API**: Tốc độ dịch phụ thuộc vào thời gian phản hồi nhà cung cấp API

### 11.3 Giới hạn Chức năng
- **Phiên Đơn**: Không thể làm việc trên nhiều tài liệu cùng lúc
- **Yêu cầu Internet**: Phải có kết nối internet cho các lần gọi API
- **Phụ thuộc API**: Các tính năng phụ thuộc vào tính khả dụng API bên ngoài
- **Xem xét Thủ công**: Bản dịch AI có thể yêu cầu xem xét của con người để đảm bảo độ chính xác

### 11.4 Giới hạn Kỹ thuật
- **Bảng Phức tạp**: Định dạng bảng rất phức tạp có thể có vấn đề nhỏ
- **Font Tùy chỉnh**: Font không tiêu chuẩn có thể không giữ nếu không được cài đặt
- **Văn bản Từ phải sang trái**: Không được thiết kế cho ngôn ngữ RTL
- **Ngôn ngữ Hỗn hợp**: Tốt nhất cho tài liệu chủ yếu bằng tiếng Nhật

---

## 12. CẢI TIẾN TƯƠNG LAI (NGOÀI PHẠM VI)

Các tính năng này không được bao gồm trong phiên bản hiện tại nhưng có thể được xem xét cho các bản phát hành tương lai:

### 12.1 Xử lý Hàng loạt
- Xử lý nhiều tài liệu trong hàng đợi
- Dịch hàng loạt tự động qua đêm
- Export hàng loạt nhiều tài liệu

### 12.2 Tích hợp Đám mây
- Lưu trữ đám mây cho glossary (Google Drive, Dropbox)
- Sao lưu đám mây các phiên
- Đồng bộ glossary qua các thiết bị

### 12.3 Tính năng Cộng tác
- Dự án dịch đa người dùng
- Cộng tác thời gian thực
- Hệ thống nhận xét và xem xét
- Kiểm soát phiên bản cho bản dịch

### 12.4 Tính năng AI Nâng cao
- Đào tạo model AI tùy chỉnh
- Cải thiện tự động phát hiện lĩnh vực
- Chấm điểm chất lượng dịch
- Đề xuất chỉnh sửa sau tự động

### 12.5 Định dạng Bổ sung
- Export PDF với văn bản có thể tìm kiếm
- Export HTML để xuất bản web
- Định dạng XLIFF cho công cụ CAT
- Định dạng TMX cho bộ nhớ dịch

### 12.6 UI Nâng cao
- Phiên bản ứng dụng di động
- Giao diện dựa trên web
- Tùy chọn theme sáng
- Bảng màu tùy chỉnh
- Phím tắt có thể cấu hình

---

## 13. TRIỂN KHAI

### 13.1 Định dạng Phân phối
- File thực thi độc lập (không yêu cầu cài đặt Python)
- Đóng gói bằng PyInstaller
- Tất cả phụ thuộc được gộp
- Ưu tiên file thực thi đơn

### 13.2 Quy trình Cài đặt
- Tải file thực thi
- Không cần trình hướng dẫn cài đặt
- Chế độ di động (chạy từ bất kỳ thư mục nào)
- Trình hướng dẫn thiết lập lần chạy đầu tiên cho cấu hình API
- Tự động tạo thư mục dữ liệu

### 13.3 Cơ chế Cập nhật
- Tải xuống và thay thế file thực thi thủ công
- Hiển thị phiên bản hiện tại trong dialog Giới thiệu
- Tùy chọn: Kiểm tra cập nhật khi khởi động (cải tiến tương lai)

### 13.4 Gỡ cài đặt
- Xóa file thực thi
- Tùy chọn xóa thư mục dữ liệu
- Không có mục nhập registry hoặc sửa đổi hệ thống
- Gỡ cài đặt sạch mà không để lại dư lượng

---

## 14. THUẬT NGỮ KỸ THUẬT

### Thuật ngữ Cụ thể Ứng dụng

| Thuật ngữ | Tiếng Nhật | Tiếng Việt | Mô tả |
|-----------|------------|------------|-------|
| Segment | 段落 (danraku) | Đoạn văn | Khối văn bản bắt đầu với dấu 【text】 |
| Domain | 分野 (bunya) | Lĩnh vực | Khu vực chủ đề hoặc lĩnh vực chuyên môn |
| Glossary | 用語集 (yōgoshū) | Bộ thuật ngữ | Từ điển thuật ngữ chuyên môn |
| Page | ページ (pēji) | Trang | Trang UI chứa một hoặc nhiều đoạn |
| Session | セッション (sesshon) | Phiên làm việc | Trạng thái công việc đã lưu với tiến độ |
| Consistency | 一貫性 (ikkansei) | Tính nhất quán | Khớp sử dụng thuật ngữ giữa các ngôn ngữ |

### Thuật ngữ Kỹ thuật

| Thuật ngữ | Mô tả |
|-----------|-------|
| DOCX | Định dạng tài liệu Microsoft Word Open XML |
| Markdown | Ngôn ngữ đánh dấu nhẹ để định dạng |
| API | Giao diện Lập trình Ứng dụng |
| Token | Đơn vị văn bản được xử lý bởi AI (khoảng 4 ký tự) |
| Encryption | Quá trình mã hóa dữ liệu để bảo mật |
| JSON | JavaScript Object Notation (định dạng dữ liệu) |
| CSV | Comma-Separated Values (định dạng bảng tính) |

---

## 15. TIÊU CHUẨN CHẤT LƯỢNG

### 15.1 Chất lượng Dịch
- Thuật ngữ glossary phải được áp dụng nhất quán 100%
- Yêu cầu ngữ pháp tiếng Việt tự nhiên
- Giữ độ chính xác kỹ thuật
- Duy trì ý nghĩa và giọng điệu gốc

### 15.2 Giữ nguyên Định dạng
- Font phải khớp chính xác với bản gốc
- Màu sắc phải được giữ chính xác
- Cấu trúc bảng phải còn nguyên vẹn
- Kiểu bullet và numbering phải khớp

### 15.3 Hiệu năng Ứng dụng
- Khởi động ứng dụng: Dưới 5 giây
- Điều hướng trang: Tức thì (dưới 0.5 giây)
- Thao tác lưu: Dưới 2 giây
- Xử lý phản hồi API: Hiển thị trong vòng 1 giây sau khi nhận

### 15.4 Độ tin cậy
- Không mất dữ liệu trong hoạt động bình thường
- Tự động lưu ngăn mất công việc
- Khôi phục phiên sau khi đóng bất ngờ
- Ghi log lỗi cho tất cả lỗi

### 15.5 Bảo mật
- API key được mã hóa khi lưu trữ
- Không có dữ liệu nhạy cảm trong log
- Không truyền dữ liệu ngoại trừ đến nhà cung cấp AI đã chọn
- Xóa an toàn các file tạm thời

---

## 16. YÊU CẦU TÀI LIỆU

### 16.1 Tài liệu Người dùng
Phải bao gồm:
- Hướng dẫn cài đặt
- Hướng dẫn bắt đầu
- Giải thích tính năng với ảnh chụp màn hình
- Hướng dẫn quản lý glossary
- Hướng dẫn cấu hình API
- Khắc phục sự cố thông thường
- Phần câu hỏi thường gặp

### 16.2 Tài liệu Kỹ thuật
Phải bao gồm:
- Tổng quan kiến trúc
- Đặc tả cấu trúc dữ liệu
- Chi tiết tích hợp API
- Đặc tả định dạng file
- Tham chiếu mã lỗi
- Hướng dẫn thiết lập phát triển

### 16.3 Video Hướng dẫn
Các chủ đề được đề xuất:
- Thiết lập và cấu hình lần đầu
- Quy trình dịch cơ bản
- Quản lý glossary
- Sử dụng nhập hàng loạt
- Kiểm tra tính nhất quán

---

## 17. HỖ TRỢ VÀ BẢO TRÌ

### 17.1 Hỗ trợ Người dùng
- File README với các vấn đề thường gặp
- Thông báo lỗi với đề xuất hữu ích
- Tài liệu trợ giúp tích hợp
- Phần câu hỏi thường gặp trong ứng dụng

### 17.2 Kế hoạch Bảo trì
- Sửa lỗi khi cần
- Cập nhật bảo mật cho phụ thuộc
- Cập nhật tương thích cho phiên bản OS mới
- Cập nhật tích hợp API cho thay đổi nhà cung cấp

### 17.3 Thu thập Phản hồi
- Nút phản hồi trong ứng dụng (tương lai)
- Tạo báo cáo lỗi
- Thống kê sử dụng (chỉ khi chọn tham gia)

---

## 18. TUÂN THỦ VÀ TIÊU CHUẨN

### 18.1 Quyền riêng tư Dữ liệu
- Không gửi dữ liệu đến máy chủ bên ngoài trừ API AI
- Người dùng kiểm soát tất cả dữ liệu cục bộ
- Không có telemetry hoặc analytics
- API key không bao giờ được chia sẻ

### 18.2 Cấp phép
- Điều khoản cấp phép rõ ràng cho phần mềm
- Ghi công cho phụ thuộc mã nguồn mở
- Thỏa thuận người dùng cho sử dụng API AI

### 18.3 Khả năng Tiếp cận
- UI độ tương phản cao cho khả năng hiển thị
- Vùng văn bản có thể thay đổi kích thước
- Thông báo lỗi rõ ràng
- Điều hướng bàn phím trong trường văn bản

---

## LỊCH SỬ PHIÊN BẢN

- **Phiên bản 1.0.0** - Tài liệu đặc tả ban đầu
- **Ngày**: 2024-01-XX
- **Trạng thái**: Bản nháp để Phát triển

---

## KIỂM SOÁT TÀI LIỆU

- **Loại Tài liệu**: Đặc tả Yêu cầu
- **Mục đích**: Hướng dẫn phát triển phần mềm
- **Đối tượng**: Nhóm phát triển, các bên liên quan dự án
- **Bảo trì**: Cập nhật khi yêu cầu phát triển
- **Yêu cầu Phê duyệt**: Có, trước khi bắt đầu triển khai

---

**KẾT THÚC ĐẶC TẢ YÊU CẦU**

Tài liệu này định nghĩa tất cả yêu cầu cho Ứng dụng Dịch Tài liệu Chuyên ngành Nhật-Việt. Việc triển khai phải tuân theo đặc tả này. Các thay đổi yêu cầu tài liệu và cập nhật phiên bản.