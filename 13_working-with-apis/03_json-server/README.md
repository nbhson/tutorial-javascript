# JSON Server — Giả lập REST API — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**JSON Server** là một công cụ chạy bằng Node.js, biến một **file JSON** thành một **REST API giả lập** (fake REST server) — phục vụ mục đích **prototyping / phát triển frontend** mà không cần backend thật.

JSON Server tự động tạo ra các endpoint CRUD dựa trên cấu trúc JSON của bạn. Chỉ cần một file `server.json` và một lệnh — bạn có server RESTfull chạy ngay lập tức.

### Tự động generated routes

Với file JSON:
```json
{
  "courses": [
    { "id": 1, "name": "HTML", "price": 0 },
    { "id": 2, "name": "CSS", "price": 0 }
  ],
  "posts": [
    { "id": 1, "title": "Post 1" }
  ]
}
```

JSON Server tự động tạo:
- `GET /courses` → toàn bộ mảng
- `GET /courses/1` → phần tử theo id
- `POST /courses` → thêm mới (tự generate id)
- `PUT /courses/1` → thay thế toàn bộ
- `PATCH /courses/1` → cập nhật một phần
- `DELETE /courses/1` → xóa

### Advanced query parameters

```
GET /courses?price_gte=100     // price >= 100
GET /courses?_sort=name&_order=asc   // sort
GET /courses?_limit=5         // paginate limit
GET /courses?_page=2&_limit=10 // paginate page
GET /courses/name_like=HTML   // fuzzy search
```

## 📐 Cấu trúc / Cú pháp

### Cài đặt và chạy

```bash
# Cài global (hoặc dùng npx không cần install)
npm i -g json-server

# Chạy server
json-server --watch server.json --port 3000

# Hoặc one-liner không cần install
npx json-server --watch server.json --port 3000
```

### File structure

```
project/
├── server.json        # dữ liệu mock
├── index.html         # frontend
└── app.js             # fetch calls
```

### server.json example

```json
{
  "courses": [
    { "id": 1, "name": "HTML", "description": "Free", "level": "beginner" },
    { "id": 2, "name": "CSS", "description": "Free", "level": "beginner" },
    { "id": 3, "name": "JavaScript", "description": "Free", "level": "intermediate" }
  ],
  "students": [
    { "id": 1, "name": "Minh", "enrolledCourseIds": [1, 2] }
  ]
}
```

### CLI options

| Option | Default | Mô tả |
|--------|---------|-------|
| `--watch` | — | Reload data khi server.json đổi |
| `--port` | `3000` | Port chạy server |
| `--host` | `0.0.0.0` | Host bind |
| `--routes` | — | Custom routes file |
| `--static` | — | Static files directory |
| `--middlewares` | — | Express middlewares |
| `--id` | `"id"` | Field name cho auto-ID |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Tạo full-CRUD API** chỉ trong vài giây, không viết backend.
2. **Dữ liệu trong `server.json`** thay đổi trực quan — thêm/sửa/xóa là update file.
3. **Hỗ trợ filter, sort, paginate** (`?_limit=2`, `?_sort=name`...) — query powerful.
4. **Lý tưởng để học fetch/CRUD** trước khi gặp backend thật.
5. **Chạy localhost**, không tốn chi phí cloud.
6. **Hot reload** — `--watch` tự động reload khi file đổi.
7. **RESTful conventions** — đúng chuẩn HTTP methods và status codes.
8. **Micro-serialization** — tự động format JSON response.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Chỉ là giả lập — không dùng được cho production

```bash
# JSON Server lưu data vào file, không có database thật
# Không có authentication, rate limiting, validation phức tạp
json-server --watch server.json
# ✅ Good cho: prototype, demo, learning
# ❌ Bad cho: production, real auth, complex business logic
```

### Bẫy 2: Resource name phải khớp — `coures` ≠ `courses`

```json
{
  "coures": [...]  // key trong JSON = route name
}
```
```js
fetch("http://localhost:3000/coures"); // phải đúng key name
```

### Bẫy 3: Tự generate id nếu không cung cấp

```js
// POST không cần truyền id — server tự tạo
fetch("http://localhost:3000/courses", {
  method: "POST",
  body: JSON.stringify({ name: "React", description: "Advanced" })
  // id sẽ tự sinh: 4, 5, 6...
});
```

### Bẫy 4: Không có relationship/foreign key support

```json
{
  "courses": [{ "id": 1, "teacherId": 5 }], // teacherId không tự join
  "teachers": [{ "id": 5, "name": "Anh" }]
}
// Phải tự filter bằng JS phía client
```

### Bẫy 5: CORS — mặc định enabled nhưng cần để ý

```bash
# JSON Server mặc định enable CORS
# Nhưng nếu dùng custom middleware thì có thể bị block
```

### Bẫy 6: Database persistence — data mất khi kill server nếu không --watch

