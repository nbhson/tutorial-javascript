# Bài 12 — EventListener Thường Dùng — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

Các event DOM chia làm 4 nhóm chính. Hiểu rõ từng nhóm giúp bạn chọn đúng event cho đúng tình huống — đặc biệt phân biệt `input` vs `change`, `mouseenter` vs `mouseover`, `DOMContentLoaded` vs `load`.

### Mouse Events

| Event | Kích hoạt | Bubbling? |
|---|---|---|
| `click` | Click trái chuột | ✅ Có |
| `dblclick` | Double click | ✅ Có |
| `mousedown` / `mouseup` | Nhấn / thả nút chuột | ✅ Có |
| `mousemove` | Di chuyển chuột (nhiều lần) | ✅ Có |
| `mouseenter` / `mouseleave` | Chuột vào/ra element | ❌ **Không** bubble |
| `mouseover` / `mouseout` | Chuột vào/ra element | ✅ Có (bubble đến con) |
| `contextmenu` | Right-click | ✅ Có |

### Keyboard Events

| Event | Kích hoạt | Bubbling? |
|---|---|---|
| `keydown` | Nhấn phím (giữ → repeat) | ✅ Có |
| `keyup` | Thả phím | ✅ Có |
| `keypress` | ~~Deprecated~~ dùng keydown/keyup thay | ✅ Có |

### Form Events

| Event | Kích hoạt | Bubbling? |
|---|---|---|
| `submit` | Submit form | ✅ Có |
| `input` | Giá trị thay đổi ngay (real-time) | ✅ Có |
| `change` | Giá trị thay đổi + blur (sau khi rời input) | ✅ Có |
| `focus` / `blur` | Nhận/bỏ focus | ❌ **Không** bubble |
| `focusin` / `focusout` | Nhận/bỏ focus | ✅ Có (bubble) |

### Window/Document Events

| Event | Kích hoạt | Thời điểm |
|---|---|---|
| `DOMContentLoaded` | DOM parse xong (ảnh chưa load) | Sớm nhất |
| `load` | Tất cả tài nguyên (ảnh, CSS, iframe) load xong | Muộn nhất |
| `scroll` | Cuộn trang | Liên tục |
| `resize` | Đổi kích thước viewport | Liên tục |
| `visibilitychange` | Tab ẩn/hiện | Khi switch tab |
| `beforeunload` | Chuẩn bị rời trang | Trước khi unload |
| `hashchange` | Phần `#...` của URL đổi | SPA routing |

## 📐 Cấu trúc / Cú pháp

### Search real-time với debounce
```js
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

searchInput.addEventListener("input", debounce((e) => {
  const query = e.target.value;
  if (query.length < 2) return;
  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300));
```

### Tab visibility — pause video/audio
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
  initApp(); // DOM manipulation an toàn
});

// Chậm — mọi thứ load xong
window.addEventListener("load", () => {
  lazyLoadImages(); // đo kích thước ảnh an toàn
});
```

### Input vs Change — khác biệt quan trọng
```js
input.addEventListener('input', (e) => {
  // Fire mỗi lần keystroke — real-time
  console.log('input:', e.target.value);
});

input.addEventListener('change', (e) => {
  // Fire khi input blur HOẶC enter — sau khi thay đổi xong
  console.log('change:', e.target.value);
});
```

### Focusin/Focusout vs Focus/Blur (bubbling version)
```js
// focus/blur KHÔNG bubble
container.addEventListener('focus', () => console.log('container focus'), true);
input.addEventListener('focus', () => console.log('input focus'));
// Click input → chỉ in "input focus" (container listener không chạy vì không bubble)

