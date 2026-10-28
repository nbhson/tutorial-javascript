# Raster & SVG

## Khái niệm

Trước khi vẽ bất kỳ thứ gì trong browser, bạn cần trả lời câu hỏi nền tảng: **ảnh được lưu và render theo cách nào?** Có hai họ lớn:

| Loại | Đặc điểm | Định dạng | Zoom | Tương tác |
|---|---|---|---|---|
| **Raster** | Tập hợp điểm ảnh (pixel), mờ khi zoom | PNG, JPG, GIF, WebP | Mờ/nhòe | CSS filter, canvas drawImage |
| **SVG** | Vector dựa trên XML, co giãn vô hạn | `.svg` inline hoặc file | Sắc nét mọi level | DOM query, CSS, JS animate |

- **Raster (bitmap)**: file mô tả màu của từng pixel. Phóng to = trình duyệt phải "đoán" pixel mới → nhòe. Phù hợp ảnh chụp, texture, hiệu ứng gradient phức tạp.
- **SVG (Scalable Vector Graphics)**: file mô tả *hình học* (đường tròn tâm nào, bán kính bao nhiêu...). Trình duyệt vẽ lại sắc nét ở mọi kích thước. Phù hợp icon, logo, chart, illustration.

Điểm quan trọng nhất cần ghi nhớ: **SVG là thành phần DOM** — có thể query bằng `document.querySelector`, style bằng CSS, animate bằng JS/CSS. Điều này khiến SVG khác biệt hoàn toàn so với ảnh raster và cả Canvas (bài 04).

## Hệ tọa độ của SVG

Mọi SVG làm việc trên hệ tọa độ riêng, điều khiển bởi 2 thuộc tính:

```html
<svg width="200" height="100" viewBox="0 0 200 100">
```

- `width`/`height`: kích thước hiển thị trên trang (CSS pixels).
- `viewBox="minX minY width height"`: "cửa sổ" vào hệ tọa độ nội bộ. Trình duyệt scale nội dung của viewBox cho vừa với width/height.

```html
<!-- Cùng một hình, hiển thị 2 kích thước — vẫn sắc nét vì vector -->
<svg width="50"  height="50" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>
<svg width="300" height="300" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="red"/>
</svg>
```

Lưu ý hướng trục: **y tăng từ trên xuống** (khác hệ tọa độ toán học quen thuộc). Điều này gây lỗi rất thường gặp khi vẽ chart — cột bar phải tính `y = chiềuCao - chiềuCaoCột`, không phải `y = 0`.

## Các element SVG thường dùng

| Element | Dùng để | Ví dụ |
|---|---|---|
| `<rect>` | Hình chữ nhật | `<rect x="10" y="10" width="80" height="50" rx="4"/>` |
| `<circle>` | Đường tròn | `<circle cx="50" cy="50" r="40"/>` |
| `<ellipse>` | Elip | `<ellipse cx="50" cy="50" rx="40" ry="20"/>` |
| `<line>` | Đoạn thẳng | `<line x1="0" y1="0" x2="100" y2="50"/>` |
| `<polyline>` | Đường gấp khúc mở | biểu đồ đường |
| `<polygon>` | Đa giác kín | mũi tên, ngôi sao |
| `<path>` | Mọi hình bất kỳ | `d="M10 80 Q 95 10 180 80"` — element mạnh nhất |
| `<text>` | Chữ | label của chart |
| `<g>` | Nhóm element | áp transform/fill cho cả nhóm |
| `<defs>` + `<use>` | Định nghĩa & tái sử dụng | icon system |
| `<image>` | Nhúng ảnh raster | `<image href="photo.jpg"/>` |

`<path>` đáng chú ý nhất: chữ `d` là một mini-language — `M` (move to), `L` (line to), `Q`/`C` (đường cong Bézier), `A` (arc), `Z` (đóng đường). Dùng nó bạn vẽ được mọi hình 2D.

```html
<svg width="100" height="100" viewBox="0 0 100 100">
  <circle cx="50" cy="50" r="40" fill="red" stroke="#333" stroke-width="2"/>
  <text x="50" y="55" text-anchor="middle" fill="white" font-size="12">SVG</text>
</svg>
```

## Điểm mạnh

- SVG không mờ khi zoom -- lý tưởng cho icon, logo, chart, map
- Inline SVG có thể style CSS trực tiếp (fill, stroke, transform, animation)
- Animated SVG qua CSS @keyframes hoặc JS requestAnimationFrame
- File size nhỏ cho shape đơn giản (icon ~1KB vs PNG ~10KB)
- Accessible: `<title>`, `<desc>` cho screen readers
- Scriptable: mỗi element là DOM node, attach event listener được

```html
<!-- Accessibility cho SVG -->
<svg role="img" aria-labelledby="chartTitle chartDesc">
  <title id="chartTitle">Doanh thu quý 4</title>
  <desc id="chartDesc">Biểu đồ cột doanh thu 3 tháng: 120, 150, 180 triệu đồng</desc>
  <!-- ...các shape... -->
</svg>
```

## Lưu ý

- SVG phức tạp (nhiều path, hàng nghìn element) có thể nặng DOM, chậm render — nếu vượt ngưỡng này, chuyển sang Canvas (bài 04)
- `<image>` trong SVG cần CORS header để load external URL
- Raster ảnh nhỏ hơn SVG cho ảnh chụp thực tế (photo vs illustration)
- SVG inline làm tăng HTML size -- dùng `<img src="*.svg">` cho file độc lập (nhưng khi đó KHÔNG style được từ CSS bên ngoài)
- Firefox/Safari có khác biệt nhỏ về SVG rendering -- test đa browser

