# 2D Animation

## Khái niệm

**2D animation** trong browser dùng `requestAnimationFrame` (rAF) -- callback được gọi trước mỗi frame repaint (~60fps). Khác với `setInterval` vì rAF sync với browser refresh rate, pause khi tab inactive, tiết kiệm pin.

```js
let lastTime = 0;
function animate(timestamp) {
  const delta = (timestamp - lastTime) / 1000; // seconds
  lastTime = timestamp;
  // update position based on delta
  requestAnimationFrame(animate);
}
requestAnimationFrame(animate);
```

### Delta time là gì?

Delta time = thời gian giữa 2 frames (giây). Dùng để tính position độc lập với fps:

- 60fps: delta ≈ 0.016s
- 30fps: delta ≈ 0.033s
- Cùng tốc độ vật lý, khác fps --> delta time đảm bảo animation mượt như nhau

Không dùng delta time thì animation của bạn sẽ **chạy nhanh gấp đôi trên màn hình 120Hz** so với màn hình 60Hz — đây là bug rất phổ biến khi người mới viết game loop.

### Tại sao không dùng setInterval?

| | `setInterval(fn, 16)` | `requestAnimationFrame` |
|---|---|---|
| Sync với refresh rate | Không (timer của OS) | Có |
| Tab ẩn | Vẫn chạy (throttle ~1s/lần nhưng vẫn tốn) | Tự dừng/tiêu giảm |
| Frame drop | Chạy dồn các callback bị trễ | Bỏ qua frame lỡ, không dồn |
| Timestamp chính xác | `Date.now()` trong callback | `DOMHighResTimeStamp` vi-độ chính xác |
| Battery | Tốn pin | Tối ưu bởi browser |

Ngoài ra `setInterval(fn, 16)` không đảm bảo 16ms — timer có tối thiểu ~4ms và có thể trễ vì main thread bận. rAF được browser lên lịch ngay trước lần vẽ tiếp theo nên không bao giờ "vẽ thừa" frame mà không ai thấy.

## Điểm mạnh

- Sync với monitor refresh --> mượt, không giật, không waste frames
- Tự pause khi tab inactive --> tiết kiệm CPU/pin đáng kể
- Delta time đảm bảo tốc độ animation đồng nhất mọi frame rate
- Callback nhận timestamp chính xác (DOMHighResTimeStamp)
- Có thể cancel bằng `cancelAnimationFrame(id)`

## Lưu ý

- Không dùng `setInterval` cho animation -- không sync với refresh rate, có thể miss frames
- rAF callback nhận `DOMHighResTimeStamp` (ms since navigationStart) -- KHÔNG phải Date.now()
- Animation loop phải `cancelAnimationFrame(id)` khi component unmount (cleanup)
- rAF chạy trên main thread -- heavy computation blocks UI rendering
- Một số browser throttle rAF xuống 1fps khi tab ẩn (tiết kiệm pin)

### Cleanup — bẫy rò rỉ callback

```js
let rafId;

function loop() {
  // ...vẽ...
  rafId = requestAnimationFrame(loop);
}

function start() {
  cancelAnimationFrame(rafId); // hủy loop cũ trước khi tạo mới (no-op nếu chưa chạy)
  rafId = requestAnimationFrame(loop);
}

function stop() {
  cancelAnimationFrame(rafId);
}

// Ví dụ thực chiến: dừng animation khi user rời khỏi section
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => (entry.isIntersecting ? start() : stop()));
});
observer.observe(document.querySelector("canvas"));
```

Nếu bạn quên cancel, mỗi lần component "tạo mới" sẽ chồng thêm một loop — animation chạy nhanh dần đều và CPU tăng vọt. Trong React, đây chính là lý do `useEffect` cần return cleanup function.

## Khi nào dùng

- Game 2D đơn giản (platformer, pong, snake)
- Particle system, firework, rain effects
- Data visualization động (bar chart animate, line chart scroll)
- UI micro-interaction (hover effects, loading spinner)
- Scroll-triggered animations

### rAF vs CSS animation vs Web Animations API

Trước khi viết animation loop, kiểm tra xem CSS có đủ dùng không — CSS animation chạy trên compositor thread, rẻ hơn rAF chạy trên main thread:

| Nhu cầu | Giải pháp tốt nhất |
|---|---|
| Di chuyển/fade một element theo thời gian cố định | CSS transition/animation |
| Animation lặp vô hạn đơn giản (spinner, pulse) | CSS `@keyframes` |
| Animation cần tương tác vật lý (nảy, va chạm, kéo) | rAF + Canvas/SVG |
| Kiểm soát play/pause/reverse từ JS | Web Animations API (`element.animate()`) |
| Vẽ hàng nghìn object mỗi frame | rAF + Canvas 2D |

```js
// Web Animations API — khi muốn điều khiển animation bằng JS mà vẫn để engine tối ưu
element.animate(
  [{ transform: "translateX(0)" }, { transform: "translateX(200px)" }],
  { duration: 1000, easing: "ease-in-out", fill: "forwards" }
);
```

## Ví dụ 1: Bouncing Ball

```js
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
let x = 50, y = 50, vx = 3, vy = 3;
const gravity = 0.5;
const bounce = 0.8;
const radius = 20;

function loop() {
  vy += gravity;
  x += vx;
  y += vy;

  // Floor collision
  if (y > canvas.height - radius) {
    y = canvas.height - radius;
    vy *= -bounce;
  }
  // Wall collision
  if (x > canvas.width - radius || x < radius) {
    vx *= -1;
  }

  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(x, y, radius, 0, Math.PI * 2);
  ctx.fillStyle = "coral";
  ctx.fill();
  ctx.strokeStyle = "#333";
  ctx.stroke();

  requestAnimationFrame(loop);
}
loop();
```