// focusin/focusout CÓ bubble
container.addEventListener('focusin', () => console.log('container focusin'));
input.addEventListener('focusin', () => console.log('input focusin'));
// Click input → in "input focusin" rồi "container focusin" (bubble up)
```

## ✅ Điểm mạnh

1. **`DOMContentLoaded` nhanh hơn `load`** — render content sớm, không chờ ảnh.
2. **`input` real-time tốt hơn `change`** cho search/filter — respond ngay khi keystroke.
3. **`mouseenter` không bubble** — tránh event delegation complication cho hover effects.
4. **`focusin/focusout` bubble** — khi cần listen focus change trên parent container.
5. **`visibilitychange`** — auto-pause video/audio khi tab ẩn, tiết kiệm battery.
6. **`hashchange`** — nền tảng SPA router kiểu hash-based.
7. **`beforeunload`** — xác nhận thoát trang có dữ liệu chưa lưu.

## ⚠️ Bẫy thường gặp & Hạn chế

1. **`keypress` đã deprecated** — dùng `keydown`/`keyup` thay thế. `keypress` không consistent giữa browsers.
2. **`scroll` event fires rất nhiều lần** → dùng `{ passive: true }` hoặc debounce/throttle.
3. **`resize` cũng fire nhiều** → debounce/throttle bắt buộc để tránh performance issue.
4. **`focus/blur` không bubble** — dùng `focusin`/`focusout` nếu cần bubble lên parent.
5. **`input` vs `change`** — `input` fire mọi khi value đổi (keystroke, paste, dropdown); `change` chỉ fire khi blur hoặc enter.
6. **`load` event trên window** — chỉ fire một lần, sau khi tất cả tài nguyên xong. Không dùng cho DOM init.
7. **`DOMContentLoaded` không đảm bảo CSS loaded** — nếu cần đo computed style, đợi `load` hoặc `DOMContentLoaded` + CSS ready check.

## 💡 Khi nào dùng — Tình huống thực tến

1. **Search live** — `input` event + debounce 200-300ms.
2. **Tab visibility** — `visibilitychange` cho auto-pause video/audio.
3. **Infinite scroll** — `scroll` event + threshold check.
4. **Resize responsive** — `resize` event + debounce.
5. **Form real-time validation** — `input` event trên mỗi field.
6. **Track page unload** — `beforeunload` để warn unsaved changes.
7. **Hash-based SPA routing** — `hashchange` event lắng nghe URL fragment.
8. **Initialize after DOM ready** — `DOMContentLoaded` cho DOM manipulation.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Debounce search input
```js
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

const searchInput = document.querySelector('#search');
searchInput.addEventListener("input", debounce((e) => {
  const query = e.target.value.trim();
  if (query.length < 2) {
    clearResults();
    return;
  }
  fetch(`/api/search?q=${encodeURIComponent(query)}`)
    .then(r => r.json())
    .then(renderResults);
}, 300));
```

### Ví dụ 2: Tab visibility — pause video
```js
const video = document.querySelector('video');

document.addEventListener("visibilitychange", () => {
  if (document.hidden) {
    video.pause();
    console.log('Video paused (tab hidden)');
  } else {
    video.play();
    console.log('Video resumed (tab visible)');
  }
});
```

### Ví dụ 3: DOMContentLoaded vs load
```js
// DOM ready — safe to manipulate DOM
document.addEventListener("DOMContentLoaded", () => {
  const btn = document.querySelector('#action-btn');
  btn.addEventListener('click', handleAction);
  console.log('DOM ready — can access all elements');
});

// All resources loaded — safe to measure images
window.addEventListener("load", () => {
  document.querySelectorAll('img').forEach(img => {
    console.log(`${img.src}: ${img.naturalWidth}x${img.naturalHeight}`);
  });
  initLazyLoading();
  console.log('All resources loaded');
});
```

### Ví dụ 4: Input vs Change comparison
```js
const input = document.querySelector('#search-input');

input.addEventListener('input', (e) => {
  console.log('[input]', e.target.value); // mỗi keystroke
});

