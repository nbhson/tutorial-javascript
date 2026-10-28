# Graphics in JavaScript — Elective

> Nhóm elective — đồ họa 2D/3D trong browser, không nằm trực tiếp trong core roadmap nhưng là skill bổ trợ quan trọng cho frontend developer.

## Vì sao nên học đồ họa trong browser?

Bốn lý do thực tế khiến đồ họa trở thành kỹ năng "ăn tiền" với bạn:

1. **Data visualization** — dashboard, biểu đồ, báo cáo xuất hiện trong hầu hết sản phẩm web. Hiểu cách SVG/Canvas hoạt động giúp bạn dùng Chart.js, D3, ECharts hiệu quả hơn nhiều (vì bạn biết chúng đang làm gì phía dưới).
2. **Hiệu ứng tương tác** — loading spinner, particle effect, scroll animation, mini-game... đều dựa trên `requestAnimationFrame` và loop vẽ lại.
3. **Hiệu năng** — khi bạn cần render hàng nghìn phần tử, biết chọn SVG hay Canvas quyết định app chạy mượt hay lag.
4. **Nền tảng cho WebGL/Three.js** — muốn đi sâu 3D, bạn phải hiểu trước cách browser vẽ 2D và cách pipeline render hoạt động.

## Bản đồ kiến thức

| Mục | Chủ đề | Công nghệ | Liên quan roadmap |
|---|---|---|---|
| **01** | Raster & SVG | `<svg>`, `<image>`, CSS animation | `18_dom-apis` |
| **02** | 2D Animation | `requestAnimationFrame`, delta time | `12_asynchronous-javascript` |
| **03** | SVG Bar Chart | `<rect>`, `<text>`, SVG dynamic | `03_data-structures` |
| **04** | Canvas 2D | `<canvas>`, Context2D API | `18_dom-apis` |

## Bốn công nghệ vẽ trong browser — so sánh tổng quan

Trước khi vào từng bài, bạn nên có bức tranh lớn: browser cho bạn 4 cách vẽ chính, mỗi cách phù hợp một loại bài toán.

| | SVG | Canvas 2D | WebGL | CSS (transform/animation) |
|---|---|---|---|---|
| Mô hình | Vector, mỗi shape là DOM node | Raster bitmap, vẽ bằng lệnh | Raster + GPU shader | Vector do engine render |
| Scale | Sắc nét vô hạn | Mờ khi phóng to | Tùy resolution buffer | Sắc nét |
| Số element "thời điểm vàng" | < ~1.000 nodes | hàng chục nghìn object/frame | hàng trăm nghìn vertex | vài chục element |
| Tương tác từng shape | Dễ (event listener) | Tự viết hit-testing | Phải tự raycast | Giới hạn |
| Đường học tập | Dễ nhất | Dễ | Dốc nhất (shaders, matrices) | Dễ nhất |
| Dùng cho | Icon, chart, infographic | Game 2D, drawing app, filter | Game 3D, data viz phức tạp | UI micro-interaction |

Quy tắc chọn nhanh mà bạn có thể nhớ:

- **Ít element, cần tương tác/crisp** → SVG
- **Nhiều element, vẽ liên tục mỗi frame** → Canvas 2D
- **3D hoặc hiệu ứng GPU** → WebGL (thường qua thư viện Three.js)
- **Chỉ chuyển động UI đơn giản** → CSS animation (rẻ nhất, off-main-thread)

Trong lộ trình này ta đi sâu vào hai cái đầu (SVG + Canvas 2D), vì chúng bao phủ ~90% nhu cầu của frontend developer.

## Lộ trình học đề xuất

```
01_raster-svg     -> hiểu vector vs raster
       |
       v
02_2d-animation   -> animation loop cơ bản
       |
       v
03_svg-bar-chart  -> ứng dụng SVG cho data viz
       |
       v
04_canvas         -> pixel-level rendering
```

Sau khi xong 4 bài, bạn có thể tự kiểm tra bằng các "mốc năng lực" sau:

- [ ] Giải thích được khi nào chọn SVG, khi nào chọn Canvas (có ví dụ cụ thể)
- [ ] Vẽ được SVG bằng markup tĩnh VÀ tạo dynamic bằng `createElementNS`
- [ ] Viết được animation loop chuẩn có delta time và cleanup bằng `cancelAnimationFrame`
- [ ] Xử lý được retina/HiDPI cho canvas (`devicePixelRatio`)
- [ ] Export được nội dung canvas ra ảnh PNG (`toDataURL` / `toBlob`)

