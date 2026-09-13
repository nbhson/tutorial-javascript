# Bài 12 — EventListener Thường Dùng

## 🔑 Khái niệm

Các event phổ biến chia làm 4 nhóm:

### Mouse Events
| Event | Kích hoạt |
|---|---|
| `click` | Click trái chuột |
| `dblclick` | Double click |
| `mousedown` / `mouseup` | Nhấn / thả nút chuột |
| `mouseenter` / `mouseleave` | Chuột vào/ra element (không bubble) |
| `mousemove` | Di chuyển chuột (nhiều lần) |
| `contextmenu` | Right-click |

### Keyboard Events
| Event | Kích hoạt |
|---|---|
| `keydown` | Nhấn phím (giữ → repeat) |
| `keyup` | Thả phím |
| `keypress` | ~~Deprecated~~ dùng keydown/keyup thay |

### Form Events
| Event | Kích hoạt |
|---|---|
| `submit` | Submit form |
| `input` | Giá trị thay đổi ngay (real-time) |
| `change` | Giá trị thay đổi + blur (sau khi rời input) |
| `focus` / `blur` | Nhận/bỏ focus |

### Window/Document Events
| Event | Kích hoạt |
|---|---|
| `DOMContentLoaded` | DOM parsing xong (không chờ ảnh) |
| `load` | Tất cả tài nguyên (ảnh, CSS, iframe) load xong |
| `scroll` | Cuộn trang |
| `resize` | Đổi kích thước viewport |
| `visibilitychange` | Tab ẩn/hiện |

## ✅ Điểm mạnh
- `DOMContentLoaded` nhanh hơn `load` — render content sớm
- `input` real-time tốt hơn `change` cho search/filter
- `mouseenter` không bubble → tránh event delegation complication

## ⚠️ Lưu ý
- `keypress` đã deprecated — dùng `keydown`/`keyup`
- `scroll` event fires rất nhiều lần → dùng `{ passive: true }` hoặc debounce
- `resize` cũng fire nhiều — debounce/throttle bắt buộc
- `focus/blur` không bubble; dùng `focusin/focusout` nếu cần bubble

## 💡 Khi nào dùng
- Search live: `input` event
- Tab visibility: `visibilitychange` cho auto-pause video/audio
- Infinite scroll: `scroll` + threshold
- Debounce search input 300ms

## 🎯 Ví dụ minh họa

### Search real-time (debounce)
```js
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

searchInput.addEventListener("input", debounce((e) => {
  fetch(`/api/search?q=${encodeURIComponent(e.target.value)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300));
```

### Tab visibility — pause video
```js
document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    video.pause();
  } else {
    video.play();
  }
});
```

### DOMContentLoaded vs load
```js
// Nhanh — DOM đã sẵn sàng, ảnh chưa load
document.addEventListener("DOMContentLoaded", () => {
  initApp();
});

// Chậm — mọi thứ load xong
window.addEventListener("load", () => {
  lazyLoadImages();
});
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `12_EventListener/`
- Thực hành: debounce search input 200ms
- Câu hỏi: `focus` vs `focusin` khác nhau ở điểm nào?
