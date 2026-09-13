# Sự kiện trang web và vòng đời load — Ví dụ To-do List — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ví dụ này là một **to-do list thuần JavaScript** (`app.js` + `index.html` + `style.css`), tận dụng *các sự kiện vòng đời của trang* và DOM Manipulation để vận hành:

### Các sự kiện vòng đời trang

| Event | Khi nào fire | Dùng cho |
|---|---|---|
| `DOMContentLoaded` | HTML parse xong, DOM ready (ảnh/CSS chưa cần xong) | Gắn handler vào elements — thời điểm an toàn nhất |
| `load` | Tất cả tài nguyên (ảnh, CSS, font, iframe) load xong | Đo kích thước ảnh, lazy load init |
| `beforeunload` | Người dùng chuẩn bị rời trang (đóng tab/điều hướng) | Xác nhận lưu dữ liệu chưa save |
| `unload` | Trang đang bị đóng — cleanup cuối | Gửi ping, localStorage save |
| `hashchange` | Phần `#...` của URL đổi | SPA router kiểu hash-based |
| `resize` | Cửa sổ đổi kích thước | Responsive layout update |

### Tại sao `DOMContentLoaded` quan trọng?
Đây là thời điểm **đúng nhất** để gắn handler vào các phần tử — bảo đảm `getElementById` tìm được nút như `taskInput`, `addTaskBtn`, `taskList`. Nếu chạy sớm hơn (trước DOM parse xong), query sẽ trả `null`.

### Cơ chế core của to-do list
Mỗi lần bấm **Add task**, app `createElement('li')`, set `textContent`, gắn listener riêng để `remove()` khi click vào task. Vòng lặp DOM + events như vậy là nền tảng của mọi ứng dụng động.

## 📐 Cấu trúc / Cú pháp

### Basic to-do list
```js
document.addEventListener('DOMContentLoaded', function () {
  const taskInput = document.getElementById('taskInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', function () {
    const text = taskInput.value.trim();
    if (text !== '') {
      const li = document.createElement('li');
      li.textContent = text;
      li.addEventListener('click', () => li.remove());
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });
});
```

### Lifecycle events
```js
// DOM ready — attach handlers
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM ready — safe to query elements');
});

// All resources loaded
window.addEventListener('load', function () {
  console.log('All resources loaded');
});

// Before unload — warn unsaved changes
window.addEventListener('beforeunload', (event) => {
  if (hasUnsavedChanges) {
    event.returnValue = ''; // modern browsers show confirm dialog
  }
});

// Hash change — SPA routing
window.addEventListener('hashchange', () => {
  console.log('Hash changed to:', window.location.hash);
});

// Resize — responsive adjustments
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    console.log('Window resized to:', window.innerWidth, 'x', window.innerHeight);
  }, 150);
});
```

## ✅ Điểm mạnh

1. **Thao tác DOM tối giản nhưng đủ** — tạo element, gắn text, thêm vào list, xóa bằng chính sự kiện click.
2. **Sự kiện vòng đời bao phủ đủ tình huống** load/tải/rời trang — một bộ kiến thức hay gặp khi làm SPA.
3. **Vanilla JS** — không phụ thuộc framework, hiểu được luồng trực tiếp.
4. **`removeEventListener` dễ thử** cùng mẫu — ôn lại bài 12 của `01_f8-basic-dom`.
5. **Event delegation ready** — mẫu này dễ nâng cấp lên delegation pattern.
6. **Lifecycle awareness** — hiểu khi nào DOM ready, khi nào resources loaded.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`DOMContentLoaded` ≠ `load`** — gắn handler vào `load` sau khi DOM xong khiến trang **phản ứng chậm** hơn với user.
2. **`unload`/`beforeunload` không đáng tin để lưu state quan trọng** — có thể bị cancel, chạy không đủ hoàn tất — nên lưu qua `pagehide`/`visibilitychange`.
3. **Listener remove gắn trực tiếp vào từng `<li>`** — list nhiều thêm sẽ nhiều listener; nên dùng **event delegation** (gắn một listener ở `taskList`) khi scale.
4. **`resize`/`hashchange` thường xuyên kích hoạt** — nếu callback nặng nên **debounce/throttle**.
5. **Closure trong listener giữ reference** — mỗi `<li>` listener giữ closure scope → memory overhead khi list dài.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Gắn handlers sau khi DOM parse xong** — chuẩn của mọi trang dùng JS.
2. **Xác nhận rời trang có dữ liệu chưa lưu** — `beforeunload` event.
3. **Điều hướng SPA đơn giản bằng hash** — `hashchange` event.
4. **Hiển thị UI đáp ứng đúng kích thước** — `resize` event + debounce.
5. **Vẽ danh sách động kiểu to-do** — thêm/xóa phần tử theo sự kiện.
6. **Page visibility API** — pause/resume content khi tab ẩn/hiện.