## Cấu trúc

```
21_graphics/
+-- 01_raster-svg/      SVG basics, clock example
+-- 02_2d-animation/    requestAnimationFrame, delta time
+-- 03_svg-bar-chart/   dynamic SVG chart
+-- 04_canvas/          Canvas 2D Context API
```

Mỗi thư mục con chứa `index.html` + code chạy trực tiếp trong browser.

## Cách chạy

Mỗi folder có `index.html` -- mở bằng Live Server hoặc HTTP server:

```bash
npx serve .
# hoặc
python3 -m http.server 8080
```

Lý do cần HTTP server (thay vì double-click file): một số API như `fetch`, `<image>` với external URL, hay WebGL texture đều yêu cầu origin HTTP — mở bằng `file://` có thể bị chặn bởi CORS.

## Mô hình học của nhóm này

Mỗi bài được tổ chức theo cùng một cấu trúc để bạn dễ đối chiếu:

1. **Khái niệm** — mô hình kỹ thuật đằng sau (vector/raster, DOM/bitmap, frame loop)
2. **Điểm mạnh / Lưu ý** — khi nào công nghệ này phát huy, khi nào nó cản đường
3. **Ví dụ chạy được** — code bạn copy vào `index.html` là thấy kết quả ngay
4. **Checklist tự kiểm tra** — tiêu chí "đã hiểu" trước khi sang bài kế

Bốn bài nối tiếp nhau: 01 cho bạn nền tảng SVG, 02 cho bạn vòng lặp animation dùng chung cho cả SVG lẫn Canvas, 03 áp dụng cả hai vào một sản phẩm thật (biểu đồ), 04 mở ra thế giới pixel-level với Canvas 2D.

## WebGL — bước tiếp theo khi bạn muốn 3D

Lộ trình này dừng ở Canvas 2D, nhưng bạn nên biết phía trước có gì. **WebGL** (Web Graphics Library) là API dựa trên OpenGL ES, cho phép truy cập GPU trực tiếp qua hai loại chương trình nhỏ viết bằng GLSL: **vertex shader** (định vị đỉnh) và **fragment shader** (tô màu từng pixel).

Điều bạn cần biết ở mức giới thiệu:

- WebGL **không có khái niệm shape** — bạn chỉ vẽ điểm, đường, tam giác. Mọi hình phức tạp đều ghép từ tam giác.
- Vẽ 1 hình cũng phải viết boilerplate: tạo context, compile shader, tạo buffer, truyền attribute... Vì vậy thực tế hầu hết dùng **Three.js**, **Babylon.js** hoặc **PixiJS** (2D trên nền WebGL).
- `<canvas>` là cùng một element cho cả 2D và WebGL — khác nhau ở tham số context: `canvas.getContext("2d")` vs `canvas.getContext("webgl2")`.
- Lộ trình gợi ý: nắm chắc Canvas 2D (bài 04) → học khái niệm matrix/transform → vào Three.js với scene/camera/mesh/lights.

```js
// Khởi tạo WebGL 2 — chỉ để bạn thấy "hình dạng" của API
const canvas = document.querySelector("canvas");
const gl = canvas.getContext("webgl2");
if (!gl) {
  console.log("WebGL2 không được hỗ trợ trên browser này");
}
// Từ đây trở đi là thế giới của shader và buffer — chủ đề của một khóa riêng.
```

Bạn **không cần** WebGL để hoàn thành core roadmap — coi đây là nhánh optional khi bạn đã vững Canvas 2D.

## Mẹo học hiệu quả

1. **Luôn mở DevTools tab Console cùng lúc đọc** — các ví dụ trong bài chạy được ngay bằng cách copy vào `index.html` kèm sẵn.
2. **Sửa số liệu theo cách của bạn** — đổi màu, tốc độ, kích thước, rồi đoán trước kết quả. Đây là cách nhanh nhất để "cảm" được hệ tọa độ.
3. **Đọc fallback của người khác** — codepen.io có hàng nghìn demo SVG/Canvas, đọc source giúp bạn thấy pattern thật.
4. **Đo hiệu năng** — mở DevTools tab Performance, record khi render 1.000 vs 10.000 element để tự thấy sự khác biệt SVG vs Canvas.

## Các tính năng hay bị bỏ qua — nhưng đáng để bạn biết

