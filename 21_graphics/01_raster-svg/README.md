# Raster & SVG

## Khái niệm

| Loại | Đặc điểm | Định dạng | Zoom | Tương tác |
|---|---|---|---|---|
| **Raster** | Tập hợp điểm ảnh (pixel), mờ khi zoom | PNG, JPG, GIF, WebP | Mờ/nhòe | CSS filter, canvas drawImage |
| **SVG** | Vector dựa trên XML, co giãn vô hạn | `.svg` inline hoặc file | Sắc nét mọi level | DOM query, CSS, JS animate |

SVG là **thành phần DOM** -- có thể query bằng `document.querySelector`, style bằng CSS, animate bằng JS/CSS.

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
- accessible: `<title>`, `<desc>` cho screen readers
- Scriptable: mỗi element là DOM node, attach event listener được

## Lưu ý

- SVG phức tạp (many paths, thousands of elements) có thể nặng DOM, chậm render
- `<image>` trong SVG cần CORS header để load external URL
- Raster ảnh nhỏ hơn SVG cho ảnh chụp thực tế (photo vs illustration)
- SVG inline làm tăng HTML size -- dùng `<img src="*.svg">` cho file độc lập
- Firefox/Safari có khác biệt nhỏ về SVG rendering -- test đa browser

## Khi nào dùng

- Icon, logo, illustration đơn giản --> SVG
- Ảnh chụp, texture phức tạp --> Raster (PNG/JPG/WebP)
- Clock/widget SVG animated --> SVG + CSS/JS
- Chart/data visualization --> SVG (mỗi element tương tác được)
- Responsive design --> SVG (scale vô hạn)
- Print output --> SVG (vector, không pixelate)

## Ví dụ: SVG Clock

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
  const h = (now.getHours() % 12) * 30 + now.getMinutes() * 0.5;
  const m = now.getMinutes() * 6;
  const s = now.getSeconds() * 6;
  document.getElementById("hour").setAttribute("transform", `rotate(${h} 100 100)`);
  document.getElementById("minute").setAttribute("transform", `rotate(${m} 100 100)`);
  document.getElementById("second").setAttribute("transform", `rotate(${s} 100 100)`);
  requestAnimationFrame(updateClock);
}
updateClock();
```

## Tham khảo

- File: `index.html`, `style.css`, `clock.png` (reference image)
- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
- SVG Cookbook: https://svgcookbook.com/
