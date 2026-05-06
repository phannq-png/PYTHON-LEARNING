# Quy trình làm việc với Git (Git Workflow)

Tài liệu này tổng hợp các quy tắc và quy trình chuẩn về việc quản lý phiên bản (version control) bằng Git, cách viết commit và luồng làm việc trên repository của dự án.

---

## 1. Định dạng Commit (Conventional Commits)

Dự án tuân thủ nghiêm ngặt chuẩn [Conventional Commits](https://conventionalcommits.org).

- **Cấu trúc chung:** `<type>(<scope>): <subject>`
- **Ngôn ngữ:** **Tiếng Anh** (Bắt buộc cho code comments, tiêu đề commit, nội dung chi tiết commit, và PR/Issue descriptions).

### 1.1. Các loại Commit (Types)
- `feature`: Tính năng mới.
- `fix`: Sửa lỗi (bug fix).
- `docs`: Thêm hoặc cập nhật tài liệu (documentation).
- `style`: Định dạng code (thụt lề, thiếu chấm phẩy, khoảng trắng... không làm thay đổi logic).
- `refactor`: Tái cấu trúc mã nguồn (không thêm tính năng mới, không sửa bug).
- `test`: Thêm mới hoặc sửa chữa các test cases.
- `chore`: Công việc bảo trì (cập nhật thư viện/dependencies, cấu hình hệ thống...).

### 1.2. Quy tắc quan trọng
- Chỉ gộp **MỘT thay đổi logic duy nhất** vào mỗi commit.
- Tiêu đề commit (subject line) **phải dưới 50 ký tự**.
- Sử dụng thể mệnh lệnh ở tiêu đề bằng Tiếng Anh (ví dụ: dùng từ "add" thay vì "added" hoặc "adds").
- **Không** sử dụng dấu chấm (`.`) ở cuối tiêu đề.

### 1.3. Ví dụ tiêu biểu
```text
feature(auth): implement OTP login flow
fix(tree): resolve lazy loading race condition
docs(api): update person endpoint documentation
refactor(notification): extract Zalo service to separate module
```

---

## 2. Chiến lược Phân bổ Nhánh (Branching Strategy) & Pull Request (PR)

### 2.1. Các nhánh chính (Main Branches)
- `main` (hoặc `master`): Nhánh chứa mã nguồn ổn định nhất, sẵn sàng cho môi trường Production. **Tuyệt đối KHÔNG** commit trực tiếp lên nhánh này.
- `develop`: Nhánh tích hợp chính cho môi trường phát triển (Development). Toàn bộ tính năng mới và bản vá lỗi sau khi hoàn thiện sẽ được merge vào đây.

### 2.2. Các nhánh hỗ trợ (Supporting Branches)
- **Nhánh Feature (`feature/<tên-tính-năng>`):**
  - Mục đích: Phát triển các tính năng hoặc task mới.
  - Tách ra từ: `develop`
  - Merge vào: `develop`
  - *Ví dụ:* `feature/auth-otp`, `feature/tree-navigation`
- **Nhánh Sửa lỗi (`fix/<tên-lỗi>` hoặc `bugfix/<tên-lỗi>`):**
  - Mục đích: Sửa các lỗi phát sinh trong quá trình phát triển hoặc kiểm thử.
  - Tách ra từ: `develop`
  - Merge vào: `develop`
  - *Ví dụ:* `fix/lazy-load-race-condition`
- **Nhánh Hotfix (`hotfix/<tên-lỗi-nghiêm-trọng>`):**
  - Mục đích: Vá các lỗi khẩn cấp đang xảy ra trên môi trường Production.
  - Tách ra từ: `main`
  - Merge vào: Cả `main` và `develop` (để đồng bộ code).
  - *Ví dụ:* `hotfix/login-crash`

### 2.3. Quy trình Pull Request (PR) và Review Code
- Mọi thay đổi từ các nhánh hỗ trợ (`feature`, `fix`, `hotfix`) muốn đưa vào nhánh chính đều phải thông qua **Pull Request (PR)**.
- **Review Code (Bắt buộc):**
  - Mọi Pull Request (PR) chứa thay đổi mã nguồn bắt buộc phải được Agent **TL (Technical Leader)** đánh giá và duyệt.
  - Quá trình review đánh giá 4 tiêu chí cốt lõi: tuân thủ convention, logic nghiệp vụ, lỗ hổng bảo mật và hiệu năng/tối ưu.
  - PR chỉ được phép merge sau khi nhận được trạng thái "Approve" rõ ràng từ TL.

---

## 3. Luồng làm việc Git dành riêng cho Tài liệu (Documentation)

Đối với các Agent đảm nhận vai trò quản lý tài liệu, phân rã yêu cầu (như Agent **BA**):

- Luôn thực hiện `git pull` bản mới nhất từ nhánh `develop` trước khi tiến hành chỉnh sửa.
- Được phép **commit trực tiếp** lên nhánh `develop` (không yêu cầu qua Pull Request đối với tài liệu phân rã requirements).
- Bắt buộc sử dụng scope là `docs(requirements)` trong thông điệp commit.
  - *Ví dụ:* `docs(requirements): create folder structure for authentication feature`

---

## 4. Quản lý Vấn đề (Issue Tracking)

- Mọi lỗi (bug), lỗ hổng bảo mật hoặc cơ hội cải thiện hiệu năng được phát hiện đều phải được lưu trữ dưới dạng **Issue trên GitHub**.
- Các Issue phải được gắn label (nhãn) rõ ràng để phân loại, ví dụ: `bug`, `review`, `security`, `performance`.
- Agent TL sẽ có trách nhiệm tạo Issue với báo cáo chi tiết. Agent Developer sẽ nhận và giải quyết Issue này theo **Quy trình Triển khai 3 Bước (Critical Workflow)**.
