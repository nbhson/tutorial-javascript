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
- `y = containerHeight - barHeight` (SVG y tăng từ trên xuống — cột "mọc" từ đáy lên)

Đây là pattern **data → scale → render** cốt lõi của mọi thư viện chart (Chart.js, D3, ECharts đều làm đúng 3 bước này bên dưới):

```
dữ liệu (array số) → tính tỉ lệ (scale) → tạo element SVG tương ứng
```

Khi bạn tự viết được bar chart thủ công, việc đọc code D3 (`d3.scaleLinear()`, `d3.select()...`) trở nên dễ hiểu gấp nhiều lần.

## Điểm mạnh

- SVG scalable -- phóng to không mờ, retina-ready (không cần xử lý devicePixelRatio như Canvas)
- Mỗi `<rect>` là DOM element --> attach event listener riêng (hover, click)
- Animation bằng CSS transition hoặc JS rAF
- Accessible: `<title>`, `<desc>` cho screen readers
- Không cần thư viện ngoài -- pure SVG + JS

## Lưu ý

- SVG viewBox cần tính toán đúng tỷ lệ aspect ratio
- Nhiều cột chồng lên nhau nếu không tính gap đúng
- `Math.max` empty array --> `-Infinity` --> scale lỗi -- cần check guard
- SVG elements tạo bằng `createElementNS` với namespace "http://www.w3.org/2000/svg"
- DOM creation nhiều lần trong loop --> dùng DocumentFragment hoặc innerHTML chèn hàng loạt

### Bẫy `createElement` vs `createElementNS`

Bẫy số 1 của người mới khi vẽ SVG động:

```js
// ❌ SAI — element rơi vào namespace HTML, browser không render
const rect = document.createElement("rect");

// ✅ ĐÚNG — namespace SVG
const SVG_NS = "http://www.w3.org/2000/svg";
const rect2 = document.createElementNS(SVG_NS, "rect");
```

Không có error nào được throw — element chỉ "im lặng" không hiện ra. Nếu chart của bạn trắng trơn, kiểm tra chỗ này trước tiên.

## Khi nào dùng

- Dashboard widget (biểu đồ đơn giản, không interactive phức tạp)
- Report visualization (static export, print-friendly)
- Simple chart không cần thư viện nặng (Chart.js, D3)
- Embed trong email HTML (SVG supported trong một số clients)

### SVG chart vs thư viện chart

| Tiêu chí | Tự viết SVG | Chart.js / D3 / ECharts |
|---|---|---|
| Bundle size | 0 KB | 60–300 KB |
| Thời gian làm chart đơn giản | ~1 giờ đầu | ~10 phút |
| Custom hiệu ứng đặc thù | Toàn quyền | Phụ thuộc API thư viện |
| Tooltip/legend/zoom có sẵn | Phải tự viết | Có sẵn |
| Phù hợp | 1-2 chart, nhu cầu riêng | Nhiều chart, chuẩn thương mại |

Kinh nghiệm: tự viết 1 bar chart + 1 line chart ít nhất một lần để hiểu nguyên lý, sau đó dùng thư viện cho sản phẩm thật.

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

renderBarChart([30, 80, 45, 90, 60], document.querySelector("#chart"));
```

## Ví dụ 2: Hoàn chỉnh — trục, hover tooltip, transition

Phiên bản "gần sản phẩm thật": có trục mốc giá trị, tooltip khi hover, cột animate từ 0 lên. Đây là lúc kiến thức DOM (18_dom-apis) và Set/Map (03_data-structures) kết hợp với đồ họa.

```html
<div id="chart" style="width: 600px"></div>
```

```js
const SVG_NS = "http://www.w3.org/2000/svg";

function el(name, attrs = {}, textContent) {
  const node = document.createElementNS(SVG_NS, name);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  if (textContent !== undefined) node.textContent = textContent;
  return node;
}

