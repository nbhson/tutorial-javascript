# Bài 11 — preventDefault & StopPropagation — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Ba phương thức quan trọng nhất để kiểm soát hành vi event trong DOM:

| Method | Mục đích | Hiệu ứng |
|---|---|---|
| `event.preventDefault()` | Ngăn **hành vi mặc định** của browser | Link không navigate, form không submit, checkbox không toggle |
| `event.stopPropagation()` | Ngăn **bubble/capture** lên parent | Parent handler KHÔNG chạy |
| `event.stopImmediatePropagation()` | Ngăn cả các handler khác trên **cùng element** | Các listener cùng element cũng không chạy |

### preventDefault — chặn hành vi mặc định
- `<a href="...">` → không navigate
- `<form submit>` → không reload trang
- `<input type="checkbox">` → không toggle check
- `<input type="radio">` → không select
- `right-click` → không hiện context menu
- `spacebar` trên input → không scroll trang

**Quan trọng**: `preventDefault` **không hủy event** — các handler khác vẫn chạy. Nó chỉ ngăn hành vi mặc định của browser.

### stopPropagation — chặn đường lan truyền
```
document
  └─ body
       └─ div.box
            └─ button
```
Nếu click `button` và gọi `stopPropagation()`, handler trên `div.box` và `document` sẽ **không chạy** (trong bubble phase).

### stopImmediatePropagation — chặn handler cùng element
```js
el.addEventListener('click', () => console.log('handler 1'));
el.addEventListener('click', (e) => {
  e.stopImmediatePropagation();
  console.log('handler 2');
});
el.addEventListener('click', () => console.log('handler 3'));
// Click → chỉ in "handler 2", handler 1 và 3 không chạy
```

## 📐 Cấu trúc / Cú pháp

### preventDefault — form validation
```js
form.addEventListener("submit", (e) => {
  e.preventDefault(); // dừng reload trang
  
  if (!emailValid(emailInput.value)) {
    emailInput.classList.add("error");
    return;
  }
  
  // submit qua fetch thay vì reload
  fetch("/api/login", { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => console.log(data));
});
```

### preventDefault — link trong-app navigation
```js
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener("click", (e) => {
    e.preventDefault(); // không cuộn lên đầu trang
    const targetId = link.getAttribute("href").slice(1);
    document.getElementById(targetId)?.scrollIntoView({ behavior: 'smooth' });
  });
});
```

### stopPropagation — nested clickable elements
```js
const parent = document.querySelector('.parent');
const child = document.querySelector('.child');

parent.addEventListener("click", () => console.log("parent"));
child.addEventListener("click", (e) => {
  e.stopPropagation(); // parent không log
  console.log("child");
});
// click child → chỉ log "child"
// click parent area → chỉ log "parent"
```

### stopImmediatePropagation — cùng element
```js
const btn = document.querySelector('button');
btn.addEventListener('click', () => console.log('first'));
btn.addEventListener('click', (e) => {
  e.stopImmediatePropagation();
  console.log('second');
});
btn.addEventListener('click', () => console.log('third'));
// click → chỉ in "second"
```

## ✅ Điểm mạnh

1. **`preventDefault` giữ UX intact** — form validation rồi submit JS thay vì reload trang.
2. **`stopPropagation` cách ly event scope** — component không ảnh hưởng parent handler.
3. **Kết hợp cả 2** khi cần prevent default + chặn parent handler.
4. **`stopImmediatePropagation`** — kiểm soát chính xác thứ tự handler trên cùng element.
5. **SPA routing** — preventDefault trên link, dùng JS router thay vì browser navigate.
6. **Custom keyboard shortcuts** — preventDefault default browser behavior (F5 reload, Ctrl+S save).
7. **Context menu override** — preventDefault right-click, hiện custom menu.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`preventDefault` không hủy event** — handler khác vẫn chạy. Chỉ ngăn hành vi mặc định của browser.
2. **`stopPropagation` không gọi `preventDefault`** — hành vi mặc định vẫn xảy ra. Hai phương thức độc lập.
3. **Không lạm dụng `stopPropagation`** — có thể phá vỡ event delegation của thư viện bên thứ 3.
4. **Trong `<form>`, `e.preventDefault()` trong submit handler là pattern chuẩn** — để xử lý async submit.
5. **`stopImmediatePropagation` chỉ effect trên cùng element** — không ngăn bubbling lên parent.
6. **Native control default behavior** — một số event không thể preventDefault (ví dụ: `beforeunload` cần `returnValue`).
7. **Event delegation + stopPropagation** — nếu child stopPropagation, parent delegation listener sẽ không nhận được event.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Form validation** — ngăn submit nếu dữ liệu sai, hiển thị error message.
2. **Link trong-app navigation** — ngăn reload, dùng SPA router thay thế.
3. **Modal/Dialog** — `Esc` key thoát modal (preventDefault focus steal).
4. **Nested clickable elements** — button trong link chỉ toggle, không navigate.
5. **Custom context menu** — thay thế native right-click menu.
6. **Keyboard shortcut** — override default browser shortcuts (Ctrl+S, F5).
7. **Infinite scroll** — preventDefault trên scroll events nếu cần custom logic.
8. **Touch gesture handling** — preventDefault trên touchmove để chặn scroll mặc định.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Form validation pattern
```js
const form = document.querySelector('#login-form');
const emailInput = form.querySelector('#email');

form.addEventListener("submit", (e) => {
  e.preventDefault(); // ⭐ dừng reload trang
  
  const email = emailInput.value.trim();
  if (!email.includes('@')) {
    emailInput.classList.add("error");
    emailInput.focus();
    return;
  }
  
  emailInput.classList.remove("error");
  // process form via fetch/AJAX
  fetch('/api/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email })
  })
  .then(res => res.json())
  .then(data => console.log('Logged in:', data))
  .catch(err => console.error('Login failed:', err));
});
```

