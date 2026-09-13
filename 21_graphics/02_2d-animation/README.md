# 2D Animation

## 🔑 Khái niệm

**2D animation** trong browser dùng `requestAnimationFrame` (rAF) — callback được gọi trước mỗi frame repaint (~60fps). Khác với `setInterval` vì rAF sync với browser refresh rate, pause khi tab inactive, tiết kiệm pin.

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

## ✅ Điểm mạnh
- Sync với monitor refresh → mượt, không giật
- Tự pause khi tab ẩn → tiết kiệm CPU/pin
- Delta time đảm bảo tốc độ animation đồng nhất mọi frame rate

## ⚠️ Lưu ý
- Không dùng `setInterval` cho animation — không sync với refresh rate
- `requestAnimationFrame` callback nhận `DOMHighResTimeStamp` (ms)
- Animation loop phải `cancelAnimationFrame(id)` khi không cần (cleanup)
- rAF callback chạy trên main thread — heavy computation blocks UI

## 💡 Khi nào dùng
- Game 2D đơn giản
- Particle system, firework
- Data visualization động (bar chart animate)
- UI micro-interaction

## 🎯 Ví dụ minh họa

### Ball bounce animation
```js
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
let x = 50, y = 50, vx = 3, vy = 3;
const gravity = 0.3;
const bounce = 0.8;

function loop() {
  vy += gravity;
  x += vx;
  y += vy;
  
  if (y > canvas.height - 20) { y = canvas.height - 20; vy *= -bounce; }
  if (x > canvas.width - 20 || x < 20) { vx *= -1; }
  
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(x, y, 20, 0, Math.PI * 2);
  ctx.fillStyle = "coral";
  ctx.fill();
  
  requestAnimationFrame(loop);
}
loop();
```

### Delta time smooth movement
```js
let pos = 0;
const speed = 100; // px per second

function move(timestamp, lastTime) {
  const delta = (timestamp - lastTime) / 1000;
  pos += speed * delta;
  if (pos > canvas.width) pos = 0;
  // draw...
  requestAnimationFrame(move);
}
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html`, `style.css` trong folder `02_2d-animation/`
- Thực hành: tạo animation bouncing ball có gravity
- Câu hỏi: tại sao dùng delta time thay vì fixed step?
