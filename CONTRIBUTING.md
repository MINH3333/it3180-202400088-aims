# Hướng dẫn đóng góp

Cảm ơn bạn đã quan tâm đến TaskFlow. Tài liệu này mô tả quy trình đề xuất cho
mọi thay đổi.

## Quy trình

1. Tạo issue mô tả lỗi hoặc chức năng cần bổ sung (nếu phù hợp).
2. Tạo branch từ `main`, ví dụ `feature/task-deadline` hoặc `fix/empty-title`.
3. Viết code và bổ sung/cập nhật test tương ứng.
4. Chạy `python -m pytest -v` tại thư mục gốc.
5. Cập nhật README hoặc tài liệu trong `docs/` nếu hành vi/cách chạy thay đổi.
6. Push branch và mở Pull Request theo mẫu có sẵn.
7. Chờ CI chạy, xử lý review và chỉ merge khi thay đổi đã được kiểm tra.

## Quy tắc code

- Dùng tên hàm/biến dễ hiểu và giữ mỗi hàm tập trung vào một nhiệm vụ.
- Backend phải kiểm tra dữ liệu đầu vào.
- Dùng SQL parameterized query; không nối chuỗi dữ liệu người dùng vào SQL.
- Không commit `.env`, database local, token hoặc mật khẩu.
- Không đưa thư viện hoặc file build được sinh tự động vào repository.
- Không xóa test chỉ để làm CI chuyển sang trạng thái thành công.

## Commit message

Dùng định dạng `<type>: <mô tả ngắn>`.

Ví dụ: `feat: add task completion filter`, `fix: reject blank task title`,
`test: cover task deletion`, `docs: update setup guide`.