Đây là "hello world" của game loop: **update** trạng thái → **draw** → **hẹn frame kế tiếp**. Ba bước này xuất hiện nguyên xi trong mọi game engine.

## Ví dụ 2: Delta Time Movement

```js
let x = 0;
const speed = 200; // pixels per second

let lastTime = performance.now();
function move(timestamp) {
  const delta = (timestamp - lastTime) / 1000; // seconds
  lastTime = timestamp;
  x += speed * delta; // pixels moved this frame — độc lập với fps!
  if (x > canvas.width) x = 0;
  // ...draw...
  requestAnimationFrame(move);
}
requestAnimationFrame(move);
```

Giải thích đơn vị: `speed` khai báo bằng **pixels/giây** (đại lượng vật lý), còn từng frame chỉ di chuyển `speed × delta`. Frame nhanh (delta nhỏ) → đi ít; frame chậm (delta lớn) → đi nhiều. Tổng quãng đường mỗi giây luôn đúng 200px.

## Ví dụ 3: Easing — chuyển động tự nhiên

Chuyển động tuyến tính trông "robot". Thực tế vật tăng tốc rồi giảm tốc — gọi là **easing**:

```js
// t: 0 → 1 (tiến độ animation)
const easings = {
  linear: (t) => t,
  easeInQuad: (t) => t * t,
  easeOutQuad: (t) => t * (2 - t),
  easeInOutCubic: (t) => (t < 0.5 ? 4 * t ** 3 : 1 - (-2 * t + 2) ** 3 / 2),
};

function animateValue(from, to, duration, ease, onFrame) {
  const start = performance.now();
  function frame(now) {
    const t = Math.min((now - start) / duration, 1); // clamp về 1
    onFrame(from + (to - from) * ease(t));
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

// Trượt panel từ -300px về 0 trong 600ms
animateValue(-300, 0, 600, easings.easeOutCubic, (v) => {
  panel.style.transform = `translateX(${v}px)`;
});
```

Trong thực tế bạn có thể dùng `element.animate()` (Web Animations API) hoặc CSS `transition-timing-function` thay vì tự viết — nhưng hiểu easing tay giúp bạn tùy biến hiệu ứng mà thư viện không hỗ trợ.

## Ví dụ 4: Animation loop hoàn chỉnh — pause/resume + cleanup

```js
class AnimationLoop {
  constructor(renderFn) {
    this.renderFn = renderFn;
    this.lastTime = 0;
    this.rafId = null;
    this.running = false;
  }

  start() {
    if (this.running) return; // tránh chạy 2 loop song song
    this.running = true;
    this.lastTime = performance.now();
    const frame = (now) => {
      const delta = Math.min((now - this.lastTime) / 1000, 0.1); // clamp: tránh "teleport" sau khi tab ẩn lâu
      this.lastTime = now;
      this.renderFn(delta);
      if (this.running) this.rafId = requestAnimationFrame(frame);
    };
    this.rafId = requestAnimationFrame(frame);
  }

  stop() {
    this.running = false;
    cancelAnimationFrame(this.rafId);
  }
}

// Sử dụng
const loop = new AnimationLoop((delta) => {
  // update + draw với delta
});
loop.start();
window.addEventListener("beforeunload", () => loop.stop()); // cleanup
```

Ba chi tiết "pro" trong ví dụ trên đáng ghi nhớ:

1. **Clamp delta** (giới hạn tối đa ~0.1s): khi tab ẩn 30 giây rồi quay lại, nếu không clamp thì mọi vật thể sẽ bay vọt đi 30 giây.
2. **Cờ `running`**: `cancelAnimationFrame` đơn lẻ không chống được việc callback đã vào hàng đợi.
3. **Cleanup** gắn với vòng đời (unmount, beforeunload, IntersectionObserver...).

## Bẫy tổng hợp

| # | Bẫy | Hệ quả | Cách tránh |
|---|---|---|---|
| 1 | Không dùng delta time | Tốc độ khác nhau giữa 60/120Hz | Nhân mọi thay đổi vị trí với delta |
| 2 | Không clamp delta | Vật "teleport" sau khi tab ẩn | `Math.min(delta, 0.1)` |
| 3 | Gọi rAF nhiều lần trong cùng loop | Animation nhanh dần đều | Đảm bảo mỗi frame chỉ schedule đúng 1 callback |
| 4 | Quên `cancelAnimationFrame` | Leak, CPU nóng khi unmount | Cleanup trong effect/unmount |
| 5 | Xóa canvas bằng `fillRect` màu trắng mờ đuổi | Hiệu ứng "trail" không chủ đích | Dùng `clearRect` hoặc chủ động muốn trail |

## Checklist tự kiểm tra

- [ ] Giải thích được vì sao rAF tốt hơn setInterval cho animation
- [ ] Viết được loop có delta time, chạy đúng tốc độ trên màn hình 60Hz lẫn 120Hz
- [ ] Biết clamp delta để tránh nhảy vọt sau khi tab ẩn
- [ ] Cancel được loop đúng lúc (unmount, tab rời view)
- [ ] Biết khi nào nên dùng CSS animation thay vì rAF

## Tham khảo

- File: `app.js`, `index.html`, `style.css`
- MDN rAF: https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
- MDN — Web Animations API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API
- Bài liên quan: `12_asynchronous-javascript/` (event loop), `js-info/vi/34_animation/` (chương animation của javascript.info)
