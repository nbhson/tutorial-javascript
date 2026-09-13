# Postman — Kiểm thử API không cần viết code — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Postman** là công cụ (GUI) để **gửi HTTP request và xem response** — bạn test API mà không cần viết code, rất hữu ích để kiểm tra server trước khi tích hợp vào frontend. Ngoài Postman, **Thunder Client** (extension VS Code) cũng làm việc tương tự — nhẹ hơn, không cần install app riêng.

Giao diện Postman bạn cần biết:

- **Method** (GET / POST / PUT / PATCH / DELETE) — chọn HTTP method.
- **URL** — ví dụ `http://localhost:3000/courses`.
- **Headers** — ví dụ `Content-Type: application/json`, `Authorization: Bearer token`.
- **Body** — dữ liệu JSON cho POST/PUT/PATCH (raw JSON).
- **Params** — query parameters (`?key=value`).
- **Send** → xem **Status code**, **JSON response**, thời gian phản hồi.
- **Environment** — lưu biến môi trường (`{{baseUrl}}`) để switch giữa dev/prod.

Vì Postman chỉ "gõ tay", nó đi kèm với **JSON Server**: mở `server.json` làm REST fake ở local, rồi dùng Postman bắn request về đó để test CRUD.

## 📐 Cấu trúc / Cú pháp

### Postman workspace structure

```
Postman
├── Collections     # nhóm các request liên quan
│   └── Courses API
│       ├── GET all courses
│       ├── GET course by id
│       ├── POST new course
│       ├── PUT update course
│       ├── PATCH partial update
│       └── DELETE course
├── Environments    # biến môi trường
│   └── Local (baseUrl = http://localhost:3000)
├── History         # lịch sử request đã gửi
└── Newman          # command-line runner cho collections
```

### HTTP Method reference trong Postman

| Method | Body? | Typical use | Status code mong đợi |
|--------|-------|-------------|---------------------|
| `GET` | ❌ | Read data | 200 |
| `POST` | ✅ JSON | Create resource | 201 |
| `PUT` | ✅ JSON | Replace resource | 200 |
| `PATCH` | ✅ JSON | Partial update | 200 |
| `DELETE` | ❌ | Delete resource | 204 |

### Headers thường dùng

| Header | Value | Khi nào dùng |
|--------|-------|--------------|
| `Content-Type` | `application/json` | POST/PUT/PATCH với JSON body |
| `Authorization` | `Bearer <token>` | Authenticated requests |
| `Accept` | `application/json` | Yêu cầu response JSON |
| `X-Request-ID` | UUID | Tracking request |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Kiểm thử server không cần code** — nhanh, trực quan,适合 non-developer.
2. **Lưu lịch sử request**, collections, môi trường biến để tái dùng.
3. **Xem rõ status code, header, body** — hỗ trợ debug CORS/lỗi server.
4. **Làm tài liệu API** — Export collection, đọc được OpenAPI/Swagger.
5. **Hoàn hảo phối hợp JSON Server** để phát triển frontend độc lập.
6. **Test edge cases** — sai body, thiếu field, invalid ID — xem server phản ứng thế nào.
7. **Team collaboration** — share collection qua Postman cloud.
8. **Automated tests** — viết test script trong Postman (JavaScript).

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Chỉ kiểm thử thủ công — chưa tự động hóa

```
// Postman GUI = manual testing
// Muốn automated? Cần Newman (CLI) hoặc script riêng
newman run collection.json -e environment.json
```

### Bẫy 2: Không thay thế được frontend fetch code

```
// Postman test server OK
// Nhưng frontend vẫn có thể fail vì:
// - CORS policy
// - Auth token missing
// - Network issues
// - Frontend parsing error
```

### Bẫy 3: Phải nhớ đúng method/body — gõ sai gây hiểu lầm

```
// POST nhưng body để empty → server trả 400 Bad Request
// PUT nhưng send PATCH body → partial update thay vì full replace
```

### Bẫy 4: Server chưa chạy → connection refused

```
// Phải chạy json-server trước:
npx json-server --watch server.json --port 3000
// Sau đó mới mở Postman gửi request
```

### Bẫy 5: Environment variables chưa set đúng

```
// Dùng {{baseUrl}} nhưng environment chưa chọn → request fail
// Check:右上角 environment selector → chọn "Local"
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Kiểm tra một endpoint mới** trước khi viết code gọi.
2. **Xem response shape** để biết trường nào render trong UI.
3. **Trao đổi với backend**: gửi request mẫu, minh chứng lỗi.
4. **Demo/tài liệu API** cho team — share Postman collection.
5. **Debug CORS issues** — test cùng origin, different origin.
6. **Load testing basics** — gửi nhiều request liên tiếp.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: GET all courses

```
Method: GET
URL: http://localhost:3000/courses
Headers: (none needed)
Body: (none)

