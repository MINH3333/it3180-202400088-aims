# Hướng dẫn thực hành Git theo mốc Lab

Tài liệu này đưa ra kịch bản thực hành trên TaskFlow để minh họa các thao tác Git thường gặp. Đây là hướng dẫn, không phải bằng chứng rằng thao tác đã được thực hiện trên GitHub. Hãy đối chiếu với handout chính thức của giảng viên nếu tên nhánh, mốc release hoặc yêu cầu PR khác.

## Lab 01 — Thiết lập repository và refactor

```bash
git init
git add .
git commit -m "chore: initialize TaskFlow repository"
git switch -c release/lab01
```

Thực hành di chuyển/đổi tên file bằng `git mv`, sau đó kiểm tra:

```bash
git status
git diff --cached
git log --oneline --decorate --all
```

`git mv` hỗ trợ di chuyển file và đưa thay đổi vào staging. Có thể thực hiện thao tác tương đương bằng lệnh hệ điều hành kết hợp `git add`/`git rm`; Git nhận diện rename khi so sánh nội dung giữa các commit.

## Lab 02 — Feature branch và Pull Request

```bash
git switch main
git pull origin main
git switch -c feature/task-priority
# chỉnh sửa code và test
git add .
git commit -m "feat: add task priority"
git push -u origin feature/task-priority
```

Mở Pull Request từ `feature/task-priority` vào `main`. Mô tả mục tiêu, thay đổi, cách test; nhờ thành viên khác review. Cập nhật branch theo góp ý rồi merge khi CI pass.

## Lab 03 — Bugfix, conflict và hoàn tác

Tạo branch sửa lỗi:

```bash
git switch -c fix/task-title-validation
# sửa code và thêm test
git add .
git commit -m "fix: reject blank task title"
```

Khi hai branch sửa cùng một đoạn, thực hành merge để quan sát conflict, chỉnh file, sau đó:

```bash
git add <file-da-giai-quyet>
git commit
```

Phân biệt lệnh hoàn tác:

- `git reset --soft`: di chuyển HEAD, giữ thay đổi trong staging.
- `git reset --mixed`: di chuyển HEAD, đưa thay đổi về working tree (mặc định).
- `git reset --hard`: xóa thay đổi chưa lưu; chỉ dùng trên branch thử nghiệm khi hiểu rõ hậu quả.
- `git reflog`: xem lịch sử di chuyển HEAD để tìm lại commit/nhánh bị di chuyển.
- `git revert <commit>`: tạo commit mới đảo ngược thay đổi; thường an toàn hơn trên branch đã chia sẻ vì không viết lại lịch sử công khai.

Không thực hành `reset --hard` trên branch dùng chung hoặc dữ liệu chưa backup.

## Lab 04 — Release, tag và changelog

Cập nhật `CHANGELOG.md`, chạy test, sau đó tạo tag khi phiên bản thực sự đã chốt:

```bash
python -m pytest -v
git switch main
git tag -a v1.0.0 -m "TaskFlow 1.0.0"
git push origin v1.0.0
```

Dùng Semantic Versioning: `MAJOR.MINOR.PATCH`. Không tạo tag chỉ để có hình thức; tag phải trỏ đến commit đã được kiểm tra.

## Lab 05 — Hotfix và bảo trì phiên bản

Khi phải sửa một lỗi nghiêm trọng trên phiên bản đang phát hành, có thể tạo branch hotfix từ tag/release tương ứng:

```bash
git switch -c hotfix/1.0.1 v1.0.0
# sửa lỗi và bổ sung test
git add .
git commit -m "fix: handle invalid task payload"
```

Sau khi kiểm thử và phát hành hotfix, đưa cùng thay đổi trở lại `main` bằng merge hoặc `cherry-pick` tùy quy trình nhóm. Kiểm tra để tránh bỏ sót bản sửa ở nhánh phát triển chính.

## Bằng chứng nên lưu

- Link branch, Pull Request, commit và tag thực tế.
- Ảnh chụp CI run sau khi push/PR.
- Mô tả ngắn conflict đã gặp và cách giải quyết.
- Ghi chú thao tác nào chỉ được thực hành local, thao tác nào đã được push lên remote.
