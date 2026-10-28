# setTimeout / setInterval — hẹn giờ trong JavaScript — [Level: Beginner]

## 🔑 Khái niệm cốt lõi

`setTimeout` và `setInterval` là hai hàm hẹn giờ (timer) thuộc **Web APIs** — kết quả của chúng rơi vào **Macrotask Queue**. Chúng cho phép lập lịch thực thi code sau một khoảng thời gian, mà không chặn luồng chính.

| Hàm | Cách hoạt động | Dừng lại |
|-----|----------------|----------|
| `setTimeout(fn, ms)` | Chạy `fn` **một lần** sau ít nhất `ms` ms | `clearTimeout(id)` |
| `setInterval(fn, ms)` | Chạy `fn` **lặp lại mỗi** `ms` ms | `clearInterval(id)` |

Quan trọng: thời gian chỉ là **tối thiểu** (minimum delay). Callback chỉ chạy khi **Call Stack trống** — nên `setTimeout(fn, 0)` vẫn chạy sau toàn bộ code đồng bộ (và sau mọi microtask).

Vì `setTimeout`/`setInterval` là **macrotask**, chúng luôn chạy **sau** mọi microtask (promise) đang chờ cùng lúc.

## 📐 Cấu trúc / Cú pháp

### Signature đầy đủ

```js
// setTimeout
const timeoutId = setTimeout(callback, delay_ms, arg1, arg2, ...);

// setInterval
const intervalId = setInterval(callback, delay_ms, arg1, arg2, ...);

// Hủy
clearTimeout(timeoutId);
clearInterval(intervalId);
```

### Bảng tham số

| Tham số | Bắt buộc? | Ý nghĩa |
|---------|-----------|---------|
| `callback` | ✅ | Hàm sẽ được gọi khi timer trigger |
| `delay_ms` | ✅ | Thời gian chờ (ms) trước khi chạy callback |
| `arg1, arg2, ...` | ❌ | Đối số truyền vào callback |

### Return value

| Hàm | Trả về | Kiểu |
|-----|--------|------|
| `setTimeout` | Timer ID | `number` (browser) / `Timeout` (Node) |
| `setInterval` | Timer ID | `number` (browser) / `Timeout` (Node) |

## ✅ Điểm mạnh — Tại sao nên dùng

1. **Trì hoãn/định kỳ tác vụ** mà không chặn luồng chính.
2. **Dùng `setTimeout`** chạy trễ sau khi sự kiện hiện tại xử lý xong.
3. **`setInterval`** tiện cho đồng hồ, đếm ngược, polling nhẹ.
4. **Kết hợp với `clearTimeout`/`clearInterval`** kiểm soát vòng lặp chính xác.
5. **Debouncing** — delay thực thi cho đến khi user stop typing.
6. **Throttling** — giới hạn tần suất chạy function.
7. **Animation frames** — thay thế `setInterval` bằng `requestAnimationFrame`.
8. **Retry logic** — retry request sau N giây khi fail.

## ⚠️ Bẫy thường gặp & Hạn chế

### Bẫy 1: `setTimeout(fn, 0)` không chạy ngay

```js
console.log("A");
setTimeout(() => console.log("B"), 0);
console.log("C");
// Output: A → C → B (B chạy sau sync code)
```

### Bẫy 2: `setInterval` chạy mãi nếu không `clearInterval`

```js
const id = setInterval(() => console.log("tick"), 1000);
// Phải gọi clearInterval(id) khi không cần nữa
// Nếu quên: tốn CPU, memory leak, UI lag
```

### Bẫy 3: Callback dồn chồng khi task nặng hơn interval

```js
setInterval(() => {
  // giả sử fetch mất 2 giây
  fetch("/api").then(...);
}, 1000); // mỗi 1s trigger, nhưng fetch mất 2s → requests dồn chồng!
```

### Bẫy 4: `setTimeout(0)` chạy sau tất cả microtask

```js
setTimeout(() => console.log("timeout"), 0);
Promise.resolve().then(() => console.log("promise"));
// promise chạy trước timeout, dù setTimeout khai báo trước
```

### Bẫy 5: Timer accuracy không đảm bảo

```js
// setTimeout(fn, 100) có thể chạy sau 100ms, 150ms, hoặc 500ms
// tùy thuộc vào stack load tại thời điểm đó
```

### Bẫy 6: Arrow function trong timer — `this` kế thừa outer scope

```js
const obj = {
  count: 0,
  start() {
    setTimeout(() => {
      this.count++; // ✅ arrow giữ this = obj
      console.log(this.count);
    }, 1000);
  }
};
```

