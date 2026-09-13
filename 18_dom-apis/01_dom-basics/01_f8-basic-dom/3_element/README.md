# Bài 3 — DOM Element: Truy Vấn Phần Tử — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

**Element** là loại node đại diện cho một thẻ HTML (`<div>`, `<span>`, `<input>`…). Có 5 cách chính để truy vấn element trong DOM, mỗi cách có trade-off về performance, tính live/static, và độ linh hoạt của selector.

### Bảng so sánh 5 phương thức

| Method | Trả về | Selector | Performance | Live/Static |
|---|---|---|---|---|
| `getElementById(id)` | Element hoặc null | id duy nhất | ⭐⭐⭐ nhanh nhất (O(1)) | N/A (1 element) |
| `getElementsByClassName(name)` | HTMLCollection | class name(s) | ⭐⭐ | **Live** — tự cập nhật |
| `getElementsByTagName(tag)` | HTMLCollection | tag name | ⭐⭐ | **Live** — tự cập nhật |
| `querySelector(sel)` | Element hoặc null | CSS selector | ⭐ | N/A (1 element) |
| `querySelectorAll(sel)` | NodeList (static) | CSS selector | ⭐ | **Static** — snapshot |

> **HTMLCollection** (live) — tự cập nhật khi DOM thay đổi. Nếu bạn thêm/xóa element, collection tự reflect.
> **NodeList** (static) — snapshot tại thời điểm gọi, không đổi khi DOM thay đổi sau đó.

### Sự khác biệt quan trọng

- `getElementsByClassName` nhận **space-separated** nhiều class: `.el.getElementsByClassName("btn primary")` tìm element có CẢ hai class.
- `getElementsByTagName` **không phân biệt hoa/thường** — `DIV` = `div`.
- `querySelector` chỉ trả **phần tử đầu tiên** matching — cần `querySelectorAll` để lấy tất cả.
- DOM lookup mỗi lần gọi — nên gán biến và reuse thay vì gọi lặp trong loop.

## 📐 Cấu trúc / Cú pháp

### 4 cách so sánh
```js
// 1. getElementById — nhanh nhất, 1 element duy nhất
const box = document.getElementById("app");

// 2. getElementsByClassName — HTMLCollection (live)
const btns = document.getElementsByClassName("btn");
// btns.length tự tăng/giảm khi DOM đổi

// 3. getElementsByTagName — HTMLCollection (live)
const lis = document.getElementsByTagName("li");

// 4. querySelector / querySelectorAll — NodeList (static)
const firstP = document.querySelector("p.highlight");
const allLinks = document.querySelectorAll("a[href^='https://']");
```

### Lặp qua NodeList vs HTMLCollection
```js
// NodeList — static, không có .forEach native (nhưng có trong modern browser)
const items = document.querySelectorAll(".item");
items.forEach((el, i) => {
  console.log(i, el.textContent.trim());
});

// Hoặc dùng for...of — an toàn cho cả NodeList và HTMLCollection
for (const el of items) {
  el.style.color = "blue";
}

// HTMLCollection — cũng dùng được for...of
for (const li of lis) {
  li.style.fontWeight = "bold";
}
```

### Spread NodeList thành mảng
```js
const arr = [...document.querySelectorAll("div.box")];
arr.reverse();       // giờ có array methods
arr.map(el => el.id);
arr.filter(el => el.classList.contains('active'));

// Hoặc Array.from
const arr2 = Array.from(document.querySelectorAll("span"));
```

### CSS selector power của querySelector
```js
// Complex selectors
const el1 = document.querySelector("#main .content > p:first-child");
const el2 = document.querySelectorAll("input[type='email']:valid");
const el3 = document.querySelector("div:not(.hidden)");
const el4 = document.querySelectorAll("li:nth-child(odd)");
const el5 = document.querySelector("[data-role='admin']");
```

## ✅ Điểm mạnh

1. **`querySelector` hỗ trợ mọi CSS selector phức tạp** — `div > p.class:nth-child(2)` viết được tất cả.
2. **`querySelectorAll` + spread `[...elements]`** biến NodeList thành mảng — dùng được `map`/`filter`/`reduce`.
3. **`getElementsBy*` live collection** — không cần gọi lại khi DOM đổi, tự update.
4. **`getElementById` O(1)** — nhanh nhất, dùng khi có id.
5. **`querySelector` return null nếu không tìm thấy** — an toàn hơn throw error.
6. **CSS specificity rules áp dụng** — selector đúng ngữ cảnh trang.
7. **Return first match** — `querySelector` dừng sớm, fast cho "first" search.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`getElementsByClassName` nhận space-separated nhiều class** — `.el.getElementsByClassName("btn primary")` yêu cầu element có CẢ hai class, không phải "btn HOẶC primary".
2. **`getElementsByTagName` không phân biệt hoa/thường** — `DIV` = `div` = `DiV`.
3. **`querySelector` chỉ trả phần tử đầu tiên** — cần `querySelectorAll` để lấy tất cả.
4. **DOM lookup mỗi lần gọi** — `document.querySelectorAll(...).length` trong loop condition gây lookup lặp. Gán biến trước.
5. **`querySelectorAll` trả NodeList static** — nếu DOM đổi sau khi query, NodeList không update.
6. **ID phải unique** — `getElementById` chỉ trả element đầu tiên nếu có nhiều id trùng (invalid HTML).
7. **Selector invalid → SyntaxError** — `querySelector("[invalid")` throw error ngay.

