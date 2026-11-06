# Hướng dẫn tái hiện (Reproduce)

Tài liệu này giúp người chấm hoặc thành viên khác tự chạy lại dự án từ một bản clone sạch.

## 1. Môi trường

- Python 3.11 trở lên.
- pip.
- Trình duyệt hiện đại.

## 2. Clone và cài đặt

```bash
git clone <URL_REPOSITORY>
cd TaskFlow
python -m venv .venv
```

Kích hoạt môi trường ảo theo hệ điều hành, sau đó:

```bash
python -m pip install -r requirements-dev.txt
```

## 3. Chạy test và ứng dụng

```bash
python -m pytest -v
python backend/run.py
```

Mở `http://127.0.0.1:5000`. Lần đầu chạy, ứng dụng tự tạo SQLite database tại `instance/taskflow.sqlite3`.

## 4. Kiểm tra Git khi đã đẩy lên GitHub

```bash
git branch -a
git tag -n
git log --oneline --graph --decorate --all
```

Trên GitHub, kiểm tra thêm tab Pull requests, Actions và Insights. ZIP tải xuống không chứa `.git`, do đó không dùng ZIP để xác minh lịch sử branch/commit/PR.

## 5. Kết quả cần ghi nhận khi nộp

- Phiên bản Python và hệ điều hành dùng để chạy.
- Lệnh test đã chạy và số test thực tế pass/fail.
- URL repository và nhánh mặc định.
- URL CI run sau khi workflow chạy trên GitHub.
- URL PR/Release nếu thực sự có tạo.

Không điền số liệu hoặc URL minh chứng trước khi kiểm tra chúng trên repository thật.