## 💡 Khi nào dùng — Tình huống thực tế

1. **Debounce tìm kiếm** — `setTimeout` + `clearTimeout` cho autocomplete.
2. **Animation, đếm ngược, đồng hồ** — `setInterval` + `clearInterval`.
3. **Xếp tác vụ chạy sau khi render** — `setTimeout(0)` sau DOM mutation.
4. **Lazy loading** — load resource sau N ms khi element vào viewport.
5. **Auto-dismiss notification** — `setTimeout` ẩn toast sau 3s.
6. **Retrying failed requests** — exponential backoff với setTimeout.
7. **Rate limiting** — throttling API calls.

## 🎯 Ví dụ minh họa — Từ cơ bản đến nâng cao

### Ví dụ 1: Basic setTimeout

```js
console.log(1);
setTimeout(() => console.log("timeout 0"), 0); // macrotask → chạy sau
console.log(3);
// Output: 1 → 3 → timeout 0
```

### Ví dụ 2: Basic setInterval

```js
let n = 0;
const id = setInterval(() => {
  console.log("interval", ++n);
  if (n >= 2) clearInterval(id); // dừng vòng lặp
}, 10);
// interval 1 → interval 2 (rồi dừng)
```

### Ví dụ 3: Debounce pattern

```js
function debounce(fn, delay) {
  let timer;
  return function (...args) {
    clearTimeout(timer); // hủy timer cũ
    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

const search = debounce((query) => {
  console.log("Searching:", query);
}, 300);

search("a"); // chưa search
search("ab"); // chưa search
search("abc"); // sau 300ms → "Searching: abc"
```

### Ví dụ 4: Throttle pattern

```js
function throttle(fn, limit) {
  let inThrottle;
  return function (...args) {
    if (!inThrottle) {
      fn.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}

const scrollHandler = throttle(() => {
  console.log("Scroll at:", Date.now());
}, 200);

window.addEventListener("scroll", scrollHandler);
// Chỉ log mỗi 200ms dù scroll liên tục
```

### Ví dụ 5: Retry với exponential backoff

```js
async function fetchWithRetry(url, retries = 3, delay = 1000) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (res.ok) return res.json();
    } catch (err) {
      if (i === retries - 1) throw err;
    }
    // exponential backoff
    await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
  }
}
```

### Ví dụ 6: Countdown timer

```js
function countdown(seconds, element) {
  let remaining = seconds;
  element.textContent = remaining;
  
  const id = setInterval(() => {
    remaining--;
    element.textContent = remaining;
    if (remaining <= 0) clearInterval(id);
  }, 1000);
  
  return id; // trả id để caller có thể clearInterval
}

const timerEl = document.getElementById("timer");
const timerId = countdown(10, timerEl);
// clearInterval(timerId); // hủy nếu cần
```

### Ví dụ 7: Lazy image loading

```js
const images = document.querySelectorAll("img[data-src]");

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const img = entry.target;
      setTimeout(() => {
        img.src = img.dataset.src; // load sau khi visible
      }, 100); // delay nhẹ để không burst load
      observer.unobserve(img);
    }
  });
});

images.forEach(img => observer.observe(img));
```

## 🔬 So sánh với alternatives

| Cách | Chính xác | Control | Browser support |
|------|-----------|---------|-----------------|
| `setTimeout` | ± vài ms | Manual clear | All |
| `setInterval` | ± vài ms | Manual clear | All |
| `requestAnimationFrame` | Sync with repaint (~60fps) | Auto-cancel on hide | All modern |
| `Atomics.wait` (Worker) | Precise | Thread-level | Limited |

## 📊 Performance & Best Practices

- **Prefer `requestAnimationFrame`** cho animation — sync với browser refresh rate.
- **Always clear timers** — `clearTimeout`/`clearInterval` khi component unmount.
- **Avoid nested setInterval** — dùng setTimeout recursive thay thế.
- **Debounce input handlers** — giảm frequency của expensive operations.
- **Throttle scroll/resize handlers** — giới hạn callback frequency.
- **Không dùng setInterval cho animation** — có thể miss frames, jittery.
- **Monitor timer count** — quá nhiều active timers = memory leak risk.

## 🔗 Liên kết chéo

- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/02_event-loop` — event loop cơ chế
- **Xem thêm:** `12_asynchronous-javascript/01_event-loop/00_js-runtime-deep-dive` — runtime architecture
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/01_promise-theory` — promise vs timer
- **Xem thêm:** `12_asynchronous-javascript/02_callbacks-promises/02_async-await` — async pattern alternative
- **Xem thêm:** `18_dom-apis/README` — DOM APIs interaction với timers