## 🎯 Ví dụ minh họa

### Ví dụ 1: To-do list cơ bản
```js
document.addEventListener('DOMContentLoaded', function () {
  const taskInput = document.getElementById('taskInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', function () {
    const text = taskInput.value.trim();
    if (text !== '') {
      const li = document.createElement('li');
      li.textContent = text;
      li.addEventListener('click', () => li.remove());
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });
});
```

### Ví dụ 2: Event delegation version (better for scale)
```js
document.addEventListener('DOMContentLoaded', function () {
  const taskInput = document.getElementById('taskInput');
  const addTaskBtn = document.getElementById('addTaskBtn');
  const taskList = document.getElementById('taskList');

  addTaskBtn.addEventListener('click', function () {
    const text = taskInput.value.trim();
    if (text !== '') {
      const li = document.createElement('li');
      li.textContent = text;
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });

  // 1 listener ở parent lo được mọi click trên child
  taskList.addEventListener('click', function (e) {
    if (e.target.tagName === 'LI') {
      e.target.remove();
    }
  });
});
```

### Ví dụ 3: Lifecycle events đầy đủ
```js
document.addEventListener('DOMContentLoaded', function () {
  console.log('DOM ready');
  initApp();
});

window.addEventListener('load', function () {
  console.log('All resources loaded');
  initLazyLoading();
});

window.addEventListener('beforeunload', (event) => {
  if (hasUnsavedChanges()) {
    event.returnValue = '';
  }
});

window.addEventListener('hashchange', () => {
  console.log('Hash changed to:', location.hash);
  routeTo(location.hash);
});

let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    adjustLayout();
  }, 150);
});
```

### Ví dụ 4: Add "Clear All" button
```js
const clearBtn = document.getElementById('clearAllBtn');
clearBtn.addEventListener('click', () => {
  taskList.innerHTML = ''; // clear all tasks
});
```

### Ví dụ 5: Enter key to add task
```js
taskInput.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') {
    addTaskBtn.click(); // trigger add
  }
});
```

### Ví dụ 6: Persist tasks to localStorage
```js
// Save on every change
function saveTasks() {
  const tasks = [...taskList.querySelectorAll('li')].map(li => li.textContent);
  localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Load on startup
function loadTasks() {
  const tasks = JSON.parse(localStorage.getItem('tasks') || '[]');
  tasks.forEach(text => {
    const li = document.createElement('li');
    li.textContent = text;
    taskList.appendChild(li);
  });
}

// Hook into add/remove
addTaskBtn.addEventListener('click', () => { saveTasks(); });
taskList.addEventListener('click', (e) => {
  if (e.target.tagName === 'LI') {
    e.target.remove();
    saveTasks();
  }
});
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — event types.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/10_dom-event/` — addEventListener basics.
- Xem thêm: `18_dom-apis/03_events/` — bubbling/capturing deep dive.
- Ôn sự kiện tiếp theo tại: `18_dom-apis/03_events/README.md`.
- File tham khảo: `app.js`, `index.html`, `style.css` trong folder `example-2/`.
