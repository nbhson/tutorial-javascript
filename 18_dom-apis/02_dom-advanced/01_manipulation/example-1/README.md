# DOM Manipulation — Example 1 — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ví dụ này minh họa các thao tác **thêm/xóa/đổi vị trí node** trong DOM tree. Đây là nền tảng của mọi DOM manipulation — hiểu rõ các method này giúp bạn làm chủ việc xây dựng dynamic UI.

### Bảng methods thao tác node

| Method | Mô tả |
|---|---|
| `parent.appendChild(node)` | Đưa node vào cuối children |
| `parent.insertBefore(new, ref)` | Chèn node trước ref node |
| `parent.replaceChild(new, old)` | Thay thế old bằng new |
| `parent.removeChild(node)` | Xóa node khỏi parent |
| `node.cloneNode(deep)` | Clone node (deep=true clone cả children) |
| `node.remove()` | Xóa node (modern, tương đương removeChild) |
| `parent.append(...nodes)` | DOM Level 4 — thêm nhiều node, accept strings |
| `parent.prepend(...nodes)` | DOM Level 4 — thêm vào đầu |
| `node.replaceWith(...nodes)` | DOM Level 4 — thay thế node bằng nodes mới |
| `node.before(...nodes)` | DOM Level 4 — chèn trước node |
| `node.after(...nodes)` | DOM Level 4 — chèn sau node |

### Điểm quan trọng: append node đã tồn tại → DI CHUYỂN chứ không COPY
```js
const parent = document.querySelector('#parent');
const child = document.querySelector('#child');
parent.appendChild(child); // child di chuyển từ vị trí cũ sang cuối parent
// child KHÔNG bị copy — nó biến khỏi vị trí cũ
```

## 📐 Cấu trúc / Cú pháp

### Todo list CRUD
```js
const list = document.querySelector("ul");
const input = document.querySelector("input");
const btn = document.querySelector("button");

function addTodo(text) {
  const li = document.createElement("li");
  li.textContent = text;
  
  const delBtn = document.createElement("button");
  delBtn.textContent = "✕";
  delBtn.addEventListener("click", () => li.remove());
  
  li.appendChild(delBtn);
  list.appendChild(li);
}

btn.addEventListener("click", () => {
  if (input.value.trim()) {
    addTodo(input.value.trim());
    input.value = "";
  }
});
```

### Clone và thêm
```js
const template = document.querySelector("#item-template");
const clone = template.cloneNode(true); // deep clone — cả children
clone.querySelector(".name").textContent = "New Item";
list.appendChild(clone);
```

### Reorder bằng drag (giả lập)
```js
// Di chuyển item đầu tiên xuống cuối
const first = list.firstElementChild;
if (first) list.appendChild(first);

// Hoặc đưa lên đầu
const last = list.lastElementChild;
if (last) list.insertBefore(last, list.firstElementChild);
```

## ✅ Điểm mạnh

1. **Di chuyển node không copy** — node biến khỏi vị trí cũ tự động, tiết kiệm bộ nhớ.
2. **`cloneNode(true)` copy nguyên subtree** — hữu ích cho template-based rendering.
3. **`append`/`prepend`/`replaceWith`/`before`/`after`** (DOM Level 4) gọn hơn phương thức cũ — accept multiple nodes và strings.
4. **`remove()` modern** — ngắn gọn hơn `removeChild`, không cần reference đến parent.
5. **Straightforward API** — dễ hiểu, dễ nhớ, không có abstraction layer.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **Append node đã tồn tại → di chuyển chứ không copy** — nếu muốn copy, dùng `cloneNode(true)` trước.
2. **`removeChild` cần reference đến node con** — nếu chỉ có selector phải query lại.
3. **`cloneNode(false)` chỉ clone node itself, không clone children** — thường không phải cái bạn muốn.
4. **Clone giữ event listeners?** — `cloneNode(true)` clone DOM structure nhưng NOT event listeners (trừ khi dùng `{ capture: true }` special case).
5. **insertBefore với ref=null** — tương đương appendChild (thêm vào cuối).

## 💡 Khi nào dùng — Tình huống thực tến

1. **Todo list**: add/remove/edit item động.
2. **Drag & drop reorder** — di chuyển element trong list.
3. **Dynamic table row addition/removal** — thêm/xóa dòng table.
4. **Template-based rendering** — clone template node, fill data, append.
5. **Modal/dialog insertion** — insert vào correct position trong DOM.
6. **Accordions/tabs** — show/hide content bằng append/remove.

## 🎯 Ví dụ minh họa

### Ví dụ 1: Todo list CRUD hoàn chỉnh
```js
const list = document.querySelector("ul");
const input = document.querySelector("input");
const btn = document.querySelector("button");

function addTodo(text) {
  const li = document.createElement("li");
  li.textContent = text;
  
  const delBtn = document.createElement("button");
  delBtn.textContent = "✕";
  delBtn.addEventListener("click", () => li.remove());
  
  li.appendChild(delBtn);
  list.appendChild(li);
}

btn.addEventListener("click", () => {
  if (input.value.trim()) {
    addTodo(input.value.trim());
    input.value = "";
  }
});
```

### Ví dụ 2: Clone template
```js
const template = document.querySelector("#item-template");
const clone = template.cloneNode(true);
clone.querySelector(".name").textContent = "New Item";
clone.querySelector(".price").textContent = "$9.99";
list.appendChild(clone);
```

### Ví dụ 3: Move to top
```js
function moveToTop(item) {
  if (item.parentElement.firstChild !== item) {
    item.parentElement.insertBefore(item, item.parentElement.firstChild);
  }
}
```

### Ví dụ 4: Replace entire list
```js
function replaceList(newItems) {
  const list = document.querySelector("ul");
  list.innerHTML = ''; // clear all
  newItems.forEach(text => {
    const li = document.createElement("li");
    li.textContent = text;
    list.appendChild(li);
  });
}
```

### Ví dụ 5: DOM Level 4 methods (modern)
```js
const el = document.querySelector(".container");

// prepend — thêm vào đầu
el.prepend("<span>First</span>", document.createTextNode(" Text"));

// append — thêm vào cuối
el.append("<span>Last</span>");

// before/after — sibling insertion
el.before("<div>Before</div>");
el.after("<div>After</div>");

// replaceWith — thay thế
el.replaceWith("<span>Replaced</span>");
```

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/02_dom-advanced/01_manipulation/` — DOM manipulation tổng quan.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — node properties.
- File tham khảo: `app.js`, `index.html`, `style.css` trong folder `example-1/`.