input.addEventListener('change', (e) => {
  console.log('[change]', e.target.value); // chỉ khi blur hoặc enter
});
// Type "hello":
// [input] h
// [input] he
// [input] hel
// [input] hell
// [input] hello
// (blur or enter)
// [change] hello
```

### Ví dụ 5: Infinite scroll
```js
let isLoading = false;

window.addEventListener('scroll', () => {
  if (isLoading) return;
  
  const scrollHeight = document.documentElement.scrollHeight;
  const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
  const clientHeight = window.innerHeight;
  
  if (scrollTop + clientHeight >= scrollHeight - 100) {
    isLoading = true;
    loadMoreItems().then(() => { isLoading = false; });
  }
}, { passive: true });
```

### Ví dụ 6: Beforeunload — warn unsaved changes
```js
let hasUnsavedChanges = false;

document.querySelector('#editor').addEventListener('input', () => {
  hasUnsavedChanges = true;
});

window.addEventListener('beforeunload', (e) => {
  if (hasUnsavedChanges) {
    e.preventDefault();
    e.returnValue = ''; // required for modern browsers
  }
});
```

### Ví dụ 7: Hash-based routing
```js
function route() {
  const hash = window.location.hash || '#home';
  const page = hash.slice(1) || 'home';
  console.log(`Navigating to: ${page}`);
  // render page based on hash
}

window.addEventListener('hashchange', route);
window.addEventListener('DOMContentLoaded', route); // initial load
```

### Ví dụ 8: Resize debounce
```js
function debounce(fn, ms) {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
}

window.addEventListener('resize', debounce(() => {
  const width = window.innerWidth;
  console.log('Viewport width:', width);
  // re-layout based on width
}, 150));
```

## 🔬 So sánh với alternatives

| Event | Fire khi | Best for |
|---|---|---|
| **`input`** | Mỗi giá trị đổi (keystroke, paste, dropdown) | Real-time search, live validation |
| **`change`** | Giá trị đổi + blur/enter | Final value confirmation |
| **`keydown`** | Nhấn phím (repeat nếu giữ) | Keyboard shortcuts, game controls |
| **`keyup`** | Thả phím | Detect single key press completion |
| **`click`** | Click trái chuột | Button action, link navigation |
| **`dblclick`** | Double click | Specific double-click actions |
| **`scroll`** | Cuộn (nhiều lần) | Infinite scroll, parallax |
| **`resize`** | Cửa sổ đổi kích thước | Responsive layout updates |
| **`DOMContentLoaded`** | DOM parse xong | DOM initialization |
| **`load`** | Tất cả resources xong | Image measurement, lazy load init |
| **`visibilitychange`** | Tab ẩn/hiện | Video/audio pause-resume |
| **`hashchange`** | URL hash đổi | SPA hash routing |

## 📊 Performance & Best Practices

- **Debounce scroll/resize** — 100-300ms delay để giảm frequency.
- **Throttle input** — nếu search API call, debounce 200-300ms.
- **Passive scroll listener** — `{ passive: true }` giúp browser optimize.
- **Use `DOMContentLoaded` cho init** — không đợi `load` nếu không cần ảnh.
- **`input` > `change` cho real-time** — respond ngay khi user type.
- **`focusin` > `focus` cho delegation** — bubble lên parent container.
- **`mouseenter` > `mouseover` cho hover** — không bubble, ít false triggers.
- **Remove listener khi unmount** — component cleanup để tránh leak.

## 🔗 Liên kết chéo

- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/10_dom-event/` — event basics.
- Xem thêm: `18_dom-apis/01_dom-basics/01_f8-basic-dom/11_PreventDefault-StopPropagation/` — event control.
- Xem thêm: `18_dom-apis/03_events/` — bubbling/capturing deep dive.
- Xem thêm: `18_dom-apis/01_dom-basics/02_how-browser-reads-html/` — DOMContentLoaded timing.
- File tham khảo: `app.js`, `index.html` trong folder `12_EventListener/`.
