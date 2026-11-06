# Checklist trước khi nộp GitHub

## Thông tin repository

- [ ] Đổi tên repository và cập nhật URL clone trong README.
- [ ] Bổ sung tên thành viên, mã sinh viên, lớp và giảng viên nếu bài yêu cầu.
- [ ] Chọn visibility phù hợp (Public nếu giảng viên yêu cầu repository public).
- [ ] Kiểm tra nhánh mặc định là `main`.

## Mã nguồn và tài liệu

- [ ] Chạy lại project trên môi trường sạch theo `docs/REPRODUCE.md`.
- [ ] Chạy `python -m pytest -v` và lưu kết quả thực tế.
- [ ] Kiểm tra README, API, kiến trúc và use case đúng với mã nguồn.
- [ ] Không commit database local, `.env`, token hoặc mật khẩu.
- [ ] Kiểm tra `.gitignore` và `git status` trước khi commit.

## Bằng chứng GitHub

- [ ] Có commit đầu tiên với message rõ ràng.
- [ ] Có branch làm việc riêng cho thay đổi (nếu bài yêu cầu).
- [ ] Có Pull Request thực tế (nếu bài yêu cầu).
- [ ] CI chạy thành công trên GitHub Actions.
- [ ] Có review/approval từ thành viên khác nếu rubric yêu cầu.
- [ ] Có tag/release nếu bài thực hành yêu cầu.
- [ ] Ghi link thật của commit, PR, Actions và release vào báo cáo.

## Báo cáo và nộp bài

- [ ] Hoàn thiện `docs/REPRODUCE.md` với môi trường và kết quả thực tế.
- [ ] Đối chiếu yêu cầu trong handout/rubric của giảng viên.
- [ ] Kiểm tra trạng thái nộp trên LMS.

> Checklist này là danh sách việc cần tự xác minh. Các ô chưa được đánh dấu không có nghĩa là repository đã đáp ứng.
