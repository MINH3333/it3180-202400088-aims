# Security Policy

TaskFlow là dự án học tập và chưa được thiết kế để xử lý dữ liệu nhạy cảm hoặc
triển khai production.

## Báo cáo vấn đề bảo mật

Không đăng công khai mật khẩu, token, API key hoặc dữ liệu cá nhân trong issue.
Nếu phát hiện thông tin nhạy cảm đã bị commit, hãy thu hồi/đổi thông tin đó ngay
lập tức; xóa file khỏi commit mới không làm bí mật cũ biến mất khỏi Git history.

## Giới hạn hiện tại

- Chưa có đăng nhập và phân quyền.
- Chưa có bảo vệ CSRF cho mô hình triển khai đa nguồn gốc.
- Chưa có giới hạn tốc độ (rate limiting) hoặc giám sát production.
- Không nên mở ứng dụng debug ra mạng công cộng.
