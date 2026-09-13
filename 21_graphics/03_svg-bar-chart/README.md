# SVG Bar Chart

## 🔑 Khái niệm

Vẽ biểu đồ cột (bar chart) bằng SVG: mỗi cột là `<rect>`, label là `<text>`. Dữ liệu array → tính scale → render SVG elements.

```js
const data = [30, 80, 45, 90, 60];
const max = Math.max(...data);
const barWidth = 60;
const gap = 20;
const height = 300;

data.forEach((val, i) => {
  const barHeight = (val / max) * height;
  const x = i * (barWidth + gap) + gap;
  const y = height - barHeight;
  // <rect x="..." y="..." width="60" height="..." />
});
```

## ✅ Điểm mạnh
- SVG scalable — phóng to không mờ
- Mỗi `<rect>` là DOM element → attach event listener riêng
- Animation bằng CSS `transition` hoặc JS rAF
- Accessible: `<title>`, `<desc>` trong SVG

## ⚠️ Lưu ý
- SVG viewBox cần tính toán đúng tỷ lệ aspect ratio
- Nhiều柱重叠 nếu không tính gap đúng
- `Math.max` empty array → `-Infinity` → scale lỗi — cần check

## 💡 Khi nào dùng
- Dashboard widget
- Report visualization
- Simple chart không cần thư viện nặng

## 🎯 Ví dụ minh họa

### Bar chart responsive
```js
function renderBarChart(data, container) {
  const max = Math.max(...data);
  const width = container.clientWidth;
  const height = 300;
  const barW = (width - data.length * 20) / data.length;
  
  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  
  data.forEach((val, i) => {
    const barH = (val / max) * (height - 40);
    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", i * (barW + 20) + 10);
    rect.setAttribute("y", height - barH);
    rect.setAttribute("width", barW);
    rect.setAttribute("height", barH);
    rect.setAttribute("fill", "steelblue");
    rect.style.transition = "height 0.5s";
    svg.appendChild(rect);
    
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", i * (barW + 20) + barW / 2 + 10);
    text.setAttribute("y", height - 10);
    text.setAttribute("text-anchor", "middle");
    text.textContent = val;
    svg.appendChild(text);
  });
  
  container.appendChild(svg);
}
```

## 📚 Tham khảo & Bài tập
- File: `app.js`, `index.html` trong folder `03_svg-bar-chart/`
- Thực hành: thêm hover tooltip hiện giá trị
- Câu hỏi: làm sao animate bar grow từ dưới lên?
