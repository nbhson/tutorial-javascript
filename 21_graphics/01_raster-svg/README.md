# Raster & SVG

## 🔑 Khái niệm

| Loại | Đặc điểm | Định dạng |
|---|---|---|
| **Raster** | Tập hợp điểm ảnh (pixel), mờ khi zoom | PNG, JPG, GIF, WebP |
| **SVG** | Vector dựa trên XML, co giãn vô hạn | `.svg` inline hoặc file |

SVG là **thành phần DOM** — có thể query, style bằng CSS, animate bằng JS/CSS.

```html
<svg width="100" height="100">
  <circle cx="50" cy="50" r="40" fill="red" />
</svg>
```

## ✅ Điểm mạnh
- SVG không mờ khi zoom — lý tưởng cho icon, logo, chart
- Inline SVG có thể style CSS trực tiếp (`fill`, `stroke`, `transform`)
- Animated SVG qua CSS `@keyframes` hoặc JS `requestAnimationFrame`
- File size nhỏ cho shape đơn giản

## ⚠️ Lưu ý
- SVG phức tạp (many paths) có thể nặng DOM, chậm render
- `<image>` trong SVG cần CORS header để load external
- Raster ảnh nhỏ hơn SVG cho ảnh chụp thực tế

## 💡 Khi nào dùng
- Icon, logo, illustration đơn giản → SVG
- Ảnh chụp, texture phức tạp → Raster (PNG/JPG)
- Clock/widget SVG animated → SVG + CSS/JS

## 🎯 Ví dụ minh họa

### SVG clock cơ bản
```html
<svg viewBox="0 0 200 200">
  <circle cx="100" cy="100" r="90" fill="white" stroke="#333" stroke-width="3"/>
  <line id="hour" x1="100" y1="100" x2="100" y2="50" stroke="#333" stroke-width="4" stroke-linecap="round"/>
  <line id="minute" x1="100" y1="100" x2="100" y2="30" stroke="#666" stroke-width="3" stroke-linecap="round"/>
  <line id="second" x1="100" y1="100" x2="100" y2="20" stroke="red" stroke-width="2"/>
</svg>
```
```js
function updateClock() {
  const now = new Date();
  const h = now.getHours() % 12 * 30 + now.getMinutes() * 0.5;
  const m = now.getMinutes() * 6;
  const s = now.getSeconds() * 6;
  document.getElementById("hour").setAttribute("transform", `rotate(${h} 100 100)`);
  document.getElementById("minute").setAttribute("transform", `rotate(${m} 100 100)`);
  document.getElementById("second").setAttribute("transform", `rotate(${s} 100 100)`);
  requestAnimationFrame(updateClock);
}
updateClock();
```

## 📚 Tham khảo & Bài tập
- File: `index.html`, `style.css`, `clock.png` (reference image) trong folder `01_raster-svg/`
- Thực hành: vẽ SVG biểu đồ tròn (pie chart) đơn giản
- Câu hỏi: inline SVG khác gì `<img src="*.svg">` về mặt CSS access?
