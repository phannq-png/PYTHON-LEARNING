# 📋 Project Blueprint — Quy trình Triển khai Dự án Chuẩn

Tài liệu này tổng hợp toàn bộ các quy tắc, quy trình và vai trò đã được thiết lập để đảm bảo dự án được phát triển một cách nhất quán, chất lượng và dễ dàng quản lý bởi sự phối hợp giữa Project Owner (P) và các AI Agents.

---

## 1. Đội ngũ AI Agents (Roles)

Hệ thống sử dụng các Agent chuyên biệt với vai trò rõ ràng:
- **PM (Project Manager):** Theo dõi tiến độ tổng thể, báo cáo trạng thái hoàn thành các Feature/Task. KHÔNG viết code, chỉ Read-only.
- **BA (Business Analyst & System Architect):** Phân tích nghiệp vụ, phân rã yêu cầu từ `requirement.md` thành các Feature và Task chi tiết. Thiết kế cấu trúc thư mục yêu cầu và duy trì tài liệu kiến trúc.
- **TL (Technical Leader):** Review code, kiểm soát kiến trúc, đảm bảo tuân thủ convention và bảo mật. Tạo Issue cho các vấn đề kỹ thuật.
- **Developer:** Thực hiện triển khai tính năng theo kế hoạch đã được phê duyệt.
- **Tester:** Thực thi kịch bản kiểm thử, phát hiện lỗi và tạo Issue trên GitHub.

---

## 2. Quy trình Khởi tạo Dự án Mới (Project Bootstrap)

Để bắt đầu một dự án mới ngay lập tức, hãy thực hiện theo thứ tự sau:
1. **Bước 1 (Khởi tạo Repo):** Tạo repository mới trên GitHub, clone về máy.
2. **Bước 2 (Import Agents):** Copy toàn bộ thư mục `.antigravity/` (chứa `PROJECT_BLUEPRINT.md` và các file `Agent.md`) từ dự án chuẩn sang dự án mới.
3. **Bước 3 (Định nghĩa Yêu cầu):** Project Owner (P) viết file `docs/requirements/requirement.md` mô tả tổng quan dự án.
4. **Bước 4 (Thiết kế Kiến trúc):** Tạo các file định hướng kỹ thuật ban đầu (VD: `docs/architecture/system-architecture.md`, `docs/styleguides/frontend-styleguide.md`).
5. **Bước 5 (Phân rã Task):** Gọi Agent **BA** thực hiện đọc `requirement.md` và sinh ra cấu trúc thư mục Feature/Task.
6. **Bước 6 (Bắt đầu Code):** Gọi Agent **Developer** thực hiện từng Task theo quy trình 3 Bước.

---

## 3. Quy trình Quản lý Yêu cầu (Requirements Management)

Mọi dự án bắt đầu bằng việc phân rã yêu cầu:
- **Nguồn sự thật (SSOT):** File `docs/requirements/requirement.md`.
- **Cấu trúc thư mục:**
  - Mỗi tính năng lớn là một thư mục: `[Số thứ tự]-[Tên-Feature]` (VD: `01-authentication`).
  - Trong mỗi Feature có 2 thư mục con: `opening/` (Task đang/chưa làm) và `closed/` (Task đã xong).
  - Tên file task: `task-[Số thứ tự]-[Tên-Task].md`.
- **Nội dung Task:** Phải cực kỳ chi tiết bao gồm: Mô tả, Tiêu chí hoàn thành (Acceptance Criteria), Ghi chú kỹ thuật và Kịch bản kiểm thử (Test Cases).

---

## 3. Quy trình Triển khai 3 Bước (Critical Workflow)

Mọi Agent thực hiện nhiệm vụ thay đổi mã nguồn/tài liệu phải tuân thủ:
1. **Bước 1: Làm rõ yêu cầu (Clarify) ❓**
   - DỪNG LẠI và HỎI P nếu có bất kỳ điểm nào chưa rõ. Không tự ý đoán.
2. **Bước 2: Trình kế hoạch thực hiện (Plan) 📋**
   - Soạn thảo kế hoạch chi tiết các file sẽ thêm/sửa/xóa và phương pháp tiếp cận.
   - Chờ P phản hồi "OK" hoặc "Go ahead" mới được thực hiện.
3. **Bước 3: Thực thi sau khi được duyệt (Execute) ✅**
   - Triển khai đúng như kế hoạch. Nếu phát hiện vấn đề phát sinh, phải dừng lại báo cáo P.

---

## 4. Quy tắc Ngôn ngữ & Coding Standards

- **Ngôn ngữ:**
  - **Tiếng Việt:** Dùng cho toàn bộ trao đổi với P, tài liệu `.md`, commit message và comment giải thích nghiệp vụ.
  - **Tiếng Anh:** Dùng cho Code (biến, hàm, class), tên API endpoints và comment kỹ thuật.
- **Git & Commit:**
  - Sử dụng **Conventional Commits**: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`.
  - Một thay đổi logic mỗi commit. Subject dưới 50 ký tự.
- **An toàn & Bảo mật:**
  - KHÔNG đưa Secret (API Key, Password) vào code. Sử dụng `.env`.
  - Các hành động phá hủy (Xóa file, Drop DB) phải yêu cầu xác nhận cụ thể bằng từ khóa (VD: "DELETE CONFIRMED").

---

## 5. Quy trình Kiểm soát Chất lượng (Review & Test)

- **Review:** Mọi Pull Request phải được **TL** review. TL sử dụng GitHub CLI (`gh pr review`) để approve hoặc request changes.
- **Issue Tracking:** Sử dụng GitHub Issues để quản lý Bug và các vấn đề phát sinh. Sử dụng label (`bug`, `review`, `security`, `performance`) để phân loại.
- **Testing:** **Tester** đối chiếu thực tế với AC trong Task. Chỉ khi đạt toàn bộ AC mới được chuyển task sang `closed/`.

---

## 7. Quản lý Tài liệu Kỹ thuật (Technical Documentation)

Dự án cần duy trì các tài liệu kỹ thuật làm kim chỉ nam cho Dev:
- **Architecture:** `docs/architecture/system-architecture.md` (Sơ đồ hệ thống, công nghệ cốt lõi).
- **Styleguides:** `docs/styleguides/` (Các quy chuẩn code riêng cho Frontend, Backend, Database).
- Mọi Agent Code phải tuân thủ nghiêm ngặt các Styleguide này trong quá trình thực thi.

---

## 8. Luồng làm việc Git cho Tài liệu

Đối với các Agent quản lý tài liệu (như **BA**):
- Luôn pull bản mới nhất từ `develop`.
- Commit trực tiếp lên `develop` (không qua PR cho tài liệu yêu cầu).
- Sử dụng scope `docs(requirements)` trong commit message.

---
*Tài liệu này là "Sổ tay vận hành" dành cho mọi dự án mới theo mô hình P & AI Agents.*