## 💡 Khi nào dùng — Tình huống thực tế

1. **Lấy phần tử duy nhất theo id** → `getElementById` (nhanh nhất).
2. **Selector phức tạp** (nested, pseudo-class, attribute) → `querySelector`/`querySelectorAll`.
3. **Lấy nhiều phần tử theo class/tag** → `querySelectorAll` (static, predictable) hoặc `getElementsBy*` (live, auto-update).
4. **Duyệt danh sách** → `for...of` NodeList an toàn hơn `for` mảng truyền thống.
5. **React-style pattern** — query once, cache result, only re-query when DOM definitely changed.
6. **Dynamic content** — nếu element có thể thêm/xóa sau query, dùng live HTMLCollection.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: 4 cách truy vấn cơ bản
```js
//ByID — nhanh nhất
const box = document.getElementById("app");

// By class — HTMLCollection live
const btns = document.getElementsByClassName("btn");
console.log(typeof btns.forEach); // undefined — không phải array

// By tag — HTMLCollection live
const lis = document.getElementsByTagName("li");

// By selector — NodeList static
const firstP = document.querySelector("p.highlight");
const allLinks = document.querySelectorAll("a[href^='https://']");
```

### Ví dụ 2: Lặp qua NodeList an toàn
```js
const items = document.querySelectorAll(".item");

// Cách 1: for...of (recommend)
for (const el of items) {
  el.style.color = "blue";
}

// Cách 2: Array.from
Array.from(items).forEach((el, i) => {
  el.textContent = `Item ${i + 1}`;
});

// Cách 3: Spread + forEach
[...items].forEach(el => el.classList.add('highlighted'));
```

### Ví dụ 3: Spread NodeList thành mảng + array methods
```js
const divs = [...document.querySelectorAll("div.box")];
divs.reverse(); // giờ có array methods
const ids = divs.map(d => d.id).filter(id => id);
console.log(ids);
```

### Ví dụ 4: Complex CSS selector
```js
// Tìm input email chưa valid
const invalidEmails = document.querySelectorAll("input[type='email']:invalid");

// Tìm tất cả link external (開新 tab)
const externalLinks = document.querySelectorAll("a[href^='http']:not([href*='example.com'])");

// Tìm checkbox trong form có class 'settings'
const settingsCheckboxes = document.querySelectorAll("form.settings input[type='checkbox']");
```

### Ví dụ 5: Live vs Static behavior demo
```js
const ul = document.querySelector("ul");

// HTMLCollection — LIVE
const lis_live = ul.getElementsByTagName("li");
console.log(lis_live.length); // 3

const newLi = document.createElement("li");
newLi.textContent = "New item";
ul.appendChild(newLi);
console.log(lis_live.length); // 4 — tự update! ✅

// NodeList — STATIC
const lis_static = ul.querySelectorAll("li");
console.log(lis_static.length); // 4 (snapshot tại thời điểm query)

const anotherLi = document.createElement("li");
anotherLi.textContent = "Another";
ul.appendChild(anotherLi);
console.log(lis_static.length); // vẫn 4 — không update! ⚠️
```

### Ví dụ 6: Cache query results in loop
```js
// ❌ BAD — query mỗi iteration
for (let i = 0; i < 1000; i++) {
  document.querySelector(".target").style.left = i + 'px';
}

// ✅ GOOD — cache result
const target = document.querySelector(".target");
for (let i = 0; i < 1000; i++) {
  target.style.left = i + 'px';
}
```

### Ví dụ 7: Safe query with null check
```js
function safeQuery(selector, context = document) {
  const el = context.querySelector(selector);
  if (!el) {
    console.warn(`Element not found: ${selector}`);
    return null;
  }
  return el;
}

const btn = safeQuery('#submit-btn');
if (btn) {
  btn.addEventListener('click', handleSubmit);
}
```

## 🔬 So sánh với alternatives

| Method | Trả về | Live? | Selector power | Performance |
|---|---|---|---|---|
| `getElementById` | Element/null | N/A | Chỉ id | ⭐⭐⭐ |
| `getElementsByClassName` | HTMLCollection | ✅ Live | Class names | ⭐⭐ |
| `getElementsByTagName` | HTMLCollection | ✅ Live | Tag name | ⭐⭐ |
| `querySelector` | Element/null | N/A | Full CSS | ⭐ |
| `querySelectorAll` | NodeList (static) | ❌ Static | Full CSS | ⭐ |

## 📊 Performance & Best Practices

- **Prefer `getElementById`** khi có id — O(1) lookup, nhanh nhất.
- **Cache query results** — gán biến `const el = ...` thay vì gọi lặp.
- **Batch DOM reads/writes** — đọc tất cả trước, ghi tất cả sau — tránh layout thrashing.
- **Use `for...of`** thay vì `for` vòng với index — cleaner, works với iterable.
- **Avoid `getElementsBy*` in performance-critical code** — live collection có overhead tracking DOM changes.
- **Prefer `querySelectorAll` + spread** over `getElementsBy*` — predictable static snapshot, array methods.
- **Test selector validity** — invalid CSS selector throw SyntaxError, wrap in try/catch nếu dynamic selector.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/1_dom-api/` — document basics.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/4_attribute/` — attribute manipulation sau khi query.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/7_node-property/` — node properties sau khi có element.
- File tham khảo: `app.js`, `index.html` trong folder `3_element/`.
