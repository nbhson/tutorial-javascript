# DOM Manipulation — Thao Tác Trực Tiếp DOM — [Level: Intermediate]

## 🔑 Khái niệm cốt lõi

**DOM Manipulation** (hay *JS DOM Manipulation*) là **quá trình thay đổi cấu trúc, nội dung và kiểu dáng của trang web** bằng cách tương tác trực tiếp với cây DOM qua JavaScript. Không qua framework, không qua lớp trung gian ảo — bạn gọi API của trình duyệt để:

- **Tìm phần tử**: `document.getElementById`, `querySelector`, `querySelectorAll`.
- **Sửa nội dung**: `textContent`, `innerText`, `innerHTML`, `appendChild`, `remove`.
- **Sửa thuộc tính/style/class**: `setAttribute`, `element.style`, `classList`.
- **Lắng nghe sự kiện**: `addEventListener`.

Ưu điểm cốt lõi: **linh hoạt, tức thì, không phụ thuộc framework, tương thích mọi trình duyệt**. Nhược điểm cũng nằm ở chỗ đó: nếu thao tác quá nhiều (nhất là trong vòng lặp, hoặc làm rải rác nhiều chỗ cùng lúc) mỗi lần đổi DOM đều gây **reflow/layout và paint lại** → hiệu năng giảm, xác suất lỗi tăng khi code phình to.

### Các thao tác DOM cơ bản

| Thao tác | Method | Ví dụ |
|---|---|---|
| Tạo element | `document.createElement(tag)` | `const div = document.createElement('div')` |
| Thêm vào parent | `parent.appendChild(child)` | `container.appendChild(div)` |
| Chèn trước ref | `parent.insertBefore(new, ref)` | `container.insertBefore(new, ref)` |
| Thay thế | `parent.replaceChild(new, old)` | `container.replaceChild(new, old)` |
| Xóa con | `parent.removeChild(child)` | `container.removeChild(div)` |
| Xóa bản thân | `node.remove()` | `div.remove()` |
| Clone | `node.cloneNode(deep)` | `div.cloneNode(true)` |
| Set nội dung | `el.textContent = '...'` | `el.textContent = 'Hello'` |
| Set HTML | `el.innerHTML = '...'` | `el.innerHTML = '<b>Bold</b>'` |

Thư mục này có 2 ví dụ:
- `example-1/` — nút "Click me": khi click sẽ cập nhật `innerText`, đổi `setAttribute("style", ...)` và thay luôn `outerHTML` thành một `<image>`.
- `example-2/` — **to-do list** thuần JS: `DOMContentLoaded`, `createElement('li')`, gắn sự kiện click để `remove()` task.

## 📐 Cấu trúc / Cú pháp

### Node manipulation methods
```js
const parent = document.querySelector('#parent');
const child = document.createElement('div');

// Append (add to end)
parent.appendChild(child);

// Insert before reference node
const ref = parent.firstElementChild;
parent.insertBefore(child, ref);

// Replace
parent.replaceChild(child, ref);

// Remove
parent.removeChild(child);
// hoặc modern:
child.remove();

// Clone
const clone = child.cloneNode(true); // true = deep clone (cả children)
const shallow = child.cloneNode(false); // false = chỉ node itself
```

### Content manipulation
```js
const el = document.querySelector('.box');

// Text content (safe, no HTML parse)
el.textContent = 'Hello World';

// Inner HTML (parses HTML string)
el.innerHTML = '<p>Hello <strong>World</strong></p>';

// Insert adjacent (preserves existing listeners)
el.insertAdjacentHTML('beforeend', '<span>New</span>');
el.insertAdjacentElement('afterbegin', newElement);

// Outer HTML (replace the element itself)
el.outerHTML = '<span>Replaced</span>';
```

### Class and style manipulation
```js
el.classList.add('active', 'highlight');
el.classList.remove('inactive');
el.classList.toggle('open', isVisible);

el.style.color = 'red';
el.style.fontSize = '16px';
Object.assign(el.style, { color: 'blue', fontSize: '20px' });
```

## ✅ Điểm mạnh