```bash
# --watch giúp reload, nhưng data vẫn nằm trong file
# Kill server ≠ mất data (vì file còn đó)
# Tuy nhiên nếu sửa file thủ công cần restart hoặc --watch
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Học CRUD**: GET/POST/PUT/PATCH/DELETE bằng fetch.
2. **Dựng prototype UI** trước khi backend chính thức có.
3. **Demo tính năng frontend** khi chưa có server.
4. **Testing frontend code** — cần mock API endpoint.
5. **Team collaboration** — backend và frontend cùng working với same mock data.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Cài đặt và chạy

```bash
# Terminal 1: chạy server
cd 03_json-server
npx json-server --watch server.json --port 3000

# Terminal 2: test bằng curl
curl http://localhost:3000/courses
# [{"id":1,"name":"HTML",...}, ...]

curl http://localhost:3000/courses/1
# {"id":1,"name":"HTML",...}
```

### Ví dụ 2: GET tất cả courses

```js
var courseAPI = "http://localhost:3000/courses";

fetch(courseAPI)
  .then((res) => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then((courses) => console.log(courses))
  .catch((err) => console.error(err));
```

### Ví dụ 3: GET theo id

```js
fetch("http://localhost:3000/courses/1")
  .then(res => res.json())
  .then(course => console.log(course.name)); // "HTML"
```

### Ví dụ 4: POST tạo mới

```js
fetch("http://localhost:3000/courses", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    name: "React",
    description: "Frontend library",
    level: "intermediate"
  })
})
  .then(res => res.json())
  .then(newCourse => console.log("Created:", newCourse));
// Created: { id: 4, name: "React", ... }
```

### Ví dụ 5: PUT update toàn bộ

```js
fetch("http://localhost:3000/courses/1", {
  method: "PUT",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    id: 1,
    name: "HTML nâng cao",
    description: "Advanced HTML",
    level: "advanced"
  })
})
  .then(res => res.json())
  .then(updated => console.log(updated));
```

### Ví dụ 6: PATCH update một phần

```js
fetch("http://localhost:3000/courses/1", {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ description: "đã sửa" })
})
  .then(res => res.json())
  .then(updated => console.log(updated));
// chỉ cập nhật description, các field khác giữ nguyên
```

### Ví dụ 7: DELETE

```js
fetch("http://localhost:3000/courses/1", {
  method: "DELETE"
})
  .then(res => {
    console.log("Deleted:", res.status === 200);
  });
```

### Ví dụ 8: Query parameters — filter, sort, paginate

```js
// Filter
fetch("http://localhost:3000/courses?level=beginner")
  .then(res => res.json())
  .then(courses => console.log(courses));

// Sort
fetch("http://localhost:3000/courses?_sort=name&_order=asc")
  .then(res => res.json())
  .then(courses => console.log(courses));

// Paginate
fetch("http://localhost:3000/courses?_page=1&_limit=2")
  .then(res => res.json())
  .then(courses => console.log(courses));
```

### Ví dụ 9: đầy đủ CRUD app

```js
const API = "http://localhost:3000/courses";

async function getCourses() {
  const res = await fetch(API);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function addCourse(course) {
  const res = await fetch(API, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(course)
  });
  return res.json();
}

async function deleteCourse(id) {
  const res = await fetch(`${API}/${id}`, { method: "DELETE" });
  return res.ok;
}

// Usage
getCourses().then(console.log);
addCourse({ name: "Vue", description: "Progressive framework" });
deleteCourse(1);
```

## 🔬 So sánh với alternatives

| Tool | Setup | Features | Best for |
|------|-------|----------|----------|
| JSON Server | `npx json-server` | Auto CRUD, queries | Quick prototype |
| Mockoon | GUI app | Visual, export | Team collaboration |
| Mirage JS | npm package | In-browser mock | Frontend-only |
| MSW (Mock Service Worker) | npm package | Service worker based | Realistic network |
| True backend | Requires DB + code | Full featured | Production |

## 📊 Performance & Best Practices

- **Dùng `npx`** thay install global — không cần `npm i -g`, luôn latest version.
- **`:8080` thay `:3000`** nếu port 3000 bị conflict.
- **`--watch`** luôn dùng khi dev — tự reload khi sửa file JSON.
- **Backup `server.json`** — dữ liệu mock quan trọng, tránh mất khi reset.
- **Transition to real API** — đổi URL từ `localhost:3000` sang real backend khi ready.
- **Use environment variables** — `const API = process.env.API_URL || "http://localhost:3000/courses"`.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch calls to JSON Server
- **Xem thêm:** `13_working-with-apis/04_postman` — test JSON Server với Postman
- **Xem thêm:** `13_working-with-apis/05_crud` — CRUD app hoàn chỉnh
- **Xem thêm:** `13_working-with-apis/README` — APIs overview
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise + fetch
