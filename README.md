# TaskFlow — Quản lý công việc cá nhân

TaskFlow là ứng dụng web quản lý công việc cá nhân được xây dựng phục vụ học tập môn Nhập môn Công nghệ phần mềm (IT3180). Người dùng có thể tạo, xem, cập nhật trạng thái, lọc và xóa công việc. Dữ liệu được lưu bằng SQLite.

> Đây là dự án học tập, không phải hệ thống production. Ứng dụng hiện chưa có tài khoản, phân quyền hoặc đồng bộ nhiều người dùng.

## 1. Công nghệ

| Thành phần | Công nghệ | Vai trò |
|---|---|---|
| Frontend | HTML5, CSS3, JavaScript | Giao diện và gọi REST API |
| Backend | Python 3.11+, Flask | Xử lý nghiệp vụ và cung cấp API |
| Database | SQLite | Lưu công việc |
| Testing | pytest, Flask test client | Kiểm thử API |
| CI | GitHub Actions | Tự động cài dependencies và chạy test |

## 2. Chức năng

- Tạo công việc với tiêu đề và mô tả.
- Xem danh sách công việc, công việc mới tạo được hiển thị trước.
- Đánh dấu công việc hoàn thành hoặc đang thực hiện.
- Lọc theo tất cả, đang làm và đã hoàn thành.
- Xóa công việc sau khi xác nhận.
- Kiểm tra dữ liệu đầu vào ở backend.
- Lưu dữ liệu trong SQLite; dữ liệu vẫn còn sau khi tải lại trang.

## 3. Cấu trúc repository

```text
TaskFlow/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   ├── config.yml
│   │   └── feature_request.md
│   ├── workflows/ci.yml
│   └── pull_request_template.md
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── schema.sql
│   │   └── tasks.py
│   ├── tests/conftest.py
│   ├── tests/test_tasks_api.py
│   ├── requirements.txt
│   └── run.py
├── docs/
│   ├── API.md
│   ├── ARCHITECTURE.md
│   ├── GIT_EVIDENCE.md
│   ├── GIT_LAB_PRACTICE.md
│   ├── GIT_WORKFLOW.md
│   ├── PROJECT_REPORT_TEMPLATE.md
│   ├── REPRODUCE.md
│   ├── SUBMISSION_CHECKLIST.md
│   ├── TESTING.md
│   └── USE_CASES.md
├── frontend/
│   ├── css/styles.css
│   ├── js/app.js
│   └── index.html
├── instance/.gitkeep
├── .env.example
├── .gitattributes
├── .gitignore
├── CHANGELOG.md
├── CONTRIBUTING.md
├── LICENSE
├── pytest.ini
├── requirements.txt
├── requirements-dev.txt
└── SECURITY.md
```

## 4. Yêu cầu môi trường

- Python 3.11 trở lên.
- pip.
- Git (nếu clone repository).

Không cần cài SQLite server riêng. SQLite được tích hợp trong Python.

## 5. Cài đặt và chạy

### Bước 1 — Clone repository

```bash
git clone <URL_REPOSITORY>
cd TaskFlow
```

Thay `<URL_REPOSITORY>` bằng URL repository GitHub của bạn.

### Bước 2 — Tạo môi trường ảo

Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Bước 3 — Cài dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

### Bước 4 — Cấu hình (không bắt buộc)

`.env.example` là file mẫu để tham khảo; ứng dụng không tự nạp file `.env`. Ứng dụng đọc biến môi trường `DATABASE_PATH`; mặc định cơ sở dữ liệu được tạo tại `instance/taskflow.sqlite3`.

Windows PowerShell:

```powershell
$env:DATABASE_PATH="instance/taskflow.sqlite3"
```

macOS/Linux:

```bash
export DATABASE_PATH="instance/taskflow.sqlite3"
```

### Bước 5 — Chạy ứng dụng

```bash
python backend/run.py
```

Mở trình duyệt tại <http://127.0.0.1:5000>.

Health check: <http://127.0.0.1:5000/api/health>.

Cơ sở dữ liệu SQLite được khởi tạo tự động khi ứng dụng khởi động lần đầu.

## 6. Chạy kiểm thử

Từ thư mục gốc repository:

```bash
python -m pytest -v
```

CI trên GitHub Actions chạy kiểm thử trên Python 3.11 và 3.12 khi push hoặc tạo Pull Request vào `main`/`develop`.

Danh sách trường hợp kiểm thử được mô tả trong [`docs/TESTING.md`](docs/TESTING.md).

## 7. REST API

| Method | Endpoint | Chức năng |
|---|---|---|
| GET | `/api/health` | Kiểm tra trạng thái API |
| GET | `/api/tasks` | Lấy danh sách công việc |
| POST | `/api/tasks` | Tạo công việc |
| GET | `/api/tasks/{id}` | Lấy chi tiết công việc |
| PATCH | `/api/tasks/{id}` | Cập nhật một hoặc nhiều trường |
| DELETE | `/api/tasks/{id}` | Xóa công việc |

Chi tiết request, response và mã lỗi: [`docs/API.md`](docs/API.md).

## 8. Tài liệu

- [Kiến trúc hệ thống](docs/ARCHITECTURE.md)
- [Đặc tả API](docs/API.md)
- [Các ca sử dụng](docs/USE_CASES.md)
- [Kiểm thử](docs/TESTING.md)
- [Quy trình Git, branch và Pull Request](docs/GIT_WORKFLOW.md)
- [Hướng dẫn thực hành Git theo Lab](docs/GIT_LAB_PRACTICE.md)
- [Hướng dẫn tái hiện kết quả](docs/REPRODUCE.md)
- [Checklist trước khi nộp](docs/SUBMISSION_CHECKLIST.md)
- [Hướng dẫn đóng góp](CONTRIBUTING.md)
- [Lịch sử thay đổi](CHANGELOG.md)

## 9. Quy trình Git đề xuất

- `main`: nhánh ổn định.
- `feature/<ten-chuc-nang>`: phát triển chức năng.
- `fix/<ten-loi>`: sửa lỗi.
- `docs/<noi-dung>`: cập nhật tài liệu.

Dùng Pull Request để đưa thay đổi vào `main`; chạy test trước khi merge. Hướng dẫn chi tiết nằm ở [`docs/GIT_WORKFLOW.md`](docs/GIT_WORKFLOW.md).

**Lưu ý:** Các tên nhánh và quy trình trên là quy ước đề xuất. Chúng chỉ trở thành bằng chứng hoạt động khi bạn thực sự tạo nhánh, commit và Pull Request trên GitHub. ZIP không chứa lịch sử Git.

## 10. Giới hạn và hướng phát triển

- Chưa có đăng nhập, phân quyền hoặc dữ liệu riêng theo người dùng.
- Chưa có hạn hoàn thành, mức độ ưu tiên, tìm kiếm và phân trang.
- Chưa có kiểm thử trình duyệt tự động.
- Chưa cấu hình triển khai production.

Các hướng phát triển phù hợp: bổ sung deadline/priority, tìm kiếm, tài khoản người dùng, kiểm thử giao diện và triển khai có HTTPS.
- [Bảng ghi nhận bằng chứng GitHub](docs/GIT_EVIDENCE.md)