## Các định dạng raster — chọn cái nào?

| Định dạng | Nén | Transparency | Dùng khi |
|---|---|---|---|
| PNG | Không mất dữ liệu | Có | Ảnh cần nét chữ, screenshot, đồ họa phẳng |
| JPG | Mất dữ liệu | Không | Ảnh chụp (nhỏ nhất cho photo) |
| WebP | Cả hai loại | Có | Mặc định hiện đại — nhỏ hơn PNG ~25% |
| AVIF | Mất dữ liệu | Có | Mới nhất, nhỏ hơn WebP nữa (Baseline 2025) |
| GIF | 256 màu, mất dữ liệu | 1-bit | Chỉ còn hợp lý cho animation đơn giản |
| SVG | Vector | Có | Icon, logo, chart |

Quy tắc thực chiến: **photo → WebP/AVIF, icon/logo → SVG**, và luôn cung cấp `srcset`/`<picture>` cho responsive.

## Khi nào dùng

- Icon, logo, illustration đơn giản --> SVG
- Ảnh chụp, texture phức tạp --> Raster (PNG/JPG/WebP)
- Clock/widget SVG animated --> SVG + CSS/JS
- Chart/data visualization --> SVG (mỗi element tương tác được)
- Responsive design --> SVG (scale vô hạn)
- Print output --> SVG (vector, không pixelate)

## Ví dụ 1: SVG Clock

```html
<svg viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="90" fill="white" stroke="#333" stroke-width="3"/>
  <!-- Hour markers -->
  <g stroke="#333" stroke-width="2">
    <line x1="100" y1="15" x2="100" y2="25"/>
    <line x1="100" y1="185" x2="100" y2="195"/>
    <line x1="15" y1="100" x2="25" y2="100"/>
    <line x1="175" y1="100" x2="185" y2="100"/>
  </g>
  <line id="hour" x1="100" y1="100" x2="100" y2="50" stroke="#333" stroke-width="4" stroke-linecap="round"/>
  <line id="minute" x1="100" y1="100" x2="100" y2="30" stroke="#666" stroke-width="3" stroke-linecap="round"/>
  <line id="second" x1="100" y1="100" x2="100" y2="20" stroke="red" stroke-width="2"/>
  <circle cx="100" cy="100" r="4" fill="#333"/>
</svg>
```

```js
function updateClock() {
  const now = new Date();
  const h = (now.getHours() % 12) * 30 + now.getMinutes() * 0.5; // 360°/12h, kim giờ trôi theo phút
  const m = now.getMinutes() * 6;                                 // 360°/60ph
  const s = now.getSeconds() * 6;                                 // 360°/60s
  document.getElementById("hour").setAttribute("transform", `rotate(${h} 100 100)`);
  document.getElementById("minute").setAttribute("transform", `rotate(${m} 100 100)`);
  document.getElementById("second").setAttribute("transform", `rotate(${s} 100 100)`);
  requestAnimationFrame(updateClock);
}
updateClock();
```

Điểm đáng học ở ví dụ này: `setAttribute("transform", "rotate(góc, tâmX, tâmY)")` — quay quanh điểm bất kỳ mà không cần tự tính tọa độ kim đồng hồ.

## Ví dụ 2: SVG tương tác bằng event listener

```js
// SVG element = DOM node bình thường, mọi thứ bạn học ở 18_dom-apis đều áp dụng được
document.querySelectorAll("circle").forEach((circle) => {
  circle.addEventListener("mouseenter", () => {
    circle.setAttribute("fill", "navy");
    circle.setAttribute("r", 45); // phồng lên khi hover
  });
  circle.addEventListener("mouseleave", () => {
    circle.setAttribute("fill", "red");
    circle.setAttribute("r", 40);
  });
});
```

```css
/* Cách thứ 3: style SVG bằng CSS — gọn hơn JS cho hiệu ứng đơn giản */
circle {
  transition: r 0.2s ease, fill 0.2s ease;
  cursor: pointer;
}
```

## Ví dụ 3: Tạo SVG element bằng JS

```js
// ⚠️ Bẫy kinh điển: document.createElement("circle") SẼ KHÔNG hoạt động
// — phải dùng createElementNS với namespace SVG
const SVG_NS = "http://www.w3.org/2000/svg";

function makeCircle(cx, cy, r, fill) {
  const c = document.createElementNS(SVG_NS, "circle");
  c.setAttribute("cx", cx);
  c.setAttribute("cy", cy);
  c.setAttribute("r", r);
  c.setAttribute("fill", fill);
  return c;
}

document.querySelector("svg").appendChild(makeCircle(80, 50, 10, "green"));
```

Lý do: SVG là XML với namespace riêng. Nếu quên `createElementNS`, element được tạo nằm sai namespace → browser coi là HTML element không rõ nghĩa và **không render**. Bẫy này xuất hiện ở bài 03 (bar chart) nữa, bạn sẽ thấy dùng lại nhiều lần.

## Checklist tự kiểm tra

- [ ] Phân biệt được raster vs vector và chọn đúng định dạng cho từng loại nội dung
- [ ] Hiểu `viewBox` và tại sao SVG scale không mờ
- [ ] Biết y-axis của SVG hướng xuống
- [ ] Tạo được SVG element bằng `createElementNS` (không dùng `createElement` thường)
- [ ] Attach được event listener lên shape SVG

## Tham khảo

- File: `index.html`, `style.css`, `clock.png` (reference image)
- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
- MDN — Getting started with SVG: https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Getting_Started
- SVG Cookbook: https://svgcookbook.com/
