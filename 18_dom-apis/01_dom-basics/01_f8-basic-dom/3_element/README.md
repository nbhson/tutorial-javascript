# Bài 3 — DOM Element: Truy Vấn Phần Tử

## 🔑 Khái niệm

**Element** là loại node đại diện cho một thẻ HTML (`<div>`, `<span>`, `<input>`…). Có 4 cách chính để truy vấn:

| Method | Trả về | Selector | Performance |
|---|---|---|---|
| `getElementById(id)` | Element hoặc null | id duy nhất | ⭐⭐⭐ nhanh nhất |
| `getElementsByClassName(name)` | HTMLCollection | class | ⭐⭐ |
| `getElementsByTagName(tag)` | HTMLCollection | tag name | ⭐⭐ |
| `querySelector(sel)` | Element hoặc null | CSS selector | ⭐ |
| `querySelectorAll(sel)` | NodeList (static) | CSS selector | ⭐ |

> **HTMLCollection** (live) — tự cập nhật khi DOM thay đổi.  
> **NodeList** (static) — snapshot tại thời điểm gọi, không đổi khi DOM thay đổi.

## ✅ Điểm mạnh
- `querySelector` hỗ trợ mọi CSS selector phức tạp (`div > p.class:nth-child(2)`)
- `querySelectorAll` + spread `[...elements]` biến NodeList thành mảng array methods
- `getElementsBy*` live collection — không cần gọi lại khi DOM đổi

## ⚠️ Lưu ý
- `getElementsByClassName` nhận **space-separated** nhiều class: `.el.getElementsByClassName("btn primary")`
- `getElementsByTagName` không phân biệt hoa/thường `DIV` = `div`
- `querySelector` chỉ trả **phần tử đầu tiên**, cần `querySelectorAll` để lấy tất cả
- DOM lookup mỗi lần gọi — nên gán biến và reuse thay vì gọi lặp trong loop

## 💡 Khi nào dùng
- Lấy phần tử duy nhất: `id` → `getElementById`; selector phức tạp → `querySelector`
- Lấy nhiều phần tử: class/tag → `querySelectorAll` hoặc `getElementsBy*`
- Duyệt danh sách: `for...of` NodeList an toàn hơn `for` mảng

## 🎯 Ví dụ minh họa

### 4 cách so sánh
```js
// 1. getElementById
const box = document.getElementById("app");

// 2. getElementsByClassName → HTMLCollection (live)
const btns = document.getElementsByClassName("btn");

// 3. getElementsByTagName → HTMLCollection
const lis = document.getElementsByTagName("li");

// 4. querySelector / querySelectorAll → NodeList (static)
const firstP = document.querySelector("p.highlight");
const allLinks = document.querySelectorAll("a[href^='https://']");
```

### Lặp qua NodeList
```js
const items = document.querySelectorAll(".item");
items.forEach((el, i) => {
  console.log(i, el.textContent.trim());
});

// Hoặc dùng for...of
for (const el of items) {
  el.style.color = "blue";
}
```

### Spread NodeList thành mảng
```js
const arr = [...document.querySelectorAll("div.box")];
arr.reverse(); // giờ có array methods
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `3_element/`
- Thử: đổi class của một element rồi kiểm tra `getElementsByClassName` có tự cập nhật không
- Câu hỏi: sự khác biệt giữa `HTMLCollection` và `NodeList`?
