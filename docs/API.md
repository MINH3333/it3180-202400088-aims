# TaskFlow REST API

Base URL local: `http://127.0.0.1:5000`.

Tất cả endpoint API trả JSON. Request tạo/cập nhật phải gửi `Content-Type: application/json`.

## Health check

`GET /api/health`

Response `200 OK`:

```json
{"status": "ok", "service": "TaskFlow API"}
```

## Task object

```json
{
  "id": 1,
  "title": "Hoàn thành bài tập lớn",
  "description": "Viết tài liệu và kiểm thử",
  "completed": false,
  "created_at": "2026-11-06 10:30:00",
  "updated_at": "2026-11-06 10:30:00"
}
```

`created_at` và `updated_at` do SQLite tạo theo UTC.

## Lấy danh sách công việc

`GET /api/tasks`

Response `200 OK`: mảng task, sắp xếp mới nhất trước.

## Tạo công việc

`POST /api/tasks`

Request:

```json
{
  "title": "Hoàn thành bài tập lớn",
  "description": "Viết tài liệu và kiểm thử",
  "completed": false
}
```

Quy tắc:

- `title`: bắt buộc, chuỗi từ 1 đến 120 ký tự sau khi bỏ khoảng trắng đầu/cuối.
- `description`: tùy chọn, chuỗi tối đa 1000 ký tự; mặc định chuỗi rỗng.
- `completed`: tùy chọn, phải là boolean; mặc định `false`.
- Không chấp nhận thuộc tính ngoài `title`, `description`, `completed`.

Response thành công: `201 Created` và task vừa tạo.

## Lấy một công việc

`GET /api/tasks/{id}`

Response `200 OK`; trả `404 Not Found` nếu ID không tồn tại.

## Cập nhật công việc

`PATCH /api/tasks/{id}`

Có thể gửi một hoặc nhiều trường trong `title`, `description`, `completed`. Chỉ các trường có mặt trong request được cập nhật.

Ví dụ:

```json
{"completed": true}
```

Response `200 OK` với task sau cập nhật. Payload rỗng, trường không hỗ trợ hoặc giá trị không hợp lệ trả `400 Bad Request`.

## Xóa công việc

`DELETE /api/tasks/{id}`

Response `200 OK`:

```json
{"message": "Đã xóa công việc."}
```

Trả `404 Not Found` nếu ID không tồn tại.

## Mã lỗi

| HTTP | Ý nghĩa |
|---|---|
| 400 | JSON không hợp lệ, thiếu trường bắt buộc hoặc dữ liệu không đạt validation |
| 404 | Không tìm thấy endpoint hoặc công việc |
| 405 | Phương thức HTTP không được hỗ trợ |
| 413 | Request vượt giới hạn kích thước |
| 500 | Lỗi máy chủ không mong đợi |