### Ví dụ 2: SPA hash routing
```js
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener("click", (e) => {
    const href = link.getAttribute("href");
    if (href.startsWith("#")) {
      e.preventDefault(); // không cuộn lên đầu trang
      const target = document.querySelector(href);
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
        history.pushState(null, '', href); // update URL without reload
      }
    }
  });
});
```

### Ví dụ 3: Nested element — stopPropagation
```js
const parent = document.querySelector('.parent');
const child = document.querySelector('.child');

parent.addEventListener("click", () => console.log("parent clicked"));
child.addEventListener("click", (e) => {
  e.stopPropagation(); // ⭐ ngăn bubble lên parent
  console.log("child clicked");
});
// click child → chỉ "child clicked"
// click parent area (không phải child) → chỉ "parent clicked"
```

### Ví dụ 4: Button inside link — both methods
```js
const link = document.querySelector('a.external');
const btn = link.querySelector('button.toggle');

link.addEventListener("click", (e) => {
  // Nếu click vào link area (không phải button) → navigate
  if (e.target === link) {
    window.location.href = link.href;
  }
});

btn.addEventListener("click", (e) => {
  e.stopPropagation();   // ⭐ không navigate
  e.preventDefault();    // ⭐ không default link behavior
  btn.classList.toggle('active');
});
```

### Ví dụ 5: Custom context menu
```js
const customMenu = document.querySelector('#context-menu');

document.addEventListener('contextmenu', (e) => {
  e.preventDefault(); // ⭐ chặn native context menu
  customMenu.style.left = e.clientX + 'px';
  customMenu.style.top = e.clientY + 'px';
  customMenu.classList.add('visible');
});

document.addEventListener('click', () => {
  customMenu.classList.remove('visible');
});
```

### Ví dụ 6: Keyboard shortcut
```js
document.addEventListener('keydown', (e) => {
  // Ctrl+S — save
  if (e.ctrlKey && e.key === 's') {
    e.preventDefault(); // ⭐ chặn browser save dialog
    saveDocument();
  }
  // Escape — close modal
  if (e.key === 'Escape') {
    closeModal();
  }
  // F5 — prevent reload (example)
  if (e.key === 'F5') {
    e.preventDefault();
    softRefresh();
  }
});
```

### Ví dụ 7: stopImmediatePropagation
```js
const btn = document.querySelector('#special-btn');

btn.addEventListener('click', () => console.log('Logger: button clicked'));
btn.addEventListener('click', (e) => {
  e.stopImmediatePropagation(); // ⭐ chặn các handler sau
  console.log('Security check: passed');
});
btn.addEventListener('click', () => console.log('Analytics: track click'));
// Chỉ in: "Logger" → "Security check" — Analytics không chạy
```

### Ví dụ 8: preventDefault trên checkbox
```js
const checkbox = document.querySelector('#agree-checkbox');
const submitBtn = document.querySelector('#submit-btn');

checkbox.addEventListener('change', (e) => {
  submitBtn.disabled = !e.target.checked;
});

form.addEventListener('submit', (e) => {
  if (!checkbox.checked) {
    e.preventDefault(); // ⭐ không submit nếu chưa tick
    checkbox.focus();
    alert('Vui lòng đồng ý điều khoản');
  }
});
```

## 🔬 So sánh với alternatives

| Method | Chặn default? | Chặn bubble? | Chặn same-element handlers? |
|---|---|---|---|
| **preventDefault** | ✅ | ❌ | ❌ |
| **stopPropagation** | ❌ | ✅ (upward) | ❌ |
| **stopImmediatePropagation** | ❌ | ❌ | ✅ (same element) |
| **return false** (jQuery) | ✅ | ✅ | ✅ |
| **inline `return false`** | ✅ | ❌ | ❌ |

## 📊 Performance & Best Practices

- **Always call `preventDefault` at the start** của submit handler nếu muốn xử lý async.
- **Use `stopPropagation` sparingly** — có thể phá event delegation patterns.
- **Combine both when needed** — form submit: preventDefault + xử lý async.
- **Don't preventDefault on every event** — some default behaviors are important for accessibility.
- **Test with DevTools** — Event listener breakpoints để debug propagation chain.
- **Passive listeners + preventDefault conflict** — `{ passive: true }` khiến preventDefault bị ignore.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/10_dom-event/` — event basics.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/12_EventListener/` — event types.
- Xem thêm: `18_dom-apis/03_events/` — bubbling/capturing deep dive.
- File tham khảo: `app.js`, `index.html` trong folder `11_PreventDefault-StopPropagation/`.
