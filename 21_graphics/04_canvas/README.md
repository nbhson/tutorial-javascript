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

Tư duy then chốt: khi bạn vẽ một hình tròn lên canvas, **không có "object hình tròn" nào tồn tại** — chỉ có màu các pixel thay đổi. Muốn di chuyển hình, bạn phải xóa vùng vẽ và vẽ lại toàn bộ. Đây là lý do mọi canvas app đều có animation loop (xem bài 02_2d-animation).

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

### Retina/HiDPI — bẫy số 1 của người mới

Trên màn hình Retina (dpr = 2), một canvas 300×300 CSS sẽ bị render ở 300×300 device pixels rồi phóng to 2 lần → **nhòe**. Cách chuẩn:

```js
function setupCanvas(canvas) {
  const dpr = window.devicePixelRatio || 1;
  const rect = canvas.getBoundingClientRect();
  canvas.width = rect.width * dpr;   // buffer thật lớn hơn
  canvas.height = rect.height * dpr;
  const ctx = canvas.getContext("2d");
  ctx.scale(dpr, dpr);               // hệ tọa độ code vẫn dùng CSS pixel
  return ctx;
}
// Từ đây bạn vẽ theo tọa độ CSS pixel, browser tự scale sắc nét.
```

## Khi nào dùng

- Game 2D (platformer, breakout, snake)
- Drawing/painting app (brush, eraser, layers)
- Image processing filter (blur, grayscale, sepia)
- Real-time data visualization (heatmap, waveform, oscilloscope)
- Particle systems, visual effects

## Ví dụ 1: Basic Shapes

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

Quy trình path cần thuộc như bảng cửu chương: `beginPath()` → `moveTo()` → các lệnh vẽ (`lineTo`, `arc`, `quadraticCurveTo`...) → `closePath()` (nếu muốn kín) → `fill()` và/hoặc `stroke()`. Quên gọi `fill()`/`stroke()` thì đường chỉ tồn tại trong bộ nhớ, không hiện lên.

## Ví dụ 2: Animation loop

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

## Ví dụ 3: Transform & save/restore

Transform (translate, rotate, scale) là cách "di chuyển bút vẽ" thay vì tự cộng tọa độ. `save()`/`restore()` hoạt động như một **stack** — save đẩy trạng thái hiện tại vào stack, restore lấy ra:

```js
// Vẽ 5 hình vuông xoay quanh một điểm, mỗi cái lệch 72°
ctx.save();
ctx.translate(150, 150);        // dời gốc tọa độ về tâm
for (let i = 0; i < 5; i++) {
  ctx.rotate((Math.PI * 2) / 5);
  ctx.fillStyle = `hsl(${i * 72}, 70%, 60%)`;
  ctx.fillRect(40, -10, 50, 20);
}
ctx.restore(); // trở về trạng thái trước khi translate/rotate — như chưa có gì xảy ra

// Sau dòng này, vẽ tiếp ở (0,0) vẫn là góc trên trái như thường
ctx.fillRect(0, 0, 20, 20);
```

Tại sao cần save/restore? Vì `fillStyle`, `lineWidth`, transform... là **trạng thái toàn cục** của context — nếu hàm vẽ của bạn đổi trạng thái mà không restore, mọi hình vẽ sau đó đều bị ảnh hưởng.

## Ví dụ 4: Gradient & text

```js
// Gradient tuyến tính
const grad = ctx.createLinearGradient(0, 0, 200, 0);
grad.addColorStop(0, "coral");
grad.addColorStop(1, "steelblue");
ctx.fillStyle = grad;
ctx.fillRect(10, 10, 200, 60);

// Text
ctx.fillStyle = "#333";
ctx.font = "16px system-ui, sans-serif";
ctx.fillText("Xin chào Canvas", 10, 100);
ctx.font = "bold 24px sans-serif";
ctx.textAlign = "center";
ctx.fillText("Đậm hơn", 100, 140);
```

## Ví dụ 5: Vẽ ảnh & image processing

```js
const img = new Image();
img.onload = () => {
  ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

  // Đọc pixel — nền tảng của mọi image filter
  const imgData = ctx.getImageData(0, 0, canvas.width, canvas.height);
  const d = imgData.data; // Uint8ClampedArray: [r,g,b,a, r,g,b,a, ...]

  // Filter grayscale — truy cập pixel thô
  for (let i = 0; i < d.length; i += 4) {
    const gray = d[i] * 0.299 + d[i + 1] * 0.587 + d[i + 2] * 0.114;
    d[i] = d[i + 1] = d[i + 2] = gray;
  }
  ctx.putImageData(imgData, 0, 0);
};
img.src = "photo.jpg"; // cùng origin, hoặc server phải có CORS header
```

Lưu ý: `ctx.drawImage` với ảnh cross-origin (không có CORS) khiến canvas bị "tainted" — các lệnh `toDataURL()`, `toBlob()`, `getImageData()` sẽ throw `SecurityError`.

