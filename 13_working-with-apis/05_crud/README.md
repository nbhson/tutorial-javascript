# CRUD hoàn chỉnh với Fetch + JSON Server — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**CRUD** viết tắt của bốn thao tác dữ liệu cơ bản, ánh xạ trực tiếp sang HTTP REST:

| Thao tác | HTTP Method | Trong ví dụ |
|----------|-------------|-------------|
| **Create** | `POST` | `addCourses()` — thêm khóa học |
| **Read** | `GET` | `getCourses()` — lấy danh sách |
| **Update** | `PUT` / `PATCH` | (bài tập — chưa code trong file) |
| **Delete** | `DELETE` | `deleteCourse(id)` — xóa khóa học |

Đây là một ứng dụng nhỏ hoàn chỉnh (form nhập `name`, `description`; danh sách khóa học có nút **Xóa**) kết nối với **JSON Server** ở `http://localhost:3000/courses`. Cách tổ chức trong `app.js`:

- `start()` — khởi chạy: load danh sách + gắn sự kiện form.
- `getCourses(callback)` — GET + `callback` render.
- `addCourses(data, callback)` — POST với `Content-Type: application/json` và `body: JSON.stringify(data)`.
- `deleteCourse(id)` — DELETE `coursesAPI + "/" + id`, xóa luôn element khỏi DOM.

## 📐 Cấu trúc / Cú pháp

### CRUD function signatures

```js
// READ — GET all
function getCourses(callback) {
  fetch(coursesAPI)
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(callback);
}

// CREATE — POST new
function addCourses(data, callback) {
  fetch(coursesAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  })
    .then(res => {
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return res.json();
    })
    .then(callback);
}

// UPDATE — PUT full / PATCH partial (bài tập)
function updateCourse(id, data) {
  return fetch(`${coursesAPI}/${id}`, {
    method: "PUT",        // hoặc "PATCH" cho partial
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
}

// DELETE — DELETE by id
function deleteCourse(id) {
  return fetch(`${coursesAPI}/${id}`, {
    method: "DELETE"
  });
}
```

### HTML structure

```html
<!-- Form thêm course -->
<form id="course-form">
  <input name="name" placeholder="Tên khóa học" required />
  <input name="description" placeholder="Mô tả" required />
  <button type="submit">Thêm</button>
</form>

<!-- Danh sách -->
<ul id="list-course"></ul>
```

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Mẫu chuẩn** cho mọi app quản lý danh sách (to-do, blog, khóa học...).
2. **Ví dụ điển hình** về `headers` và `JSON.stringify` cho POST/DELETE.
3. **Cập nhật DOM ngay** sau khi server phản hồi — luồng dữ liệu thực tế.
4. **Dễ mở rộng**: thêm Update (PUT/PATCH) chỉ vài dòng.
5. **Separation of concerns** — API layer riêng, DOM rendering riêng.
6. **Callback pattern** dễ hiểu cho người mới — sau đó convert sang async/await.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: Demo chỉ có Create/Read/Delete — Update chưa code

```js
// File hiện tại thiếu updateCourse()
// Bài tập: tự viết PUT/PATCH handler
```

### Bẫy 2: `server.json` cần resource đúng tên — `courses` ≠ `coures`

```json
{
  "courses": [...]  // key này phải khớp với URL trong app.js
}
```
```js
var coursesAPI = "http://localhost:3000/courses"; // phải trùng key
```

### Bẫy 3: Input `name` attribute phải khớp `document.querySelector`

```js
// HTML: <input name="name">
// JS: document.querySelector('input[name="name"]')
// Nếu sai name → undefined → submit không hoạt động
```

### Bẫy 4: Chưa có error handling chi tiết

```js
// Nếu server chưa chạy, mọi fetch đều reject
// Cần thêm try/catch và user feedback (alert, toast)
```

### Bẫy 5: Thứ tự chạy — phải khởi động JSON Server trước

```bash
# Terminal 1: chạy server
npx json-server --watch server.json --port 3000

# Terminal 2: mở index.html trong browser
# Nếu mở trước khi server chạy → fetch fail
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **App quản lý danh sách** dữ liệu kết nối REST backend.
2. **Học cách dùng POST/DELETE** với fetch + JSON thực tế.
3. **Làm nền tảng** trước khi học framework (React/Vue có state management).
4. **Dashboard admin** — CRUD cho products, users, orders.
5. **Blog/CMS** — create post, list posts, delete post.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Full CRUD flow (có sẵn trong file)

```js
var coursesAPI = "http://localhost:3000/courses";

// READ
function getCourses(callback) {
  fetch(coursesAPI)
    .then((res) => res.json())
    .then(callback);
}

