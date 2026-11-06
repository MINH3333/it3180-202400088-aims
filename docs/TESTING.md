# Kiểm thử TaskFlow

## Công cụ

- `pytest`: tổ chức và chạy test tự động.
- Flask test client: gọi endpoint mà không cần bật HTTP server.
- `tmp_path`: mỗi test sử dụng SQLite database riêng, tránh phụ thuộc dữ liệu local.

## Chạy kiểm thử

Từ thư mục gốc:

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -v
```

## Phạm vi test

Bộ test kiểm tra:

1. Trang chủ trả HTML.
2. Health check trả trạng thái OK.
3. Danh sách ban đầu rỗng và truy xuất được nhiều task.
4. Tạo task hợp lệ, tự chuẩn hóa khoảng trắng và cho phép trạng thái hoàn thành ban đầu.
5. Từ chối JSON sai định dạng hoặc JSON không phải object.
6. Từ chối tiêu đề thiếu, rỗng, sai kiểu hoặc dài quá 120 ký tự.
7. Từ chối mô tả dài quá 1000 ký tự.
8. Từ chối `completed` không phải boolean.
9. Từ chối trường ngoài danh sách cho phép.
10. Lấy task theo ID.
11. Cập nhật một trường hoặc nhiều trường.
12. Từ chối payload cập nhật rỗng và giá trị cập nhật không hợp lệ.
13. Trả 404 khi đọc/cập nhật/xóa ID không tồn tại.
14. Xóa task đã tồn tại.

## Kiểm thử thủ công giao diện

1. Chạy `python backend/run.py`, mở `http://127.0.0.1:5000`.
2. Thêm công việc có tiêu đề và mô tả.
3. Chuyển bộ lọc Tất cả / Đang làm / Hoàn thành.
4. Đánh dấu công việc hoàn thành, sau đó bỏ đánh dấu.
5. Xóa một công việc và xác nhận hộp thoại.
6. Tải lại trang để xác nhận dữ liệu vẫn còn trong SQLite.
7. Thử tiêu đề chỉ chứa dấu cách để xác nhận validation.

## CI

`.github/workflows/ci.yml` cài dependencies và chạy test trên Python 3.11, 3.12 cho push và Pull Request vào `main`/`develop`. Kết quả CI thực tế chỉ xuất hiện sau khi repository được đẩy lên GitHub và workflow chạy.