1. **Độ linh hoạt cao** — đóng/mở, thêm/sửa/xóa bất kỳ phần nào của trang không cần reload.
2. **Phản hồi nhanh, trực tiếp** — thao tác tức thì, không phải chờ change detection của framework.
3. **Tương thích rộng** — API chuẩn trên mọi trình duyệt, không yêu cầu framework/thư viện.
4. **Dễ học, dễ debug** — không có lớp diff — bạn thấy đúng hành vi mình viết.
5. **Kết hợp tốt với framework** — dùng trong hook/no-FW case, micro-interaction.
6. **Zero dependency** — không cần install gì, chạy trên mọi browser.
7. **Full control** — bạn kiểm soát exact DOM state tại mọi thời điểm.
8. **Performance predictable** — không có abstraction overhead, biết chính xác khi nào reflow xảy ra.
9. **Learning foundation** — hiểu DOM manipulation là nền tảng để hiểu React/Vue internals.
10. **Small bundle size** — không thêm dependency vào project.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Hiệu suất** — nhiều lần thay đổi trong vòng lặp / quá nhiều listener → reflow, render lại, giật.
2. **Bảo trì khó khi to** — cây DOM lớn, ít cấu trúc — việc quản lý code thao tác tay trở nên phức tạp.
3. **Rò rỉ bộ nhớ** — quên `removeEventListener`, giữ ref tới node đã gỡ → detached DOM, memory leak.
4. **Khác biệt trình duyệt nhỏ** trong vài API/khoảng trắng text node — thường phải tinh chỉnh.
5. **innerHTML với user input = XSS risk** — luôn escape hoặc dùng textContent.
6. **No state management** — phải tự track state và sync với DOM (framework làm việc này auto).
7. **Tight coupling** — DOM logic trộn với business logic, khó test unit.
8. **Scalability limit** — app lớn với nhiều DOM interactions khó maintain hơn so với declarative approach.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Ứng dụng nhỏ / prototype** — thao tác trực tiếp đơn giản, linh hoạt.
2. **Thay đổi DOM tức thời** khi sự kiện xảy ra (đổi màu, hiện/ẩn, filter phía client).
3. **Thêm widget nhỏ** vào trang có sẵn mà không muốn đưa cả framework vào.
4. **Khi cần điều khiển chính xác từng nút** — micro-animation, được đo đếm thủ công.
5. **Progressive enhancement** — trang HTML cơ bản + JS enhancementlayers.
6. **Bookmarklet / userscript** — modify existing pages without framework.
7. **Performance-critical paths** — khi abstraction overhead không acceptable.
8. **Học tập / demonstration** — hiểu rõ mechanism trước khi dùng framework.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: DOM Manipulation cơ bản (example-1 pattern)
```js
document.addEventListener('DOMContentLoaded', function () {
  const btn = document.getElementById('btnClickMe');
  btn.addEventListener('click', function () {
    btn.innerText = "What's up";                       // đổi text
    btn.setAttribute('style', 'color:red; padding:4px'); // đổi inline style
    // Có thể thay luôn outerHTML bằng ảnh đại diện
    // btn.outerHTML = '<img src="..." alt="replaced">';
  });
});
```

### Ví dụ 2: To-do list CRUD (example-2 pattern)
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
      li.addEventListener('click', () => li.remove()); // xóa khi click
      taskList.appendChild(li);
      taskInput.value = '';
    }
  });
});
```

### Ví dụ 3: Event delegation — scalable to-do
```js
const taskList = document.getElementById('taskList');

