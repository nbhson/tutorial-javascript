# Canvas 2D

## Khái niệm

`<canvas>` là vùng raster (pixel-based) vẽ bằng **Canvas 2D Context API**. Khác SVG -- canvas là 1 bitmap, không phải DOM tree. Mỗi pixel được vẽ trực tiếp vào buffer bộ nhớ.

```js
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");
ctx.fillStyle = "coral";
ctx.fillRect(50, 50, 100, 100);
ctx.beginPath();
ctx.arc(150, 100, 50, 0, Math.PI * 2);
ctx.stroke();
```

### Canvas vs SVG -- Sự khác biệt cốt lõi

| | Canvas 2D | SVG |
|---|---|---|
| Type | Raster (bitmap) | Vector (XML DOM) |
| Resolution | Fixed (pixel) | Scalable (infinite) |
| Event handling | Manual hit detection | Direct on elements |
| DOM access | No (need manual tracking) | Yes (querySelector) |
| Performance | Better for many objects | Better for few objects |
| Animation | Native (clear + redraw) | CSS/JS on elements |
| Use case | Games, image processing | Icons, charts, illustrations |

## Điểm mạnh

- Hiệu suất cao -- vẽ hàng ngàn object 60fps
- Pixel-level control --> image filter, drawing app, photo editor
- Batch operations: `ctx.save()` / `ctx.restore()` state management
- Export thành ảnh: `canvas.toDataURL()` / `canvas.toBlob()`
- OffscreenCanvas cho web worker (không block main thread)
- WebGL extension cho 3D graphics

## Lưu ý

- Canvas **không phải DOM** -- không attach event listener trực tiếp lên shape đã vẽ
- Mỗi frame phải **clear** rồi **redraw** tất cả (không có incremental render)
- Không tự động scale responsive -- cần tính toán lại width/height mỗi resize
- `devicePixelRatio` cần xử lý cho retina screen (1x, 2x, 3x)
- Path không tự động stroke/fill -- phải gọi `ctx.stroke()` / `ctx.fill()` sau `beginPath()`
- Canvas context state là global -- dùng save/restore khi cần

## Khi nào dùng

- Game 2D (platformer, breakout, snake)
- Drawing/painting app (brush, eraser, layers)
- Image processing filter (blur, grayscale, sepia)
- Real-time data visualization (heatmap, waveform, oscilloscope)
- Particle systems, visual effects

## Ví dụ: Basic Shapes

```js
const ctx = canvas.getContext("2d");

// Rectangle
ctx.fillStyle = "teal";
ctx.fillRect(10, 10, 80, 60);
ctx.strokeStyle = "#333";
ctx.lineWidth = 2;
ctx.strokeRect(10, 10, 80, 60);

// Circle
ctx.beginPath();
ctx.arc(120, 40, 30, 0, Math.PI * 2);
ctx.fillStyle = "crimson";
ctx.fill();

// Line
ctx.beginPath();
ctx.moveTo(10, 100);
ctx.lineTo(200, 150);
ctx.strokeStyle = "purple";
ctx.lineWidth = 3;
ctx.stroke();

// Triangle
ctx.beginPath();
ctx.moveTo(100, 200);
ctx.lineTo(150, 280);
ctx.lineTo(50, 280);
ctx.closePath();
ctx.fillStyle = "orange";
ctx.fill();
```

### Animation loop
```js
let x = 0;
function draw() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.beginPath();
  ctx.arc(x, 50, 20, 0, Math.PI * 2);
  ctx.fillStyle = "coral";
  ctx.fill();
  x += 2;
  if (x > canvas.width + 20) x = -20;
  requestAnimationFrame(draw);
}
draw();
```

### Retina/HiDPI support
```js
function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;
  canvas.height = rect.height * dpr;
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);
  return ctx;
}
```

## Tham khảo

- File: `index.html`
- MDN Canvas: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- Canvas 2D API Reference: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D
