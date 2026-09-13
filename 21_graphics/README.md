# Graphics in JavaScript — Elective

> Nhóm elective — đồ họa 2D/3D trong browser, không nằm trực tiếp trong core roadmap nhưng là skill bổ trợ quan trọng cho frontend developer.

## Bản đồ kiến thức

| Mục | Chủ đề | Công nghệ | Liên quan roadmap |
|---|---|---|---|
| **01** | Raster & SVG | `<svg>`, `<image>`, CSS animation | `18_dom-apis` |
| **02** | 2D Animation | `requestAnimationFrame`, delta time | `12_asynchronous-javascript` |
| **03** | SVG Bar Chart | `<rect>`, `<text>`, SVG dynamic | `03_data-structures` |
| **04** | Canvas 2D | `<canvas>`, Context2D API | `18_dom-apis` |

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

## Cấu trúc

```
21_graphics/
+-- 01_raster-svg/      SVG basics, clock example
+-- 02_2d-animation/    requestAnimationFrame, delta time
+-- 03_svg-bar-chart/   dynamic SVG chart
+-- 04_canvas/          Canvas 2D Context API
```

## Cách chạy

Mỗi folder có `index.html` -- mở bằng Live Server hoặc HTTP server:
```bash
npx serve .
# hoặc
python3 -m http.server 8080
```

## Tài nguyên tham khảo

- MDN SVG: https://developer.mozilla.org/en-US/docs/Web/SVG
- MDN Canvas: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- CSS-Tricks SVG: https://css-tricks.com/svg-secrets/
- Canvas API Reference: https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D