taskList.addEventListener('click', (e) => {
  const li = e.target.closest('li');
  if (!li) return;
  
  if (e.target.classList.contains('delete')) {
    li.remove();
  } else if (e.target.tagName === 'LI') {
    li.classList.toggle('completed');
  }
});
// 1 listener ở ul lo được mọi action — thêm/xóa task tùy ý
```

### Ví dụ 4: Dynamic list rendering
```js
function renderList(items, containerId) {
  const container = document.getElementById(containerId);
  container.innerHTML = items.map(item => `
    <div class="item" data-id="${item.id}">
      <span class="name">${escapeHtml(item.name)}</span>
      <span class="status">${item.active ? '✅' : '❌'}</span>
    </div>
  `).join('');
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}
```

### Ví dụ 5: Batch DOM changes — DocumentFragment
```js
function appendMany(parentSelector, items) {
  const parent = document.querySelector(parentSelector);
  const fragment = document.createDocumentFragment();
  
  items.forEach(text => {
    const li = document.createElement('li');
    li.textContent = text;
    fragment.appendChild(li);
  });
  
  parent.appendChild(fragment); // 1 reflow thay vì N reflows
}
```

### Ví dụ 6: Accordion pattern
```js
document.querySelectorAll('.accordion-header').forEach(header => {
  header.addEventListener('click', () => {
    const panel = header.nextElementSibling;
    const isOpen = header.classList.toggle('opened');
    panel.style.maxHeight = isOpen ? panel.scrollHeight + 'px' : '0';
    
    // Close others
    document.querySelectorAll('.accordion-header').forEach(other => {
      if (other !== header) {
        other.classList.remove('opened');
        other.nextElementSibling.style.maxHeight = '0';
      }
    });
  });
});
```

### Ví dụ 7: Modal with lifecycle events
```js
const modal = document.querySelector('.modal');
const overlay = document.querySelector('.modal-overlay');

function openModal() {
  modal.classList.add('visible');
  overlay.addEventListener('click', closeModal);
  document.addEventListener('keydown', handleKey);
}

function closeModal() {
  modal.classList.remove('visible');
  overlay.removeEventListener('click', closeModal);
  document.removeEventListener('keydown', handleKey);
}

function handleKey(e) {
  if (e.key === 'Escape') closeModal();
}
```

### Ví dụ 8: Infinite scroll pattern
```js
let page = 1;
let isLoading = false;

function loadMore() {
  if (isLoading) return;
  isLoading = true;
  
  fetch(`/api/items?page=${page}`)
    .then(res => res.json())
    .then(data => {
      const fragment = document.createDocumentFragment();
      data.items.forEach(item => {
        const div = document.createElement('div');
        div.textContent = item.name;
        fragment.appendChild(div);
      });
      document.getElementById('list').appendChild(fragment);
      page++;
      isLoading = false;
    });
}

window.addEventListener('scroll', () => {
  if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500) {
    loadMore();
  }
}, { passive: true });
```

## 🔬 So sánh với alternatives

| Approach | Flexibility | Performance | Maintainability | Bundle Size |
|---|---|---|---|---|
| **Vanilla DOM Manipulation** | ⭐⭐⭐ Highest | ⭐⭐⭐ Fastest | ⭐⭐ Medium | 0KB |
| **jQuery** | ⭐⭐⭐ High | ⭐⭐⭐ Fast | ⭐⭐⭐ Better | ~30KB |
| **React Virtual DOM** | ⭐⭐⭐ Declarative | ⭐⭐ Medium | ⭐⭐⭐ High | ~30-100KB |
| **Vue Reactivity** | ⭐⭐⭐ Declarative | ⭐⭐ Medium | ⭐⭐⭐ High | ~30-50KB |
| **Vanilla + Template Strings** | ⭐⭐ Medium | ⭐⭐⭐ Fast | ⭐⭐ Medium | 0KB |

## 📊 Performance & Best Practices

- **Batch DOM mutations**: dùng `DocumentFragment` hoặc `innerHTML` batch thay vì append từng node.
- **Avoid reflow in loop**: đọc `offsetWidth`/`offsetHeight` trong loop gây layout thrashing — batch reads trước, writes sau.
- **Event delegation**: 1 listener ở parent thay vì N listeners ở children — giảm memory, tăng performance.
- **Cache references**: `const el = document.querySelector(...)` thay vì gọi lặp.
- **Passive listeners for scroll**: `{ passive: true }` giúp browser optimize scroll handling.
- **Use `requestAnimationFrame`**: cho animation DOM changes — sync với browser paint cycle.
- **textContent > innerHTML for user data**: tránh XSS, faster (không parse HTML).
- **Clean up listeners**: `removeEventListener` khi component unmount — tránh memory leak.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/example-1/` — click button demo.
- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/example-2/` — to-do list pattern.
- Xem thêm: `18_dom-apis/01_dom-basics/` — 12 bài fundamentals DOM.
- Xem thêm: `18_dom-apis/03_events/` — event system chi tiết.
- Xem thêm: `17_memory-management/01_memory-lifecycle-gc/02_memory-leaks/` — listener leak pattern.