// CREATE
function addCourses(data, callback) {
  fetch(coursesAPI, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
    .then((res) => res.json())
    .then(callback);
}

// DELETE
function deleteCourse(id) {
  fetch(coursesAPI + "/" + id, {
    method: "DELETE",
    headers: { "Content-Type": "application/json" },
  }).then(() => console.log("deleted", id));
}

// Start
function start() {
  getCourses(renderCourses);
  
  document.getElementById("course-form").addEventListener("submit", function(e) {
    e.preventDefault();
    const name = document.querySelector('input[name="name"]').value;
    const description = document.querySelector('input[name="description"]').value;
    
    addCourses({ name, description }, function(newCourse) {
      renderCourses([...courses, newCourse]);
      e.target.reset();
    });
  });
}

function renderCourses(courses) {
  const list = document.getElementById("list-course");
  list.innerHTML = courses.map(c => `
    <li>
      <strong>${c.name}</strong> - ${c.description}
      <button class="delete" data-id="${c.id}">Xóa</button>
    </li>
  `).join("");
  
  list.addEventListener("click", function(e) {
    if (e.target.classList.contains("delete")) {
      const id = e.target.dataset.id;
      deleteCourse(id);
      e.target.closest("li").remove();
    }
  });
}

start();
```

### Ví dụ 2: Async/await version (modern)

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
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

async function deleteCourse(id) {
  const res = await fetch(`${API}/${id}`, { method: "DELETE" });
  return res.ok;
}

async function updateCourse(id, updates) {
  const res = await fetch(`${API}/${id}`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(updates)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Usage
async function init() {
  let courses = await getCourses();
  render(courses);
  
  document.getElementById("form").addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = e.target.name.value;
    const desc = e.target.description.value;
    const newCourse = await addCourse({ name, description: desc });
    courses.push(newCourse);
    render(courses);
    e.target.reset();
  });
}
init();
```

### Ví dụ 3: With loading state và error handling

```js
async function crudApp() {
  const listEl = document.getElementById("list-course");
  const formEl = document.getElementById("course-form");
  
  async function load() {
    listEl.innerHTML = "<li>Loading...</li>";
    try {
      const res = await fetch("http://localhost:3000/courses");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const courses = await res.json();
      render(courses);
    } catch (err) {
      listEl.innerHTML = `<li class="error">Error: ${err.message}</li>`;
    }
  }
  
  function render(courses) {
    if (courses.length === 0) {
      listEl.innerHTML = "<li>Chưa có khóa học nào</li>";
      return;
    }
    listEl.innerHTML = courses.map(c => `
      <li>
        <strong>${c.name}</strong> - ${c.description}
        <button class="delete" data-id="${c.id}">Xóa</button>
      </li>
    `).join("");
    
    listEl.querySelectorAll(".delete").forEach(btn => {
      btn.addEventListener("click", async () => {
        const id = btn.dataset.id;
        try {
          const res = await fetch(`http://localhost:3000/courses/${id}`, {
            method: "DELETE"
          });
          if (res.ok) btn.closest("li").remove();
        } catch (err) {
          alert("Delete failed: " + err.message);
        }
      });
    });
  }
  
  formEl.addEventListener("submit", async (e) => {
    e.preventDefault();
    const name = e.target.name.value;
    const desc = e.target.description.value;
    
    try {
      const res = await fetch("http://localhost:3000/courses", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, description: desc })
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const newCourse = await res.json();
      render([...courses, newCourse]);
      e.target.reset();
    } catch (err) {
      alert("Add failed: " + err.message);
    }
  });
  
  await load();
}
crudApp();
```

### Ví dụ 4: Exercise — thêm Update (PUT)

```js
// TODO: Implement updateCourse function
async function updateCourse(id, data) {
  const res = await fetch(`http://localhost:3000/courses/${id}`, {
    method: "PUT",           // hoặc "PATCH" cho partial update
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// Usage: edit button click handler
function renderEditButton(course) {
  return `<button class="edit" data-id="${course.id}">Sửa</button>`;
}
```

## 🔬 So sánh với alternatives

| Approach | Code complexity | Error handling | Best for |
|----------|-----------------|----------------|----------|
| Callback + fetch | Medium | Manual chain | Learning |
| Async/await + fetch | Low | try/catch | Production |
| Axios | Low | interceptors | Enterprise |
| Framework (React hooks) | Medium | React-query/SWR | Large apps |

## 📊 Performance & Best Practices

- **Luôn check `res.ok`** sau fetch — fetch không throw với HTTP error.
- **Set `Content-Type: application/json`** cho mọi POST/PUT/PATCH.
- **`JSON.stringify(data)`** cho body — object không tự convert thành string.
- **Re-render after mutation** — sau POST/DELETE/PUT, load lại list hoặc update DOM inline.
- **Add loading states** — "Loading..." trong lúc fetch.
- **Handle empty state** — "No courses" message khi list rỗng.
- **Run JSON server first** — `npx json-server --watch server.json --port 3000`.

## 🔗 Liên kết chéo

- **Xem thêm:** `13_working-with-apis/01_fetch` — fetch API details
- **Xem thêm:** `13_working-with-apis/03_json-server` — JSON Server setup
- **Xem thêm:** `13_working-with-apis/04_postman` — test endpoints với Postman
- **Xem thêm:** `13_working-with-apis/README` — APIs overview
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async/await pattern
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise foundation
