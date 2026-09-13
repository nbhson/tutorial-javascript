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

## Khi nào dùng

- Game 2D đơn giản (platformer, pong, snake)
- Particle system, firework, rain effects
- Data visualization động (bar chart animate, line chart scroll)
- UI micro-interaction (hover effects, loading spinner)
- Scroll-triggered animations

## Ví dụ: Bouncing Ball

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

## Ví dụ: Delta Time Movement

```js
let x = 0;
const speed = 200; // pixels per second

function move(timestamp, lastTime) {
  const delta = (timestamp - lastTime) / 1000; // seconds
  x += speed * delta; // pixels moved this frame
  if (x > canvas.width) x = 0;
  // draw...
  requestAnimationFrame(move);
}
requestAnimationFrame((ts) => move(ts, ts));
```

## Tham khảo

- File: `app.js`, `index.html`, `style.css`
- MDN rAF: https://developer.mozilla.org/en-US/docs/Web/API/window/requestAnimationFrame
- Game loop pattern: https://gamedev.net/forums/topic/535875-basic-game-loop/