Khi đã quen với nền tảng, đây là các "nấc thang tiếp theo" mà ít tài liệu đề cập:

1. **Canvas `Path2D`** — gom nhóm path để vẽ lại nhiều lần mà không tính lại tọa độ:
   ```js
   const star = new Path2D();
   star.moveTo(100, 10);
   for (let i = 0; i < 5; i++) {
     star.lineTo(Math.cos((i * 4 * Math.PI) / 5 - Math.PI / 2) * 90 + 100,
                 Math.sin((i * 4 * Math.PI) / 5 - Math.PI / 2) * 90 + 100);
   }
   star.closePath();
   ctx.stroke(star); ctx.fill(star); // dùng lại nhiều lần
   ```

2. **SVG `<use>`** — định nghĩa một shape trong `<defs>`, reuse bằng `<use href="#id">` — tạo icon system mà không copy-paste markup:
   ```html
   <svg><defs><circle id="dot" r="5" fill="red"/></defs>
     <use href="#dot" x="10" y="10"/>
     <use href="#dot" x="30" y="30"/>
   </svg>
   ```

3. **Canvas `globalCompositeOperation`** — blend mode giữa layers, cho phép tạo hiệu ứng overlay (multiply, screen, overlay, lighten...) mà không cần thư viện.

4. **SVG SMIL animation** (`<animate>`, `<animateTransform>`) — animate SVG thuần markup, không cần JS:
   ```html
   <circle r="10" fill="red">
     <animate attributeName="r" from="10" to="30" dur="2s" repeatCount="indefinite"/>
   </circle>
   ```
   SMIL bị deprecated trên Chrome một thời gian (nhưng đã quay lại và tiếp tục hỗ trợ). Vẫn dùng được nhưng CSS/JS animation linh hoạt hơn.

5. **Canvas `filter`** — áp dụng CSS filter lên canvas context:
   ```js
   ctx.filter = "blur(3px) drop-shadow(0 2px 4px rgba(0,0,0,.3))";
   ctx.drawImage(img, 0, 0);
   ```

Nắm những thứ này giúp bạn viết code gọn hơn và hiểu sâu hơn khi đọc source thư viện đồ họa.

## Bài liên quan trong khóa

- `18_dom-apis/` — SVG element là DOM node; thao tác SVG dùng chính kiến thức DOM ở đó.
- `12_asynchronous-javascript/` — `requestAnimationFrame` là một loại async callback, nằm trong event loop.
- `19_browser-devtools/` — dùng tab Performance để profile animation.
- js-info (mirror tiếng Việt): `js-info/vi/34_animation/` — chương animation của javascript.info, đọc thêm để hiểu lý thuyết timing/easing.

## Các lỗi thường gặp khi bắt đầu học đồ họa

Để bạn tránh mất thời gian của chính mình, đây là những sai lầm lặp lại nhiều nhất ở người mới:

1. **Nhầm hệ tọa độ** — y tăng từ trên xuống (không phải từ dưới lên như toán học), góc quay tính bằng **radian** chứ không phải độ. Ghi nhớ: `180° = Math.PI`.
2. **Quên clear canvas mỗi frame** — các hình vẽ chồng đè lên nhau thành "bức tranh bẩn". Luôn `clearRect(0, 0, w, h)` ở đầu mỗi frame (trừ khi cố tình muốn hiệu ứng trail).
3. **Chỉnh `canvas.style.width` rồi tưởng là đã resize** — style chỉ đổi kích thước hiển thị; buffer vẽ thực tế là `canvas.width`/`canvas.height`. Đổi buffer sẽ xóa sạch nội dung đã vẽ.
4. **Đặt script vẽ trước element canvas trong HTML** — `document.querySelector("canvas")` trả `null` → lỗi `Cannot read properties of null`. Đặt script cuối body hoặc dùng `defer`/`type="module"`.
5. **Dùng `createElement` thay vì `createElementNS` cho SVG** — element tạo ra không render và không có error (chi tiết ở bài 01 và 03).
6. **Tối ưu quá sớm** — viết code đơn giản, chạy được trước; chỉ khi profile (DevTools Performance) cho thấy chậm mới tối ưu.

## Tài nguyên tham khảo

- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
- MDN Canvas: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- Canvas API Reference: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D
- MDN WebGL: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API
- CSS-Tricks SVG: https://css-tricks.com/svg-secrets/
- Three.js: https://threejs.org/ — khi bạn muốn bắt đầu 3D