Expected: 200 OK
Response: [{"id":1,"name":"HTML",...}, ...]
```

### Ví dụ 2: GET course by id

```
Method: GET
URL: http://localhost:3000/courses/1
Headers: (none)
Body: (none)

Expected: 200 OK
Response: {"id":1,"name":"HTML","description":"Free","level":"beginner"}

// Test invalid id
URL: http://localhost:3000/courses/999
Expected: 404 Not Found
Response: {} (empty object)
```

### Ví dụ 3: POST create course

```
Method: POST
URL: http://localhost:3000/courses
Headers: Content-Type: application/json
Body (raw JSON):
{
  "name": "React",
  "description": "Frontend library",
  "level": "intermediate"
}

Expected: 201 Created
Response: {"id":4,"name":"React","description":"Frontend library","level":"intermediate"}
// id tự sinh
```

### Ví dụ 4: PUT full update

```
Method: PUT
URL: http://localhost:3000/courses/1
Headers: Content-Type: application/json
Body (raw JSON):
{
  "id": 1,
  "name": "HTML nâng cao",
  "description": "Advanced HTML course",
  "level": "advanced"
}

Expected: 200 OK
Response: updated course object
```

### Ví dụ 5: PATCH partial update

```
Method: PATCH
URL: http://localhost:3000/courses/1
Headers: Content-Type: application/json
Body (raw JSON):
{
  "description": "đã sửa mô tả"
}

Expected: 200 OK
Response: course với description mới, các field khác giữ nguyên
```

### Ví dụ 6: DELETE course

```
Method: DELETE
URL: http://localhost:3000/courses/1
Headers: (none)
Body: (none)

Expected: 200 OK hoặc 204 No Content
Server.json file sẽ bị update (course id=1 bị xóa)
```

### Ví dụ 7: Test query parameters

```
// Filter by level
GET http://localhost:3000/courses?level=beginner
Expected: chỉ courses có level = "beginner"

// Sort by name ascending
GET http://localhost:3000/courses?_sort=name&_order=asc
Expected: array sorted by name A→Z

// Paginate
GET http://localhost:3000/courses?_page=1&_limit=2
Expected: 2 courses đầu tiên
```

### Ví dụ 8: Thunder Client (VS Code extension alternative)

```
// Install: VS Code Extensions → search "Thunder Client"
// Tạo request:
{
  "name": "GET Courses",
  "url": "http://localhost:3000/courses",
  "method": "GET",
  "headers": {}
}
// Sent directly from VS Code — no separate app needed
```

### Ví dụ 9: Collection với tests (Postman script)

```javascript
// Trong tab Tests của Postman, viết JavaScript:

pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has courses array", function () {
    const response = pm.response.json();
    pm.expect(response).to.be.an("array");
    pm.expect(response.length).to.be.greaterThan(0);
});

pm.test("First course has id", function () {
    const response = pm.response.json();
    pm.expect(response[0].id).to.exist;
});
```

## 🔬 So sánh với alternatives

| Tool | Type | Cost | Best for |
|------|------|------|----------|
| **Postman** | Desktop app | Free (team features paid) | Full-featured testing |
| **Thunder Client** | VS Code extension | Free | Quick tests in editor |
| **Insomnia** | Desktop app | Free | Clean UI, GraphQL |
| **curl** | CLI | Free | Scripting, CI/CD |
| **HTTPie** | CLI | Free | Human-friendly CLI |

## 📊 Performance & Best Practices

- **Luôn chạy JSON Server trước** khi test với Postman — `npx json-server --watch server.json`.
- **Dùng Environment variables** — `{{baseUrl}}` thay vì hardcode URL.
- **Group requests vào Collection** — tổ chức theo feature/module.
- **Thêm tests script** — automated validation mỗi request.
- **Export collection** — share với team qua JSON file.
- **Test error cases** — send invalid data, missing fields, wrong ID.
- **Sử dụng Thunder Client** cho quick tests mà không muốn mở app riêng.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/03_json-server` — JSON Server setup
- **Xem thêm:** `13_working-with-apis/05_crud` — CRUD implementation to test
- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch code to validate against
- **Xem thêm:** `13_working-with-apis/README` — APIs overview
