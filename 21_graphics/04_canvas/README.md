# Canvas 2D

## 🔑 Khái niệm

`<canvas>` là vùng raster (pixel-based) vẽ bằng **Canvas 2D Context API**. Khác SVG — canvas là 1 bitmap, không phải DOM tree.

```js
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

ctx.fillStyle = "coral";
ctx.fillRect(50, 50, 100, 100); // x, y, width, height

ctx.beginPath();
ctx.arc(150, 100, 50, 0, Math.PI * 2);
ctx.stroke();
```

## ✅ Điểm mạnh
- Hiệu suất cao — vẽ hàng ngàn object 60fps
- Pixel-level control → image filter, drawing app
- Batch operations: `ctx.save()` / `ctx.restore()` state management
- Export thành ảnh: `canvas.toDataURL()` / `canvas.toBlob()`

## ⚠️ Lưu ý
- Canvas **không phải DOM** — không attach event listener trực tiếp lên shape
- Mỗi frame phải **clear** rồi **redraw** tất cả (không có incremental render)
- Không tự động scale responsive — cần tính toán lại width/height mỗi resize
- `devicePixelRatio` cần xử lý cho retina screen

## 💡 Khi nào dùng
- Game 2D
- Drawing/painting app
- Image processing filter
- Real-time data visualization (heatmap, waveform)

## 🎯 Ví dụ minh họa

### Basic shapes
```js
const ctx = canvas.getContext("2d");

// Rectangle
ctx.fillStyle = "teal";
ctx.fillRect(10, 10, 80, 60);

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
```

### Animation loop trên canvas
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

### Retina support
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

## 📚 Tham khảo & Bài tập
- File: `index.html` trong folder `04_canvas/`
- Thực hành: vẽ hệ mặt trời (orbits) bằng canvas
- Câu hỏi: canvas vs SVG khác nhau ở điểm nào quan trọng nhất?