## Ví dụ 6: Hit detection — tương tác với shape

Vì shape không phải DOM node, bạn tự kiểm tra tọa độ click:

```js
const circles = [{ x: 100, y: 100, r: 30 }];

canvas.addEventListener("click", (e) => {
  // đổi tọa độ chuột về hệ tọa độ canvas
  const rect = canvas.getBoundingClientRect();
  const mx = e.clientX - rect.left;
  const my = e.clientY - rect.top;

  // hit-test thủ công: duyệt các shape đã vẽ (bạn phải tự lưu chúng)
  const hit = circles.find((c) => {
    const dx = mx - c.x, dy = my - c.y;
    return mx * mx + my * my <= c.r * c.r; // nằm trong đường tròn
  });
  if (hit) console.log("Clicked circle at", hit.x, hit.y);
});
```

Đây là "giá" phải trả cho hiệu năng của canvas: thay vì browser lo hit-testing (như SVG), bạn tự quản lý danh sách object và viết thuật toán kiểm tra click. Với nhiều loại shape phức tạp, dùng `ctx.isPointInPath(x, y)` sau khi dựng path lại.

## Ví dụ 7: Tính năng tiện dụng của API hiện đại

```js
// roundRect — Baseline 2023, không cần tự viết path bo góc nữa
ctx.roundRect(10, 10, 100, 50, 12); // cạnh cuối có bán kính bo
ctx.fill();

// Gradients, patterns
const pattern = ctx.createPattern(img, "repeat");

// Shadow
ctx.shadowColor = "rgba(0,0,0,0.3)";
ctx.shadowBlur = 8;
ctx.shadowOffsetY = 3;

// Compositing — vẽ sprite với blend mode
ctx.globalCompositeOperation = "multiply";

// Export
canvas.toDataURL("image/png");           // string data URL
canvas.toBlob((blob) => save(blob));      // Blob — nhẹ hơn cho file lớn
```

### OffscreenCanvas — vẽ ngoài main thread

```js
// Vẽ ở web worker, không block UI — hữu ích khi có hàng chục nghìn object
const offscreen = new OffscreenCanvas(800, 600);
const octx = offscreen.getContext("2d");
// ...vẽ trong worker...
// Chuyển kết quả về main thread: transferToImageBitmap() hoặc postMessage transfer
```

`OffscreenCanvas` được hỗ trợ tốt trên các browser hiện đại (Baseline 2024). Dùng khi canvas của bạn cần recompute nặng (filter, particle lớn) mà không muốn UI khựng.

## Canvas vs SVG — quyết định cuối cùng

Hỏi bản thân 3 câu, theo thứ tự:

1. **Có cần phóng to không mất nét?** (icon, logo, chart in ấn) → SVG
2. **Có cần tương tác riêng với từng shape không?** (hover/click từng cột) → SVG
3. **Có nhiều hơn ~1.000 object hoặc vẽ lại 60 lần/giây không?** (game, particle, filter) → Canvas

Trường hợp biên: chart vài trăm điểm nhưng cần hiệu năng mobile → vẫn nên cân nhắc Canvas; icon cần đổi màu theo theme → SVG với `currentColor`.

## Bẫy tổng hợp

| # | Bẫy | Triệu chứng | Cách tránh |
|---|---|---|---|
| 1 | Không xử lý `devicePixelRatio` | Canvas nhòe trên Retina | setupCanvas với dpr như trên |
| 2 | Đổi `canvas.width` khi chỉ muốn resize CSS | Buffer bị reset, mất hết hình | Tách CSS size vs buffer size |
| 3 | Vẽ path mà không `beginPath()` | Hình nối dính nhau | `beginPath()` trước mỗi shape mới |
| 4 | Đọc pixel từ ảnh cross-origin | SecurityError | Cần CORS header hoặc cùng origin |
| 5 | Quên `restore()` | Màu/transform "dính" sang shape sau | `save()`/`restore()` theo cặp |
| 6 | Vẽ trước khi `DOMContentLoaded` | Canvas size = 0 | Chạy code sau khi DOM ready |

## Checklist tự kiểm tra

- [ ] Giải thích được canvas = bitmap vs SVG = DOM, và hệ quả của mỗi mô hình
- [ ] Vẽ được rect, arc, line, path tự do
- [ ] Dùng được `save()`/`restore()` với transform
- [ ] Xử lý được devicePixelRatio cho màn hình Retina
- [ ] Export canvas ra PNG và biết hạn chế của ảnh cross-origin
- [ ] Tự viết được hit-testing đơn giản cho một shape

## Tham khảo

- File: `index.html`
- MDN Canvas: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- Canvas 2D API Reference: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D
- MDN — Optimizing canvas: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas
- Bài liên quan: `21_graphics/02_2d-animation/` (animation loop), `21_graphics/01_raster-svg/` (khi nào chọn SVG thay vì Canvas)
