# Bài 11 — preventDefault & stopPropagation

## 🔑 Khái niệm

| Method | Mục đích |
|---|---|
| `event.preventDefault()` | Ngăn **hành vi mặc định** của browser |
| `event.stopPropagation()` | Ngăn **bubble/capture** lên parent |
| `event.stopImmediatePropagation()` | Ngăn cả các handler khác trên cùng element |

### preventDefault — hành vi mặc định
- `<a href>` → không navigate
- `<form submit>` → không reload trang
- `<input type="checkbox">` → không toggle check
- Context menu `right-click` → không hiện menu

### stopPropagation — không để bubble
```
document
  └─ body
       └─ div.box
            └─ button
```
Nếu click `button` và gọi `stopPropagation()`, handler trên `div.box` và `document` sẽ **không chạy**.

## ✅ Điểm mạnh
- `preventDefault` giữ UX intact (form validation rồi submit JS)
- `stopPropagation` cách ly event scope trong component
- Kết hợp cả 2 khi cần prevent default + chặn parent handler

## ⚠️ Lưu ý
- `preventDefault` không hủy event — handler khác vẫn chạy
- `stopPropagation` không gọi `preventDefault` — hành vi mặc định vẫn xảy ra
- Không lạm dụng `stopPropagation` — có thể phá vỡ event delegation của thư viện bên thứ 3
- Trong `<form>`, `e.preventDefault()` trong submit handler là pattern chuẩn để xử lý async

## 💡 Khi nào dùng
- Form validation: ngăn submit nếu dữ liệu sai
- Link trong-app navigation: ngăn reload, dùng router JS
- Modal: `Esc` key thoát modal (prevent default focus steal)
- Nested clickable elements: button trong link chỉ toggle, không navigate

## 🎯 Ví dụ minh họa

### Form validation
```js
form.addEventListener("submit", (e) => {
  e.preventDefault(); // dừng reload trang
  
  if (!emailValid(emailInput.value)) {
    emailInput.classList.add("error");
    return;
  }
  
  // submit qua fetch
  fetch("/api/login", { method: "POST", body: formData })
    .then(res => res.json())
    .then(data => console.log(data));
});
```

### Link trong-app (SPA router)
```js
links.forEach(link => {
  link.addEventListener("click", (e) => {
    const href = link.getAttribute("href");
    if (href.startsWith("#")) {
      e.preventDefault(); // không cuộn lên đầu trang
      navigateTo(href); // SPA router
    }
  });
});
```

### Stop propagation — nested click
```js
parent.addEventListener("click", () => console.log("parent"));
child.addEventListener("click", (e) => {
  e.stopPropagation(); // parent không log
  console.log("child");
});
// click child → chỉ log "child"
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `11_PreventDefault-StopPropagation/`
- Thực hành: form login submit bằng fetch thay vì reload
- Câu hỏi: `stopPropagation` vs `stopImmediatePropagation` khác nhau ở đâu?
