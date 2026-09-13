# SVG Bar Chart

## Khái niệm

Vẽ biểu đồ cột (bar chart) bằng SVG: mỗi cột là `<rect>`, label là `<text>`. Dữ liệu array --> tính scale --> render SVG elements.

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

### Scale calculation

- `barHeight = (val / max) * availableHeight`
- `x = index * (barWidth + gap) + leftPadding`
- `y = containerHeight - barHeight` (SVG y tăng từ trên xuống)

## Điểm mạnh

- SVG scalable -- phóng to không mờ, retina-ready
- Mỗi `<rect>` là DOM element --> attach event listener riêng (hover, click)
- Animation bằng CSS transition hoặc JS rAF
- Accessible: `<title>`, `<desc>` cho screen readers
- Không cần thư viện ngoài -- pure SVG + JS

## Lưu ý

- SVG viewBox cần tính toán đúng tỷ lệ aspect ratio
- Nhiều柱重叠 nếu không tính gap đúng
- `Math.max` empty array --> `-Infinity` --> scale lỗi -- cần check guard
- SVG elements tạo bằng `createElementNS` với namespace "http://www.w3.org/2000/svg"
- DOM creation nhiều lần trong loop --> dùng DocumentFragment hoặc innerHTML批量插入

## Khi nào dùng

- Dashboard widget (biểu đồ đơn giản, không interactive phức tạp)
- Report visualization (static export, print-friendly)
- Simple chart không cần thư viện nặng (Chart.js, D3)
- Embed trong email HTML (SVG supported trong một số clients)

## Ví dụ: Responsive Bar Chart

```js
function renderBarChart(data, container) {
  const max = Math.max(...data);
  const width = container.clientWidth || 600;
  const height = 300;
  const padding = 40;
  const barW = (width - padding * 2 - data.length * 10) / data.length;

  const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
  svg.setAttribute("viewBox", `0 0 ${width} ${height}`);
  svg.setAttribute("width", "100%");
  svg.setAttribute("height", height);

  data.forEach((val, i) => {
    const barH = max > 0 ? (val / max) * (height - padding * 2) : 0;
    const x = padding + i * (barW + 10);
    const y = height - padding - barH;

    const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
    rect.setAttribute("x", x);
    rect.setAttribute("y", y);
    rect.setAttribute("width", barW);
    rect.setAttribute("height", barH);
    rect.setAttribute("fill", "steelblue");
    rect.style.transition = "height 0.5s ease, y 0.5s ease";
    svg.appendChild(rect);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", x + barW / 2);
    text.setAttribute("y", height - padding + 15);
    text.setAttribute("text-anchor", "middle");
    text.setAttribute("font-size", "12");
    text.textContent = val;
    svg.appendChild(text);
  });

  container.appendChild(svg);
}
```

## Tham khảo

- File: `app.js`, `index.html`
- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
