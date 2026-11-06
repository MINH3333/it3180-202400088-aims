# Quy trình Git đề xuất

Tài liệu này là quy trình hướng dẫn. Nó không khẳng định các branch, commit hay Pull Request đã được tạo trên remote.

## 1. Quy ước branch

| Loại | Mẫu tên | Ví dụ |
|---|---|---|
| Nhánh ổn định | `main` | `main` |
| Chức năng | `feature/<ten>` | `feature/task-deadline` |
| Sửa lỗi | `fix/<ten>` | `fix/blank-task-title` |
| Tài liệu | `docs/<ten>` | `docs/update-api-guide` |
| Phát hành | `release/<version>` | `release/1.0.0` |

## 2. Tạo nhánh và commit

```bash
git switch main
git pull origin main
git switch -c feature/task-deadline
# chỉnh sửa code và test
git add .
git commit -m "feat: add task deadline field"
git push -u origin feature/task-deadline
```

## 3. Commit message

Dùng định dạng `<type>: <mô tả ngắn>`.

- `feat`: thêm chức năng.
- `fix`: sửa lỗi.
- `docs`: cập nhật tài liệu.
- `test`: thêm/sửa kiểm thử.
- `refactor`: tái cấu trúc không đổi hành vi.
- `chore`: cấu hình hoặc bảo trì.

Ví dụ: `fix: reject blank task title`, `test: cover missing task endpoint`.
Tránh message không mô tả thay đổi như `update`, `ok`, `fix bug`, `aaa`.

## 4. Pull Request và review

1. Mở PR từ branch công việc vào `main`.
2. Mô tả mục đích, các thay đổi và cách kiểm thử.
3. Kiểm tra diff, đảm bảo không có secret hoặc file sinh tự động.
4. Chờ CI chạy và nhờ ít nhất một thành viên khác review nếu làm việc nhóm.
5. Sửa góp ý, chạy test lại và merge theo quy định của nhóm.

## 5. Tag và version

Có thể dùng Semantic Versioning:

- `MAJOR`: thay đổi không tương thích.
- `MINOR`: thêm chức năng tương thích ngược.
- `PATCH`: sửa lỗi tương thích ngược.

Chỉ tạo tag/release sau khi phiên bản thực sự được kiểm thử và chốt:

```bash
git tag -a v1.0.0 -m "TaskFlow 1.0.0"
git push origin v1.0.0
```

Không tạo tag hoặc ghi nhận PR/approval giả chỉ để làm đẹp báo cáo.
