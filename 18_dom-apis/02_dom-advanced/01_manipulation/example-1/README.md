# DOM Manipulation — Example 1

## 🔑 Khái niệm

Thao tác thêm/xóa/đổi vị trí node trong DOM cây:

| Method | Mô tả |
|---|---|
| `parent.appendChild(node)` | Đưa node vào cuối children |
| `parent.insertBefore(new, ref)` | Chèn node trước ref node |
| `parent.replaceChild(new, old)` | Thay thế old bằng new |
| `parent.removeChild(node)` | Xóa node khỏi parent |
| `node.cloneNode(deep)` | Clone node (deep=true clone cả children) |
| `node.remove()` | Xóa node (modern, tương đương removeChild) |

## ✅ Điểm mạnh
- Di chuyển node không copy → node biến khỏi vị trí cũ tự động
- `cloneNode(true)` copy nguyên subtree
- `append`/`prepend`/`replaceWith`/`before`/`after` (DOM Level 4) gọn hơn phương thức cũ

## ⚠️ Lưu ý
- Append node đã tồn tại → **di chuyển** chứ không copy
- `removeChild` cần reference đến node con — nếu chỉ có selector phải query lại
- `cloneNode(false)` chỉ clone node itself, không clone children

## 💡 Khi nào dùng
- Todo list: add/remove/edit item động
- Drag & drop reorder
- Dynamic table row addition/removal

## 🎯 Ví dụ minh họa

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
const clone = template.cloneNode(true);
clone.querySelector(".name").textContent = "New Item";
list.appendChild(clone);
```

### reorder bằng drag (giả lập)
```js
// Di chuyển item đầu tiên xuống cuối
const first = list.firstElementChild;
if (first) list.appendChild(first);
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html`, `style.css` trong folder `example-1/`
- Thực hành: thêm nút "Move to top" cho mỗi item
- Câu hỏi: append node đã tồn tại sẽ copy hay di chuyển?