function renderChart(labels, values, container) {
  container.innerHTML = ""; // re-render an toàn

  const W = 600, H = 320, PAD = 40;
  const max = Math.max(...values, 1); // guard: tránh -Infinity với array rỗng
  const innerH = H - PAD * 2;
  const barW = (W - PAD * 2 - (values.length - 1) * 10) / values.length;

  const svg = el("svg", { viewBox: `0 0 ${W} ${H}`, width: "100%" });

  // Trục + mốc giá trị (4 vạch)
  for (let i = 0; i <= 4; i++) {
    const y = PAD + (innerH * i) / 4;
    const value = Math.round(max - (max * i) / 4);
    svg.appendChild(el("line", { x1: PAD, y1: y, x2: W - PAD, y2: y, stroke: "#ddd" }));
    svg.appendChild(el("text", { x: PAD - 6, y: y + 4, "text-anchor": "end", "font-size": 10 }, value));
  }

  values.forEach((val, i) => {
    const barH = (val / max) * innerH;
    const x = PAD + i * (barW + 10);

    // Cột: animate bằng scale từ 0 → dùng <rect> với height transition qua JS
    const rect = el("rect", {
      x, y: H - PAD - barH, width: barW, height: barH,
      fill: "steelblue", rx: 3,
    });
    rect.style.transformOrigin = `${x + barW / 2}px ${H - PAD}px`;
    rect.style.transform = "scaleY(0)";
    requestAnimationFrame(() => { // frame kế: bật transition
      rect.style.transition = "transform 0.6s ease-out";
      rect.style.transform = "scaleY(1)";
    });

    // Tooltip trên chính shape — dùng <title> (native) + hover JS
    rect.appendChild(el("title", {}, `Giá trị: ${val}`));
    rect.addEventListener("mouseenter", () => rect.setAttribute("fill", "darkorange"));
    rect.addEventListener("mouseleave", () => rect.setAttribute("fill", "steelblue"));

    svg.appendChild(rect);
    svg.appendChild(el("text", { x: x + barW / 2, y: H - PAD + 15, "text-anchor": "middle", "font-size": 12 }, labels[i]));
  });

  container.appendChild(svg);
}

renderChart(
  ["T1", "T2", "T3", "T4", "T5"],
  [120, 150, 90, 180, 165],
  document.querySelector("#chart")
);
```

### Vì sao animate bằng `scaleY` mà không đổi `height` trong transition?

Đổi attribute `y`/`height` của SVG bằng CSS transition hoạt động ở đa số browser hiện đại, nhưng `transform: scaleY()` vẫn ổn định và mượt hơn (nếu thêm `transform-box: fill-box` cho SVG). Nguyên tắc chung: **animate bằng transform khi có thể**, đổi attribute khi cần.

## Bẫy tổng hợp

| # | Bẫy | Triệu chứng | Cách tránh |
|---|---|---|---|
| 1 | `createElement("rect")` không NS | Chart trống, không lỗi | `createElementNS(SVG_NS, "rect")` |
| 2 | `Math.max(...[])` → `-Infinity` | Cột height `NaN`, biến mất | `Math.max(...values, 1)` |
| 3 | Quên trục y hướng xuống | Cột "treo ngược" trên nóc | `y = đáy - chiềuCaoCột` |
| 4 | Ghép chuỗi lớn bằng `+=` vào `innerHTML` | Chậm, mất event listener | Tạo node + `appendChild`, hoặc build string rồi gán 1 lần |
| 5 | Re-render chồng SVG cũ | Chart trùng lớp | `container.innerHTML = ""` trước khi render |
| 6 | Đổi `width/height` khi resize mà không đổi `viewBox` | Chart méo | Đặt `width="100%"` và chỉ đổi `viewBox` |

## Bước tiếp theo

Sau khi tự viết được bar chart, bạn đã hiểu đủ nền tảng để:

- Đọc source code đơn giản của Chart.js plugins
- Học D3.js — thư viện "scale + shape" mạnh nhất cho data viz (chỉ dùng phần scale của D3 kết hợp với SVG bạn đã biết cũng rất giá trị)
- Tự viết line chart (thay `<rect>` bằng `<polyline>`/`<path>`) như bài tập về nhà

## Tham khảo

- File: `app.js`, `index.html`
- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
- MDN — createElementNS: https://developer.mozilla.org/en-US/docs/Web/API/Document/createElementNS
- Bài liên quan: `21_graphics/01_raster-svg/` (nền tảng SVG), `18_dom-apis/` (DOM manipulation)
